# Tutorial 2: Build a simple chat application with Cortex Search¶

## Introduction¶

This tutorial describes how to use Cortex Search and the [COMPLETE
(SNOWFLAKE.CORTEX)](../../../../sql-reference/functions/complete-snowflake-
cortex) function to setup a Retrieval-Augmented Generation (RAG) chatbot in
Snowflake.

### What you will learn¶

  * Create a Cortex Search Service based on a dataset downloaded from Kaggle.

  * Create a Streamlit in Snowflake app that lets you query your Cortex Search Service.

### Prerequisites¶

The following prerequisites are required to complete this tutorial:

  * You have a Snowflake account and user with a role that grants the necessary privileges to create a database, tables, virtual warehouse objects, Cortex Search services, and Streamlit apps.

Refer to the [Snowflake in 20 minutes](../../../tutorials/snowflake-
in-20minutes) for instructions to meet these requirements.

## Step 1: Setup¶

### Getting the sample data¶

You will use a sample dataset hosted on Kaggle for this tutorial. The Books
dataset is a collection of book name, title and descriptions. You can download
the dataset from the following link:

The complete dataset can be found on
[Kaggle](https://www.kaggle.com/datasets/elvinrustam/books-dataset/data).

Note

In a non-tutorial setting, you would bring your own data, possibly already in
a Snowflake table.

### Creating the database, schema, stage and warehouse¶

Run the following SQL code to set up the necessary database, schema, and
warehouse:

    
    
    CREATE DATABASE IF NOT EXISTS cortex_search_tutorial_db;
    
    CREATE OR REPLACE WAREHOUSE cortex_search_tutorial_wh WITH
        WAREHOUSE_SIZE='X-SMALL'
        AUTO_SUSPEND = 120
        AUTO_RESUME = TRUE
        INITIALLY_SUSPENDED=TRUE;
    
    USE WAREHOUSE cortex_search_tutorial_wh;
    

Copy

Note the following:

  * The `CREATE DATABASE` statement creates a database. The database automatically includes a schema named PUBLIC.

  * The `CREATE WAREHOUSE` statement creates an initially suspended warehouse.

## Step 2: Load the data into Snowflake¶

First create a stage to store the files downloaded from Kaggle. This stage
will hold the books dataset.

    
    
    CREATE OR REPLACE STAGE books_data_stage
        DIRECTORY = (ENABLE = TRUE)
        ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
    

Copy

Now upload the dataset. You can upload the dataset in Snowsight or using SQL.
To upload in Snowsight:

  1. Sign in to [Snowsight](../../../ui-snowsight).

  2. Select Data in the left-side navigation menu.

  3. Select your database `cortex_search_tutorial_db`.

  4. Select your schema `public`.

  5. Select Stages and select `books_data_stage`.

  6. On the top right, Select the \+ Files button.

  7. Drag and drop files into the UI or select Browse to choose a file from the dialog window.

  8. Select Upload to upload your file, `BooksDatasetClean.csv`

  9. Select the three dots on the right of the file and select Load into table.

  10. Name the table `BOOKS_DATASET_RAW` and select Next.

[![../../../../_images/basic_chatbot_tutorial_add_data.png](../../../../_images/basic_chatbot_tutorial_add_data.png)](../../../../_images/basic_chatbot_tutorial_add_data.png)

  11. In the left panel of the load data dialog, choose First line contains header from the Header menu.

  12. Then select Load.

## Step 3: Create a Chunking UDF¶

Feeding long documents to Cortex Search will not be performant because
retrieval models work best with small chunks of text. So next, create a Python
UDF to chunk the text. Navigate back to a SQL editor and execute the
following:

    
    
    CREATE OR REPLACE FUNCTION cortex_search_tutorial_db.public.books_chunk(
        description string, title string, authors string, category string, publisher string
    )
        returns table (chunk string, title string, authors string, category string, publisher string)
        language python
        runtime_version = '3.9'
        handler = 'text_chunker'
        packages = ('snowflake-snowpark-python','langchain')
        as
    $$
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    import copy
    from typing import Optional
    
    class text_chunker:
    
        def process(self, description: Optional[str], title: str, authors: str, category: str, publisher: str):
            if description == None:
                description = "" # handle null values
    
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size = 2000,
                chunk_overlap  = 300,
                length_function = len
            )
            chunks = text_splitter.split_text(description)
            for chunk in chunks:
                yield (title + "\n" + authors + "\n" + chunk, title, authors, category, publisher) # always chunk with title
    $$;
    

Copy

## Step 4: Build the Chunks Table¶

Create a table to store the chunks of text extracted from the transcripts.
Include the title and speaker in the chunk to provide context:

    
    
    CREATE TABLE cortex_search_tutorial_db.public.book_description_chunks AS (
        SELECT
            books.*,
            t.CHUNK as CHUNK
        FROM cortex_search_tutorial_db.public.books_dataset_raw books,
            TABLE(cortex_search_tutorial_db.public.books_chunk(books.description, books.title, books.authors, books.category, books.publisher)) t
    );
    

Copy

Verify the table contents:

    
    
    SELECT chunk, * FROM book_description_chunks LIMIT 10;
    

Copy

## Step 5: Create a Cortex Search Service¶

Create a Cortex Search Service on the table to allow you to search through the
chunks in the `book_description_chunks`:

    
    
    CREATE CORTEX SEARCH SERVICE cortex_search_tutorial_db.public.books_dataset_service
        ON CHUNK
        WAREHOUSE = cortex_search_tutorial_wh
        TARGET_LAG = '1 hour'
        AS (
            SELECT *
            FROM cortex_search_tutorial_db.public.book_description_chunks
        );
    

Copy

## Step 6: Create a Streamlit app¶

You can query the service with Python SDK (using the `snowflake` Python
package). This tutorial demonstrates using the Python SDK in a Streamlit in
Snowflake application.

First, ensure your global Snowsight UI role is the same as the role used to
create the service in the service creation step.

  1. Sign in to [Snowsight](../../../ui-snowsight).

  2. Select Projects » Streamlit in the left-side navigation menu.

  3. Select \+ Streamlit App.

  4. **Important** : Select the `cortex_search_tutorial_db` database and `public` schema for the app location.

  5. In the left pane of the Streamlit in Snowflake editor, select Packages and add `snowflake` (version >= 0.8.0) to install the package in your application.

  6. Replace the example application code with the following Streamlit app:
    
        import streamlit as st
    from snowflake.core import Root # requires snowflake>=0.8.0
    from snowflake.snowpark.context import get_active_session
    
    MODELS = [
        "mistral-large",
        "snowflake-arctic",
        "llama3-70b",
        "llama3-8b",
    ]
    
    def init_messages():
        """
        Initialize the session state for chat messages. If the session state indicates that the
        conversation should be cleared or if the "messages" key is not in the session state,
        initialize it as an empty list.
        """
        if st.session_state.clear_conversation or "messages" not in st.session_state:
            st.session_state.messages = []
    
    def init_service_metadata():
        """
        Initialize the session state for cortex search service metadata. Query the available
        cortex search services from the Snowflake session and store their names and search
        columns in the session state.
        """
        if "service_metadata" not in st.session_state:
            services = session.sql("SHOW CORTEX SEARCH SERVICES;").collect()
            service_metadata = []
            if services:
                for s in services:
                    svc_name = s["name"]
                    svc_search_col = session.sql(
                        f"DESC CORTEX SEARCH SERVICE {svc_name};"
                    ).collect()[0]["search_column"]
                    service_metadata.append(
                        {"name": svc_name, "search_column": svc_search_col}
                    )
    
            st.session_state.service_metadata = service_metadata
    
    def init_config_options():
        """
        Initialize the configuration options in the Streamlit sidebar. Allow the user to select
        a cortex search service, clear the conversation, toggle debug mode, and toggle the use of
        chat history. Also provide advanced options to select a model, the number of context chunks,
        and the number of chat messages to use in the chat history.
        """
        st.sidebar.selectbox(
            "Select cortex search service:",
            [s["name"] for s in st.session_state.service_metadata],
            key="selected_cortex_search_service",
        )
    
        st.sidebar.button("Clear conversation", key="clear_conversation")
        st.sidebar.toggle("Debug", key="debug", value=False)
        st.sidebar.toggle("Use chat history", key="use_chat_history", value=True)
    
        with st.sidebar.expander("Advanced options"):
            st.selectbox("Select model:", MODELS, key="model_name")
            st.number_input(
                "Select number of context chunks",
                value=5,
                key="num_retrieved_chunks",
                min_value=1,
                max_value=10,
            )
            st.number_input(
                "Select number of messages to use in chat history",
                value=5,
                key="num_chat_messages",
                min_value=1,
                max_value=10,
            )
    
        st.sidebar.expander("Session State").write(st.session_state)
    
    def query_cortex_search_service(query):
        """
        Query the selected cortex search service with the given query and retrieve context documents.
        Display the retrieved context documents in the sidebar if debug mode is enabled. Return the
        context documents as a string.
    
        Args:
            query (str): The query to search the cortex search service with.
    
        Returns:
            str: The concatenated string of context documents.
        """
        db, schema = session.get_current_database(), session.get_current_schema()
    
        cortex_search_service = (
            root.databases[db]
            .schemas[schema]
            .cortex_search_services[st.session_state.selected_cortex_search_service]
        )
    
        context_documents = cortex_search_service.search(
            query, columns=[], limit=st.session_state.num_retrieved_chunks
        )
        results = context_documents.results
    
        service_metadata = st.session_state.service_metadata
        search_col = [s["search_column"] for s in service_metadata
                        if s["name"] == st.session_state.selected_cortex_search_service][0]
    
        context_str = ""
        for i, r in enumerate(results):
            context_str += f"Context document {i+1}: {r[search_col]} \n" + "\n"
    
        if st.session_state.debug:
            st.sidebar.text_area("Context documents", context_str, height=500)
    
        return context_str
    
    def get_chat_history():
        """
        Retrieve the chat history from the session state limited to the number of messages specified
        by the user in the sidebar options.
    
        Returns:
            list: The list of chat messages from the session state.
        """
        start_index = max(
            0, len(st.session_state.messages) - st.session_state.num_chat_messages
        )
        return st.session_state.messages[start_index : len(st.session_state.messages) - 1]
    
    def complete(model, prompt):
        """
        Generate a completion for the given prompt using the specified model.
    
        Args:
            model (str): The name of the model to use for completion.
            prompt (str): The prompt to generate a completion for.
    
        Returns:
            str: The generated completion.
        """
        return session.sql("SELECT snowflake.cortex.complete(?,?)", (model, prompt)).collect()[0][0]
    
    def make_chat_history_summary(chat_history, question):
        """
        Generate a summary of the chat history combined with the current question to extend the query
        context. Use the language model to generate this summary.
    
        Args:
            chat_history (str): The chat history to include in the summary.
            question (str): The current user question to extend with the chat history.
    
        Returns:
            str: The generated summary of the chat history and question.
        """
        prompt = f"""
            [INST]
            Based on the chat history below and the question, generate a query that extend the question
            with the chat history provided. The query should be in natural language.
            Answer with only the query. Do not add any explanation.
    
            <chat_history>
            {chat_history}
            </chat_history>
            <question>
            {question}
            </question>
            [/INST]
        """
    
        summary = complete(st.session_state.model_name, prompt)
    
        if st.session_state.debug:
            st.sidebar.text_area(
                "Chat history summary", summary.replace("$", "\$"), height=150
            )
    
        return summary
    
    def create_prompt(user_question):
        """
        Create a prompt for the language model by combining the user question with context retrieved
        from the cortex search service and chat history (if enabled). Format the prompt according to
        the expected input format of the model.
    
        Args:
            user_question (str): The user's question to generate a prompt for.
    
        Returns:
            str: The generated prompt for the language model.
        """
        if st.session_state.use_chat_history:
            chat_history = get_chat_history()
            if chat_history != []:
                question_summary = make_chat_history_summary(chat_history, user_question)
                prompt_context = query_cortex_search_service(question_summary)
            else:
                prompt_context = query_cortex_search_service(user_question)
        else:
            prompt_context = query_cortex_search_service(user_question)
            chat_history = ""
    
        prompt = f"""
                [INST]
                You are a helpful AI chat assistant with RAG capabilities. When a user asks you a question,
                you will also be given context provided between <context> and </context> tags. Use that context
                with the user's chat history provided in the between <chat_history> and </chat_history> tags
                to provide a summary that addresses the user's question. Ensure the answer is coherent, concise,
                and directly relevant to the user's question.
    
                If the user asks a generic question which cannot be answered with the given context or chat_history,
                just say "I don't know the answer to that question.
    
                Don't saying things like "according to the provided context".
    
                <chat_history>
                {chat_history}
                </chat_history>
                <context>
                {prompt_context}
                </context>
                <question>
                {user_question}
                </question>
                [/INST]
                Answer:
            """
        return prompt
    
    def main():
        st.title(f":speech_balloon: Chatbot with Snowflake Cortex")
    
        init_service_metadata()
        init_config_options()
        init_messages()
    
        icons = {"assistant": "❄️", "user": "👤"}
    
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar=icons[message["role"]]):
                st.markdown(message["content"])
    
        disable_chat = (
            "service_metadata" not in st.session_state
            or len(st.session_state.service_metadata) == 0
        )
        if question := st.chat_input("Ask a question...", disabled=disable_chat):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": question})
            # Display user message in chat message container
            with st.chat_message("user", avatar=icons["user"]):
                st.markdown(question.replace("$", "\$"))
    
            # Display assistant response in chat message container
            with st.chat_message("assistant", avatar=icons["assistant"]):
                message_placeholder = st.empty()
                question = question.replace("'", "")
                with st.spinner("Thinking..."):
                    generated_response = complete(
                        st.session_state.model_name, create_prompt(question)
                    )
                    message_placeholder.markdown(generated_response)
    
            st.session_state.messages.append(
                {"role": "assistant", "content": generated_response}
            )
    
    if __name__ == "__main__":
        session = get_active_session()
        root = Root(session)
        main()
    

Copy

## Step 7: Try out the app¶

Enter a query in the text box to try out your new app. Some sample queries you
can try are:

  * `I like Harry Potter. Can you recommend more books I will like?`

  * `Can you recommend me books on Greek Mythology?`

## Step 7: Clean up¶

### Clean up (optional)¶

Execute the following [DROP <object>](../../../../sql-reference/sql/drop)
commands to return your system to its state before you began the tutorial:

    
    
    DROP DATABASE IF EXISTS cortex_search_tutorial_db;
    DROP WAREHOUSE IF EXISTS cortex_search_tutorial_wh;
    

Copy

Dropping the database automatically removes all child database objects such as
tables.

## Next steps¶

Congratulations! You have successfully built a simple search app on text data
in Snowflake. You can move on to [Tutorial 3](cortex-search-tutorial-3-chat-
advanced) to see how to build an AI chatbot with Cortex Search from a set of
PDF files.

### Additional resources¶

Continue learning using the following resources:

  * [Cortex Search overview](../cortex-search-overview)

  * [Query a Cortex Search Service](../query-cortex-search-service)


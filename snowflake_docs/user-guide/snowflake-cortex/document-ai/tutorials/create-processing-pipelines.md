[![Snowflake logo in black \(no text\)](../../../../_images/logo-snowflake-
black.png)](../../../../_images/logo-snowflake-black.png) Feature — Generally
Available

Available to accounts in [AWS and Microsoft Azure commercial
regions](../../../intro-regions.html#label-na-general-regions), with some
exceptions. For more information, see [Document AI
availability](../limitations.html#label-document-ai-availability).

# Tutorial: Create a document processing pipeline with Document AI¶

## Introduction¶

With Document AI, you can process documents of various formats, and extract
information from both text-heavy paragraphs and the images that contain text,
such as logos, handwritten text (signatures), or checkmarks. This tutorial
introduces you to Document AI by setting up the required objects and
privileges, and creating a Document AI model build to use in a processing
pipeline.

The tutorial uses the Snowsight web interface. For the steps that require
using SQL, you can use any Snowflake client that supports executing SQL.

### What you will learn¶

In this tutorial, you will learn how to:

  * Set up the objects and privileges required to work with Document AI.

  * Prepare a Document AI model build using Document AI user interface in Snowsight to extract data from unstructured documents.

  * Create a pipeline for continuous processing of new documents in stage, using a Document AI model build, and streams and tasks.

### Prerequisites¶

The following prerequisites are required to complete this tutorial:

  * You must connect as a user that has the ACCOUNTADMIN role which is used to create a custom role used in this tutorial and grant the new role required privileges.

  * You must have a Snowflake account in one of the commercial regions supported for Document AI. For more information about supported regions, see [Document AI availability](../limitations.html#label-document-ai-availability).

  * You must have a warehouse ready to use with Document AI. For more information about selecting a warehouse, see [Determining optimal warehouse size for Document AI](../cost-governance.html#label-document-ai-determining-optimal-warehouse-size).

## Set up the required objects and privileges¶

In this section, you will:

  * Create a database and schema to contain the Document AI model build.

  * Create a custom role to prepare a Document AI model build and a document processing pipeline.

  * Grant the required privileges to the custom role.

### Create a database, schema, and custom role¶

To create a database, schema, and a role to work with Document AI, do the
following:

  1. Create a database and schema in which to create a Document AI model build:
    
        CREATE DATABASE doc_ai_db;
    CREATE SCHEMA doc_ai_db.doc_ai_schema;
    

Copy

  2. Create custom role `doc_ai_role` to prepare the Document AI model build and to create processing pipelines:
    
        USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE doc_ai_role;
    

Copy

### Grant the required privileges¶

To grant the privileges required to work with Document AI, do the following:

  1. Grant the SNOWFLAKE.DOCUMENT_INTELLIGENCE_CREATOR database role to the `doc_ai_role` role:
    
        GRANT DATABASE ROLE SNOWFLAKE.DOCUMENT_INTELLIGENCE_CREATOR TO ROLE doc_ai_role;
    

Copy

  2. Grant warehouse usage and operating privileges to the `doc_ai_role` role:
    
        GRANT USAGE, OPERATE ON WAREHOUSE <your_warehouse> TO ROLE doc_ai_role;
    

Copy

  3. Grant the privileges to use the database and schema you created to the `doc_ai_role`:
    
        GRANT USAGE ON DATABASE doc_ai_db TO ROLE doc_ai_role;
    GRANT USAGE ON SCHEMA doc_ai_db.doc_ai_schema TO ROLE doc_ai_role;
    

Copy

  4. Grant the create stage privilege on the schema to the `doc_ai_role` role to store the documents for extraction:
    
        GRANT CREATE STAGE ON SCHEMA doc_ai_db.doc_ai_schema TO ROLE doc_ai_role;
    

Copy

  5. Grant the privilege to create model builds (instances of the DOCUMENT_INTELLIGENCE class) to the `doc_ai_role` role:
    
        GRANT CREATE SNOWFLAKE.ML.DOCUMENT_INTELLIGENCE ON SCHEMA doc_ai_db.doc_ai_schema TO ROLE doc_ai_role;
    

Copy

  6. Grant the privileges required to create a processing pipeline using streams and tasks to the `doc_ai_role` role:
    
        GRANT CREATE STREAM, CREATE TABLE, CREATE TASK, CREATE VIEW ON SCHEMA doc_ai_db.doc_ai_schema TO ROLE doc_ai_role;
    GRANT EXECUTE TASK ON ACCOUNT TO ROLE doc_ai_role;
    

Copy

  7. Grant the `doc_ai_role` to tutorial user for use in the next steps of the tutorial:
    
        GRANT ROLE doc_ai_role TO USER <your_user_name>;
    

Copy

### What you learned in this section¶

In this section you learned how to:

  * Create the database and schema to contain a Document AI model build.

  * Create the `doc_ai_role` custom role.

  * Grant required privileges to the `doc_ai_role` role, and grant that role to the tutorial user.

## Prepare a Document AI model build¶

In this section, you will prepare a Document AI model build by creating the
model build and uploading documents to test the model.

The Document AI model build represents a single type of the document. For this
tutorial, you will create a model build for extracting information from
inspection reviews. The Document AI model build includes the model, the data
values to be extracted, and the documents uploaded to test the model.

### Create a Document AI model build¶

To create a Document AI model build, do the following:

  1. Sign in to Snowsight.

  2. In the navigation menu, select AI & ML » Document AI.

  3. Select a warehouse.

  4. Select \+ Build.

  5. In the dialog that appears, enter `inspection_reviews` as a name for your model build, and select the location (`doc_ai_db` database and `doc_ai_schema` schema).

  6. Select Create.

### Upload documents to the Document AI model build¶

To upload documents to the newly created Document AI model build, do the
following:

  1. To obtain the documents required for the tutorial to test the model build, download the [`zip file`](../../../../_downloads/46f477f3cfc07018ed96294a4600745c/testing_dataset.zip) to your local file system.

  2. Unzip the content, which includes PDF documents.

  3. In the `inspection_reviews` model build, select the Build Details tab.

  4. Select Upload documents.

  5. Select Browse or drag the documents you downloaded.

  6. Select Upload.

### What you learned in this section¶

In this section you learned how to:

  * Create a Document AI model build.

  * Upload documents to test the Document AI model build.

## Define data values and review the results¶

In this section, you will define data values by asking the Document AI model
questions in natural language. You will then review the answers that the model
provides.

Data values are the information you want to extract from documents. A value
consists of a value name and a question asked in natural language.

To define values for the Document AI model build:

  1. In the `inspection_reviews` model build, select the Build Details tab.

  2. Select Define values.

  3. In the Documents review view, select \+ Value.

  4. For each document, enter the following pairs of value names and questions:

     * `inspection_date`: What is the inspection date?

     * `inspection_grade`: What is the grade?

     * `inspector`: Who performed the inspection?

     * `list_of_units`: What are all the units?

  5. For each document and data value, review the answers that the model provides:

     * If the answer is correct, select the checkmark.

     * If the answer is incorrect, enter the correct value manually.

### What you learned in this section¶

In this section you learned how to:

  * Define data values to extract by asking the model questions in natural language.

  * Review results by confirming or correcting the answers that the model provided.

## Publish a Document AI model build¶

In this section, you will publish the Document AI model build to use it for
extraction in processing pipelines. Publishing the model build enables using
the latest version of the model build in production.

To publish the model build, do the following:

  1. In the `inspection_reviews` model build, select the Build Details tab.

  2. Under Model accuracy, select Publish version.

  3. In the dialog that appears, select Publish to confirm.

Note

If the model accuracy and the results are not satisfactory, you can optionally
fine-tune the model to improve it. Fine-tuning is not a part of this tutorial.
For more information about evaluating and training the model, see [Evaluate a
Document AI model](../prepare-model-build.html#label-document-ai-evaluate-
model).

### What you learned in this section¶

In this section you published the Document AI model build to use the model
build for extraction in processing pipelines.

## Create a document processing pipeline¶

In this section, you will create a processing pipeline using the already
prepared Document AI model build, streams, and tasks. The pipeline will
extract information from new inspection documents stored in an internal stage.

To create a processing pipeline:

  * Set up the pipeline using streams and tasks.

  * Upload new documents to an internal stage.

  * View the extracted information.

### Set up the processing pipeline¶

  1. Create an internal `my_pdf_stage` stage to store the documents:
    
        CREATE OR REPLACE STAGE my_pdf_stage
      DIRECTORY = (ENABLE = TRUE)
      ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
    

Copy

  2. Create a `my_pdf_stream` stream on a `my_pdf_stage` stage:

> >     CREATE STREAM my_pdf_stream ON STAGE my_pdf_stage;
>  
>
> Copy

  3. Refresh the metadata of the directory table that will store the staged document files:

> >     ALTER STAGE my_pdf_stage REFRESH;
>  
>
> Copy

  4. Specify the database and schema:

> >     USE DATABASE doc_ai_db;
>     USE SCHEMA doc_ai_schema;
>  
>
> Copy

  5. Create a `pdf_reviews` table to store the information about the documents (such as `file_name`) and the data to be extracted from the PDF documents:

> >     CREATE OR REPLACE TABLE pdf_reviews (
>       file_name VARCHAR,
>       file_size VARIANT,
>       last_modified VARCHAR,
>       snowflake_file_url VARCHAR,
>       json_content VARCHAR
>     );
>  
>
> Copy
>
> The `json_content` column will include the extracted information in JSON
> format.

  6. Create a `load_new_file_data` task to process new documents in the stage:
    
        CREATE OR REPLACE TASK load_new_file_data
      WAREHOUSE = <your_warehouse>
      SCHEDULE = '1 minute'
      COMMENT = 'Process new files in the stage and insert data into the pdf_reviews table.'
    WHEN SYSTEM$STREAM_HAS_DATA('my_pdf_stream')
    AS
    INSERT INTO pdf_reviews (
      SELECT
        RELATIVE_PATH AS file_name,
        size AS file_size,
        last_modified,
        file_url AS snowflake_file_url,
        inspection_reviews!PREDICT(GET_PRESIGNED_URL('@my_pdf_stage', RELATIVE_PATH), 1) AS json_content
      FROM my_pdf_stream
      WHERE METADATA$ACTION = 'INSERT'
    );
    

Copy

Note that newly created tasks are automatically suspended.

  7. Start the newly created task:
    
        ALTER TASK load_new_file_data RESUME;
    

Copy

Note

Document AI does not support [serverless tasks](../../../tasks-
intro.html#label-tasks-compute-resources-serverless).

### Upload new documents to an internal stage¶

  1. To obtain the documents required for the tutorial, download the [`zip file`](../../../../_downloads/79147fc17de2a37ecd330f0e45f29bf3/extraction_dataset.zip) to your local file system.

  2. Unzip the content, which includes PDF files.

  3. In Snowsight, select Data » Databases.

  4. Select the `doc_ai_db` database, the `doc_ai_schema`, and the `my_pdf_stage` stage.

  5. Select \+ Files.

  6. In the Upload Your Files dialog that appears, select the files you just downloaded.

  7. Select Upload.

### View the extracted information¶

  1. After uploading the documents to the stage, view the information extracted from new documents:
    
        SELECT * FROM pdf_reviews;
    

Copy

  2. Create a `pdf_reviews_2` table to analyze the extracted information in separate columns:

> >     CREATE OR REPLACE TABLE doc_ai_db.doc_ai_schema.pdf_reviews_2 AS (
>      WITH temp AS (
>        SELECT
>          RELATIVE_PATH AS file_name,
>          size AS file_size,
>          last_modified,
>          file_url AS snowflake_file_url,
>          inspection_reviews!PREDICT(get_presigned_url('@my_pdf_stage',
> RELATIVE_PATH), 1) AS json_content
>        FROM directory(@my_pdf_stage)
>      )
>  
>      SELECT
>        file_name,
>        file_size,
>        last_modified,
>        snowflake_file_url,
>        json_content:__documentMetadata.ocrScore::FLOAT AS ocrScore,
>        f.value:score::FLOAT AS inspection_date_score,
>        f.value:value::STRING AS inspection_date_value,
>        g.value:score::FLOAT AS inspection_grade_score,
>        g.value:value::STRING AS inspection_grade_value,
>        i.value:score::FLOAT AS inspector_score,
>        i.value:value::STRING AS inspector_value,
>        ARRAY_TO_STRING(ARRAY_AGG(j.value:value::STRING), ', ') AS
> list_of_units
>      FROM temp,
>        LATERAL FLATTEN(INPUT => json_content:inspection_date) f,
>        LATERAL FLATTEN(INPUT => json_content:inspection_grade) g,
>        LATERAL FLATTEN(INPUT => json_content:inspector) i,
>        LATERAL FLATTEN(INPUT => json_content:list_of_units) j
>      GROUP BY ALL
>     );
>  
>
> Copy

  3. View the output:
    
        SELECT * FROM pdf_reviews_2;
    

Copy

The table uses the [FLATTEN](../../../../sql-reference/functions/flatten)
function to parse the `json_content` JSON into separate columns for easier
viewing.

The table contains the data values (such as `inspection_grade_value`,
`inspection_date_value`) that were defined when the model build was prepared
for inspection documents, and the corresponding confidence scores
(`inspection_grade_score`, `inspection_date_score`).

### What you learned in this section¶

In this section you learned how to:

  * Create an internal stage to store new documents.

  * Create a stream and a task required to prepare a processing pipeline.

  * Upload documents to an internal stage.

  * View the extracted information in a table.

## Learn more¶

Congratulations! You have successfully completed this tutorial. You are now
ready to start working with Document AI on your own use cases.

Along the way, you learned how to:

  * Set up the required objects and privileges to work with Document AI.

  * Create a Document AI model build.

  * Upload documents to the Document AI model build to test the model.

  * Define the data values to extract by asking the model questions in natural language.

  * Review the results by confirming or correcting the answers that the model provides.

  * Publish the Document AI model build to use the model build for extraction in processing pipelines.

  * Prepare a document processing pipeline by creating a stream and a task and using the Document AI model build to extract information from new documents.

### Additional resources¶

Continue learning using the following resources:

  * [Working with Document AI](../working-with-document-ai)

  * [Question optimization for extracting information with Document AI](../optimizing-questions)

  * [Prepare your documents for Document AI](../preparing-documents)

  * [Introduction to Streams](../../../streams-intro)

  * [Introduction to tasks](../../../tasks-intro)

  * [Stream and task commands](../../../../sql-reference/commands-stream)


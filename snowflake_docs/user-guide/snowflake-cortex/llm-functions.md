# Large Language Model (LLM) Functions (Snowflake Cortex)¶

Supported regions

Available to all accounts in select regions.

Snowflake Cortex gives you instant access to industry-leading large language
models (LLMs) trained by researchers at companies like Mistral, Reka, Meta,
and Google, including [Snowflake Arctic](https://www.snowflake.com/en/data-
cloud/arctic/), an open enterprise-grade model developed by Snowflake.

Since these LLMs are fully hosted and managed by Snowflake, using them
requires no setup. Your data stays within Snowflake, giving you the
performance, scalability, and governance you expect.

## Available functions¶

Snowflake Cortex features are provided as SQL functions and are also available
in Python. Cortex LLM Functions can be grouped into the following categories:

  * COMPLETE function

  * Task-specific functions

  * Helper functions

### COMPLETE function¶

The COMPLETE function is a general purpose function that can perform a wide
range of user-specified tasks, such as aspect-based sentiment classification,
synthetic data generation, and customized summaries. Cortex Guard is a safety
parameter available within the COMPLETE function designed to filter possible
unsafe and harmful responses from a language model. You can also use this
function with your fine-tuned models.

### Task-specific functions¶

Task-specific functions are purpose-built and managed functions that automate
routine tasks, like simple summaries and quick translations, that don’t
require any customization.

  * CLASSIFY_TEXT: Given a piece of text, classifies it into one of the categories that you define.

  * EXTRACT_ANSWER: Given a question and unstructured data, returns the answer to the question if it can be found in the data.

  * PARSE_DOCUMENT: Given an internal or external stage with documents, returns an object that contains a JSON-formatted string with extracted text content using OCR mode, or the extracted text and layout elements using LAYOUT mode.

  * SENTIMENT: Returns a sentiment score, from -1 to 1, representing the detected positive or negative sentiment of the given text.

  * SUMMARIZE: Returns a summary of the given text.

  * TRANSLATE: Translates given text from any supported language to any other.

  * EMBED_TEXT_768: Given a piece of text, returns a [vector embedding](vector-embeddings) of 768 dimensions that represents that text.

  * EMBED_TEXT_1024: Given a piece of text, returns a [vector embedding](vector-embeddings) of 1024 dimensions that represents that text.

### Helper functions¶

Helper functions are purpose-built and managed functions that reduce cases of
failures when running other LLM functions, for example by getting the count of
tokens in an input prompt to ensure the call doesn’t exceed a model limit.

  * COUNT_TOKENS: Given an input text, returns the token count based on the model or Cortex function specified.

  * TRY_COMPLETE: Works like the COMPLETE function, but returns NULL when the function could not execute instead of an error code.

## Required privileges¶

The CORTEX_USER database role in the SNOWFLAKE database includes the
privileges that allow users to call Snowflake Cortex LLM functions. By
default, the CORTEX_USER role is granted to the PUBLIC role. The PUBLIC role
is automatically granted to all users and roles, so this allows all users in
your account to use the Snowflake Cortex LLM functions.

If you don’t want all users to have this privilege, you can revoke access to
the PUBLIC role and grant access to specific roles.

To revoke the CORTEX_USER database role from the PUBLIC role, run the
following commands using the ACCOUNTADMIN role:

    
    
    REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER
      FROM ROLE PUBLIC;
    
    REVOKE IMPORTED PRIVILEGES ON DATABASE SNOWFLAKE
      FROM ROLE PUBLIC;
    

Copy

You can then selectively provide access to specific roles. The
SNOWFLAKE.CORTEX_USER database role cannot be granted directly to a user. For
more information, see [Using SNOWFLAKE database roles](../../sql-
reference/snowflake-db-roles.html#label-using-snowflake-db-roles). A user with
the ACCOUNTADMIN role can grant this role to a custom role in order to allow
users to access Cortex LLM Functions. In the following example, use the
ACCOUNTADMIN role and grant the user `some_user` the CORTEX_USER database role
via the account role `cortex_user_role`, which you create for this purpose.

    
    
    USE ROLE ACCOUNTADMIN;
    
    CREATE ROLE cortex_user_role;
    GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE cortex_user_role;
    
    GRANT ROLE cortex_user_role TO USER some_user;
    

Copy

You can also grant access to Snowflake Cortex LLM functions through existing
roles commonly used by specific groups of users. (See [User roles](../admin-
user-management.html#label-user-management-user-roles).) For example, if you
have created an `analyst` role that is used as a default role by analysts in
your organization, you can easily grant these users access to Snowflake Cortex
LLM functions with a single GRANT statement.

    
    
    GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE analyst;
    

Copy

## Availability¶

Snowflake Cortex LLM functions are currently available in the following
regions. To access LLMs from regions not listed, use [cross-region inference
parameter](cross-region-inference.html#label-use-cross-region-inference).

Note

  * The TRY_COMPLETE function is available in the same regions as COMPLETE.

  * The COUNT_TOKENS function is available in all regions, but model inference is region-specific, as per the table.

Function (Model) |  AWS US West 2 (Oregon) |  AWS US East 1 (N. Virginia) |  AWS Europe Central 1 (Frankfurt) |  AWS Europe West 1 (Ireland) |  AWS AP Southeast 2 (Sydney) |  AWS AP Northeast 1 (Tokyo) |  Azure East US 2 (Virginia) |  Azure West Europe (Netherlands)  
---|---|---|---|---|---|---|---|---  
COMPLETE (`llama3.2-1b`) | ✔ |  |  |  |  |  |  |   
COMPLETE (`llama3.2-3b`) | ✔ |  |  |  |  |  |  |   
COMPLETE (`llama3.1-8b`) | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ | ✔  
COMPLETE (`llama3.1-70b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
COMPLETE (`llama3.1-405b`) | ✔ | ✔ |  |  |  |  | ✔ |   
COMPLETE (`snowflake-arctic`) | ✔ |  |  |  |  |  |  |   
COMPLETE (`reka-core`) |  | ✔ |  |  |  |  |  |   
COMPLETE (`reka-flash`) | ✔ | ✔ |  |  |  | ✔ |  |   
COMPLETE (`mistral-large2`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
COMPLETE (`mixtral-8x7b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
COMPLETE (`mistral-7b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
COMPLETE (`jamba-instruct`) | ✔ |  | ✔ |  |  | ✔ |  |   
COMPLETE (`jamba-1.5-mini`) | ✔ |  | ✔ |  |  | ✔ |  |   
COMPLETE (`jamba-1.5-large`) | ✔ |  |  |  |  |  |  |   
COMPLETE (`gemma-7b`) | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔  
COMPLETE (`claude-3-5-sonnet`) | Coming soon |  |  |  |  |  |  |   
EMBED_TEXT_768 (`e5-base-v2`) | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔  
EMBED_TEXT_768 (`snowflake-arctic-embed-m`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EMBED_TEXT_768 (`snowflake-arctic-embed-m-v1.5`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EMBED_TEXT_1024 (`snowflake-arctic-embed-l-v2.0`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EMBED_TEXT_1024 (`nv-embed-qa-4`) | ✔ |  |  |  |  |  |  |   
EMBED_TEXT_1024 (`multilingual-e5-large`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EMBED_TEXT_1024 (`voyage-multilingual-2`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
CLASSIFY_TEXT | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EXTRACT_ANSWER | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
SENTIMENT | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
SUMMARIZE | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
TRANSLATE | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
  
The following Snowflake Cortex LLM functions are currently available in the
following extended regions.

Function (Model) |  AWS US East 2 (Ohio) |  AWS CA Central 1 (Central) |  AWS SA East 1 (São Paulo) |  AWS Europe West 2 (London) |  AWS Europe Central 1 (Frankfurt) |  AWS Europe North 1 (Stockholm) |  AWS AP Northeast 1 (Tokyo) |  AWS AP South 1 (Mumbai) |  AWS AP Southeast 2 (Syndey) |  AWS AP Southeast 3 (Jakarta) |  Azure South Central US (Texas) |  Azure UK South (London) |  Azure North Europe (Ireland) |  Azure Switzerland North (Zürich) |  Azure Central India (Pune) |  Azure Japan East (Tokyo, Saitama) |  Azure Southeast Asia (Singapore) |  Azure Australia East (New South Wales) |  GCP Europe West 2 (London) |  GCP Europe West 4 (Netherlands) |  GCP US Central 1 (Iowa) |  GCP US East 4 (N. Virginia)  
---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---  
EMBED_TEXT_768 (`snowflake-arctic-embed-m-v1.5`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EMBED_TEXT_768 (`snowflake-arctic-embed-m`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
EMBED_TEXT_1024 (`multilingual-e5-large`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔  
  
The following table lists legacy models. If you’re just getting started, start
with models in the previous tables:

Legacy¶ Function (Model) |  AWS US West 2 (Oregon) |  AWS US East 1 (N. Virginia) |  AWS Europe Central 1 (Frankfurt) |  AWS Europe West 1 (Ireland) |  AWS AP Southeast 2 (Sydney) |  AWS AP Northeast 1 (Tokyo) |  Azure East US 2 (Virginia) |  Azure West Europe (Netherlands)  
---|---|---|---|---|---|---|---|---  
COMPLETE (`llama2-70b-chat`) | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔  
COMPLETE (`llama3-8b`) | ✔ | ✔ | ✔ |  | ✔ | ✔ | ✔ |   
COMPLETE (`llama3-70b`) | ✔ | ✔ | ✔ |  |  | ✔ | ✔ |   
COMPLETE (`mistral-large`) | ✔ | ✔ | ✔ |  |  |  | ✔ | ✔  
  
## Cost considerations¶

Note

PARSE_DOCUMENT billing that scales with the number of pages processed is
expected soon.

Snowflake Cortex LLM functions incur compute cost based on the number of
tokens processed. Refer to the [Snowflake Service Consumption
Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for
each function’s cost in credits per million tokens.

A token is the smallest unit of text processed by Snowflake Cortex LLM
functions, approximately equal to four characters. The equivalence of raw
input or output text to tokens can vary by model.

  * For functions that generate new text in the response (COMPLETE, CLASSIFY_TEXT, SUMMARIZE, and TRANSLATE), both input and output tokens are counted.

  * For CORTEX GUARD, only input tokens are counted. The number of input tokens is based on the number of output tokens per LLM model used in the COMPLETE function.

  * For the EMBED_TEXT_* functions, only input tokens are counted.

  * For functions that only extract information from the input (EXTRACT_ANSWER and SENTIMENT), only input tokens are counted.

  * For EXTRACT_ANSWER, the number of billable tokens is the sum of the number of tokens in the `from_text` and `question` fields.

  * SUMMARIZE, TRANSLATE, EXTRACT_ANSWER, CLASSIFY_TEXT, and SENTIMENT add a prompt to the input text in order to generate the response. As a result, the input token count is slightly higher than the number of tokens in the text you provide.

  * TRY_COMPLETE does not incur costs for error handling. This means that if the TRY_COMPLETE function returns NULL, no cost is incurred.

  * COUNT_TOKENS incurs only compute cost to run the function. No additional token based costs are incurred.

Snowflake recommends executing queries that call a Snowflake Cortex LLM
Function or the Cortex PARSE_DOCUMENT function with a smaller warehouse (no
larger than MEDIUM) because larger warehouses do not increase performance. The
cost associated with keeping a warehouse active will continue to apply when
executing a query that calls a Snowflake Cortex LLM Function. For general
information on compute costs, see [Understanding compute cost](../cost-
understanding-compute).

### Track costs for AI services¶

To track credits used for AI Services including LLM Functions in your account,
use the [METERING_HISTORY view](../../sql-reference/account-
usage/metering_history):

    
    
    SELECT *
      FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
      WHERE SERVICE_TYPE='AI_SERVICES';
    

Copy

### Track credit consumption for LLM functions¶

To view the credit and token consumption for each LLM function call, use the
[CORTEX_FUNCTIONS_USAGE_HISTORY view](../../sql-reference/account-
usage/cortex_functions_usage_history):

    
    
    SELECT *
      FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_USAGE_HISTORY;
    

Copy

## Usage quotas¶

To ensure that all Snowflake customers can access LLM capabilities, Snowflake
Cortex LLM functions may be subject to throttling during periods of high
utilization. Usage quotas are not applied at the account level.

Throttled requests will receive an error response and should be retried later.

Note

On-demand Snowflake accounts without a valid payment method (such as trial
accounts) are limited to roughly one credit per day in Snowflake Cortex LLM
function usage. To remove this restriction, [convert your trial account to a
paid account](../admin-trial-account.html#label-trial-account-convert).

## Managing costs and throttling¶

Snowflake recommends using a warehouse size no larger than MEDIUM when calling
Snowflake Cortex LLM functions. Using a larger warehouse than necessary does
not increase performance, but can result in unnecessary costs and a higher
risk of throttling. This recommendation might not apply in the future due to
upcoming product updates.

## Model restrictions¶

Models used by Snowflake Cortex have limitations on size as described in the
table below. Sizes are given in tokens. Tokens generally represent about four
characters of text, so the number of words corresponding to a limit is less
than the number of tokens. Inputs that exceed the limit result in an error.

Important

In the AWS AP Southeast 2 (Sydney) region, the context window for the
following models are 4k:

  * `llama3-8b` and `mistral-7b` for the COMPLETE function.

  * Snowflake managed model from the SUMMARIZE function.

In the AWS Ireland region, the context window for `llama3.1-8b` is 16,384.

Function | Model | Context window (tokens)  
---|---|---  
COMPLETE | `snowflake-arctic` | 4,096  
| `mistral-large` | 32,000  
| `mistral-large2` | 128,000  
| `reka-flash` | 100,000  
| `reka-core` | 32,000  
| `jamba-instruct` | 256,000  
| `jamba-1.5-mini` | 256,000  
| `jamba-1.5-large` | 256,000  
| `mixtral-8x7b` | 32,000  
| `llama2-70b-chat` | 4,096  
| `llama3-8b` | 8,000  
| `llama3-70b` | 8,000  
| `llama3.1-8b` | 128,000  
| `llama3.1-70b` | 128,000  
| `llama3.1-405b` | 128,000  
| `llama3.2-1b` | 128,000  
| `llama3.2-3b` | 128,000  
| `mistral-7b` | 32,000  
| `gemma-7b` | 8,000  
EMBED_TEXT_768 | `e5-base-v2` | 512  
| `snowflake-arctic-embed-m` | 512  
EMBED_TEXT_1024 | `nv-embed-qa-4` | 512  
| `multilingual-e5-large` | 512  
| `voyage-multilingual-2` | 32,000  
CLASSIFY_TEXT | Snowflake managed model | 128,000  
EXTRACT_ANSWER | Snowflake managed model |  2,048 for text 64 for question  
SENTIMENT | Snowflake managed model | 512  
SUMMARIZE | Snowflake managed model | 32,000  
TRANSLATE | Snowflake managed model | 4,096  
  
## Choosing a model¶

The Snowflake Cortex COMPLETE function supports multiple models of varying
capability, latency, and cost. These models have been carefully chosen to
align with common customer use cases. To achieve the best performance per
credit, choose a model that’s a good match for the content size and complexity
of your task. Here are brief overviews of the available models.

### Large models¶

If you’re not sure where to start, try the most capable models first to
establish a baseline to evaluate other models. `reka-core` and `mistral-
large2` are the most capable models offered by Snowflake Cortex, and will give
you a good idea what a state-of-the-art model can do.

  * `reka-core` is Reka AI’s most advanced large language model with strong reasoning abilities, code generation, and multilingual fluency.

  * `mistral-large2` is Mistral AI’s most advanced large language model with top-tier reasoning capabilities. Compared to `mistral-large`, it’s significantly more capable in code generation, mathematics, reasoning, and provides much stronger multilingual support. It’s ideal for complex tasks that require large reasoning capabilities or are highly specialized, such as synthetic text generation, code generation, and multilingual text analytics.

  * `llama3.1-405b` is an open source model from the `llama3.1` model family from Meta with a large 128K context window. It excels in long document processing, multilingual support, synthetic data generation and model distillation.

### Medium models¶

  * `llama3.1-70b` is an open source model that demonstrates state-of-the-art performance ideal for chat applications, content creation, and enterprise applications. It is a highly performant, cost effective model that enables diverse use cases with a context window of 128K. `llama3-70b` is still supported and has a context window of 8K.

  * `snowflake-arctic` is Snowflake’s top-tier enterprise-focused LLM. Arctic excels at enterprise tasks such as SQL generation, coding and instruction following benchmarks.

  * `reka-flash` is a highly capable multilingual language model optimized for fast workloads that require high quality, such as writing product descriptions or blog posts, coding, and extracting answers from documents with hundreds of pages.

  * `mixtral-8x7b` is ideal for text generation, classification, and question answering. Mistral models are optimized for low latency with low memory requirements, which translates into higher throughput for enterprise use cases.

  * The `jamba-Instruct` model is built by AI21 Labs to efficiently meet enterprise requirements. It is optimized to offer a 256k token context window with low cost and latency, making it ideal for tasks like summarization, Q&A, and entity extraction on lengthy documents and extensive knowledge bases.

  * The AI21 Jamba 1.5 family of models is state-of-the-art, hybrid SSM-Transformer instruction following foundation models. The `jamba-1.5-mini` and `jamba-1.5-large` with a context length of 256K supports use cases such as structured output (JSON), and grounded generation.

### Small models¶

  * The `llama3.2-1b` and `llama3.2-3b` models support context length of 128K tokens and are state-of-the-art in their class for use cases like summarization, instruction following, and rewriting tasks. The Llama 3.2 models deliver multilingual capabilities, with support for English, German, French, Italian, Portuguese, Hindi, Spanish and Thai.

  * `llama3.1-8b` is ideal for tasks that require low to moderate reasoning. It’s a light-weight, ultra-fast model with a context window of 128K. `llama3-8b` and `llama2-70b-chat` are still supported models that provide a smaller context window and relatively lower accuracy.

  * `mistral-7b` is ideal for your simplest summarization, structuration, and question answering tasks that need to be done quickly. It offers low latency and high throughput processing for multiple pages of text with its 32K context window.

  * `gemma-7b` is suitable for simple code and text completion tasks. It has a context window of 8,000 tokens but is surprisingly capable within that limit, and quite cost-effective.

The following table provides information on how popular models perform on
various benchmarks, including the models offered by Snowflake Cortex COMPLETE
as well as a few other popular models.

Model |  Context Window (Tokens) |  MMLU (Reasoning) |  HumanEval (Coding) |  GSM8K (Arithmetic Reasoning) |  Spider 1.0 (SQL)  
---|---|---|---|---|---  
[GPT 4.o](https://openai.com/index/hello-gpt-4o/)* | 128,000 | 88.7 | 90.2 | 96.4 | -  
[llama3.1-405b](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) | 128,000 | 88.6 | 89 | 96.8 | -  
[reka-core](https://arxiv.org/pdf/2404.12387) | 32,000 | 83.2 | 76.8 | 92.2 | -  
[llama3.1-70b](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) | 128,000 | 86 | 80.5 | 95.1 | -  
[mistral-large2](https://mistral.ai/news/mistral-large-2407/) | 128,000 | 84 | 92 | 93 | -  
[mistral-large](https://mistral.ai/news/mistral-large/) | 32,000 | 81.2 | 45.1 | 81 | 81  
[reka-flash](https://arxiv.org/pdf/2404.12387) | 100,000 | 75.9 | 72 | 81 | -  
[llama3.1-8b](https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md) | 128,000 | 73 | 72.6 | 84.9 | -  
[mixtral-8x7b](https://mistral.ai/news/mixtral-of-experts/) | 32,000 | 70.6 | 40.2 | 60.4 | -  
[llama-2-70b-chat](https://huggingface.co/meta-llama/Llama-2-70b-chat) | 4,096 | 68.9 | 30.5 | 57.5 | -  
[jamba-instruct](https://www.ai21.com/jamba) | 256,000 | 68.2 | 40 | 59.9 | -  
[jamba-1.5-mini](https://huggingface.co/ai21labs/AI21-Jamba-1.5-Mini) | 256,000 | 69.7 | - | 75.8 | -  
[jamba-1.5-large](https://huggingface.co/ai21labs/AI21-Jamba-1.5-Large) | 256,000 | 81.2 | - | 87 | -  
[Snowflake Arctic](https://www.snowflake.com/en/data-cloud/arctic/) | 4,096 | 67.3 | 64.3 | 69.7 | 79  
[llama3.2-1b](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md) | 128,000 | 49.3 | - | 44.4 | -  
[llama3.2-3b](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/MODEL_CARD.md) | 128,000 | 69.4 | - | 77.7 | -  
[gemma-7b](https://huggingface.co/google/gemma-7b-it) | 8,000 | 64.3 | 32.3 | 46.4 | -  
[mistral-7b](https://mistral.ai/news/announcing-mistral-7b/) | 32,000 | 62.5 | 26.2 | 52.1 | -  
GPT 3.5 Turbo* | 4,097 | 70 | 48.1 | 57.1 | -  
  
*Provided for comparison; not available in Snowflake Cortex COMPLETE.

## LLM functions overview¶

Cortex LLM Functions can be grouped into the following categories:

  * **COMPLETE function** : General purpose function that can perform a wide range of user-specified tasks, such as aspect-based sentiment classification, synthetic data generation, and customized summaries. You can also use this function with your [fine-tuned models](cortex-finetuning).

  * **Task-specific functions** : Purpose-built and managed functions that deliver high-quality results for routine tasks, such as text classification, sentiment, and translation, without requiring you to optimize your prompt.

  * **Helper functions** : Purpose-built and managed functions that reduce cases of failures when running other LLM functions, for example by getting the count of tokens in an input prompt to ensure the call doesn’t exceed a model limit.

### COMPLETE¶

Given a prompt, the instruction-following COMPLETE function generates a
response using your choice of language model. In the simplest use case, the
prompt is a single string. You may also provide a conversation including
multiple prompts and responses for interactive chat-style usage, and in this
form of the function you can also specify hyperparameter options to customize
the style and size of the output. In order to implement safeguards, you can
also enable the Cortex Guard parameter that filters potentially unsafe and
harmful responses from a LLM.

To implement safeguards, you can enable the Cortex Guard parameter that
filters unsafe and harmful responses from an LLM.

The COMPLETE function supports the following models. Different models can have
different costs.

  * `gemma-7b`

  * `jamba-1.5-mini`

  * `jamba-1.5-large`

  * `jamba-instruct`

  * `llama2-70b-chat`

  * `llama3-8b`

  * `llama3-70b`

  * `llama3.1-8b`

  * `llama3.1-70b`

  * `llama3.1-405b`

  * `llama3.2-1b`

  * `llama3.2-3b`

  * `mistral-large`

  * `mistral-large2`

  * `mistral-7b`

  * `mixtral-8x7b`

  * `reka-core`

  * `reka-flash`

  * `snowflake-arctic`

See [COMPLETE (SNOWFLAKE.CORTEX)](../../sql-reference/functions/complete-
snowflake-cortex) for syntax and examples.

#### Cortex Guard¶

Cortex Guard is a safety parameter available within the COMPLETE function
designed to filter possible unsafe and harmful responses from a language
model. Cortex Guard is currently built with Meta’s Llama Guard 3. Cortex Guard
works by evaluating the responses of a language model before that output is
returned to the application. Once you activate Cortex Guard, language model
responses which may be associated with violent crimes, hate, sexual content,
self-harm, and more are automatically filtered. See the [COMPLETE
(SNOWFLAKE.CORTEX)](../../sql-reference/functions/complete-snowflake-cortex)
arguments section for syntax and examples.

Note

Usage of Cortex Guard incurs compute charges based on the number of input
tokens processed.

### Task-specific functions¶

Task-specific functions are managed by the Snowflake AI team to deliver high-
quality results, without requiring you to develop your own prompts. Under the
hood, the Snowflake AI team might implement various prompt optimizations and
fine-tuning to deliver high-quality results for each task. Task-specific
functions provide the benefits of ease of use and efficiency, without any
compromise on quality.

#### CLASSIFY_TEXT¶

The CLASSIFY_TEXT function classifies free-form text into categories that you
provide. The text may be a plain English string.

For syntax and examples, see [CLASSIFY_TEXT (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/classify_text-snowflake-cortex).

#### EMBED_TEXT_768¶

The EMBED_TEXT_768 function creates a vector embedding of 768 dimensions for a
given English-language text. To learn more about embeddings and vector
comparison functions, see [Vector Embeddings](vector-embeddings).

For syntax and examples, see [EMBED_TEXT_768 (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/embed_text-snowflake-cortex).

#### EMBED_TEXT_1024¶

The EMBED_TEXT_1024 function creates a vector embedding of 1024 dimensions for
a given text. To learn more about embeddings and vector comparison functions,
see [Vector Embeddings](vector-embeddings).

For syntax and examples, see [EMBED_TEXT_1024 (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/embed_text_1024-snowflake-cortex).

#### EXTRACT_ANSWER¶

The EXTRACT_ANSWER function extracts an answer to a given question from a text
document. The document may be a plain-English document or a string
representation of a semi-structured (JSON) data object.

For syntax and examples, see [EXTRACT_ANSWER (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/extract_answer-snowflake-cortex).

#### PARSE_DOCUMENT¶

The PARSE_DOCUMENT function extracts text or layout from documents stored in
an internal stage or an external stage.

For syntax and examples, see [PARSE_DOCUMENT (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/parse_document-snowflake-cortex).

#### SENTIMENT¶

The SENTIMENT function returns sentiment as a score between -1 to 1 (with -1
being the most negative and 1 the most positive, with values around 0 neutral)
for the given English-language input text.

For syntax and examples, see [SENTIMENT (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/sentiment-snowflake-cortex).

#### SUMMARIZE¶

The SUMMARIZE function returns a summary of the given English text.

For syntax and examples, see [SUMMARIZE (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/summarize-snowflake-cortex).

#### TRANSLATE¶

The TRANSLATE function translates text from the indicated or detected source
language to a target language.

For syntax and examples, see [TRANSLATE (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/translate-snowflake-cortex).

### Helper functions¶

Helper functions are managed functions that are built to help reduce errors
when running other Cortex LLM functions.

#### COUNT_TOKENS¶

The COUNT_TOKENS function calculates the number of tokens in a prompt for the
large language model specified in COMPLETE, and the input text for task-
specific functions.

For syntax and examples, see [COUNT_TOKENS (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/count_tokens-snowflake-cortex).

#### TRY_COMPLETE¶

The TRY_COMPLETE function performs the same operation as the COMPLETE function
but returns NULL instead of raising an error when the operation cannot be
performed.

For syntax and examples, see [TRY_COMPLETE (SNOWFLAKE.CORTEX)](../../sql-
reference/functions/try_complete-snowflake-cortex).

## Error conditions¶

Snowflake Cortex LLM functions can produce the following error messages.

Message | Explanation  
---|---  
`too many requests` | The request was rejected due to excessive system load. Please try your request again.  
`invalid options object` | The `options` object passed to the function contains invalid options or values.  
`budget exceeded` | The model consumption budget was exceeded.  
`unknown model "<model name>"` | The specified model does not exist.  
`invalid language "<language>"` | The specified language is not supported by the TRANSLATE function.  
`max tokens of <count> exceeded` | The request exceeded the maximum number of tokens supported by the model (see Model restrictions).  
`all requests were throttled by remote service` | The request has been throttled due to a high level of usage. Try again later.  
`invalid number of categories: <num_categories>` | The specified number of categories is above the limit for CLASSIFY_TEXT  
`invalid category input type` | The specified type of category is not supported by CLASSIFY_TEXT.  
`empty classification input` | The input to CLASSIFY_TEXT is an empty string or null.  
  
## Using Snowflake Cortex LLM functions with Python¶

Snowflake Cortex LLM functions are available in [Snowpark ML](../../developer-
guide/snowflake-ml/overview) version 1.1.2 and later. See [Using Snowflake ML
Locally](../../developer-guide/snowflake-ml/snowpark-ml.html#label-snowpark-
ml-get-started) for instructions on setting up Snowpark ML.

If you run your Python script outside of Snowflake, you must create a Snowpark
session to use these functions. See [Connecting to Snowflake](../../developer-
guide/snowflake-ml/snowpark-ml.html#label-snowpark-ml-authenticating) for
instructions.

The following Python example illustrates calling Snowflake Cortex LLM
functions on single values:

    
    
    from snowflake.cortex import Complete, ExtractAnswer, Sentiment, Summarize, Translate, ClassifyText
    
    text = """
        The Snowflake company was co-founded by Thierry Cruanes, Marcin Zukowski,
        and Benoit Dageville in 2012 and is headquartered in Bozeman, Montana.
    """
    
    print(Complete("llama2-70b-chat", "how do snowflakes get their unique patterns?"))
    print(ExtractAnswer(text, "When was snowflake founded?"))
    print(Sentiment("I really enjoyed this restaurant. Fantastic service!"))
    print(Summarize(text))
    print(Translate(text, "en", "fr"))
    print(ClassifyText("France", ["Europe", "Asia"]))
    

Copy

You can also call an LLM function on a table column, as shown below. This
example requires a session object (stored in `session`) and a table `articles`
containing a text column `abstract_text`, and creates a new column
`abstract_summary` containing a summary of the abstract.

    
    
    from snowflake.cortex import Summarize
    from snowflake.snowpark.functions import col
    
    article_df = session.table("articles")
    article_df = article_df.withColumn(
        "abstract_summary",
        Summarize(col("abstract_text"))
    )
    article_df.collect()
    

Copy

Note

The advanced chat-style (multi-message) form of COMPLETE is not currently
supported in Python.

## Using Snowflake Cortex LLM functions with Snowflake CLI¶

Snowflake Cortex LLM functions are available in [Snowflake
CLI](../../developer-guide/snowflake-cli/index) version 2.4.0 and later. See
[Introducing Snowflake CLI](../../developer-guide/snowflake-
cli/introduction/introduction) for more information about using Snowflake CLI.

The following examples illustrate using the `snow cortex` commands on single
values. The `-c` parameter specifies which connection to use.

Note

The advanced chat-style (multi-message) form of COMPLETE is not currently
supported in Snowflake CLI.

    
    
    snow cortex complete "Is 5 more than 4? Please answer using one word without a period." -c "snowhouse"
    

Copy

    
    
    snow cortex extract-answer "what is snowflake?" "snowflake is a company" -c "snowhouse"
    

Copy

    
    
    snow cortex sentiment "Mary had a little Lamb" -c "snowhouse"
    

Copy

    
    
    snow cortex summarize "John has a car. John's car is blue. John's car is old and John is thinking about buying a new car. There are a lot of cars to choose from and John cannot sleep because it's an important decision for John."
    

Copy

    
    
    snow cortex translate herb --to pl
    

Copy

You can also use files that contain the text you want to use for the commands.
For this example, assume that the file `about_cortex.txt` contains the
following content:

    
    
    Snowflake Cortex gives you instant access to industry-leading large language models (LLMs) trained by researchers at companies like Mistral, Reka, Meta, and Google, including Snowflake Arctic, an open enterprise-grade model developed by Snowflake.
    
    Since these LLMs are fully hosted and managed by Snowflake, using them requires no setup. Your data stays within Snowflake, giving you the performance, scalability, and governance you expect.
    
    Snowflake Cortex features are provided as SQL functions and are also available in Python. The available functions are summarized below.
    
    COMPLETE: Given a prompt, returns a response that completes the prompt. This function accepts either a single prompt or a conversation with multiple prompts and responses.
    EMBED_TEXT_768: Given a piece of text, returns a vector embedding that represents that text.
    EXTRACT_ANSWER: Given a question and unstructured data, returns the answer to the question if it can be found in the data.
    SENTIMENT: Returns a sentiment score, from -1 to 1, representing the detected positive or negative sentiment of the given text.
    SUMMARIZE: Returns a summary of the given text.
    TRANSLATE: Translates given text from any supported language to any other.
    

You can then execute the `snow cortex summarize` command by passing in the
filename using the `--file` parameter, as shown:

    
    
    snow cortex summarize --file about_cortex.txt
    

Copy

    
    
    Snowflake Cortex offers instant access to industry-leading language models, including Snowflake Arctic, with SQL functions for completing prompts (COMPLETE), text embedding (EMBED\_TEXT\_768), extracting answers (EXTRACT\_ANSWER), sentiment analysis (SENTIMENT), summarizing text (SUMMARIZE), and translating text (TRANSLATE).
    

For more information about these commands, see [snow cortex
commands](../../developer-guide/snowflake-cli/command-reference/cortex-
commands/overview).

## Legal notices¶

The data classification of inputs and outputs are as set forth in the
following table.

Input data classification | Output data classification | Designation  
---|---|---  
Usage Data | Customer Data | Covered AI Features [1]  
[1]

Represents the defined term used in the AI Terms and Acceptable Use Policy.

For additional information, refer to [Snowflake AI and ML](../../guides-
overview-ai-features).


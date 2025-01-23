# Loading unstructured data with Document AI¶

By integrating with [Document AI](snowflake-cortex/document-ai/overview),
Snowflake now supports loading unstructured data, similar to loading
structured and semi-structured data.

Unstructured data is information that does not fit into a predefined data
model or schema. Typically text-heavy, such as form responses and social media
conversations, unstructured data also encompasses images, video, and audio.

To load unstructured data with this preview feature, you can run the same COPY
INTO table command with a copy option `file_processor`.

## Prerequisites¶

Before using this feature, you must prepare a Document AI model and make sure
the user who runs the COPY command has access to this model. For more
information, see [Document AI](snowflake-cortex/document-ai/overview).

## Using the COPY INTO command¶

You can load unstructured data by using the COPY INTO command with the
`file_processor` copy option. You can specify `document_ai` as the type of
custom scanner for the `file_processor` copy option and specify the associated
properties for the scanner.

For more information, see [COPY INTO TABLE syntax](../sql-reference/sql/copy-
into-table.html#label-copy-into-table-syntax) and [COPY INTO Copy
Options](../sql-reference/sql/copy-into-table.html#label-copy-into-table-
copyoptions).

To load unstructured data, we recommend specifying the type of the source stage as `CUSTOM`, which is a stage format type in preview. The other stage format types `(TYPE = { CSV | JSON | AVRO | ORC | PARQUET | XML })` are supported for backwards compatibility.

You can specify the stage type by using the `file_format` parameter when
creating a stage. The `CUSTOM` stage type specifies that the underlying stage
holds unstructured data and can only be used with the `FILE_PROCESSOR` copy
option.

## Examples¶

The following example shows loading unstructured data files from a stage
`custom_stage` to a table `my_table`, with the `document_ai` function
specified by a model name `predict` and model version `1`.

>
>     COPY INTO my_table FROM @custom_stage
>       FILE_PROCESSOR = (
>         SCANNER = 'document_ai'
>         SCANNER_OPTIONS = (project_name = 'DEMO0200', model_name = 'predict'
> model_version = '1'));
>  
>
> Copy

The following example shows loading unstructured data files to a table
`docai_results` and transforming the raw data using a [SELECT](../sql-
reference/sql/select) statement.

>
>     CREATE OR REPLACE TABLE docai_results (inspection_date date, inspector
> varchar);
>  
>     COPY INTO docai_results FROM (SELECT $1:inspection_date[0].value::date,
> $1:inspector[0].value FROM @custom_stage)
>       FILE_PROCESSOR = (
>         SCANNER = 'document_ai'
>         SCANNER_OPTIONS = (project_name = 'DEMO0201', model_name = 'predict'
> model_version = '1'));
>  
>
> Copy

## Considerations and limitations¶

  * This feature does not support the following:

    * [Table schema evolution](data-load-schema-evolution)

    * [MATCH_BY_COLUMN_NAME](../sql-reference/sql/copy-into-table.html#label-copy-into-table-copyoptions) COPY option

    * [Snowpipe](data-load-snowpipe-intro)

  * Only the default ON_ERROR COPY option `ON_ERROR = ABORT_STATEMENT` is supported. Attempts to use other ON_ERROR options will result in compilation failure.

  * The number of files per query cannot exceed 1000.


# SQL class reference¶

These topics provide reference information for Snowflake [classes](sql-
reference/snowflake-db-classes).

Each class supports one or more of the following SQL operations:

  * ALTER: Modifies the properties of an instance of a class.

  * CREATE: Creates an instance of a class.

  * DROP: Deletes an instance of a class.

  * SHOW: Lists instances of a class.

An instance of a class can have one or more methods. A method is a stored
procedure or function and can be called by using the instance name and method
name, and arguments (if any) required by the method. For example, `CALL
_instance_name_!_method_name_(...)`.

## Updating your search path¶

You can add the schema for classes you use frequently to your search path to
save typing and make your SQL statements more concise. For more information
about updating your search path, see [Update your search path](sql-
reference/snowflake-db-classes.html#label-update-search-path).

## Available classes¶

Snowflake provides the following system-defined (built-in) classes.

[ANOMALY_DETECTION (SNOWFLAKE.ML)](sql-reference/classes/anomaly_detection)

    

Allows you to detect outliers in your time series data.

[BUDGET (SNOWFLAKE.CORE)](sql-reference/classes/budget)

    

Allows you to monitor credit usage of supported objects.

[CLASSIFICATION (SNOWFLAKE.ML)](sql-reference/classes/classification)

    

Automatically sorts data into categories based on features in the data.

[CLASSIFICATION_PROFILE (SNOWFLAKE.DATA_PRIVACY)](sql-
reference/classes/classification_profile)

    

Allows you to automatically classify sensitive data.

[CUSTOM_CLASSIFIER (SNOWFLAKE.DATA_PRIVACY)](sql-
reference/classes/custom_classifier)

    

Allows you to define custom classifiers to extend your data classification
capabilities.

[DOCUMENT_INTELLIGENCE (SNOWFLAKE.ML)](sql-reference/classes/document-
intelligence)

    

Represents a Document AI model build.

[FORECAST (SNOWFLAKE.ML)](sql-reference/classes/forecast)

    

Represents a forecast model that produces a forecast for a single or multiple
time series.

[TOP_INSIGHTS (SNOWFLAKE.ML)](sql-reference/classes/top-insights)

    

Allows you to determine the segments driving changes in a metric.


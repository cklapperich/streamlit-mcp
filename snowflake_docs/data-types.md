# Snowflake Data Types¶

Snowflake supports most basic SQL data types (with some restrictions) for use
in columns, local variables, expressions, parameters, and any other
appropriate/suitable locations.

Note

You can also load unstructured data into Snowflake. For more information, see
[Introduction to unstructured data](user-guide/unstructured-intro).

In some cases, data of one type can be converted to another type. For example,
INTEGER data can be converted to FLOAT.

Some conversions are lossless, but others might lose information. The amount
of loss depends upon the data types and the specific value. For example,
converting FLOAT to INTEGER removes the digits after the decimal place. (The
value is rounded to the nearest integer.)

In some cases, the user must specify the desired conversion, such as when
passing a VARCHAR to the TIME_SLICE() function, which expects a TIMESTAMP. We
call this “explicit casting”. For more information about explicit casting, see
[Conversion functions](sql-reference/functions-conversion).

In other cases, data types are converted automatically, such as when adding a
float and an integer. We call this “implicit coercion”. In Snowflake, data
types are automatically coerced whenever necessary and possible. For more
information about implicit coercion, see [Data type conversion](sql-
reference/data-type-conversion).

For more information about Snowflake data types, see the following topics:

  * [Summary of data types](sql-reference/intro-summary-data-types)

  * [Numeric data types](sql-reference/data-types-numeric)

  * [String & binary data types](sql-reference/data-types-text)

  * [Logical data types](sql-reference/data-types-logical)

  * [Date & time data types](sql-reference/data-types-datetime)

  * [Semi-structured data types](sql-reference/data-types-semistructured)

  * [Structured data types](sql-reference/data-types-structured)

  * [Geospatial data types](sql-reference/data-types-geospatial)

  * [Vector data types](sql-reference/data-types-vector)

  * [Unsupported data types](sql-reference/data-types-unsupported)

  * [Data type conversion](sql-reference/data-type-conversion)


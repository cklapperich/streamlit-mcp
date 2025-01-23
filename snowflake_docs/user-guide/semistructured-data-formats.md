# Supported Formats for Semi-structured Data¶

This topic describes the supported formats for semi-structured data.

Snowflake natively supports the semi-structured data formats below.
Specifically, Snowflake provides options in COPY commands to load and unload
data files in these formats.

## JSON¶

### What is JSON?¶

JSON (JavaScript Object Notation) is a lightweight, plain-text, data-
interchange format based on a subset of the JavaScript Programming Language.

JSON data can be produced by any application. Some common examples include:

  * JavaScript applications using native methods to generate JSON.

  * Non-JavaScript applications using libraries (usually with extensions) to generate JSON data.

  * Ad hoc JavaScript generators.

  * Concatenation of JSON documents (which may or may not be line-separated).

Because there is no formal specification, there are significant differences
between various implementations. These differences makes import of JSON-like
data sets impossible if the JSON parser is strict in its language definition.
To make import of JSON data sets as problem-free as possible, Snowflake
follows the rule “be liberal in what you accept”. The intent is to accept the
widest possible range of JSON and JSON-like inputs that permit unambiguous
interpretation.

This topic describes the syntax for JSON documents accepted by Snowflake.

For more information about JSON, see [json.org](http://www.json.org).

### Basic JSON Syntax¶

JSON data is a hierarchical collection of name/value pairs grouped into
objects and arrays:

  * Colons `:` separate names and values in name/value pairs.

  * Curly braces `{}` denote objects.

  * Square brackets `[]` denote arrays.

  * Commas `,` separate entities in objects and arrays.

### Name/Value Pairs¶

JSON name/value pairs consist of a field name (in double quotes), followed by
a colon, then a value.

For example:

    
    
    {"firstName":"John", "empid":45611}
    

Copy

### Supported Data Types¶

A value in a name/value pair can be:

  * A number (integer or floating point)

  * A string (in double quotes)

  * A Boolean (true or false)

  * An array (in square brackets)

  * An object (in curly braces)

  * Null

### Objects¶

JSON objects are written inside curly braces. An object can contain multiple
name/values pairs, separated by commas. For example:

    
    
    {"firstName":"John", "lastName":"Doe"}
    

Copy

### Arrays¶

JSON arrays are written inside square brackets. An array can contain multiple
objects, separated by commas. For example:

    
    
    {"employees":[
        {"firstName":"John", "lastName":"Doe"},
        {"firstName":"Anna", "lastName":"Smith"},
        {"firstName":"Peter", "lastName":"Jones"}
      ]
    }
    

Copy

### Examples of JSON Documents¶

**FILE NAME:** `json_sample_data1`

Contains an array with 3 simple employee records (objects):

>
>     {"root":[{"employees":[
>         {"firstName":"John", "lastName":"Doe"},
>         {"firstName":"Anna", "lastName":"Smith"},
>         {"firstName":"Peter", "lastName":"Jones"}
>     ]}]}
>  
>
> Copy

**FILE NAME:** `json_sample_data2`

Contains an array with 3 employee records (objects) and their associated
dependent data (children, the children’s names and ages, cities where the
employee has lived, and the years that the employee has lived in those
cities):

>
>     {"root":
>        [
>         { "kind": "person",
>           "fullName": "John Doe",
>           "age": 22,
>           "gender": "Male",
>           "phoneNumber":
>             {"areaCode": "206",
>              "number": "1234567"},
>           "children":
>              [
>                {
>                  "name": "Jane",
>                  "gender": "Female",
>                  "age": "6"
>                },
>                {
>                   "name": "John",
>                   "gender": "Male",
>                   "age": "15"
>                }
>              ],
>           "citiesLived":
>              [
>                 {
>                    "place": "Seattle",
>                    "yearsLived": ["1995"]
>                 },
>                 {
>                    "place": "Stockholm",
>                    "yearsLived": ["2005"]
>                 }
>              ]
>           },
>           {"kind": "person", "fullName": "Mike Jones", "age": 35, "gender":
> "Male", "phoneNumber": { "areaCode": "622", "number": "1567845"},
> "children": [{ "name": "Earl", "gender": "Male", "age": "10"}, {"name":
> "Sam", "gender": "Male", "age": "6"}, { "name": "Kit", "gender": "Male",
> "age": "8"}], "citiesLived": [{"place": "Los Angeles", "yearsLived":
> ["1989", "1993", "1998", "2002"]}, {"place": "Washington DC", "yearsLived":
> ["1990", "1993", "1998", "2008"]}, {"place": "Portland", "yearsLived":
> ["1993", "1998", "2003", "2005"]}, {"place": "Austin", "yearsLived":
> ["1973", "1998", "2001", "2005"]}]},
>           {"kind": "person", "fullName": "Anna Karenina", "age": 45,
> "gender": "Female", "phoneNumber": { "areaCode": "425", "number":
> "1984783"}, "citiesLived": [{"place": "Stockholm", "yearsLived": ["1992",
> "1998", "2000", "2010"]}, {"place": "Russia", "yearsLived": ["1998", "2001",
> "2005"]}, {"place": "Austin", "yearsLived": ["1995", "1999"]}]}
>         ]
>     }
>  
>
> Copy

## Avro¶

### What is Avro?¶

Avro is an open-source data serialization and RPC framework originally
developed for use with Apache Hadoop. It utilizes schemas defined in JSON to
produce serialized data in a compact binary format. The serialized data can be
sent to any destination (i.e. application or program) and can be easily
deserialized at the destination because the schema is included in the data.

An Avro schema consists of a JSON string, object, or array that defines the
type of schema and the data attributes (field names, data types, etc.) for the
schema type. The attributes differ depending on the schema type. Complex data
types such as arrays and maps are supported.

Snowflake reads Avro data into a single VARIANT column. You can query the data
in a VARIANT column just as you would JSON data, using similar commands and
functions.

For more information, see [avro.apache.org](http://avro.apache.org).

### Example of an Avro Schema¶

    
    
    {
     "type": "record",
     "name": "person",
     "namespace": "example.avro",
     "fields": [
         {"name": "fullName", "type": "string"},
         {"name": "age",  "type": ["int", "null"]},
         {"name": "gender", "type": ["string", "null"]}
         ]
    }
    

Copy

## ORC¶

### What is ORC?¶

ORC (Optimized Row Columnar) is a binary format used to store Hive data. ORC
was designed for efficient compression and improved performance for reading,
writing, and processing data over earlier Hive file formats. For more
information about ORC, see
[https://orc.apache.org/](https://orc.apache.org//).

Snowflake reads ORC data into a single VARIANT column. You can query the data
in a VARIANT column just as you would JSON data, using similar commands and
functions.

Alternatively, you can extract columns from a staged ORC file into separate
table columns using a CREATE TABLE AS SELECT statement.

Note

  * Map data is deserialized into an array of objects, e.g.:
    
        "map": [{"key": "chani", "value": {"int1": 5, "string1": "chani"}}, {"key": "mauddib", "value": {"int1": 1, "string1": "mauddib"}}]
    

Copy

  * Union data is deserialized into a single object, e.g.:
    
        {"time": "1970-05-05 12:34:56.197", "union": {"tag": 0, "value": 3880900}, "decimal": 3863316326626557453.000000000000000000}
    

Copy

### Example of ORC Data Loaded into a VARIANT Column¶

    
    
    +--------------------------------------+
    | SRC                                  |
    |--------------------------------------|
    | {                                    |
    |   "boolean1": false,                 |
    |   "byte1": 1,                        |
    |   "bytes1": "0001020304",            |
    |   "decimal1": 12345678.654745,       |
    |   "double1": -1.500000000000000e+01, |
    |   "float1": 1.000000000000000e+00,   |
    |   "int1": 65536,                     |
    |   "list": [                          |
    |     {                                |
    |       "int1": 3,                     |
    |       "string1": "good"              |
    |     },                               |
    |     {                                |
    |       "int1": 4,                     |
    |       "string1": "bad"               |
    |     }                                |
    |   ]                                  |
    | }                                    |
    +--------------------------------------+
    

Copy

## Parquet¶

### What is Parquet?¶

Parquet is a compressed, efficient columnar data representation designed for
projects in the Hadoop ecosystem. The file format supports complex nested data
structures and uses Dremel record shredding and assembly algorithms. Parquet
files can’t be opened in a text editor. For more information, see
[parquet.apache.org/docs/](https://parquet.apache.org/docs/).

Note

Snowflake supports Parquet files produced using the Parquet writer V2 for
Apache Iceberg™ tables or when you use a [vectorized scanner](../sql-
reference/sql/copy-into-table.html#label-use-vectorized-scanner).

Depending on your loading use case, Snowflake either reads Parquet data into a
single VARIANT column or directly into table columns (such as when you [load
data from Iceberg-compatible Parquet files](tables-iceberg-load.html#label-
tables-iceberg-load-add-files-copy-example)).

You can query the data in a VARIANT column just as you would JSON data, using
similar commands and functions. Alternatively, you can extract select columns
from a staged Parquet file into separate table columns using a CREATE TABLE AS
SELECT statement.

### Example of Parquet Data Loaded into a VARIANT Column¶

    
    
    +------------------------------------------+
    | SRC                                      |
    |------------------------------------------|
    | {                                        |
    |   "continent": "Europe",                 |
    |   "country": {                           |
    |     "city": {                            |
    |       "bag": [                           |
    |         {                                |
    |           "array_element": "Paris"       |
    |         },                               |
    |         {                                |
    |           "array_element": "Nice"        |
    |         },                               |
    |         {                                |
    |           "array_element": "Marseilles"  |
    |         },                               |
    |         {                                |
    |           "array_element": "Cannes"      |
    |         }                                |
    |       ]                                  |
    |     },                                   |
    |     "name": "France"                     |
    |   }                                      |
    | }                                        |
    +------------------------------------------+
    

## XML¶

### What is XML?¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Preview Feature](../release-
notes/preview-features) — Open

Enabled for all accounts.

XML (eXtensible Markup Language) is a markup language that defines a set of
rules for encoding documents. It was originally based on SGML, another markup
language developed for standardizing the structure and elements that comprise
a document.

Since its introduction, XML has grown beyond an initial focus on documents to
encompass a wide range of uses, including representation of arbitrary data
structures and serving as the base language for communication protocols.
Because of its extensibility, versatility, and usability, it has become one of
the most commonly-used standards for data interchange on the Web.

An XML document consists primarily of the following constructs:

  * Tags (identified by angle brackets, `<` and `>`)

  * Elements

Elements typically consist of a “start” tag and matching “end” tag, with the
text between the tags constituting the content for the element. An element can
also consist of an “empty-element” tag with no “end” tag. “start” and “empty-
element” tags may contain attributes, which help define the characteristics or
metadata for the element.

### Example of an XML Document¶

    
    
    <?xml version="1.0"?>
    <!DOCTYPE parts system "parts.dtd">
    <?xml-stylesheet type="text/css" href="xmlpartsstyle.css"?>
    <parts>
       <title>Automobile Parts &amp; Accessories</title>
       <part>
          <item>Spark Plugs</item>
          <partnum>A3-400</partnum>
          <price> 27.00</price>
       </part>
       <part>
          <item>Motor Oil</item>
          <partnum>B5-200</partnum>
          <price> 14.00</price>
       </part>
       <part>
          <item>Motor Oil</item>
          <partnum>B5-300</partnum>
          <price> 16.75</price>
       </part>
       <part>
          <item>Engine Coolant</item>
          <partnum>B6-120</partnum>
          <price> 19.00</price>
       </part>
       <part>
          <item>Engine Coolant</item>
          <partnum>B6-220</partnum>
          <price> 18.25</price>
       </part>
    </parts>
    

Copy


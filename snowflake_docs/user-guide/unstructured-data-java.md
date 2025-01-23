# Processing unstructured data with UDF and procedure handlers¶

This topic provides examples of reading and processing unstructured data in
staged files with handler code written for the following:

  * [Java user-defined functions (UDFs)](../developer-guide/udf/java/udf-java-introduction)

  * [Java user-defined table functions (UDTFs)](../developer-guide/udf/java/udf-java-tabular-functions)

  * [Java procedures](../developer-guide/stored-procedure/stored-procedures-java)

You can also read a file with handlers written in other languages:

Python:

    

  * [Python UDFs](../developer-guide/udf/python/udf-python-examples.html#label-udf-python-read-files)

  * [Python procedures](../developer-guide/stored-procedure/python/procedure-python-read-files)

Scala:

    

  * [Scala UDFs](../developer-guide/udf/scala/udf-scala-examples.html#label-reading-file-from-scala-udf-handler)

  * [Scala procedures](../developer-guide/stored-procedure/stored-procedures-scala.html#label-stored-proc-scala-writing-reading-files)

Note

To make your code resilient to file injection attacks, always use a scoped URL
when passing a file’s location to a UDF, particularly when the function’s
caller is not also its owner. You can create a scoped URL in SQL using the
built-in function BUILD_SCOPED_FILE_URL. For more information about what the
BUILD_SCOPED_FILE_URL does, see [Introduction to unstructured
data](unstructured-intro).

**In this Topic:**

## Process a PDF with a UDF and procedure¶

The examples in this section process staged unstructured files using Java
handler code – first with a UDF, then with a procedure. Both handlers extract
the contents of a specified PDF file using the [Apache PDFBox
library](https://pdfbox.apache.org/).

The handler code is very similar between the UDF and procedure. They differ in
how the read the incoming PDF file.

  * In the UDF, the handler reads the file using a Java `InputStream`.

  * In the procedure, the handler reads the file using a Snowflake `SnowflakeFile`.

The examples use in-line handler code (as opposed to compiled in a staged
JAR), which means that you do not need to compile, package, and upload the
handler code to a stage. For more information on the difference between in-
line and staged handlers, see [Keeping handler code in-line or on a
stage](../developer-guide/inline-or-staged).

### Download the PDFBox library¶

Before you begin writing the UDF, download the PDFBox library JAR file if you
don’t have it already. It will be a dependency for your handler code. You’ll
later upload the library JAR file to a stage.

Download the latest released version of the library from the [Apache PDFBox
library download page](https://pdfbox.apache.org/download.html).

### Create stages¶

Create stages in which to keep your handler code’s dependency libraries and
the data file the handler code will read.

Using the code below, you’ll create separate internal stages to hold:

  * A library JAR file that’s a dependency for your handler. You’ll reference the stage and JAR file from the UDF.

  * A data file that your handler code will read.

Code in the following example uses the [CREATE STAGE](../sql-
reference/sql/create-stage) command to create the stages you’ll need.

    
    
    -- Create an internal stage to store the JAR files.
    CREATE OR REPLACE STAGE jars_stage;
    
    -- Create an internal stage to store the data files. The stage includes a directory table.
    CREATE OR REPLACE STAGE data_stage DIRECTORY=(ENABLE=TRUE) ENCRYPTION = (TYPE='SNOWFLAKE_SSE');
    

Copy

### Upload the required library and the PDF file to read¶

Complete the following steps to upload the dependency JAR file (with the
library code that processes the PDF) and the data file (the PDF file the
handler code will process).

You can use the PDF file of your choosing in this example.

  1. Copy the JAR file for Apache PDFBox from the local temporary directory to the stage that stores JAR files:

Linux/Mac:

    
    
        PUT file:///tmp/pdfbox-app-2.0.27.jar @jars_stage AUTO_COMPRESS=FALSE;
    

Copy

Windows:

    
    
        PUT file://C:\temp\pdfbox-app-2.0.27.jar @jars_stage AUTO_COMPRESS=FALSE;
    

Copy

  2. Copy the PDF file from the local temporary directory to the stage that stores data files:

Linux/Mac:

    
    
        PUT file:///tmp/myfile.pdf @data_stage AUTO_COMPRESS=FALSE;
    

Copy

Windows:

    
    
        PUT file://C:\temp\myfile.pdf @data_stage AUTO_COMPRESS=FALSE;
    

Copy

### Create and call the UDF¶

Complete the following steps to create a UDF that reads and processes PDF
files.

  1. Paste and run the following code to create a UDF.

This UDF’s handler parses PDF documents and retrieves their content. The
handler uses the `InputStream` class to read the file. For more on reading
files with `InputStream`, refer to [Reading a dynamically-specified file with
InputStream](../developer-guide/udf/java/udf-java-cookbook.html#label-reading-
file-from-java-udf-inputstream).

    
        CREATE FUNCTION process_pdf_func(file STRING)
    RETURNS STRING
    LANGUAGE JAVA
    RUNTIME_VERSION = 11
    IMPORTS = ('@jars_stage/pdfbox-app-2.0.27.jar')
    HANDLER = 'PdfParser.readFile'
    AS
    $$
    import org.apache.pdfbox.pdmodel.PDDocument;
    import org.apache.pdfbox.text.PDFTextStripper;
    import org.apache.pdfbox.text.PDFTextStripperByArea;
    
    import java.io.File;
    import java.io.FileInputStream;
    import java.io.IOException;
    import java.io.InputStream;
    
    public class PdfParser {
    
        public static String readFile(InputStream stream) throws IOException {
            try (PDDocument document = PDDocument.load(stream)) {
    
                document.getClass();
    
                if (!document.isEncrypted()) {
    
                    PDFTextStripperByArea stripper = new PDFTextStripperByArea();
                    stripper.setSortByPosition(true);
    
                    PDFTextStripper tStripper = new PDFTextStripper();
    
                    String pdfFileInText = tStripper.getText(document);
                    return pdfFileInText;
                }
            }
            return null;
        }
    }
    $$;
    

Copy

  2. Refresh the directory table for the `data_stage` stage with the [ALTER STAGE](../sql-reference/sql/alter-stage) command:
    
        ALTER STAGE data_stage REFRESH;
    

Copy

  3. Call the UDF to read the staged PDF file and extract the content.

Code in the following example calls the UDF, passing a scoped URL to make the
code resilient to file injection attacks. Always use a scoped URL when the
function’s caller is not also its owner. You can pass the URL argument as a
scoped URL or another form when the UDF’s caller is also its owner.

    
        SELECT process_pdf_func(BUILD_SCOPED_FILE_URL('@data_stage', '/myfile.pdf'));
    

Copy

### Create and call the procedure¶

Complete the following steps to create a procedure that reads and processes
PDF files.

  1. Paste and run the following code to create a procedure.

This procedure’s handler parses PDF documents and retrieves their content. The
handler uses the `SnowflakeFile` class to read the file. For more on reading
files with `SnowflakeFile`, refer to [Reading a dynamically-specified file
with SnowflakeFile](../developer-guide/stored-procedure/stored-procedures-
java.html#label-reading-file-snowflakefile-java).

    
        CREATE PROCEDURE process_pdf_proc(file STRING)
    RETURNS STRING
    LANGUAGE JAVA
    RUNTIME_VERSION = 11
    IMPORTS = ('@jars_stage/pdfbox-app-2.0.28.jar')
    HANDLER = 'PdfParser.readFile'
    PACKAGES = ('com.snowflake:snowpark:latest')
    AS
    $$
    import org.apache.pdfbox.pdmodel.PDDocument;
    import org.apache.pdfbox.text.PDFTextStripper;
    import org.apache.pdfbox.text.PDFTextStripperByArea;
    import com.snowflake.snowpark_java.types.SnowflakeFile;
    import com.snowflake.snowpark_java.Session;
    
    import java.io.File;
    import java.io.FileInputStream;
    import java.io.IOException;
    import java.io.InputStream;
    
    public class PdfParser {
    
        public static String readFile(Session session, String fileURL) throws IOException {
            SnowflakeFile file = SnowflakeFile.newInstance(fileURL);
            try (PDDocument document = PDDocument.load(file.getInputStream())) {
    
                document.getClass();
    
                if (!document.isEncrypted()) {
    
                    PDFTextStripperByArea stripper = new PDFTextStripperByArea();
                    stripper.setSortByPosition(true);
    
                    PDFTextStripper tStripper = new PDFTextStripper();
    
                    String pdfFileInText = tStripper.getText(document);
                    return pdfFileInText;
                }
            }
    
            return null;
        }
    }
    $$;
    

Copy

  2. Refresh the directory table for the `data_stage` stage with the [ALTER STAGE](../sql-reference/sql/alter-stage) command:
    
        ALTER STAGE data_stage REFRESH;
    

Copy

  3. Call the procedure to read the staged PDF file and extract the content.

Code in the following example passes a scoped URL pointing to the PDF file on
the stage you created.

    
        CALL process_pdf_proc(BUILD_SCOPED_FILE_URL('@data_stage', '/UsingThird-PartyPackages.pdf'));
    

Copy

## Process a CSV with a UDTF¶

The example in this section extracts and returns data from staged files using
Java UDTFs.

### Create data stage¶

Create a stage using the [CREATE STAGE](../sql-reference/sql/create-stage)
command:

The following SQL statement creates an internal stages to store the data files
for the example:

    
    
    -- Create an internal stage to store the data files. The stage includes a directory table.
    CREATE OR REPLACE STAGE data_stage DIRECTORY=(ENABLE=TRUE) ENCRYPTION = (TYPE='SNOWFLAKE_SSE');
    

Copy

### Upload the CSV file to read¶

Copy the CSV file from the local temporary directory to the stage that stores
data files:

Linux/Mac:

    
    
    
    PUT file:///tmp/sample.csv @data_stage AUTO_COMPRESS=FALSE;
    

Copy

Windows:

    
    
    
    PUT file://C:\temp\sample.csv @data_stage AUTO_COMPRESS=FALSE;
    

Copy

### Create and call the UDTF¶

This example extracts the contents of a specified set of CSV files and returns
the rows in a table. By processing file data as it’s read from the source, you
can avoid potential out-of-memory errors that might arise when the file is
very large.

Code in the following UDTF handler example uses `SnowflakeFile` to generate an
`InputStream` from a file URL to read a CSV file. (In a Java UDTF handler, row
processing begins when Snowflake calls the `process` method you implement.)
The code uses the stream when constructing an instance of a
`CsvStreamingReader` class defined in the handler itself.

The `CsvStreamingReader` class reads the contents of the received CSV file
stream row by row, providing a way for other code to retrieve each row as a
record where commas delimit columns. The `process` method returns each record
as it is read from the stream.

For more about writing tabular user-defined functions (UDTFs) with a Java
handler, see [Tabular Java UDFs (UDTFs)](../developer-guide/udf/java/udf-java-
tabular-functions).

Complete the following steps to create the Java UDTF and upload the required
files:

  1. Create a Java UDTF that uses the `SnowflakeFile` class:
    
        CREATE OR REPLACE FUNCTION parse_csv(file STRING)
    RETURNS TABLE (col1 STRING, col2 STRING, col3 STRING )
    LANGUAGE JAVA
    HANDLER = 'CsvParser'
    AS
    $$
    import org.xml.sax.SAXException;
    
    import java.io.*;
    import java.util.ArrayList;
    import java.util.List;
    import java.util.stream.Stream;
    import com.snowflake.snowpark_java.types.SnowflakeFile;
    
    public class CsvParser {
    
      static class Record {
        public String col1;
        public String col2;
        public String col3;
    
        public Record(String col1_value, String col2_value, String col3_value)
        {
          col1 = col1_value;
          col2 = col2_value;
          col3 = col3_value;
        }
      }
    
      public static Class getOutputClass() {
        return Record.class;
      }
    
      static class CsvStreamingReader {
        private final BufferedReader csvReader;
    
        public CsvStreamingReader(InputStream is) {
          this.csvReader = new BufferedReader(new InputStreamReader(is));
        }
    
        public void close() {
          try {
            this.csvReader.close();
          } catch (IOException e) {
            e.printStackTrace();
          }
        }
    
        Record getNextRecord() {
          String csvRecord;
    
          try {
            if ((csvRecord = csvReader.readLine()) != null) {
              String[] columns = csvRecord.split(",", 3);
              return new Record(columns[0], columns[1], columns[2]);
            }
          } catch (IOException e) {
            throw new RuntimeException("Reading CSV failed.", e);
          } finally {
            // No more records, we can close the reader.
            close();
          }
    
          // Return null to indicate the end of the stream.
          return null;
        }
      }
    
      public Stream<Record> process(String file_url) throws IOException {
        SnowflakeFile file = SnowflakeFile.newInstance(file_url);
    
        CsvStreamingReader csvReader = new CsvStreamingReader(file.getInputStream());
        return Stream.generate(csvReader::getNextRecord);
      }
    }
    $$
    ;
    

Copy

  2. Refresh the directory table for the `data_stage` stage:
    
        ALTER STAGE data_stage REFRESH;
    

Copy

  3. Call the Java UDTF to read one or more staged CSV files and extract the contents in a table format:

Code in the following example calls the UDF, passing a scoped URL to reduce
the risk of file injection attacks. Always used a scoped URL when the
function’s caller is not also its owner. You can pass the URL argument as a
scoped URL or another supported form when the UDF’s caller is also its owner.

> >     -- Input a file URL.
>     SELECT * FROM TABLE(PARSE_CSV(BUILD_SCOPED_FILE_URL(@data_stage,
> 'sample.csv')));
>  
>
> Copy


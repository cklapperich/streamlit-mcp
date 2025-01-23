# Tutorial: Testing Python Snowpark¶

## Introduction¶

This tutorial introduces the basics of testing your Snowpark Python code.

### What You Will Learn¶

In this tutorial, you will learn how to:

  * Test your Snowpark code while connected to Snowflake.

You can use standard testing utilities, like PyTest, to test your Snowpark
Python UDFs, DataFrame transformations, and stored procedures.

  * Test your Snowpark Python DataFrames locally without connecting to a Snowflake account by using the local testing framework.

You can use the local testing framework to test locally, on your development
machine, before deploying code changes.

### Prerequisites¶

To use the local testing framework:

  * You must use version 1.11.1 or higher of the Snowpark Python library.

  * The supported versions of Python are:

    * 3.9

    * 3.10

    * 3.11

## Set Up the Project¶

In this section, you’ll clone the project repository and set up the
environment you’ll need for the tutorial.

  1. Clone the project repository.

> >     git clone https://github.com/Snowflake-Labs/sftutorial-snowpark-
> testing
>  
>
> Copy
>
> If you do not have git installed, go to the repository page and download the
> contents by clicking Code » Download Contents.

  2. Set environment variables with your account credentials. The Snowpark API will use these to authenticate to your Snowflake account.

> >     # Linux/MacOS
>     export SNOWSQL_ACCOUNT=<replace with your account identifer>
>     export SNOWSQL_USER=<replace with your username>
>     export SNOWSQL_ROLE=<replace with your role>
>     export SNOWSQL_PWD=<replace with your password>
>     export SNOWSQL_DATABASE=<replace with your database>
>     export SNOWSQL_SCHEMA=<replace with your schema>
>     export SNOWSQL_WAREHOUSE=<replace with your warehouse>
>  
>
> Copy
>  
>     >     # Windows/PowerShell
>     $env:SNOWSQL_ACCOUNT = "<replace with your account identifer>"
>     $env:SNOWSQL_USER = "<replace with your username>"
>     $env:SNOWSQL_ROLE = "<replace with your role>"
>     $env:SNOWSQL_PWD = "<replace with your password>"
>     $env:SNOWSQL_DATABASE = "<replace with your database>"
>     $env:SNOWSQL_SCHEMA = "<replace with your schema>"
>     $env:SNOWSQL_WAREHOUSE = "<replace with your warehouse>"
>  
>
> Copy
>
> Optional: You can set this env var permanently by editing your bash profile
> (on Linux/MacOS) or using the System Properties menu (on Windows).

  3. Create and activate a conda environment using Anaconda:

> >     conda env create --file environment.yml
>     conda activate snowpark-testing
>  
>
> Copy

  4. Create the sample table in your account by running `setup/create_table.py`. This Python script will create a database called CITIBIKE, a schema called PUBLIC, and a small table called TRIPS.

> >     python setup/create_table.py
>  
>
> Copy

You’re now ready to move to the next section. In this section you:

  * Cloned the tutorial repository.

  * Created environment variables with your account information.

  * Created a conda environment for the project.

  * Connected to Snowflake using the Snowpark API and created a sample database, schema, and table.

## Try the Stored Procedure¶

The sample project includes a stored procedure handler (`sproc.py`) and three
DataFrames transformer methods (`transformers.py`). The stored procedure
handler uses the UDF and DataFrame transformers to read from the source table,
`CITIBIKE.PUBLIC.TRIPS`, and creates two fact tables: `MONTH_FACTS` and
`BIKE_FACTS`.

You can execute the stored procedure from the command line by running this
command.

    
    
    python project/sproc.py
    

Copy

Now that you’ve familiarized yourself with the project, in the next section
you will set up the test directory and create a PyTest Fixture for the
Snowflake session.

## Create a PyTest Fixture for the Snowflake Session¶

[PyTest fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) are functions
which are executed before a test (or module of tests), typically to provide
data or connections to tests. For this project, you will create a PyTest
fixture which returns a Snowpark `Session` object. Your test cases will use
this session to connect to Snowflake.

  1. Create a `test` directory under the project root directory.

> >     mkdir test
>  
>
> Copy

  2. Under the `test` directory, create a new Python file named `conftest.py`. Within `conftest.py`, create a PyTest fixture for the `Session` object:

> >     import pytest
>     from project.utils import get_env_var_config
>     from snowflake.snowpark.session import Session
>  
>     @pytest.fixture
>     def session() -> Session:
>         return Session.builder.configs(get_env_var_config()).create()
>  
>
> Copy

## Add Unit Tests for DataFrame Transformers¶

  1. In the `test` directory, create a new Python file named `test_transformers.py`.

  2. In the `test_transformers.py` file, import the transformer methods.

> >     # test/test_transformers.py
>  
>     from project.transformers import add_rider_age, calc_bike_facts,
> calc_month_facts
>  
>
> Copy

  3. Next, create unit tests for these transformers. The typical convention is to create a method for each test with the name `test_<name of method>`. In our case, the tests will be:

> >     # test/test_transformers.py
>     from project.transformers import add_rider_age, calc_bike_facts,
> calc_month_facts
>     def test_add_rider_age(session):
>         ...
>  
>     def test_calc_bike_facts(session):
>         ...
>  
>  
>     def test_calc_month_facts(session):
>         ...
>  
>
> Copy
>
> The `session` parameter in each test case refers to the PyTest fixture that
> you created in the previous section.

  4. Now implement the test cases for each transformer. Use the following pattern.

>     1. Create an input DataFrame.
>
>     2. Create the expected output DataFrame.
>
>     3. Pass the input DataFrame from step 1 into the transformer method.
>
>     4. Compare the output of step 3 to the expected output from step 2.
>  
>     >     # test/test_transformers.py
>     from project.transformers import add_rider_age, calc_bike_facts,
> calc_month_facts
>     from snowflake.snowpark.types import StructType, StructField,
> IntegerType, FloatType
>  
>     def test_add_rider_age(session: Session):
>         input = session.create_dataframe(
>             [
>                 [1980],
>                 [1995],
>                 [2000]
>             ],
>             schema=StructType([StructField("BIRTH_YEAR", IntegerType())])
>         )
>  
>         expected = session.create_dataframe(
>             [
>                 [1980, 43],
>                 [1995, 28],
>                 [2000, 23]
>             ],
>             schema=StructType([StructField("BIRTH_YEAR", IntegerType()),
> StructField("RIDER_AGE", IntegerType())])
>         )
>  
>         actual = add_rider_age(input)
>         assert expected.collect() == actual.collect()
>  
>  
>     def test_calc_bike_facts(session: Session):
>         input = session.create_dataframe([
>                 [1, 10, 20],
>                 [1, 5, 30],
>                 [2, 20, 50],
>                 [2, 10, 60]
>             ],
>             schema=StructType([
>                 StructField("BIKEID", IntegerType()),
>                 StructField("TRIPDURATION", IntegerType()),
>                 StructField("RIDER_AGE", IntegerType())
>             ])
>         )
>  
>         expected = session.create_dataframe([
>                 [1, 2, 7.5, 25.0],
>                 [2, 2, 15.0, 55.0],
>             ],
>             schema=StructType([
>                 StructField("BIKEID", IntegerType()),
>                 StructField("COUNT", IntegerType()),
>                 StructField("AVG_TRIPDURATION", FloatType()),
>                 StructField("AVG_RIDER_AGE", FloatType())
>             ])
>         )
>  
>         actual = calc_bike_facts(input)
>         assert expected.collect() == actual.collect()
>  
>  
>     def test_calc_month_facts(session: Session):
>         from patches import patch_to_timestamp
>  
>         input = session.create_dataframe(
>             data=[
>                 ['2018-03-01 09:47:00.000 +0000', 1, 10,  15],
>                 ['2018-03-01 09:47:14.000 +0000', 2, 20, 12],
>                 ['2018-04-01 09:47:04.000 +0000', 3, 6,  30]
>             ],
>             schema=['STARTTIME', 'BIKE_ID', 'TRIPDURATION', 'RIDER_AGE']
>         )
>  
>         expected = session.create_dataframe(
>             data=[
>                 ['Mar', 2, 15, 13.5],
>                 ['Apr', 1, 6, 30.0]
>             ],
>             schema=['MONTH', 'COUNT', 'AVG_TRIPDURATION', 'AVG_RIDER_AGE']
>         )
>  
>         actual = calc_month_facts(input)
>  
>         assert expected.collect() == actual.collect()
>  
>
> Copy

  5. You can now run PyTest to run all of the unit tests.

> >     pytest test/test_transformers.py
>  
>
> Copy

## Add Integration Tests for Stored Procedures¶

Now that we have unit tests for the DataFrame transformer methods, let’s add
an integration test for the stored procedure. The test case will follow this
pattern:

  1. Create a table representing the input data to the stored procedure.

  2. Create two DataFrames with the expected contents of the stored procedure’s two output tables.

  3. Call the stored procedure.

  4. Compare the actual output tables to the DataFrames from step 2.

  5. Clean up: delete the input table from step 1 and the output tables from step 3.

Create a Python file named `test_sproc.py` under the `test` directory.

Import the stored procedure hander from the project directory and create a
test case.

    
    
    # test/test_sproc.py
    from project.sproc import create_fact_tables
    
    def test_create_fact_tables(session):
        ...
    

Copy

Implement the test case, starting with the creation of the input table.

    
    
    # test/test_sproc.py
    from project.sproc import create_fact_tables
    from snowflake.snowpark.types import *
    
    def test_create_fact_tables(session):
        DB = 'CITIBIKE'
        SCHEMA = 'TEST'
    
        # Set up source table
        tbl = session.create_dataframe(
            data=[
                [1983, '2018-03-01 09:47:00.000 +0000', 551, 30958],
                [1988, '2018-03-01 09:47:01.000 +0000', 242, 19278],
                [1992, '2018-03-01 09:47:01.000 +0000', 768, 18461],
                [1980, '2018-03-01 09:47:03.000 +0000', 690, 15533],
                [1991, '2018-03-01 09:47:03.000 +0000', 490, 32449],
                [1959, '2018-03-01 09:47:04.000 +0000', 457, 29411],
                [1971, '2018-03-01 09:47:08.000 +0000', 279, 28015],
                [1964, '2018-03-01 09:47:09.000 +0000', 546, 15148],
                [1983, '2018-03-01 09:47:11.000 +0000', 358, 16967],
                [1985, '2018-03-01 09:47:12.000 +0000', 848, 20644],
                [1984, '2018-03-01 09:47:14.000 +0000', 295, 16365]
            ],
            schema=['BIRTH_YEAR', 'STARTTIME', 'TRIPDURATION',    'BIKEID'],
        )
    
        tbl.write.mode('overwrite').save_as_table([DB, SCHEMA, 'TRIPS_TEST'], mode='overwrite')
    

Copy

Next, create DataFrames for the expected output tables.

    
    
    # test/test_sproc.py
    from project.sproc import create_fact_tables
    from snowflake.snowpark.types import *
    
    def test_create_fact_tables(session):
        DB = 'CITIBIKE'
        SCHEMA = 'TEST'
    
        # Set up source table
        tbl = session.create_dataframe(
            data=[
                [1983, '2018-03-01 09:47:00.000 +0000', 551, 30958],
                [1988, '2018-03-01 09:47:01.000 +0000', 242, 19278],
                [1992, '2018-03-01 09:47:01.000 +0000', 768, 18461],
                [1980, '2018-03-01 09:47:03.000 +0000', 690, 15533],
                [1991, '2018-03-01 09:47:03.000 +0000', 490, 32449],
                [1959, '2018-03-01 09:47:04.000 +0000', 457, 29411],
                [1971, '2018-03-01 09:47:08.000 +0000', 279, 28015],
                [1964, '2018-03-01 09:47:09.000 +0000', 546, 15148],
                [1983, '2018-03-01 09:47:11.000 +0000', 358, 16967],
                [1985, '2018-03-01 09:47:12.000 +0000', 848, 20644],
                [1984, '2018-03-01 09:47:14.000 +0000', 295, 16365]
            ],
            schema=['BIRTH_YEAR', 'STARTTIME', 'TRIPDURATION',    'BIKEID'],
        )
    
        tbl.write.mode('overwrite').save_as_table([DB, SCHEMA, 'TRIPS_TEST'], mode='overwrite')
    
        # Expected values
        n_rows_expected = 12
        bike_facts_expected = session.create_dataframe(
            data=[
                [30958, 1, 551.0, 40.0],
                [19278, 1, 242.0, 35.0],
                [18461, 1, 768.0, 31.0],
                [15533, 1, 690.0, 43.0],
                [32449, 1, 490.0, 32.0],
                [29411, 1, 457.0, 64.0],
                [28015, 1, 279.0, 52.0],
                [15148, 1, 546.0, 59.0],
                [16967, 1, 358.0, 40.0],
                [20644, 1, 848.0, 38.0],
                [16365, 1, 295.0, 39.0]
            ],
            schema=StructType([
                StructField("BIKEID", IntegerType()),
                StructField("COUNT", IntegerType()),
                StructField("AVG_TRIPDURATION", FloatType()),
                StructField("AVG_RIDER_AGE", FloatType())
            ])
        ).collect()
    
        month_facts_expected = session.create_dataframe(
            data=[['Mar', 11, 502.18182, 43.00000]],
            schema=StructType([
                StructField("MONTH", StringType()),
                StructField("COUNT", IntegerType()),
                StructField("AVG_TRIPDURATION", DecimalType()),
                StructField("AVG_RIDER_AGE", DecimalType())
            ])
        ).collect()
    

Copy

And finally, call the stored procedure and read the output tables. Compare the
actual tables against the DataFrame contents.

    
    
    # test/test_sproc.py
    from project.sproc import create_fact_tables
    from snowflake.snowpark.types import *
    
    def test_create_fact_tables(session):
        DB = 'CITIBIKE'
        SCHEMA = 'TEST'
    
        # Set up source table
        tbl = session.create_dataframe(
            data=[
                [1983, '2018-03-01 09:47:00.000 +0000', 551, 30958],
                [1988, '2018-03-01 09:47:01.000 +0000', 242, 19278],
                [1992, '2018-03-01 09:47:01.000 +0000', 768, 18461],
                [1980, '2018-03-01 09:47:03.000 +0000', 690, 15533],
                [1991, '2018-03-01 09:47:03.000 +0000', 490, 32449],
                [1959, '2018-03-01 09:47:04.000 +0000', 457, 29411],
                [1971, '2018-03-01 09:47:08.000 +0000', 279, 28015],
                [1964, '2018-03-01 09:47:09.000 +0000', 546, 15148],
                [1983, '2018-03-01 09:47:11.000 +0000', 358, 16967],
                [1985, '2018-03-01 09:47:12.000 +0000', 848, 20644],
                [1984, '2018-03-01 09:47:14.000 +0000', 295, 16365]
            ],
            schema=['BIRTH_YEAR', 'STARTTIME', 'TRIPDURATION',    'BIKEID'],
        )
    
        tbl.write.mode('overwrite').save_as_table([DB, SCHEMA, 'TRIPS_TEST'], mode='overwrite')
    
        # Expected values
        n_rows_expected = 12
        bike_facts_expected = session.create_dataframe(
            data=[
                [30958, 1, 551.0, 40.0],
                [19278, 1, 242.0, 35.0],
                [18461, 1, 768.0, 31.0],
                [15533, 1, 690.0, 43.0],
                [32449, 1, 490.0, 32.0],
                [29411, 1, 457.0, 64.0],
                [28015, 1, 279.0, 52.0],
                [15148, 1, 546.0, 59.0],
                [16967, 1, 358.0, 40.0],
                [20644, 1, 848.0, 38.0],
                [16365, 1, 295.0, 39.0]
            ],
            schema=StructType([
                StructField("BIKEID", IntegerType()),
                StructField("COUNT", IntegerType()),
                StructField("AVG_TRIPDURATION", FloatType()),
                StructField("AVG_RIDER_AGE", FloatType())
            ])
        ).collect()
    
        month_facts_expected = session.create_dataframe(
            data=[['Mar', 11, 502.18182, 43.00000]],
            schema=StructType([
                StructField("MONTH", StringType()),
                StructField("COUNT", IntegerType()),
                StructField("AVG_TRIPDURATION", DecimalType()),
                StructField("AVG_RIDER_AGE", DecimalType())
            ])
        ).collect()
    
        # Call sproc, get actual values
        n_rows_actual = create_fact_tables(session, 'TRIPS_TEST')
        bike_facts_actual = session.table([DB, SCHEMA, 'bike_facts']).collect()
        month_facts_actual = session.table([DB, SCHEMA, 'month_facts']).collect()
    
        # Comparisons
        assert n_rows_expected == n_rows_actual
        assert bike_facts_expected == bike_facts_actual
        assert month_facts_expected ==  month_facts_actual
    

Copy

To run the test case, run `pytest` from the terminal.

    
    
    pytest test/test_sproc.py
    

Copy

To run all the tests in the project, run `pytest` without any other options.

    
    
    pytest
    

Copy

## Configure Local Testing¶

At this point you have a PyTest test suite for your DataFrame transformers and
stored procedure. In each test case, the `Session` fixture is used to connect
to your Snowflake account, send the SQL from the Snowpark Python API, and
retrieve the response.

Alternatively, you can use the local testing framework to run the
transformations locally without a connection to Snowflake. In large test
suites, this can add up to significantly faster test execution. This section
shows how to update the test suite to use the local testing framework
functionality.

  1. Begin by updating the PyTest `Session` fixture. We will add a command line option to PyTest to switch between local and live testing modes.

> >     # test/conftest.py
>  
>     import pytest
>     from project.utils import get_env_var_config
>     from snowflake.snowpark.session import Session
>  
>     def pytest_addoption(parser):
>         parser.addoption("--snowflake-session", action="store",
> default="live")
>  
>     @pytest.fixture(scope='module')
>     def session(request) -> Session:
>         if request.config.getoption('--snowflake-session') == 'local':
>             return Session.builder.configs({'local_testing': True}).create()
>         else:
>             return Session.builder.configs(get_env_var_config()).create()
>  
>
> Copy

  2. We must first patch this method because not all built-in functions are supported with the local testing framework, for example the `monthname()` function used in the `calc_month_facts()` transformer. Create a file named `patches.py` under the tests directory. In this file, paste the following code.

> >     from snowflake.snowpark.mock.functions import patch
>     from snowflake.snowpark.functions import monthname
>     from snowflake.snowpark.mock.snowflake_data_type import ColumnEmulator,
> ColumnType
>     from snowflake.snowpark.types import StringType
>     import datetime
>     import calendar
>  
>     @patch(monthname)
>     def patch_monthname(column: ColumnEmulator) -> ColumnEmulator:
>         ret_column = ColumnEmulator(data=[
>             calendar.month_abbr[datetime.datetime.strptime(row, '%Y-%m-%d
> %H:%M:%S.%f %z').month]
>             for row in column])
>         ret_column.sf_type = ColumnType(StringType(), True)
>         return ret_column
>  
>
> Copy
>
> The patch above accepts a single parameter, `column`, which is a
> `pandas.Series`-like object containing the rows of data within the column.
> We then use a combination of methods from the Python modules `datetime` and
> `calendar` to emulate the functionality of the built-in `monthname()`
> column. Finally, we set the return type to `String`, as the built-in method
> returns strings corresponding to the months (“Jan”, “Feb”, “Mar”, etc.).

  3. Next, import this method into the tests for the DataFrame transformer and the stored procedure.

> >     # test/test_transformers.py
>  
>     # No changes to the other unit test methods
>  
>     def test_calc_month_facts(request, session):
>         # Add conditional to include the patch if local testing is being
> used
>         if request.config.getoption('--snowflake-session') == 'local':
>             from patches import patch_monthname
>  
>         # No other changes
>  
>
> Copy

  4. Rerun `pytest` with the local flag.

> >     pytest test/test_transformers.py --snowflake-session local
>  
>
> Copy

  5. Now apply the same patch to the stored procedure test.

> >     #test/test_sproc.py
>  
>     def test_create_fact_tables(request, session):
>         # Add conditional to include the patch if local testing is being
> used
>         if request.config.getoption('--snowflake-session') == 'local':
>             from patches import patch_monthname
>  
>         # No other changes required
>  
>
> Copy

  6. Re-run pytest with the local flag.

> >     pytest test/test_sproc.py --snowflake-session local
>  
>
> Copy

  7. To wrap things up, let’s compare the time taken to run the full test suite locally versus with a live connection. We will use the `time` command to measure the time taken for both commands. Let’s start with the live connection.

> >     time pytest
>  
>
> Copy
>
> In this case, the test suite took 7.89 seconds to run. (Your exact time may
> differ depending on your computer, network connection, and other factors.)
>  
>     >     =================================== test session starts
> ==========================
>     platform darwin -- Python 3.9.18, pytest-7.4.3, pluggy-1.3.0
>     rootdir: /Users/jfreeberg/Desktop/snowpark-testing-tutorial
>     configfile: pytest.ini
>     collected 4 items
>  
>     test/test_sproc.py .
> [ 25%]
>     test/test_transformers.py ...
> [100%]
>  
>     =================================== 4 passed in 6.86s
> =================================
>     pytest  1.63s user 1.86s system 44% cpu 7.893 total
>  
>
> Now let’s try with the local testing framework:
>  
>     >     time pytest --snowflake-session local
>  
>
> Copy
>
> With the local testing framework the test suite, execution only took 1
> second!
>  
>     >     ================================== test session starts
> ================================
>     platform darwin -- Python 3.9.18, pytest-7.4.3, pluggy-1.3.0
>     rootdir: /Users/jfreeberg/Desktop/snowpark-testing-tutorial
>     configfile: pytest.ini
>     collected 4 items
>  
>     test/test_sproc.py .
> [ 25%]
>     test/test_transformers.py ...
> [100%]
>  
>     =================================== 4 passed in 0.10s
> ==================================
>     pytest --snowflake-session local  1.37s user 1.70s system 281% cpu 1.093
> total
>  

## Learn More¶

You finished! Nicely done.

In this tutorial, you got an end-to-end view of how you can test your Python
Snowpark code. Along the way, you:

  * **Created a PyTest fixture and added unit tests and integration tests.**

    * For more information, see [Writing Tests for Snowpark Python](../testing-python-snowpark).

  * **Configured local testing**

    * For more information, see [Local testing framework](../testing-locally).


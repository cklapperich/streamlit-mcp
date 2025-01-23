# Develop and run code in Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

This topic describes how to write and run SQL, Python, and Markdown code in
Snowflake Notebooks.

## Notebook cell basics¶

This section introduces some basic cell operations. When you [create a
notebook](notebooks-create.html#label-notebooks-create), three example cells
are displayed. You can modify those cells or add new ones.

### Create a new cell¶

Snowflake Notebooks support three types of cells: SQL, Python, and Markdown.
To create a new cell, you can either hover over an existing cell or scroll to
the bottom of the notebook, then select one of the buttons for the cell type
you want to add.

> ![Add new cell buttons at the bottom of the
> notebook.](../../_images/snowsight-ui-add-cell-bottom.png)

You can change the language of the cell any time after it’s created by using
one of two methods:

  * Select the language dropdown menu and then select a different language.

> ![Use the cell language drop down to change the cell
> language.](../../_images/snowsight-ui-change-cell.png)

  * Use [Keyboard shortcuts for Snowflake Notebooks](notebooks-keyboard-shortcuts).

### Move cells¶

You can move a cell either by dragging and dropping the cell using your mouse
or by using the actions menu:

  1. (Option 1) Hover your mouse over the existing cell you want to move. Select the [![Notebooks drag and drop icon](../../_images/notebooks-drag-drop.png)](../../_images/notebooks-drag-drop.png) (drag and drop) icon on the left side of the cell and move the cell to its new location.

  2. (Option 2) Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) (actions) menu. Then select the appropriate action.

Note

To just move the focus between cells, use the `Up` and `Down` arrows.

### Delete a cell¶

To delete a cell, complete the following steps in a notebook:

  1. Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) (more actions) menu.

  2. Select Delete.

  3. Select Delete again to confirm.

You can use a [keyboard shortcut](notebooks-keyboard-shortcuts) to delete a
cell as well.

For considerations when using Python and SQL cells, see Considerations for
running notebooks.

## Run cells in Snowflake Notebooks¶

To run Python and SQL cells in Snowflake Notebooks, you can:

  * **Run a single cell:** Choose this option when making frequent code updates.

    * Press `CMD` \+ `return` on a Mac keyboard, or `CTRL` \+ `Enter` on a Windows keyboard.

    * Select [![Run this cell only](../../_images/notebooks-run.png)](../../_images/notebooks-run.png), or Run this cell only.

  * **Run all cells in a notebook in sequential order:** Choose this option before presenting or sharing a notebook to ensure that the recipients see the most current information.

    * Press `CMD` \+ `shift` \+ `return` on a Mac keyboard, or `CTRL` \+ `Shift` \+ `Enter` on a Windows keyboard.

    * Select Run all.

  * **Run a cell and advance to the next cell:** Choose this option to run a cell and move on to the next cell more quickly.

    * Press `shift` \+ `return` on a Mac keyboard, or `Shift` \+ `Enter` on a Windows keyboard.

    * Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) (more actions) for a cell, and choose Run cell and advance.

  * **Run all above** : Choose this option when running a cell that references the results of earlier cells.

    * Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) (more actions) for a cell, and choose Run all above.

  * **Run all below** : Choose this option when running a cell that later cells depend on. This option runs the current cell and all following cells.

    * Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) (more actions) for a cell, and choose Run all below.

When one cell is running, other run requests are queued and will be executed
once the actively running cell finishes.

### Inspect cell status¶

The status of the cell run is indicated by the colors displayed by the cell.
This status color is displayed in two places, the left wall of the cell and in
the right cell navigation map.

Cell status color:

  * Blue dot: The cell was modified but hasn’t run yet.

  * Red: The cell ran in the current session and an error occurred.

  * Green: The cell ran in the current session without errors.

  * Moving green: The cell is currently running.

  * Gray: The cell has run in a previous session and the results shown are from the previous session. Cell results from the previous interactive session are kept for 7 days. Interactive session means the user runs the notebook in an interactive manner in Snowsight rather than those that were run by a schedule or the EXECUTE NOTEBOOK SQL command.

  * Blinking gray: The cell is waiting to be run after you select Run All.

Note

Markdown cells do not show any status.

After a cell finishes running, the time it took to run is displayed at the top
of the cell. Select this text to view the run details, including start and end
times and total elapsed time.

SQL cells contain additional information, such as the warehouse used to run
the query, rows returned, and a hyperlink to the query ID page.

> [![Cell run details window.](../../_images/snowsight-ui-cell-run-
> details.png)](../../_images/snowsight-ui-cell-run-details.png)

### Stop a running cell¶

To stop the execution of any code cells that are currently running, select
Stop on the top right of the cell. You can also select Stop on the top right
of the Notebooks page. While cells are running, Run all becomes Stop.

This stops the execution of the cell that is currently running and all
subsequent cells that have been scheduled to run.

## Format text with Markdown¶

To include Markdown in your notebook, add a Markdown cell:

  1. Use a [keyboard shortcut](notebooks-keyboard-shortcuts.html#label-notebooks-keyboard-shortcuts) and select Markdown, or select \+ Markdown.

  2. Select the Edit markdown pencil icon or double click on the cell, and start writing Markdown.

You can type valid Markdown to format a text cell. As you type, the formatted
text appears below the Markdown syntax.

[![Screenshot of a Markdown cell showing Markdown text with an H1 header
indicated with a # and a header of An example Markdown cell followed by body
text of This is an example Markdown cell in a Snowflake Notebook. Below the
raw Markdown content, the rendered Markdown appears with a different
font.](../../_images/notebooks-markdown-editing.png)](../../_images/notebooks-
markdown-editing.png)

To view only the formatted text, select the Done editing checkmark icon.

[![Screenshot of a Markdown cell that is showing only the rendered Markdown: a
header of An example Markdown cell and body text of This is an example
Markdown cell in a Snowflake Notebook.](../../_images/notebooks-markdown-
display.png)](../../_images/notebooks-markdown-display.png)

Note

Markdown cells currently do not support rendering of HTML.

### Markdown basics¶

This section describes basic Markdown syntax to get you started.

**Headers**

Heading level | Markdown syntax | Example  
---|---|---  
Top level | 
    
    
    # Top-level Header
    

Copy |  ![Header one in Markdown](../../_images/notebooks-md-header-one.png)  
2nd-level | 
    
    
    ## 2nd-level Header
    

Copy |  ![Header one in Markdown](../../_images/notebooks-md-header-two.png)  
3rd-level | 
    
    
    ### 3rd-level Header
    

Copy |  ![Header one in Markdown](../../_images/notebooks-md-header-three.png)  
  
**Inline text formatting**

Text format | Markdown syntax | Example  
---|---|---  
Italics | 
    
    
    *italicized text*
    

Copy |  ![Italicized text in Markdown](../../_images/notebooks-md-italics.png)  
Bold | 
    
    
    **bolded text**
    

Copy |  ![Bolded text in Markdown](../../_images/notebooks-md-bolded.png)  
Link | 
    
    
    [Link text](url)
    

Copy |  ![Link in Markdown](../../_images/notebooks-md-link.png)  
  
**Lists**

List type | Markdown syntax | Example  
---|---|---  
Ordered list | 
    
    
    1. first item
    2. second item
      1. Nested first
      2. Nested second
    

Copy |  ![Ordered list in Markdown](../../_images/notebooks-md-ordered-list.png)  
Unordered list | 
    
    
    - first item
    - second item
      - Nested first
      - Nested second
    

Copy |  ![Unordered list in Markdown](../../_images/notebooks-md-unordered-list.png)  
  
**Code formatting**

Language | Markdown syntax | Example  
---|---|---  
Python | 
    
    
    ```python
    import pandas as pd
    df = pd.DataFrame([1,2,3])
    ```
    

Copy |  ![Python code snippet in Markdown](../../_images/notebooks-md-python.png)  
SQL | 
    
    
    ```sql
    SELECT * FROM MYTABLE
    ```
    

Copy |  ![SQL code snippet in Markdown](../../_images/notebooks-md-sql.png)  
  
**Embed images**

File type | Markdown syntax | Example  
---|---|---  
Image | 
    
    
    ![<alt_text>](<path_to_image>)
    

Copy |  ![Embedded image in Markdown](../../_images/notebooks-md-embed-img.png)  
  
For a notebook that demonstrates these Markdown examples, see the [Markdown
cells](https://github.com/Snowflake-Labs/snowflake-demo-
notebooks/blob/main/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks/Visual%20Data%20Stories%20with%20Snowflake%20Notebooks.ipynb)
section of the visual data stories notebook.

## Understanding cell outputs¶

When you run a Python cell, the notebook displays the following types of
output from the cell are displayed in the results:

  * Any results written to the console, such as logs, errors, and warnings and output from print() statements.

  * DataFrames are automatically printed with [Streamlit’s interactive table display](https://docs.streamlit.io/develop/api-reference/data/st.dataframe), `st.dataframe()`.

    * The supported DataFrame display types include pandas DataFrame, Snowpark DataFrames, and Snowpark Tables.

    * For Snowpark, printed DataFrames are evaluated eagerly without the need to run the `.show()` command. If you prefer not to evaluate the DataFrame eagerly, for example when running the notebook in non-interactive mode, Snowflake recommends removing the DataFrame print statements to speed up the overall runtime of your Snowpark code.

  * Visualizations are rendered in outputs. To learn more about visualizing your data, see [Visualize data in Snowflake Notebooks](notebooks-visualize-data).

Additionally, you can access the results of your SQL query in Python and vice
versa. See Reference cells and variables in Snowflake Notebooks.

### Cell output limits¶

Only 10,000 rows or 8 MB of DataFrame output is shown as cell results,
whichever is lower. However, the entire DataFrame is still available in the
notebook session for use. For example, even though the entire DataFrame isn’t
rendered, you can still perform data transformation tasks.

For each cell, only 20 MB of output is allowed. If the size of the cell output
exceeds 20 MB, the output will be dropped. Consider splitting the content into
multiple cells if that happens.

## Reference cells and variables in Snowflake Notebooks¶

You can reference the previous cell results in a notebook cell. For example,
to reference the result of a SQL cell or the value of a Python variable, see
the following tables:

Note

The cell name of the reference is case-sensitive and must exactly match the
name of the referenced cell.

**Referencing SQL output in Python cells:**

Reference cell type | Current cell type | Reference syntax | Example  
---|---|---|---  
SQL | Python | `cell1` | Convert a SQL results table to a Snowpark DataFrame. If you have the following in a SQL cell called `cell1`:
    
    
    SELECT 'FRIDAY' as SNOWDAY, 0.2 as CHANCE_OF_SNOW
    UNION ALL
    SELECT 'SATURDAY',0.5
    UNION ALL
    SELECT 'SUNDAY', 0.9;
    

Copy You can reference the cell to access the SQL result:

    
    
    snowpark_df = cell1.to_df()
    

Copy Convert the result to a pandas DataFrame:

    
    
    my_df = cell1.to_pandas()
    

Copy  
  
**Referencing variables in SQL code:**

Important

In SQL code, you can only reference Python variables of type `string`. You
cannot reference a Snowpark DataFrame, pandas DataFrame or other Python native
DataFrame format.

Reference cell type | Current cell type | Reference syntax | Example  
---|---|---|---  
SQL | SQL | `{{cell2}}` | For example, in a SQL cell named `cell1`, reference the cell results from `cell2`:
    
    
    SELECT * FROM {{cell2}} where PRICE > 500
    

Copy  
Python | SQL | `{{variable}}` | For example, in a Python cell named `cell1`: **Using Python variable as a value**
    
    
    c = "USA"
    

Copy You can reference the value of the variable `c` in a SQL cell named
`cell2` by enclosing it in single quotes to ensure that it is treated as a
value:

    
    
    SELECT * FROM my_table WHERE COUNTRY = '{{c}}'
    

Copy **Using Python variable as an identifier** If the Python variable
represents a SQL identifier like a column or table name:

    
    
    column_name = "COUNTRY"
    

Copy If the Python variable represents a SQL identifier, such as a column or
table name (`column_name = "COUNTRY"`), you can reference the variable
directly without quotes:

    
    
    SELECT * FROM my_table WHERE {{column_name}} = 'USA'
    

Copy Make sure to differentiate between variables used as values (with quotes)
and as identifiers (without quotes). Note: Referencing Python DataFrames is
not supported.  
  
## Considerations for running notebooks¶

  * Notebooks run using caller’s rights. For additional considerations, see [Changing the session context for a notebook](notebooks-sessions.html#label-notebooks-callers-rights).

  * You can import Python libraries to use in a notebook. For details, see [Import Python packages to use in notebooks](notebooks-import-packages).

  * When referencing objects in SQL cells, you must use fully qualified object names, unless you are referencing object names in a specified database or schema. See [Changing the session context for a notebook](notebooks-sessions.html#label-notebooks-callers-rights).

  * Notebook drafts are saved every three seconds.

  * You can use Git integration to maintain notebook versions.

  * You can configure an idle timeout setting to automatically shut down the notebook session once the setting is met. For information, see [Idle time and reconnection](notebooks-setup.html#label-notebooks-idle-time-property).

  * Notebook cell results are only visible to the user who ran the notebook and are cached across sessions. Reopening a notebook displays past results from the last time the user ran the notebook using Snowsight.

  * [BEGIN … END (Snowflake Scripting)](../../sql-reference/snowflake-scripting/begin) is not supported in SQL cells. Instead, use the [Session.sql().collect()](https://docs.snowflake.com/en/developer-guide/snowpark/reference/python/latest/api/snowflake.snowpark.Session.sql) method in a Python cell to run the scripting block. Chain the `sql` call with a call to `collect` to immediately execute the SQL query.

The following code runs a Snowflake scripting block using the
`session.sql().collect()` method:

    
        from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    code_to_run = """
    BEGIN
        CALL TRANSACTION_ANOMALY_MODEL!DETECT_ANOMALIES(
            INPUT_DATA => SYSTEM$REFERENCE('TABLE', 'ANOMALY_INFERENCE'),
            TIMESTAMP_COLNAME =>'DATE',
            TARGET_COLNAME => 'TRANSACTION_AMOUNT',
            CONFIG_OBJECT => {'prediction_interval': 0.95}
        );
    
        LET x := SQLID;
        CREATE TABLE ANOMALY_PREDICTIONS AS SELECT * FROM TABLE(RESULT_SCAN(:x));
    END;
    """
    data = session.sql(code_to_run).collect(block=True);
    

Copy


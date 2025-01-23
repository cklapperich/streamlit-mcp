# Explore Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

This page describes the Snowflake Notebooks toolbar and the controls used to
manage the notebook and adjust cell display settings.

Control | Description  
---|---  
[![../../_images/ui-notebooks-packages.png](../../_images/ui-notebooks-packages.png)](../../_images/ui-notebooks-packages.png) | Package selector: Select and install packages for use in the notebook. See [Import Python packages to use in notebooks](notebooks-import-packages.html#label-notebooks-import-libraries).  
[![../../_images/ui-notebooks-start.png](../../_images/ui-notebooks-start.png)](../../_images/ui-notebooks-start.png) | Start: Start the Notebooks session. When the session starts, the image changes to Active.  
[![../../_images/ui-notebooks-active.png](../../_images/ui-notebooks-active.png)](../../_images/ui-notebooks-active.png) | Active: Hover over the button to view session details. Select the down arrow to access options to restart or end the session. Select Active to end the current session.  
[![../../_images/ui-notebooks-run-all.png](../../_images/ui-notebooks-run-all.png)](../../_images/ui-notebooks-run-all.png) | Run All/Stop: Run all cells or stop cell execution. See [Run cells in Snowflake Notebooks](notebooks-develop-run.html#label-notebooks-run).  
[![../../_images/ui-notebooks-scheduler.png](../../_images/ui-notebooks-scheduler.png)](../../_images/ui-notebooks-scheduler.png) | Scheduler: Set a schedule to run your notebook as a task in the future. See [Schedule your Snowflake Notebook to run](notebooks-schedule).  
[![../../_images/ui-notebooks-ellipsis.png](../../_images/ui-notebooks-ellipsis.png)](../../_images/ui-notebooks-ellipsis.png) | Vertical ellipsis menu: Customize notebook settings, clear cell outputs, duplicate, export, or delete the notebook.  
  
## Collapse cells in a notebook¶

You can collapse the code in a cell to see only the output. For example,
collapse a Python cell to show only the visualizations produced by your code,
or collapse a SQL cell to show only the results table.

  * To change what is visible, select Collapse results.
    

The drop-down offers options to collapse specific parts of the cell.

![Collapse or expand cell.](../../_images/snowsight-ui-cell-collapse.png)


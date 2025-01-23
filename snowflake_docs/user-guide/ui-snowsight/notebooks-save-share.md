# Save and share results in Snowflake Notebooks¶

Feature — Generally Available

Generally available in Amazon Web Services (AWS), Microsoft Azure, and Google
Cloud Platform (GCP) commercial regions.

You can collaborate on data analysis with others using Snowflake Notebooks.

Each Snowflake Notebook is owned by a role, so other users that are granted or
inherit the owner role can open, run, and edit notebooks owned by that role.
You cannot share the notebook with other roles.

Caution

Notebooks are saved every three seconds. If other users have the notebook open
and run it, you might overwrite each other’s work.

## Export your notebook as file for sharing¶

To share your notebook externally, you can export it as an `.ipynb` file. The
exported notebook can be shared with others who may not use Snowflake
Notebooks. They can open the notebooks with other solutions that are
compatible with the `.ipynb` format.

  1. Sign in to [Snowsight](../ui-snowsight).

  2. Select Projects » Notebooks.

  3. Open the notebook to export.

  4. Select the vertical ellipsis [![more actions for worksheet](../../_images/snowsight-worksheet-vertical-ellipsis.png)](../../_images/snowsight-worksheet-vertical-ellipsis.png) menu, and then select Export.

  5. Acknowledge that some commands might not be supported in other notebook tools, and select Export.

A file named `notebook_app` is downloaded. You can then [import the exported
notebook into another Snowflake account](notebooks-create.html#label-
notebooks-create) or another tool that supports `.ipynb` files.

Note

Only the cell content — not the cell outputs — is included as part of the
export.

## Collaborate in notebooks¶

  * The role used to create the notebook owns the notebook. For details on privileges required for notebooks, see [Set up Snowflake Notebooks](notebooks-setup).

  * Any user with that role, or whose role inherits that role, can access, edit, run, and manage the notebook.

  * To share and collaborate on a notebook with another user, that user must either have the owner role or be granted a role that inherits the owner role of the notebook.

  * You cannot share a notebook with other roles.


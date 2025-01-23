# Staging data files from a local file system¶

Execute [PUT](../sql-reference/sql/put) using the [SnowSQL client](snowsql) or
[Drivers](../developer-guide/drivers) to upload (stage) local data files into
an internal stage.

If you want to load a few small local data files into a named internal stage,
you can also use Snowsight. Refer to [Staging files using Snowsight](data-
load-local-file-system-stage-ui).

## Staging the data files¶

User Stage

    

The following example uploads a file named `data.csv` in the `/data` directory
on your local machine to your user stage and prefixes the file with a folder
named `staged`.

Note that the `@~` character combination identifies a user stage.

  * Linux or macOS

> >     PUT file:///data/data.csv @~/staged;
>  
>
> Copy

  * Windows

> >     PUT file://C:\data\data.csv @~/staged;
>  
>
> Copy

Table Stage

    

The following example uploads a file named `data.csv` in the `/data` directory
on your local machine to the stage for a table named `mytable`.

Note that the `@%` character combination identifies a table stage.

  * Linux or macOS

> >     PUT file:///data/data.csv @%mytable;
>  
>
> Copy

  * Windows

> >     PUT file://C:\data\data.csv @%mytable;
>  
>
> Copy

Named Stage

    

The following example uploads a file named `data.csv` in the `/data` directory
on your local machine to a named internal stage called `my_stage`. See
[Choosing an internal stage for local files](data-load-local-file-system-
create-stage) for information on named stages.

Note that the `@` character by itself identifies a named stage.

  * Linux or macOS

> >     PUT file:///data/data.csv @my_stage;
>  
>
> Copy

  * Windows

> >     PUT file://C:\data\data.csv @my_stage;
>  
>
> Copy

## Listing staged data files¶

To see files that have been uploaded to a Snowflake stage, use the
[LIST](../sql-reference/sql/list) command:

User stage:

    
    
    LIST @~;
    

Copy

Table stage:

    
    
    LIST @%mytable;
    

Copy

Named stage:

    
    
    LIST @my_stage;
    

Copy

**Next:** [Copying data from an internal stage](data-load-local-file-system-
copy)


# Reference organizational listings in queries¶

Note

Organizational listings can be queried without mounting.

To reference an organizational listing’s datasets in a SQL query, use the
Uniform Listing Locator (ULL). The ULL serves as a unique identifier that
points to a listing in the Internal Marketplace, making it easy to query its
datasets directly.

The ULL appears to be a fully qualified name that includes the database,
schema, and object names (database_name.schema_name.table_name), but uses
dollar signs ($) instead of periods (.). However, this is not the case.

SnowsightSQL

  1. Sign in to [Snowsight](../../../ui-snowsight).

  2. Select Data Products » Marketplace in the left-side navigation menu.

  3. Select the Internal Marketplace tab.

  4. Browse or search for a data product.

  5. Select a listing and select Copy ULL.

  6. Select Projects.

  7. Select one of the project tools, for example Worksheets or Notebooks.

  8. Write a SQL query, using the ULL in place of the database name.

To query an organizational listing, use the following syntax:

    
    
    SELECT * FROM <ull>.<schema>.<view>
    

Copy

Example queries:

    
    
    SELECT * FROM "<orgdatacloud$internal$organizational_listing_name>".<schema_name>.<object_within_listing>;
    SELECT * FROM <orgdatacloud$internal$organizational_listing_name>.<schema_name>.<object_within_listing>;
    

Copy

The following query example uses the ULL as a replacement for the database
name. Replace `<object_within_listing>` with the name of a table or view
that’s part of the listing:

    
    
    SELECT * FROM <orgdatacloud$internal$organizational_listing_name>.<schema_name>.<object_within_listing>;
    

Copy

If you prefer a more convenient name, consider creating a view:

    
    
    CREATE OR REPLACE VIEW <view_name>
    AS
    SELECT *
    FROM <orgdatacloud$internal$organizational_listing_name>.<schema_name>.<object_within_listing>;
    

Copy


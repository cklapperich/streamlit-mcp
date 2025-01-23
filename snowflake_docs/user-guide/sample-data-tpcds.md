# Sample Data: TPC-DS¶

As described in the [TPC Benchmark™ DS (TPC-
DS)](http://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-DS_v2.5.0.pdf)
specification:

> “TPC-DS models the decision support functions of a retail product supplier.
> The supporting schema contains vital business information, such as customer,
> order, and product data.
>
> In order to address the enormous range of query types and user behaviors
> encountered by a decision support system, TPC-DS utilizes a generalized
> query model. This model allows the benchmark to capture important aspects of
> the interactive, iterative nature of on-line analytical processing (OLAP)
> queries, the longer-running complex queries of data mining and knowledge
> discovery, and the more planned behavior of well known report queries.”

## Database and Schemas¶

Snowflake provides both 10 TB and 100 TB versions of TPC-DS, in schemas named
TPCDS_SF10TCL and TPCDS_SF100TCL, respectively, within the
SNOWFLAKE_SAMPLE_DATA shared database.

## Database Entities, Relationships, and Characteristics¶

TPC-DS consists of 7 fact tables and 17 dimensions in the following schemas:

  * TPCDS_SF100TCL: The 100 TB (_scale factor_ 100,000) version represents 100 million customers and over 500,000 items stored, with sales data spanning 3 channels — stores, catalogs, and the web — covering a period of 5 years. The largest table, STORE_SALES, contains nearly 300 billion rows, and the fact tables contain over 560 billion rows in total.

  * TPCDS_SF10TCL: The 10 TB (scale factor 10,000) version represents 65 million customers and over 400,000 items stored, with sales data spanning 3 channels — stores, catalogs, and the web — covering a period of 5 years. The largest table, STORE_SALES, contains nearly 29 billion rows, and the fact tables contain over 56 billion rows in total.

The relationships between facts and dimensions are represented through joins
on surrogate keys. The detailed relationships are too numerous to display
here, but can be found in the TPC-DS specification.

## Query Definitions¶

TPC-DS contains a set of 99 queries with wide variation in complexity and
range of data scanned. Each TPC-DS query asks a business question and includes
the corresponding query to answer the question. We have generated samples of
all 99 TPC-DS queries for you to explore. Alternatively, you can use the tools
in the TPC-DS Benchmark Kit to generate many different versions of these
queries that vary by parameter values.

For the 10 TB version, the full set of 99 TPC-DS queries should complete in
under 45 minutes using a Snowflake 2X-Large warehouse. If you use the 100 TB
version, queries should complete in under 1 hour using a 4X-Large warehouse.

Below, we describe just one of the queries. More information about TPC-DS and
all the queries involved can be found in the official TPC-DS specification.

### Q57: Catalog Sales Call Center Outliers¶

This query looks at a year’s worth of CATALOG_SALES table data and reveals the
categories and brands where sales in a month vary more than 10% from average
for a given call center.

#### Business Question¶

Find the item brands and categories for each call center and their monthly
sales figures for a specified year, where the monthly sales figure deviated
more than 10% of the average monthly sales for the year, sorted by deviation
and call center. Report the sales deviation from the previous and following
months.

#### Functional Query Definition¶

The query lists the following totals:

  * Extended price

  * Discounted extended price

  * Discounted extended price plus tax

  * Average quantity

  * Average extended price

  * Average discount

These aggregates are grouped by RETURNFLAG and LINESTATUS and are listed in
ascending order of RETURNFLAG and LINESTATUS. A count of the number of line
items in each group is included:

>
>     use schema snowflake_sample_data.tpcds_sf10Tcl;
>  
>     -- QID=TPC-DS_query57
>  
>     with v1 as(
>       select i_category, i_brand, cc_name, d_year, d_moy,
>             sum(cs_sales_price) sum_sales,
>             avg(sum(cs_sales_price)) over
>               (partition by i_category, i_brand,
>                          cc_name, d_year)
>               avg_monthly_sales,
>             rank() over
>               (partition by i_category, i_brand,
>                          cc_name
>                order by d_year, d_moy) rn
>       from item, catalog_sales, date_dim, call_center
>       where cs_item_sk = i_item_sk and
>            cs_sold_date_sk = d_date_sk and
>            cc_call_center_sk= cs_call_center_sk and
>            (
>              d_year = 1999 or
>              ( d_year = 1999-1 and d_moy =12) or
>              ( d_year = 1999+1 and d_moy =1)
>            )
>       group by i_category, i_brand,
>               cc_name , d_year, d_moy),
>     v2 as(
>       select v1.i_category ,v1.d_year, v1.d_moy ,v1.avg_monthly_sales
>             ,v1.sum_sales, v1_lag.sum_sales psum, v1_lead.sum_sales nsum
>       from v1, v1 v1_lag, v1 v1_lead
>       where v1.i_category = v1_lag.i_category and
>            v1.i_category = v1_lead.i_category and
>            v1.i_brand = v1_lag.i_brand and
>            v1.i_brand = v1_lead.i_brand and
>            v1.cc_name = v1_lag.cc_name and
>            v1.cc_name = v1_lead.cc_name and
>            v1.rn = v1_lag.rn + 1 and
>            v1.rn = v1_lead.rn - 1)
>     select  *
>     from v2
>     where  d_year = 1999 and
>             avg_monthly_sales > 0 and
>             case when avg_monthly_sales > 0 then abs(sum_sales -
> avg_monthly_sales) / avg_monthly_sales else null end > 0.1
>     order by sum_sales - avg_monthly_sales, 3
>     limit 100;
>  
>
> Copy


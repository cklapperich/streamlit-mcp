# Sample Data: TPC-H¶

As described in the [TPC Benchmark™ H (TPC-H)](http://www.tpc.org/tpch/)
specification:

> “TPC-H is a decision support benchmark. It consists of a suite of business-
> oriented ad hoc queries and concurrent data modifications. The queries and
> the data populating the database have been chosen to have broad industry-
> wide relevance. This benchmark illustrates decision support systems that
> examine large volumes of data, execute queries with a high degree of
> complexity, and give answers to critical business questions.”

## Database and Schemas¶

TPC-H comes with various data set sizes to test different scaling factors. For
demonstration purposes, we’ve shared four versions of the TPC-H data. The data
is provided in the following schemas in the SNOWFLAKE_SAMPLE_DATA shared
database:

  * TPCH_SF1: Consists of the base row size (several million elements).

  * TPCH_SF10: Consists of the base row size x 10.

  * TPCH_SF100: Consists of the base row size x 100 (several hundred million elements).

  * TPCH_SF1000: Consists of the base row size x 1000 (several billion elements).

## Database Entities, Relationships, and Characteristics¶

The components of TPC-H consist of eight separate and individual tables (the
Base Tables). The relationships between columns in these tables are
illustrated in the following ER diagram:

> ![Schema for TPC-H benchmark data](../_images/sample-data-tpch-schema.png)

(source: [TPC Benchmark H Standard
Specification](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-
h_v2.17.1.pdf))

## Query Definitions¶

Each TPC-H query asks a business question and includes the corresponding query
to answer the question. Some of the TPC-H queries are included in Snowflake’s
Getting Started tutorials.

This section describes one of the queries. More information about TPC-H and
all the queries involved can be found in the official [TPC Benchmark H
Standard
Specification](http://www.tpc.org/tpc_documents_current_versions/pdf/tpc-
h_v2.17.1.pdf).

### Q1: Pricing Summary Report Query¶

This query reports the amount of business that was billed, shipped, and
returned.

#### Business Question¶

The Pricing Summary Report Query provides a summary pricing report for all
line items shipped as of a given date. The date is within 60-120 days of the
greatest ship date contained in the database.

#### Functional Query Definition¶

The query lists totals for extended price, discounted extended price,
discounted extended price plus tax, average quantity, average extended price,
and average discount. These aggregates are grouped by RETURNFLAG and
LINESTATUS, and listed in ascending order of RETURNFLAG and LINESTATUS. A
count of the number of line items in each group is included:

>
>     use schema snowflake_sample_data.tpch_sf1;   -- or snowflake_sample_data.{tpch_sf10 | tpch_sf100 | tpch_sf1000}
>  
>     select
>            l_returnflag,
>            l_linestatus,
>            sum(l_quantity) as sum_qty,
>            sum(l_extendedprice) as sum_base_price,
>            sum(l_extendedprice * (1-l_discount)) as sum_disc_price,
>            sum(l_extendedprice * (1-l_discount) * (1+l_tax)) as sum_charge,
>            avg(l_quantity) as avg_qty,
>            avg(l_extendedprice) as avg_price,
>            avg(l_discount) as avg_disc,
>            count(*) as count_order
>      from
>            lineitem
>      where
>            l_shipdate <= dateadd(day, -90, to_date('1998-12-01'))
>      group by
>            l_returnflag,
>            l_linestatus
>      order by
>            l_returnflag,
>            l_linestatus;
>  
>
> Copy


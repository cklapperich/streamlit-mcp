# Design Guidelines and Constraints for Functions and Procedures¶

This topic describes constraints and guidelines to keep in mind when writing
UDFs and stored procedures.

[Keeping handler code in-line or on a stage](inline-or-staged)

    

Choose whether to have your handler code in-line or packaged in a separate
file.

[Designing Handlers that Stay Within Snowflake-Imposed Constraints](udf-
stored-procedure-constraints)

    

Ensure stability within the Snowflake environment by developing within
constraints described in this topic.

[Naming and overloading procedures and UDFs](udf-stored-procedure-naming-
conventions)

    

Learn the rules for naming and overloading procedures and UDFs.

[Defining arguments for UDFs and stored procedures](udf-stored-procedure-
arguments)

    

Specify the arguments for your procedures and UDFs.

[Data Type Mappings Between SQL and Handler Languages](udf-stored-procedure-
data-type-mapping)

    

Choose the best data types for argument and return values in handler code.

[Making dependencies available to your code](upload-dependencies)

    

Make your handler or its dependencies available for use at runtime on
Snowflake.

## Security¶

[Security Practices for UDFs and Procedures](udf-stored-procedure-security-
practices)

    

Help your handler code execute securely using these best practices.

[Protecting Sensitive Information with Secure UDFs and Stored
Procedures](secure-udf-procedure)

    

Ensure that sensitive information is concealed from users who should not have
access to it.

[Pushdown Optimization and Data Visibility](pushdown-optimization)

    

Learn about the pushdown optimization that makes queries more efficient, but
which can also expose data that you might not want to be visible.


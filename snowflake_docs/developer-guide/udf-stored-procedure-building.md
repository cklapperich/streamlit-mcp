# Packaging Handler Code¶

To make function or procedure handler code written in Java or Scala easier to
reuse, you can build a JAR file that contains the handler and its
dependencies. When you create the function or procedure, you reference the
handler JAR on a stage.

Topics in this section describe how to build handlers with commonly-used build
tools.

For more information about using packaged handler code (as well as other
dependencies) by referencing them on a stage, see [Keeping handler code in-
line or on a stage](inline-or-staged).

Note

You can also use an IntelliJ IDEA project (not an SBT project in IntelliJ) to
create the handler JAR. For more information, see the [instructions on setting
up an artifact configuration](https://www.jetbrains.com/help/idea/compiling-
applications.html#configure_artifact).

[Packaging Scala Handler Code with sbt](udf-stored-procedure-build-sbt)

    

Build Scala handler code with sbt.

[Packaging Java or Scala Handler Code with Maven](udf-stored-procedure-build-
maven)

    

Build handler code with Maven.


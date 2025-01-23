# Snowflake Scripting reference¶

These topics provide reference information for the language elements supported
in [Snowflake Scripting](developer-guide/snowflake-scripting/index).

    
    
    -- Variable declaration
    [ DECLARE ... ]
      ...
    BEGIN
      ...
      -- Branching
      [ IF ... ]
      [ CASE ... ]
    
      -- Looping
      [ FOR ... ]
      [ WHILE ... ]
      [ REPEAT ... ]
      [ LOOP ... ]
    
      -- Loop termination (within a looping construct)
      [ BREAK ]
      [ CONTINUE ]
    
      -- Variable assignment
      [ LET ... ]
    
      -- Cursor management
      [ OPEN ... ]
      [ FETCH ... ]
      [ CLOSE ... ]
    
      -- Asynchronous child job management
      [ AWAIT ... ]
      [ CANCEL ... ]
    
      -- "No-op" (no-operation) statement (usually within a branch or exception)
      [ NULL ]
    
      -- Raising exceptions
      [ RAISE ... ]
    
      -- Returning a value
      [ RETURN ... ]
    
    -- Exception handling
    [ EXCEPTION ... ]
    
    END;
    

Copy

**Next Topics:**

  * [BEGIN … END](sql-reference/snowflake-scripting/begin)

  * [BREAK](sql-reference/snowflake-scripting/break)

  * [CASE](sql-reference/snowflake-scripting/case)

  * [CLOSE](sql-reference/snowflake-scripting/close)

  * [CONTINUE](sql-reference/snowflake-scripting/continue)

  * [DECLARE](sql-reference/snowflake-scripting/declare)

  * [EXCEPTION](sql-reference/snowflake-scripting/exception)

  * [FETCH](sql-reference/snowflake-scripting/fetch)

  * [FOR](sql-reference/snowflake-scripting/for)

  * [IF](sql-reference/snowflake-scripting/if)

  * [LET](sql-reference/snowflake-scripting/let)

  * [LOOP](sql-reference/snowflake-scripting/loop)

  * [NULL](sql-reference/snowflake-scripting/null)

  * [OPEN](sql-reference/snowflake-scripting/open)

  * [RAISE](sql-reference/snowflake-scripting/raise)

  * [REPEAT](sql-reference/snowflake-scripting/repeat)

  * [RETURN](sql-reference/snowflake-scripting/return)

  * [WHILE](sql-reference/snowflake-scripting/while)


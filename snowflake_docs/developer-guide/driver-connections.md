# Considerations when reusing a session or connection among multiple threads¶

Snowflake drivers use stateful connections. Reusing the same session or
connection among threads has multiple drawbacks. For example, when a session
is initialized, it starts with a default database, schema, role, and a set of
parameters. A connection starts and ends a session, which establishes a one-
to-one relationship between a session and a connection. The following section
highlights common effects of reusing connections across concurrent threads.

## Effects of reusing a session or connection across multiple threads¶

Driver users often create multi-threaded applications. Rather than creating
separate sessions and connections for each thread, you might try to save some
overhead by reusing a session or connection in different threads. Be aware
that doing so can cause the following undesirable behaviors:

  * **Session state**

Sessions keep track of the current database, schema, and role. If one thread
changes these values (like USE DATABASE), the other thread might be affected.
This impact is particularly important because changing to another schema with
the same tables might cause a thread to accidentally modify the wrong table.
Additionally, changing connection or configuration parameters in one session
can affect all threads that use that session.

  * **Transaction state**

A transaction might start in one session. If multiple threads have access to
that session, each one can potentially modify data in the same transaction,
which might cause the data to be accidentally persisted or lost if a
transaction is committed or rolled back.

  * Sequence counter

Drivers use a sequence counter to retry requests. Because sequence counters
are global for a session, reusing a session in different threads might also
inadvertently alter the global sequence counter that can result in
unpredictable behavior for retrying requests.

  * **Query context cache**

For improved performance, sessions keep track of some internal information in
a driver-specific or internal cache. The cache updates after every query, so
running multiple queries concurrently in a session could result in data
corruption.

  * **Last query ID**

Connections keep track of the last query ID, which can then be retrieved and
used. If two queries run in parallel in different threads, a race condition
can affect which one sets the last query ID.

## Snowflake recommendations¶

  * Use connection pools when possible.

If you reuse connections across threads to avoid authenticating frequently,
you should consider using connection pools. Using connection pools decreases
the number of authentication requests, because the session is not closed at
the end—it’s just returned to a pool where it’s ready to be used for the next
occasion. Even when using connection pools, your application must be careful
not to alter or reset parameters that affect only a specific query or a
current database. Also, the application is responsible for committing or
aborting active transactions before returning a connection to the connection
pool.

  * Use asynchronous queries cautiously.

Starting multiple asynchronous queries at the same time on a single
connection, or starting a synchronous query while an asynchronous query is
still in progress, can result in a race condition that might cause
unpredictable results.

  * Use additional authentication optimizations.

Specific drivers support some or all of the following optimizations that you
can use to improve authentication performance:

    * SSO token caches

    * MFA token caches

    * Tokens in TOML configuration files

    * Custom token accessors

You should check the driver documentation to see which of these options the
driver supports.

  * Disable query context caching.

If you’re aware of all of the issues associated with reusing sessions and
connections in multiple threads, but still want to use them, Snowflake
recommends that you disable query caching by setting the
`DisableQueryContextCache` parameter to `false` in the connection definition.


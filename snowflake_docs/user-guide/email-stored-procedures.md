# Using SYSTEM$SEND_EMAIL to send email notifications¶

Note

All Snowflake customers can send email messages using this feature. Email
messages sent from the Notifications System Stored Procedure are processed
through Snowflake’s Amazon Web Services (AWS) deployments, using AWS Simple
Email Service (SES). The content of an email message sent using AWS may be
retained by Snowflake for up to thirty days to manage the delivery of the
message. After this period, the message content is deleted.

This topic explains how to use the built-in [SYSTEM$SEND_EMAIL](../../sql-
reference/stored-procedures/system_send_email) stored procedure to send email
notifications.

## Introduction¶

This feature uses the [notification integration](email-
notifications.html#label-create-email-notification-integration) object, which
is a Snowflake object that provides an interface between Snowflake and third-
party services (e.g. cloud message queues, email, etc.).

## Sending an email notification¶

Before you send a notification, you must have a notification integration that
you will use to send the notification. You must also validate the email
addresses of the recipients. For details, see [Notifications in
Snowflake](about-notifications).

To send the email notification, call the [SYSTEM$SEND_EMAIL](../../sql-
reference/stored-procedures/system_send_email) stored procedure.

For example, to use the notification integration `my_email_int` to send an
email message with the subject line “Email Alert: Task A has finished.” to
`first.last@example.com` and `first2.last2@example.com`, execute the following
statement:

    
    
    CALL SYSTEM$SEND_EMAIL(
        'my_email_int',
        'first.last@example.com, first2.last2@example.com',
        'Email Alert: Task A has finished.',
        'Task A has successfully finished.\nStart Time: 10:10:32\nEnd Time: 12:15:45\nTotal Records Processed: 115678'
    );
    

Copy

Note

If you set the ALLOWED_RECIPIENTS property of the notification integration,
and any email address in the recipient list is not on that list, no email
notifications are sent.

If you are on the Amazon Web Services (AWS) cloud platform, then the email
notification message is sent from `no-reply@snowflake.net`. If you are on the
Google Cloud Platform (GCP) or Microsoft Azure (Azure) cloud platform, the
email notification message is sent from `do-not-reply@snowflake.net`.


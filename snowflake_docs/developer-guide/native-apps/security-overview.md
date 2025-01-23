# Security requirements and guidelines for a Snowflake Native App¶

[![Snowflake logo in black \(no text\)](../../_images/logo-snowflake-
black.png)](../../_images/logo-snowflake-black.png) Feature — Generally
Available

The Snowflake Native App Framework is generally available on supported cloud
platforms. For additional information, see [Support for private connectivity,
VPS, and government regions](limitations.html#label-native-apps-supported-
clouds).

This topic provides an overview of the security requirements and guidelines
when developing a Snowflake Native App. It also provides general information
about automated security scan and review process when publishing an app to
consumers.

Caution

It is your responsibility to ensure that no personal data, sensitive data,
export-controlled data, or other regulated data is entered into any files
included in your application package.

## Overview of Snowflake Native App security requirements¶

The Snowflake Native App Framework provides security requirements and best
practices that providers must follow when developing a Snowflake Native App.
For security requirements and best practices for an app, see [Security
requirements and best practices for a Snowflake Native App](security-app-
requirements). For security requirements for an app with containers, see
[Secure a Snowflake Native App with Snowpark Container Services](security-na-
spcs).

To publish an app to consumers, either as a private listing or on the
Snowflake Marketplace, Snowflake implements a security review process that
requires a security scan of the components of an app. If an app does not pass
the automated security review, a manual review occurs.

All apps that are published to consumers must pass this security review.

## Potential security risks¶

The following are some of the possible security risks that can occur when
running an app:

  * Data exfiltration:

Malicious apps could copy consumer data to external functions or logs.

  * Compute abuse:

Apps could perform unauthorized tasks, such as cryptomining, at the consumer’s
expense.

  * Ransomware

Apps could encrypt or corrupt consumer data, demanding payment for
restoration.

  * Privilege escalation:

Apps could attempt to gain unauthorized permissions within the consumer’s
account.

To mitigate these and other possible security risks, the Snowflake Native App
Framework uses a security review to evaluate an app for security risks and to
ensure security best practices.

## Automated security reviews¶

To mitigate potential security risks, Snowflake uses the Native App Anti-Abuse
Pipeline Service (NAAAPS). This service automatically scans all new app
versions using various tools to determine if an app can be distributed to
consumers.

This automated security review occurs when a new version or patch of an app is
created. This review performs the following:

  * Copies the app to a dedicated Snowflake account used to scan apps.

  * Scans the files associated with the app and updates the security review status.

  * Auto-approves the app or initiates a manual review of the app.

Snowflake sends out automatic rejection notifications to reduce the time a
provider must wait for a response. During the manual review process, an app
can be approved or rejected.

## Scanners and tools used during a security review¶

The automated security review uses the following scanners and tools to perform
the following to analyze different components of an app:

  * Scan code for bugs, anti-patterns, and security vulnerabilities in code.

  * Scan code for malware.

  * Identify vulnerabilities in app dependencies.

The processes help detect various security issues, such as data exfiltration,
ransomware, compute abuse, privilege escalation, and dynamic code execution.

## Security requirements and best practices for an app¶

All apps must conform to the security requirements outlined in the [Security
requirements and best practices for a Snowflake Native App](security-app-
requirements).

Note

Security requirements are subject to change as Snowflake continues to monitor
new potential risks.

## Security considerations for a Snowflake Native App with Snowpark Container
Services¶

For information about additional security requirements for a Snowflake Native
App with Snowpark Container Services see [Secure a Snowflake Native App with
Snowpark Container Services](security-na-spcs).

## Guidelines for publishing an app to the Snowfalke Marketplace¶

When publishing an app to the Snowflake Marketplace, providers must consider
additional requirements and best practices. See [Guidelines for publishing an
app to the Snowflake Marketplace](publish-guidelines).

## CVE evaluation criteria for an app¶

Snowflake’s approach to addressing Common Vulnerabilities and Exposures (CVEs)
in a Snowflake Native App is based on our CVE Evaluation Criteria, a policy
that establishes clear and objective criteria for evaluating and prioritizing
CVEs based on their risk profile.

The policy aims to balance the mitigation of critical security risks with the
effort required to address less severe vulnerabilities. It applies to all apps
undergoing security review and is enforced to ensure only apps meeting the
defined criteria are approved for publishing in Snowflake’s data cloud
environment.

See [Common Vulnerabilities and Exposures (CVE) considerations](security-cve)
for additional information.

## Scanning Regions¶

When configuring a Snowflake Native App to be shared externally, providers
automatically share the code in app with Snowflake for scanning. The following
table maps the NAAAPS scanning regions to the corresponding provider regions:

Cloud provider | Provider region | Scanning region  
---|---|---  
AWS | US West (Oregon) | US West (Oregon)  
AWS | US East (Ohio) | US East (Ohio)  
AWS | US East (N. Virginia) | US East (N. Virginia)  
AWS | Canada (Central) | Canada (Central)  
AWS | South America (São Paulo) | South America (São Paulo)  
AWS | EU (Ireland) | EU (Ireland)  
AWS | Europe (London) | Europe (London)  
AWS | EU (Paris) | EU (Paris)  
AWS | EU (Frankfurt) | EU (Frankfurt)  
AWS | EU (Zurich) | EU (Zurich)  
AWS | EU (Stockholm) | EU (Stockholm)  
AWS | Asia Pacific (Tokyo) | Asia Pacific (Tokyo)  
AWS | Asia Pacific (Osaka) | Asia Pacific (Osaka)  
AWS | Asia Pacific (Seoul) | Asia Pacific (Seoul)  
AWS | Asia Pacific (Mumbai) | Asia Pacific (Mumbai)  
AWS | Asia Pacific (Singapore) | Asia Pacific (Singapore)  
AWS | Asia Pacific (Sydney) | Asia Pacific (Sydney)  
AWS | Asia Pacific (Jakarta) | Asia Pacific (Jakarta)  
Azure | 

  * West US 2 (Washington)
  * Central US (Iowa)
  * South Central US (Texas)
  * East US 2 (Virginia)
  * Canada Central (Toronto)

| Azure East US 2 (Virginia)  
Azure | 

  * UK South (London)
  * North Europe (Ireland)
  * West Europe (Netherlands)
  * Switzerland North (Zurich)
  * UAE North (Dubai)

| Azure West Europe (Netherlands)  
Azure | 

  * Central India (Pune)
  * Japan East (Tokyo)
  * Southeast Asia (Singapore)
  * Australia East (New South Wales)

| Azure Australia East (New South Wales)  
GCP | 

  * US Central1 (Iowa)
  * US East4 (N. Virginia)
  * Europe West2 (London)
  * Europe West4 (Netherlands)

| AWS US West (Oregon)


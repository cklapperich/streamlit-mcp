# Snowflake Releases¶

Snowflake is committed to providing a seamless, always up-to-date experience
for our users while also delivering ever-increasing value through rapid
development and continual innovation.

To meet this commitment, we deploy new releases each week. This allows us to
regularly deliver service improvements in the form of new features,
enhancements, and fixes. The deployments happen transparently in the
background; users experience no downtime or disruption of service, and are
always assured of running on the most-recent release with access to the latest
features.

This topic describes the process we follow for weekly releases, including the
option to request 24-hour early access for Enterprise Edition and higher
accounts to enable additional release testing (if desired).

## Release Types (Weekly)¶

Each week, Snowflake deploys two planned/scheduled releases:

Full release:

    

A full release may include any of the following:

  * New features

  * Feature enhancements or updates

  * Fixes

  * Behavior changes (see next section in this topic)

In addition, a full release includes updated Snowflake release notes
documentation per weekly cycle. See [Snowflake weekly, Snowsight, and feature
release notes](../release-notes/new-features).

Full releases may be deployed on any day of the week, except we typically do
not plan full releases on Friday to mitigate against issues that may be
encountered during off-hours.

Patch release:

    

A patch release includes fixes only. Note that the scheduled/planned patch
release for a given week may be canceled if the full release for the week is
sufficiently delayed or prolonged.

Additionally, patch releases are deployed (as needed) during or after the
completion of the full release to address any issues that are encountered.

## Behavior Changes (Monthly)¶

Each month (except for November and December), Snowflake selects one of the
weekly full releases for the month to introduce behavior changes. The weekly
release selected for the behavior changes may vary, but is typically the 3rd
or 4th release for the month.

A behavior change is defined as any change to existing behavior that returns
different results from before and may impact customer code or workloads.
Behavior changes are provided in bundles that utilize the following naming
convention:

`YYYY_NN`

Where `YYYY` is the year and `NN` is the ordinal number of the release within
the year. For example, `2022_06` would be the 6th behavior change bundle
introduced in 2022.

For more details, see [Behavior change management](../release-notes/bcr-
bundles/managing-behavior-change-releases).

### Bundle Lifecycle¶

The behavior change bundle lifecycle consists of the following two periods:

Testing period (1st month):

    

The bundle is introduced “Disabled by Default”. During this period, you can
choose to _enable_ the bundle in one or more accounts. Typically, you would
choose accounts designated for development or QA (quality assurance) so that
you can test the changes without impacting your production accounts.

Opt-out period (2nd month):

    

The bundle moves from “Disabled by Default” to “Enabled by Default”. During
this period, you can choose to _disable_ the bundle in your accounts. This
allows you to postpone the changes in the bundle, typically for production
accounts, while making any necessary adjustments to mitigate the impact of the
changes.

During these two periods, Snowflake does not override the setting for a given
bundle. For example, if you disable a bundle during the testing period, we do
not enable it at the beginning of the opt-out period.

At the end of the opt-out period, Snowflake enables the behavior changes in
the bundle across all accounts, at which time the bundle is considered
“Generally Enabled”. From this time onwards, you cannot enable or disable the
bundle. However, you can still request to temporarily disable individual
behavior changes in the bundle by contacting [Snowflake
Support](https://docs.snowflake.com/user-guide/contacting-support).

### Behavior Change Documentation¶

A release that contains behavior change bundles includes the following
documentation (in addition to the Release Notes for the release):

  * A listing of upcoming and recently implemented bundled changes. See [Behavior change log](../release-notes/behavior-changes).

  * A description of each behavior change. Behavior changes are listed on the landing page for each bundle.

  * A listing of upcoming and recently implemented unbundled changes. See [Unbundled Behavior Changes](../release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes).

## Pre-release Testing/Validation¶

At Snowflake, release quality is a top priority. Before each release is
deployed, it goes through a full suite of validation tests that include:

  * Regular build testing.

  * Continuous workload and performance testing.

In addition, before any customer accounts are moved to a release, the
following validation is performed:

  * Full round of regression testing in internal accounts across all supported cloud platforms.

  * Simulating execution of select impacted customer workloads (e.g. queries on customer data), with a focus on workloads that are most likely impacted by changes in the release.

## Staged Release Process¶

Once a full release has been deployed, Snowflake does not move all accounts to
the release at the same time. Accounts are moved to the release using a three-
stage approach over multiple days. Accounts are moved to the full release in
the following order, based on their [Snowflake Edition](intro-editions):

Day 1:

    

Stage 1 (_early access_) for designated Enterprise (or higher) accounts.

Day 1 or 2:

    

Stage 2 (_regular access_) for Standard accounts.

Day 2:

    

Stage 3 (_final_) for Enterprise (or higher) accounts.

Typically, the minimum amount of time between the early access and final
stages is 24 hours, but it may be shorter or longer. This staged approach
enables Snowflake to monitor activity as accounts are moved and respond to any
issues that may occur. It also enables designating Enterprise accounts for
early access testing (see the next section in this topic).

Note

This staged approach only applies to full releases. For patch releases, all
accounts are moved on the same day.

In addition, if issues are discovered while moving accounts to a full release
or patch release, the release may be halted or rolled back. In most cases, the
follow-up to a halted/rolled-back release is completed within 24-48 hours.

## Early Access to Full Releases¶

[![Snowflake logo in black \(no text\)](../_images/logo-snowflake-
black.png)](../_images/logo-snowflake-black.png) [Enterprise Edition
Feature](intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about
upgrading, please contact your Snowflake account representative.

If you have multiple Enterprise Edition (or higher) accounts, you can
designate one or more of these accounts as early access to take advantage of
the period between the early access and final stages for full releases. This
can be particularly useful if you maintain separate accounts for
development/testing and production.

To designate an account for early access, please contact your Snowflake
account representative.

Once you have designated an account for early access, you can implement a
testing framework similar to the following:

  1. Use [CURRENT_VERSION](../sql-reference/functions/current_version) (or a UDF that returns similar results) to verify when your early access account is on the full release.

  2. Use your early access accounts to test your production workloads against the full release.

  3. If any issues are encountered, notify [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support), who can work with you to prevent the issues from disrupting your other accounts.

Tip

Early access is not required or recommended for all organizations with
Enterprise Edition accounts. Snowflake’s rigorous release testing and
monitoring during deployments is usually sufficient to prevent most issues.
Early access is intended primarily for organizations that desire added
certainty that their production accounts will not be affected by full
releases.


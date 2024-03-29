Version History
***************


0.4.0 - Reworked Clause Validation
==================================
* Expanded/reworked handling of clauses and validation, to hopefully be much
  more user-friendly.

    * That is, creating clauses with py-dbcn should now feel much more natural,
      with most extraneous escape character requirements removed.
    * Previously, this was a problem particularly with quotation characters,
      depending on the database engine. Now this should be handled much more
      uniformly regardless of engine.
    * This will receive further refining in the future, but it's a big step
      up from original handling.

* If any validation gives issues, each clause type can have validation
  turned off via passing in the associated bool (value False) on constructing
  the connector class.

    * Clauses validation turned off this way will be entered as raw string into
      the query.


0.3.1 - Bugfix Release
======================
* Various general bugfixes.


0.3.0 - Stable PostgreSQL Querying
==================================

* **MySQL** and **PostgreSQL** are both implemented and thoroughly tested. Both
  databases implement the following query types (at each of the
  Database/Table/Record levels, where appropriate):

    * CREATE
    * SHOW
    * DESCRIBE
    * USE
    * SELECT
    * INSERT
    * INSERT MANY
    * UPDATE
    * UPDATE MANY
    * DELETE
    * TRUNCATE

* Basic aggregation functions have been confirmed to work in both database
  types.
* Syntax to call either database from this package is the same. Aka, goal of
  being database-agnostic is currently being met.
* Query validation logic is in a better state than version 0.2.0, but still not
  as robust as desired.
* Documentation describes most relevant end-user functionality. But is still not
  100% complete as of writing this.


0.2.0 - Stable MySQL Querying
=============================

* **MySQL** connections have been more thoroughly tested, and project
  setup/syntax is considered generally stable.

    * **PostgreSQL** connections have been started, but are incomplete.

* Added basic output coloring and output show/hide args.
* Query validation logic could still use work, but is partially implemented.
* Has been tested in a live project and seems to have desired functionality,
  so long as queries are fairly basic (only basic SHOW/SELECT/UPDATE/DELETE).
  These queries have been implemented for each of Database/Table/Record level.


0.1.0 - Initial Release
=======================

* First release.
* Very much WIP and subject to change.
* Minimal functionality.
* Not recommended for import/use in a live production project.

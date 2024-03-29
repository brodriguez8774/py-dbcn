Creating Queries
****************

The main purpose of ``py-dbcn`` is to create some kind of database queries
to read from or manipulate one or more database.
The syntax is meant to be as intuitive as possible, with the package taking
care of as much work as it can, behind the scenes.

For example, when providing quotes to a value, the quote type does not matter.
``Py-dbcn`` will automatically convert the quotes to the expected type,
depending on the database used. All of [", ', `] will be treated equally.

For now, the ``py-dbcn`` package only provides basic database calls, and these
are provided on the :ref:`database <database querying>`,
:ref:`table <table querying>`, and :ref:`record <record querying>` levels.


.. note::

    When applicable, these interface methods provide a result that makes sense
    for the given query type. The intention is to allow further Pythonic logic
    to be run, if desired. If nothing else, it allows for verifying the query
    result in whatever way desired.

    For methods that return ``None``, it is safe to assume the query will either
    succeed, or return a Python error.


.. important::

    While not fully implemented yet, the intention is to also have full, dynamic
    validation of all values provided to these interface methods.

    In the future, the ``py-dbcn`` package will do what it can to auto-format
    and auto-correct common mistakes in provided syntax. When it can't correct,
    it will return a descriptive error that explains the problem, before the
    query ever hits the database itself.


Database Querying
=================

All database-level querying is done via the ``connector.database`` interface.


SHOW Existing Databases
-----------------------

``connector.database.show()``

:return: A list of all found databases.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    list_of_databases = connector.database.show()

    # Print list of databases.
    for database in list_of_databases:
        print(database)


Display current Database
------------------------

``connector.database.select()``

``connector.database.current()``

:return: Str of currently selected database name.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    current_db = connector.database.select()

    # Print name of current database.
    print(current_db)


USE a different Database
------------------------

``connector.database.use(db_name)``

:param db_name: Name of database to change to.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    connector.database.use('test_db')


CREATE a new Database
---------------------

``connector.database.create(db_name)``

:param db_name: Name of database to create.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    connector.database.create('a_new_database')


DELETE an existing Database
---------------------------

``connector.database.delete(db_name)``

``connector.database.drop(db_name)``

:param db_name: Name of database to delete.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    connector.database.drop('an_old_database')


Table Querying
==============

All table-level querying is done via the ``connector.table`` interface.


SHOW Existing Tables
--------------------

``connector.tables.show()``

:return: A list of all found tables in currently selected database.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    list_of_tables = connector.tables.show()

    # Print list of tables.
    for table in list_of_tables:
        print(table)


DESCRIBE existing Table
-----------------------

``connector.tables.describe(table_name)``

:param table_name: Name of table to describe.

:return: A list of all columns in table, including several useful attributes.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    list_of_columns = connector.tables.describe('my_table')

    # Print list of table columns.
    for column in columns:
        print(column)


CREATE a new Table
------------------

``connector.tables.create(table_name, table_columns)``

:param table_name: Name of table to create.

:param table_columns: The columns to provide the new table.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    connector.tables.create(
        'a_new_table',
        """
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(100),
        description VARCHAR(100),
        PRIMARY KEY ( id )
        """,
    )


UPDATE an existing Table
------------------------

``connector.tables.update(table_name, table_columns)``

``connector.tables.modify(table_name, table_columns)``

:param table_name: Name of table to create.

:param modify_clause: The type of modification to make. IE: One of
                      [ADD, DROP, MODIFY].

:param column_clause: The columns to modify.

:return: None


TODO: Create examples and expand modify logic. Maybe not fully implemented?


DROP an existing Table
------------------------

``connector.tables.drop(table_name)``

``connector.tables.delete(table_name)``

:param table_name: Name of table to remove.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    connector.tables.drop('old_table')


COUNT records present in table
------------------------------

``connector.tables.count(table_name)``

:param table_name: Name of table to count records of.

:return: A count of records present in table.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    record_count = connector.tables.count('my_table')

    # Print number of records found.
    print(record_count)


Record Querying
===============

All record-level querying is done via the ``connector.record`` interface.


SELECT a set of Records
-----------------------

``connector.records.select(table_name, select_clause=None, where_clause=None, order_by_clause=None, limit_clause=None)``

:param table_name: Name of table to select records from.

:param select_clause: Optional clause to limit the number of columns that return
                      for each record. If not provided, ``*`` wildcard selector
                      is used.

                      Can be in format of a list, or comma separated str.

:param where_clause: Optional clause to limit number of records selected. If
                     not provided, then all records are selected.

:param order_by_clause: Optional clause to indicate the desired ordering of
                        returned records.

:param limit_clause: Optional clause to limit query scope via number of records
                     returned.

:return: A list of all returned records.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    # In this case, we only pull "id", "name", and "description" columns from
    # all records with an "id" less than 500. We then sort by descending name,
    # and then ascending id. Finally, we limit to the first 100 records.
    results = connector.records.select(
        'my_table',
        select_clause='id, name, description',
        where_clause='id < 500',
        order_by_clause='name DESC, id',
        limit_clause=100,
    )

    # Print list of pulled records.
    for record in results:
        print(record)


INSERT new Records
------------------

INSERT single Record
^^^^^^^^^^^^^^^^^^^^

``connector.records.insert(table_name, values_clause, columns_clause=None)``

:param table_name: Name of table to select records from.

:param values_clause: Clause to provide values for new record.

:param columns_clause: Optional clause to indicate what columns are being
                       provided, as well as what order they're in. If not
                       present, then query will assume all columns are being
                       provided, in the order they were originally added to the
                       table.

:return: TODO: Honestly unsure of what this provides. Probably empty array?
        Double check.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    # In this case, we insert a record by giving a "name" and "description".
    # We omit "id" so it will be auto-provided (assuming it's a field with
    # some kind of reliable default value).
    connector.records.insert(
        'my_table',
        "Regal Red Towel", "Red towel with yellow embroidery."',
        columns_clause='name, description',
    )


INSERT multiple Records
^^^^^^^^^^^^^^^^^^^^^^^

``connector.records.insert_many(table_name, values_clause, columns_clause=None)``

:param table_name: Name of table to select records from.

:param values_clause: Clause to provide values for new record(s).

:param columns_clause: Optional clause to indicate what columns are being
                       provided, as well as what order they're in. If not
                       present, then query will assume all columns are being
                       provided, in the order they were originally added to the
                       table.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Generate new record values.
    rows = [
        ('Blue Towel', 'Soft blue towel.'),
        ('Red Towel', 'Soft red towel.'),
        ('Regal Red Towel', 'Red towel with yellow embroidery.'),
    ]

    # Run query.
    # In this case, we insert records by giving a set of "name"s and "description"s.
    # We omit "id" so it will be auto-provided (assuming it's a field with
    # some kind of reliable default value).
    connector.records.insert_many(
        'my_table',
        rows,
        columns_clause='name, description',
    )


UPDATE existing Records
-----------------------

UPDATE Single Record
^^^^^^^^^^^^^^^^^^^^

``connector.records.update(table_name, values_clause, where_clause)``

:param table_name: Name of table to update records within.

:param values_clause: Clause to provide values for updated record.

:param where_clause: Clause to limit number of records selected.

                     Due to the nature of this query, where clause is mandatory
                     BUT if an empty string is provided, then the query will
                     still select all records.

:return: Returns set of all updated values.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    # In this case, we insert a record by giving a "name" and "description".
    # We omit "id" so it will be auto-provided (assuming it's a field with
    # some kind of reliable default value).
    connector.records.update(
        'my_table',
        'description = "Refurbished item"',
        'name = "Refurbished"',
    )


UPDATE Multiple Records
^^^^^^^^^^^^^^^^^^^^^^^

``connector.records.update_many(table_name, columns_clause, values_clause, where_columns_clause)``

:param table_name: Name of table to update records within.

:param columns_clause: Clause to indicate what columns are being provided, as
                        well as what order they're in.

:param values_clause: Clause to provide values for updated record.

                    Columns indicated in the below ``where_columns_clause``
                    should match values already present in the database.

                    All other columns will update to the new values provided
                    here.

:param where_columns_clause: NOT the standard WHERE clause used in other queries.

                            Clause to indicate what columns are being filtered
                            on. All columns present here should also be present
                            in the ``columns_clause`` param.

:param column_types_clause: Optional clause to provide type hinting to column
                            types.

                            Can be skipped when all columns are basic types,
                            such as text or integer.

:return: None


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Columns to update with/on.
    columns_clause = ['id', 'name']

    # Type hinting for columns.
    # Note: This is NOT required in this instance, and only shown here for
    # example. But this IS required in instances with more complicated data
    # types, such as dates or timestamps.
    column_types_clause = ['integer', 'varchar(200)']

    # Desired values after query runs.
    # Note: In this case, we match on "id" by including it in the
    # WHERE clause. Meanwhile, the "name" field is not included in the
    # WHERE, so this field is set to the desired update value. Any fields
    # that are not used to match/update should be excluded.
    values_clause = [
        # (id, name)
        (1599, 'Refurbished Item 1001'),
        (16782, 'Refurbished Item 1002'),
        (20909, 'Refurbished Item 1003'),
    ]

    # Columns to use to find existing record data.
    where_columns_clause = ['id']

    # Run query.
    # In this case, we update record "name" values, using the id to match
    # against existing records.
    connector.records.update(
        'my_table',
        columns_clause,
        values_clause,
        where_columns_clause,
        column_types_clause=column_types_clause,
    )


DELETE existing Records
-----------------------

``connector.records.delete(table_name, where_clause)``

:param table_name: Name of table to delete records from.

:param where_clause: Clause to limit number of records selected.

                     Due to the nature of this query, where clause is mandatory
                     BUT if an empty string is provided, then the query will
                     still select all records.

:return: TODO: Honestly unsure of what this provides. Double check.


Example:

.. code-block:: python

    # Import MySQL connector.
    from py_dbcn.connectors import MysqlDbConnector

    ...

    # Initialize MySQL database connection.
    connector = MysqlDbConnector(host, port, user, password, db_name)

    # Run query.
    connector.records.delete(
        'my_table',
        where_clause='name = "Refurbished"',
    )

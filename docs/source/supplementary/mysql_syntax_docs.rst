MySQL Syntax
************

Here is supplementary documentation of basic `MySQL <https://www.mysql.com/>`_
syntax, to help with using the ``py-dbcn`` package.


Quote Formatting
================
While not strictly necessary for the ``py-dbcn`` package, we document the
expected quote formatting types here:

* ````` - Column Quote Format - Used for quoting around table column names.
* ````` - Identifier Quote Format - Used for quoting around identifiers, such
  as SELECT clause field id's.
* ``"`` - Str Literal Quote Format - Used for quoting around literal strings.


Clause Formatting
=================

Below documents various clauses that are used in different query types.
Each of these clauses acts as a subsection of a larger query statement.

SELECT IDENTIFIER Clause
------------------------

Used to indicate the desired columns to return in a SELECT clause.

Can either use the wildstar character `*` to return all columns, or use syntax
for a :ref:`columns-clause`_, described below.


WHERE Clause
------------

Used to limit the selection of records for a given query.


General Syntax:

.. code-block:: sql

    WHERE <column_name> <expression> <value>


Ex:

.. code-block:: sql

    SELECT * FROM my_table
    WHERE my_column > 50;


This can be chained with `AND` s or `OR` s:

.. code-block:: sql

    SELECT * FROM my_table
    WHERE my_column == 0 OR (my_column > 50 AND my_column < 75);


COLUMNS Clause
--------------

Indicates one or more columns to reference for a given query, separated by
commas.


General Syntax:

.. code-block:: sql

    <column_1>, <column_2>, ..., <column_n>


Ex:

.. code-block:: sql

    SELECT id, name, description FROM my_table;


VALUES Clause
-------------

Used to provide values for a given record.

Should have one value provided per column being referenced.


.. code-block:: sql

    VALUES (<value_1>, <value_2>, ..., <value_n>)


Ex:

.. code-block:: sql

    INSERT INTO my_table (id, name, description)
    VALUES (5, "Red Towel", "A red linen towel.");


ORDER BY Clause
---------------

Used to reorder values within a given query.

One or more columns can be provided, and each column can have the `ASC` or
`DESC` keywords, to denote "ascending order" or "descending order" respectively.

If no keyword is provided for a column, then it defaults to ascending.


.. code-block:: sql

    ORDER BY <column_1> ASC|DESC, <column_2> ASC|DESC, ..., <column_n> ASC|DESC


Ex:

.. code-block:: sql

    SELECT * FROM my_table
    ORDER BY name DESC, id ASC;


LIMIT Clause
------------

Used to limit the number of returned records in a given query.

Queries with larger numbers of records will run slower and may be too many to
properly display on the screen.


.. code-block:: sql

    LIMIT <positive_integer>


Ex:

.. code-block:: sql

    SELECT * FROM my_table
    LIMIT 100;


Database Query Formatting
=========================


Table Query Formatting
======================


Record Query Formatting
=======================


See also:
https://sphinx-tabs.readthedocs.io/en/latest/

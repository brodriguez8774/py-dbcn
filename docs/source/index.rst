Pythonic Database Connector
===========================

The **Pythonic Database Connector** package (aka **py-dbcn**) is a
connector to allow Pythonic interaction with multiple database types.

The main original purpose of this package is to allow for an easier way to
read in and migrate data between databases, such as during a database upgrade.

The idea is to create a package that allows quick and easy interfacing to
the database of choice, using a simple Pythonic interface.
No need to necessarily know the quirks of each database type, as long as you
have a general idea of what database logic is required.
This package will handle the details from there.

Due to being written in Python, this package allows having a easily-repeatable
set of database calls, which can be thoroughly tested and examined via the
standard Python library, to ensure maximum database integrity at every step of
the way.


.. note::
    Currently, this is only implemented for `MySQL <https://www.mysql.com/>`_
    and `PostgreSQL <https://www.postgresql.org/>`_.

    There are plans to at least implement this for
    `SqLite <https://www.sqlite.org/>`_ as well.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   creating_queries
   configuration

.. toctree::
   :maxdepth: 1
   :caption: Versions:

   roadmap
   version_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

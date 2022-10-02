Quickstart
**********

1. Load up your VirtualEnvironment of choice and run:

    .. code-block:: python

        pip install py-dbcn


    Alternatively, add ``py-dbcn`` to your respective project
    requirements file, and then follow the standard package installation method
    for your project
    (`requirements.txt <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_,
    `pipenv <https://pipenv.pypa.io/en/latest/>`_,
    `poetry <https://python-poetry.org/docs/>`_, etc).


2. Install your database connection of choice:

   The ``py-dbcn`` package does not inherently install the associated pip
   libraries for each database. This is so the local installation only installs
   the bare minimum needed for your specific use case.

   Use the below packages to connect to the database type of choice:

   * Python package for **MySQL**:

     .. code-block:: python

        mysqlclient

   * Python package for **PostgreSQL**:

     .. code-block:: python

        psycopg2-binary


3. Create a new Python project (or load an existing one) and establish one or
   more database connections. For example, to connect with **MySQL**:

    .. code-block:: python

        # Here we initialize a single MySQL connection.
        from py_dbcn.connectors import MysqlDbConnector

        # Import config values from some other file.
        from .settings import mysql_config

        ...

        connector = MysqlDbConnector(
            mysql_config['db_host'],
            mysql_config['db_port'],
            mysql_config['db_user'],
            mysql_config['db_user_password'],
            mysql_config['db_name'],
        )

    .. important::
        With the above code, we're specifically importing the database settings
        from some outside location. In this case, we import these values as
        a dictionary format.

        Depending on who can access this project and how it's stored, it's often
        much more secure to avoid committing database settings to the project.

        Instead, add some file to the project's ``.gitignore`` and read in
        config values from there. It can also be helpful to make an
        ``example_config.py`` file, to show the expected format of how these
        settings should be provided (but without committing the actual database
        credentials).


4. Optionally set up logging for ``py-dbcn``, in order to get additional
   helpful logging output.

   We recommend follow logging setup as discussed in the
   `Django Docs <>`_.
   Yes, this project doesn't require Django, but the Django docs provide
   thorough documentation for what we believe is the best Python logging format.

   Once logging is set up, add the ``py-dbcn`` package to your logging
   namespace, similar to shown:


   .. code-block:: python

        'loggers': {

            ...

            'py_dbcn': {
                'handlers': [<handlers_here>],
                'level': 'NOTSET',
            },
        }

   Where ``<handlers_here>`` is replaced by your project's actual logging
   handlers.


5. Install optional packages for extra functionality.

    This package offers support for the
    `colorama <https://pypi.org/project/colorama/>`_ Python package.

    Colorama is not necessary to use ``py-dbcn``, but adding it will provide
    helpful coloring output to log messages, to help separate what kind of
    calls are being made.


6. Run database queries as desired. See <link-here>.

    .. note::

        Closing the database is not necessary, as ``py-dbcn`` will automatically
        take care of it on program termination.

        However, if desired, you can still manually close the database
        connection mid-program.

        The ``py-dbcn`` library also has no built-in limitations. You are free
        to open and close as many simultaneous connections as you wish.

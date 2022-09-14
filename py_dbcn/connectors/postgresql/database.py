"""
Database section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.database import BaseDatabase
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlDatabase(BaseDatabase):
    """
    Logic for making queries directly on the database, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Database class.')

        # Initialize variables.
        self._show_databases_query = 'SELECT datname FROM pg_database;'
        self._current_database_query = 'SELECT current_database();'

    def use(self, db_name, display_query=True, display_results=True):
        """Selects given database for use.

        :param db_name: Name of db to use.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.database_name(db_name):
            raise ValueError('Invalid database name of "{0}".'.format(db_name))

        # Get list of valid databases.
        available_databases = self._get()

        # Check if provided database matches value in list.
        # Note that PostgreSQL is simultaneously "case-insensitive" but also somehow not?
        # As in, it supposedly will see MY_TABLE and my_table and read them as the same database name.
        # Yet at the same time, using the wrong case will raise a "database does not exist" error.
        # So here, we update our db_name to match the same case that PostgreSQL thinks it should be.
        # ( See https://www.postgresql.org/docs/current/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS )
        db_found = False
        for database in available_databases:
            if db_name.casefold() == str(database).casefold():
                db_name = database
                db_found = True
                break
        if not db_found:
            # Database does not exist. Raise error.
            raise ValueError(
                'Could not find database "{0}". Valid options are {1}.'.format(db_name, available_databases)
            )

        if display_query:
            self._base.display.query('Switching databases. No query to display. Recreating connection.')

        # Switch active database.
        # PostgreSQL is annoying in that it doesn't seem to have a friendly way to switch databases.
        # The only method seems to be by destroying the current connection and recreating a new one, this time
        # with the desired new database to use.
        self._base.close_connection()
        self._base.create_connection(db_name=db_name)
        if display_results:
            self._base.display.results('Database changed to "{0}".'.format(db_name))

    def drop(self, db_name, display_query=True, display_results=True):
        """Deletes database with provided name.

        :param db_name: Name of database to delete.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.database_name(db_name):
            raise ValueError('Invalid database name of "{0}".'.format(db_name))

        # Get list of valid databases.
        available_databases = self._get()

        # Check if provided database matches value in list.
        # Similar to use(), we need to get case-sensitive version.
        # See above for notes on that.
        db_found = False
        for database in available_databases:
            if db_name.casefold() == str(database).casefold():
                db_name = database
                db_found = True
                break
        if not db_found:
            # Database does not exist. Raise error.
            raise ValueError(
                'Could not find database "{0}". Valid options are {1}.'.format(db_name, available_databases)
            )

        # Remove database.
        # Note that PostgreSQL doesn't let us drop an active database.
        # So we need to check for that, and change to an arbitrary different database if so.
        switched_db = False
        if self._base._config.db_name.casefold() == db_name.casefold():
            # Using database that we're attempting to drop. Switch.
            new_db_name = ''
            for database in available_databases:
                # Find the first database that simply does not match the one we intend to drop.
                if db_name.casefold != str(database).casefold():
                    new_db_name = database
                    break
            self.use(new_db_name)
            switched_db = True

        query = 'DROP DATABASE {0};'.format(db_name)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Dropped database "{0}".'.format(db_name))

        # If we switched database, then immediately close connection at this point,
        # to avoid accidentally doing further manipulations on an arbitrary other database.
        if switched_db:
            self._base.close_connection()

"""
Database section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# Internal Imports.
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseDatabase:
    """
    Abstract/generalized logic, for making queries directly on the database.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Database class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

        # Initialize required class query variables.
        self._show_databases_query = None
        self._current_database_query = None

    def select(self, display_query=True):
        """Returns name of currently selected database.

        :param display_query: Bool indicating if query should output to console. Defaults to True.
        """
        if not self._current_database_query:
            raise ValueError('SELECT CURRENT DATABASE query is not defined.')

        results = self._base.query.execute(
            self._current_database_query,
            display_query=display_query,
        )[0][0].strip()

        return results

    def current(self, display_query=True):
        """Returns name of currently selected database.

        Alias for select().
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        """
        return self.select(display_query=display_query)

    def _get(self, display_query=False, display_results=False):
        """Gets list of all currently-available databases.

        :param display_query: Bool indicating if query should output to console. Defaults to False.
        :param display_results: Bool indicating if results should output to console. Used for "SHOW DATABASES" query.
        """
        if not self._show_databases_query:
            raise ValueError('SHOW DATABASES query is not defined.')

        # Generate and execute query.
        results = self._base.query.execute(self._show_databases_query, display_query=display_query)

        # Convert to more friendly format.
        formatted_results = []
        for result in results:
            formatted_results.append(result[0])
        results = formatted_results

        if display_results:
            self._base.display.results('results: {0}'.format(results))

        # Return data.
        return results

    def show(self, display_query=True):
        """Displays all databases available for selection.

        :param display_query: Bool indicating if query should output to console. Defaults to True.
        """
        return self._get(display_query=display_query, display_results=True)

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
        if db_name.casefold() not in (name.casefold() for name in available_databases):
            # Database does not exist. Raise error.
            raise ValueError(
                'Could not find database "{0}". Valid options are {1}.'.format(db_name, available_databases)
            )

        # Switch active database.
        query = 'USE {0};'.format(db_name)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Database changed to "{0}".'.format(db_name))

    def create(self, db_name, display_query=True, display_results=True):
        """Creates new database with provided name.

        :param db_name: Desired name of new database.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.database_name(db_name):
            raise ValueError('Invalid database name of "{0}".'.format(db_name))

        # Get list of valid databases.
        available_databases = self._get()

        # Check if provided database matches value in list.
        if db_name in available_databases:
            # Database already exists. Raise error.
            raise ValueError(
                'Could not find database "{0}". Valid options are {1}.'.format(db_name, available_databases)
            )

        # Create new database.
        query = 'CREATE DATABASE {0};'.format(db_name)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Created database "{0}".'.format(db_name))

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
        if db_name not in available_databases:
            # Database does not exist. Raise error.
            raise ValueError('Database with name "{0}" does not exist.'.format(db_name))

        # Remove database.
        query = 'DROP DATABASE {0};'.format(db_name)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Dropped database "{0}".'.format(db_name))

    def delete(self, db_name, display_query=True, display_results=True):
        """Alias for database "drop" function.

        :param db_name: Name of database to delete.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        self.drop(db_name, display_query=display_query, display_results=display_results)

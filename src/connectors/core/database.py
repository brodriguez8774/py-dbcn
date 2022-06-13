"""
Database section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


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

    def select(self):
        """Returns name of currently selected database."""
        return (self._base.query.execute(
            'SELECT DATABASE();',
            display_query=False,
        )[0][0]).strip()

    def current(self):
        """Returns name of currently selected database.

        Alias for select().
        """
        return self.select()

    def _get(self, show=False):
        """
        Gets list of all currently-available databases.
        :param show: Bool indicating if results should be printed to console or not. Used for "SHOW DATABASES" query.
        """
        # Generate and execute query.
        query = 'SHOW DATABASES;'
        results = self._base.query.execute(query)

        # Convert to more friendly format.
        formatted_results = []
        for result in results:
            formatted_results.append(result[0])
        results = formatted_results

        if show:
            logger.results('results: {0}'.format(results))

        # Return data.
        return results

    def show(self):
        """
        Displays all databases available for selection.
        """
        return self._get(show=True)

    def use(self, db_name):
        """
        Selects given database for use.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.database_name(db_name):
            raise ValueError('Invalid database name of "{0}".'.format(db_name))

        # Get list of valid databases.
        available_databases = self._get()

        # Check if provided database matches value in list.
        if db_name not in available_databases:
            raise ValueError(
                'Could not find database "{0}". Valid options are {1}.'.format(db_name, available_databases)
            )

        # Generate and execute query.
        query = 'USE {0};'.format(db_name)
        self._base.query.execute(query)
        logger.results('Database changed to "{0}".'.format(db_name))

    def create(self, db_name):
        """
        Creates new database with provided name.
        :param db_name: Desired name of new database.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.database_name(db_name):
            raise ValueError('Invalid database name of "{0}".'.format(db_name))

        # Get list of valid databases.
        available_databases = self._get()

        # Check if provided database matches value in list.
        if db_name in available_databases:
            # Database already exists. Raise error.
            raise ValueError('Database with name "{0}" already exists.'.format(db_name))

        # Create new database.
        query = 'CREATE DATABASE {0};'.format(db_name)
        self._base.query.execute(query)
        logger.results('Created database "{0}".'.format(db_name))

    def drop(self, db_name):
        """
        Deletes database with provided name.
        :param db_name: Name of database to delete.
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
        self._base.query.execute(query)
        logger.results('Dropped database "{0}".'.format(db_name))

    def delete(self, db_name):
        """
        Alias for database "drop" function.
        """
        self.drop(db_name)

"""
Core DB Connector class.
Should be inherited by language-specific connectors
"""

# System Imports.
from abc import ABC, abstractmethod

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class AbstractDbConnector(ABC):
    """
    Abstract connector for database and
    """
    @abstractmethod
    def __init__(self, debug=False):
        logger.debug('Generating (core) Connector class.')
        self.connection = None
        self._debug = debug

        # Create references to related subclasses.
        self.database = self._get_related_database_class()
        self.display = self._get_related_display_class()
        self.query = self._get_related_query_class()
        self.tables = self._get_related_tables_class()
        self.validate = self._get_related_validate_class()

    def __del__(self):
        """
        Close database connection on exit.
        """
        try:
            self.connection.close()
        except:
            pass

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return BaseDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return BaseDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return BaseQuery(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return BaseTables(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return BaseValidate(self)


class BaseDatabase():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Database class.')
        self._base = parent

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
            logger.info('results: {0}'.format(results))

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
        logger.info('Database changed to "{0}".'.format(db_name))


class BaseDisplay():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Display class.')
        self._base = parent


class BaseQuery():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Query class.')
        self._base = parent

    def execute(self, query):
        """"""
        logger.query(query)

        # Create connection and execute query.
        cursor = self._base.connection.cursor()
        cursor.execute(query)

        # Get results.
        results = cursor.fetchall()

        # Close connection.
        self._base.connection.commit()
        cursor.close()

        # Return results.
        if results is None:
            results = []
        return results


class BaseTables():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Query class.')
        self._base = parent

    def _get(self, show=False):
        """
        Gets list of all currently-available tables in database.
        :param show: Bool indicating if results should be printed to console or not. Used for "SHOW TABLES" query.
        """
        # Generate and execute query.
        query = 'SHOW TABLES;'
        results = self._base.query.execute(query)

        # Convert to more friendly format.
        formatted_results = []
        for result in results:
            formatted_results.append(result[0])
        results = formatted_results

        if show:
            logger.info('results: {0}'.format(results))

        # Return data.
        return results

    def show(self):
        """
        Displays all tables available in database.
        """
        return self._get(show=True)

    def describe(self, table_name):
        """
        Describes given table in database.
        """
        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided table matches value in list.
        if table_name not in available_tables:
            raise ValueError(
                'Could not find table "{0}". Valid options are {1}.'.format(table_name, available_tables)
            )

        # Generate and execute query.
        query = 'DESCRIBE {0};'.format(table_name)
        results = self._base.query.execute(query)
        logger.info('results: {0}'.format(results))


class BaseValidate():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Validate class.')
        self._base = parent

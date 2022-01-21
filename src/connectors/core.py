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
        logger.info('Database changed to "{0}".'.format(db_name))

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
            raise ValueError('Database with name "{0}" already exists'.format(db_name))

        # Create new database.
        query = 'CREATE DATABASE {0};'.format(db_name)
        self._base.query.execute(query)
        logger.info('Created database "{0}".'.format(db_name))

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
            raise ValueError('Database with name "{0}" already exists'.format(db_name))

        # Remove database.
        query = 'DROP DATABASE {0};'.format(db_name)
        self._base.query.execute(query)
        logger.info('Dropped database "{0}".'.format(db_name))

    def delete(self, db_name):
        """
        Alias for database "drop" function.
        """
        self.drop(db_name)


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

    def create(self, table_name, table_columns):
        """
        Creates new table with provided name.
        :param table_name: Desired name of new table.
        :param table_columns: Column values for new table.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided columns are valid format.
        orig_table_columns = table_columns
        table_columns = self._base.validate.table_columns(table_columns)
        if table_columns is None:
            raise ValueError('Invalid table columns of "{0}"'.format(orig_table_columns))

        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided table matches value in list.
        if table_name in available_tables:
            # Table already exists. Raise error.
            raise ValueError('Table with name "{0}" already exists'.format(table_name))

        # Create new table.
        # raise NotImplemented('Function needs column-definition handling.')
        query = 'CREATE TABLE {0} {1};'.format(table_name, table_columns)
        self._base.query.execute(query)
        logger.info('Created table "{0}".'.format(table_name))

    def drop(self, table_name):
        """
        Deletes table with provided name.
        :param table_name: Name of table to delete.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided tables matches value in list.
        if table_name not in available_tables:
            # Table does not exist. Raise error.
            raise ValueError('Table with name "{0}" already exists'.format(table_name))

        # Remove table.
        query = 'DROP TABLE {0};'.format(table_name)
        self._base.query.execute(query)
        logger.info('Dropped table "{0}".'.format(table_name))

    def delete(self, table_name):
        """
        Alias for table "drop" function.
        """
        self.drop(table_name)


class BaseValidate():
    """

    """
    def __init__(self, parent):
        logger.debug('Generating related (core) Validate class.')
        self._base = parent

    def database_name(self, name):
        """
        Validates that provided database name uses set of acceptable characters.
        :param name: Potential name of database to validate.
        :return: True if name is valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def table_name(self, name):
        """
        Validates that provided table name uses set of acceptable characters.
        :param name: Potential name of table to validate.
        :return: True if name is valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def table_columns(self, columns):
        """
        Validates that provided column values match expected syntax.
        :param columns: Str or dict of columns to validate.
        :return: True if columns are valid | False otherwise.
        """
        # Add parenthesis if either side is missing them.
        if columns[0] != '(' or columns[-1] != ')':
            columns = '(' + columns + ')'

        # For now, always return as valid.
        return columns

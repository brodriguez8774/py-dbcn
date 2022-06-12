"""
Table section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseTables:
    """
    Abstract/generalized logic, for making table queries.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Query class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

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
            self._base.display.tables._get(results, logger)

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

        return results

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

    def count(self, table_name):
        """
        Returns number of all records present in provided table.
        :param table_name: Name of table to count.
        """
        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided table matches value in list.
        if table_name not in available_tables:
            raise ValueError(
                'Could not find table "{0}". Valid options are {1}.'.format(table_name, available_tables)
            )

        # Count records in table.
        result = self._base.query.select(table_name, 'COUNT(*)')
        result = result[0][0]

        return result

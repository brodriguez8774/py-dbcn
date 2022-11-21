"""
Query section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# Internal Imports.
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseQuery:
    """
    Abstract/generalized logic, for making row queries.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Query class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

    def execute(self, query, data=None, display_query=True):
        """Core function to execute database queries.

        :param query: Query to execute.
        :param display_query: Optional bool indicating if query should output to console or not. Defaults to True.
        """
        if display_query:
            self._base.display.query(query)

        if isinstance(data, str):
            data = [data]

        # Create connection and execute query.
        cursor = self._base._connection.cursor()
        # Improve query speed if PostgreSQL (supposedly. Needs more research).
        if self._base._config.db_type == 'PostgreSQL':
            query = cursor.mogrify(query)
        if data is not None:
            cursor.execute(query, data)
        else:
            cursor.execute(query)

        # Get results.
        results = self._fetch_results(cursor)

        # Close connection.
        self._base._connection.commit()
        cursor.close()

        # Return results.
        if results is None:
            results = []
        return results

    def execute_many(self, query, data, display_query=True):
        """Execute method to run multiple queries in one call.

        :param query: Query to execute.
        :param data: One or more sets of data to pass into query.
        :param display_query: Optional bool indicating if query should output to console or not. Defaults to True.
        """
        if display_query:
            self._base.display.query(query)

        # Create connection and execute query.
        cursor = self._base._connection.cursor()
        # Improve query speed if PostgreSQL (supposedly. Needs more research).
        if self._base._config.db_type == 'PostgreSQL':
            query = cursor.mogrify(query)
        cursor.executemany(query, data)

        # Get results.
        results = self._fetch_results(cursor)

        # Close connection.
        self._base._connection.commit()
        cursor.close()

        # Return results.
        if results is None:
            results = []
        return results

    def _fetch_results(self, cursor):
        """Helper function to fetch query results, based on database type."""
        raise NotImplementedError('Please override the connection.query._fetch_results() function.')

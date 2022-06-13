"""
Query section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


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

    def execute(self, query, display_query=True):
        """"""
        if display_query:
            logger.query(query)

        # Create connection and execute query.
        cursor = self._base._connection.cursor()
        cursor.execute(query)

        # Get results.
        results = cursor.fetchall()

        # Close connection.
        self._base._connection.commit()
        cursor.close()

        # Return results.
        if results is None:
            results = []
        return results


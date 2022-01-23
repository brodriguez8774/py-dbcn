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

"""
Query section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.query import BaseQuery
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlQuery(BaseQuery):
    """
    Logic for making row queries, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Query class.')

    def _fetch_results(self, cursor):
        """Helper function to fetch query results, based on database type."""
        if cursor.pgresult_ptr is not None:
            return cursor.fetchall()
        else:
            return None

"""
Query section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# User Imports.
from src.connectors.core.query import BaseQuery
from src.logging import init_logging


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

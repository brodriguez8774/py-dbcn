"""
Table section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# User Imports.
from src.connectors.core.tables import BaseTables
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlTables(BaseTables):
    """
    Logic for making table queries, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Tables class.')

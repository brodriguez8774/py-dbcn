"""
Display section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# User Imports.
from src.connectors.core.display import BaseDisplay
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlDisplay(BaseDisplay):
    """
    Logic for displaying queries and other project output in prettier format, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Display class.')

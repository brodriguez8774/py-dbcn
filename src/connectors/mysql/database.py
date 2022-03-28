"""
Database section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# User Imports.
from src.connectors.core.database import BaseDatabase
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlDatabase(BaseDatabase):
    """
    Logic for making queries directly on the database, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (MySQL) Database class.')

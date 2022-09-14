"""
Database section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.database import BaseDatabase
from py_dbcn.logging import init_logging


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

        # Initialize variables.
        self._show_databases_query = 'SHOW DATABASES;'
        self._current_database_query = 'SELECT DATABASE();'

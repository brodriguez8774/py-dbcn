"""
Table section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.tables import BaseTables
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlTables(BaseTables):
    """
    Logic for making table queries, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (MySQL) Tables class.')

        # Initialize variables.
        self._show_tables_query = 'SHOW TABLES;'
        self._describe_table_query = 'DESCRIBE {0};'


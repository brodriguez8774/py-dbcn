"""
Utils section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# User Imports.
from py_dbcn.connectors.core.utils import BaseUtils
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlUtils(BaseUtils):
    """
    Extra utility logic, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (MySQL) Utils class.')

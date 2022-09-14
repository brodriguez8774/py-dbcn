"""
Record/row/entry manipulation section of "SqLite" DB Connector class.

Contains database connection logic specific to SqLite databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.database import BaseDatabase
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class SqliteRecords(BaseDatabase):
    """
    Logic for making record/row/entry queries, for SqLite databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (SqLite) Records class.')

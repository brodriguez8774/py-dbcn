"""
Record/row/entry manipulation section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# User Imports.
from py_dbcn.connectors.core.records import BaseRecords
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlRecords(BaseRecords):
    """
    Logic for making record/row/entry queries, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Records class.')

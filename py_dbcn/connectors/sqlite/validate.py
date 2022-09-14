"""
Validation section of "SqLite" DB Connector class.

Contains database connection logic specific to SqLite databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.validate import BaseValidate
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class SqliteValidate(BaseValidate):
    """
    Logic for validating various queries and query subsections, for SqLite databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (SqLite) Validate class.')

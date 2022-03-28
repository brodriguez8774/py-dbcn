"""
Validation section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# User Imports.
from src.connectors.core.validate import BaseValidate
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlValidate(BaseValidate):
    """
    Logic for validating various queries and query subsections, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (MySQL) Validate class.')

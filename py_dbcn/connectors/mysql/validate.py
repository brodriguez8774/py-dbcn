"""
Validation section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# User Imports.
from py_dbcn.connectors.core.validate import BaseValidate
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlValidate(BaseValidate):
    """
    Logic for validating various queries and query subsections, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        self._built_in_function_calls = [
            'ADDDATE',
            'BIT_AND',
            'BIT_OR',
            'BIT_XOR',
            'CAST',
            'COUNT',
            'CURDATE',
            'CURTIME',
            'DATE_ADD',
            'DATE_SUB',
            'EXTRACT',
            'GROUP_CONCAT',
            'MAX',
            'MID',
            'MIN',
            'NOW',
            'POSITION',
            'SESSION_USER',
            'STD',
            'STDDEV',
            'STDDEV_POP',
            'STDDEV_SAMP',
            'SUBDATE',
            'SUBSTR',
            'SUBSTRING',
            'SUM',
            'SYSDATE',
            'SYSTEM_USER',
            'TRIM',
            'VARIANCE',
            'VAR_POP',
            'VAR_SAMP',
        ]

        logger.debug('Generating related (MySQL) Validate class.')

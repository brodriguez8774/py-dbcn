"""
Validation section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# User Imports.
from py_dbcn.connectors.core.validate import BaseValidate
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlValidate(BaseValidate):
    """
    Logic for validating various queries and query subsections, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        # Full List:
        # https://www.postgresql.org/docs/current/sql-keywords-appendix.html
        self._reserved_function_names = [
            'ABS',
            'AVG,'
            'BIT_LENGTH',
            'CASE',
            'CAST',
            'CEIL',
            'CEILING',
            'CHAR_LENGTH',
            'CHARACTER_LENGTH',
            'COALESCE',
            'COLLATE',
            'COLLATION',
            'CONVERT',
            'COUNT',
            'CURDATE',
            'CURRENT_DATE',
            'CURRENT_TIME',
            'CURRENT_TIMESTAMP',
            'CURRENT_USER',
            'DAY',
            'EXTRACT',
            'FLOOR',
            'ISNULL',
            'JSON_ARRAY',
            'JSON_EXISTS',
            'JSON_TABLE',
            'JSON_VALUE',
            'LAG',
            'LEAD',
            'LEFT',
            'LENGTH',
            'LOWER',
            'MAX',
            'MIN',
            'MOD',
            'MONTH',
            'NCHAR',
            'NULLIF',
            'OCTET_LENGTH',
            'POSITION',
            'RIGHT',
            'RTRIM',
            'SESSION_USER',
            'SPACE',
            'SQRT',
            'STDDEV_POP',
            'STDDEV_SAMP',
            'SUBSTRING',
            'SUM',
            'SYSTEM_USER',
            'TRIM',
            'UPPER',
            'VAR_POP',
            'VAR_SAMP',
            'YEAR',
        ]
        self._quote_column_format = """'"""
        self._quote_identifier_format = """\""""
        self._quote_str_literal_format = """'"""

        logger.debug('Generating related (PostgreSQL) Validate class.')

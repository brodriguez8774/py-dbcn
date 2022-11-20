"""
Validation section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.validate import BaseValidate
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


# Module Variables.
QUOTE_COLUMN_FORMAT = """\""""       # Used for quoting table columns.
QUOTE_IDENTIFIER_FORMAT = """\""""  # Used for quoting identifiers (such as SELECT clause field id's).
QUOTE_ORDER_BY_FORMAT = """\""""    # Used for quoting values in ORDER BY clause.
QUOTE_STR_LITERAL_FORMAT = """'"""  # Used for quoting actual strings.


class PostgresqlValidate(BaseValidate):
    """
    Logic for validating various queries and query subsections, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Validate class.')

        # Function names that are used within the database system.
        # These should not be allowed for user values, such as table names, etc.
        # Full List:
        # https://www.postgresql.org/docs/current/sql-keywords-appendix.html
        self._reserved_function_names = [
            'ABS',
            'AVG',
            'BIT_AND',
            'BIT_OR',
            'BIT_LENGTH',
            'BOOL_AND',
            'BOOL_OR',
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
            'STDDEV',
            'STDDEV_POP',
            'STDDEV_SAMP',
            'SUBSTRING',
            'SUM',
            'SYSTEM_USER',
            'TRIM',
            'UPPER',
            'VAR_POP',
            'VAR_SAMP',
            'VARIANCE',
            'YEAR',
        ]
        # Keywords that cannot be used as identifiers, such as column names, unless quoted.
        # We don't define the comprehensive list here, but get many common ones.
        # See https://www.postgresql.org/docs/current/sql-keywords-appendix.html
        self._reserved_keywords = list(self._reserved_function_names)
        self._reserved_keywords += [
            'ASC',
            'AS',
            'DESC',
        ]

        # Initialize database string-quote types.
        # Aka, what the database says is "okay" to surround string values with.
        self._quote_column_format = QUOTE_COLUMN_FORMAT
        self._quote_identifier_format = QUOTE_IDENTIFIER_FORMAT
        self._quote_order_by_format = QUOTE_ORDER_BY_FORMAT
        self._quote_str_literal_format = QUOTE_STR_LITERAL_FORMAT

"""
Validation section of "MySQL" DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# Internal Imports.
from py_dbcn.connectors.core.validate import BaseValidate
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


# Module Variables.
QUOTE_COLUMN_FORMAT = """`"""           # Used for quoting table columns.
QUOTE_IDENTIFIER_FORMAT = """`"""       # Used for quoting identifiers (such as SELECT clause field id's).
QUOTE_ORDER_BY_FORMAT = """`"""    # Used for quoting values in ORDER BY clause.
QUOTE_STR_LITERAL_FORMAT = """\""""     # Used for quoting actual strings.


class MysqlValidate(BaseValidate):
    """
    Logic for validating various queries and query subsections, for MySQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (MySQL) Validate class.')

        # Function names that are used within the database system.
        # These should not be allowed for user values, such as table names, etc.
        # Full List:
        # https://dev.mysql.com/doc/refman/8.0/en/built-in-function-reference.html
        self._reserved_function_names = [
            'ABS',
            'AVG',
            'ADDDATE',
            'BIT_AND',
            'BIT_LENGTH',
            'BIT_OR',
            'BIT_XOR',
            'CAST',
            'CEIL',
            'CEILING',
            'CHAR_LENGTH',
            'CHARACTER_LENGTH',
            'CHARSET',
            'COALESCE',
            'COLLATION',
            'COUNT',
            'CURDATE',
            'CURTIME',
            'CURRENT_DATE',
            'CURRENT_TIME',
            'CURRENT_TIMESTAMP',
            'CURRENT_USER',
            'DATE_ADD',
            'DATEDIFF',
            'DATE_SUB',
            'DAY',
            'DAYOFMONTH',
            'DAYOFWEEK',
            'DAYOFYEAR',
            'EXTRACT',
            'FLOOR',
            'GROUP_CONCAT',
            'INSERT',
            'ISNULL',
            'JSON_ARRAY',
            'JSON_CONTAINS',
            'JSON_DEPTH',
            'JSON_EXTRACT',
            'JSON_INSERT',
            'JSON_KEYS',
            'JSON_LENGTH',
            'JSON_OVERLAPS',
            'JSON_PRETTY',
            'JSON_QUOTE',
            'JSON_REMOVE',
            'JSON_REPLACE',
            'JSON_SEARCH',
            'JSON_SET',
            'JSON_TABLE',
            'JSON_TYPE',
            'JSON_VALID',
            'JSON_VALUE',
            'LAG',
            'LCASE',
            'LEAD',
            'LEFT',
            'LENGTH',
            'LOWER',
            'LTRIM',
            'MAX',
            'MID',
            'MIN',
            'MOD',
            'MONTH',
            'NOW',
            'NULLIF',
            'OCTET_LENGTH',
            'ORD',
            'POSITION',
            'RAND',
            'REVERSE',
            'RIGHT',
            'RTRIM',
            'ROUND',
            'SESSION_USER',
            'SIGN',
            'SPACE',
            'SQRT',
            'ST_LENGTH',
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
            'UNCOMPRESSED_LENGTH',
            'UCASE',
            'UPPER',
            'VARIANCE',
            'VAR_POP',
            'VAR_SAMP',
            'YEAR',
        ]

        # Keywords that cannot be used as identifiers, such as column names, unless quoted.
        # We don't define the comprehensive list here, but get many common ones.
        # See https://dev.mysql.com/doc/refman/8.0/en/keywords.html
        self._reserved_keywords = list(self._reserved_function_names)
        self._reserved_keywords += [
            'ADD',
            'ALL',
            'ALWAYS',
            'ANALYZE',
            'AND',
            'ANY',
            'AS',
            'ASC',
            'ASCI',
            'AUTO_INCREMENT',
            'AVG',

            'DESC',
        ]

        # Initialize database string-quote types.
        # Aka, what the database says is "okay" to surround string values with.
        self._quote_column_format = QUOTE_COLUMN_FORMAT
        self._quote_identifier_format = QUOTE_IDENTIFIER_FORMAT
        self._quote_order_by_format = QUOTE_ORDER_BY_FORMAT
        self._quote_str_literal_format = QUOTE_STR_LITERAL_FORMAT

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
        self._quote_column_format = """`"""
        self._quote_identifier_format = """`"""
        self._quote_str_literal_format = """\""""

        logger.debug('Generating related (MySQL) Validate class.')

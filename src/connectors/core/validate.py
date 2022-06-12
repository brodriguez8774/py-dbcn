"""
Validation section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
import copy

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseValidate:
    """
    Abstract/generalized logic, for validating various queries and query subsections.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Validate class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

    def database_name(self, name):
        """
        Validates that provided database name uses set of acceptable characters.
        :param name: Potential name of database to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    # region Name Validation

    def table_name(self, name):
        """
        Validates that provided table name uses set of acceptable characters.
        :param name: Potential name of table to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def table_columns(self, columns):
        """
        Validates that provided column values match expected syntax.
        :param columns: Str or dict of columns to validate.
        :return: True if columns are valid | False otherwise.
        """
        # NOTE: Column name cannot match:
        #   * desc
        #   * ??? Look into further "bad" values.

        orig_columns = copy.deepcopy(columns)

        # Handle based on passed type.
        if isinstance(columns, str):
            # Handle for str.

            # Verify that no bad values exist in str.
            if ';' in columns:
                raise ValueError('Invalid character found in columns "{0}"'.format(columns))

            # Add parenthesis if either side is missing them.
            if columns[0] != '(' or columns[-1] != ')':
                columns = '( ' + columns + ' )'

        elif isinstance(columns, dict):
            # Handle for dict.

            # Ensure dict has at least one key-value pair.
            if len(columns) == 0:
                raise ValueError('Columns dict cannot be empty.')

            # Generate appropriate string from dict values.
            columns = '( '
            for key, value in orig_columns.items():

                # Verify that no bad values exist in dict.
                key = str(key)
                value = str(value)
                if ';' in key:
                    raise ValueError('Invalid character found in key "{0}".'.format(key))

                if ';' in value:
                    raise ValueError('Invalid character found in value "{0}".'.format(value))

                columns += '{0} {1}, '.format(key, value)

            # Remove extra comma and space from last key-value pair.
            columns = columns[:len(columns) - 2]

            # Add closing parenthesis.
            columns += ' )'

        else:
            raise TypeError('Table columns should be of type str or dict. Received "{0}".'.format(type(columns)))

        # For now, always return as valid.
        return columns

    # endregion Name Validation

    # region Clause Validation

    def select_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: SELECT clause to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def columns_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: COLUMNS clause to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def values_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: VALUES clause to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def where_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: WHERE clause to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    def order_by_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: ORDER_BY clause to validate.
        :return: True if valid | False otherwise.
        """
        # For now, always return as valid.
        return True

    # endregion Clause Validation

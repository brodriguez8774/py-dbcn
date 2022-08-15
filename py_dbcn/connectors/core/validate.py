"""
Validation section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
import copy, re

# User Imports.
from py_dbcn.logging import init_logging


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

        # Define inheritance variables.
        self._reserved_function_names = None
        self._quote_column_format = None
        self._quote_str_literal_format = None
        self._quote_identifier_format = None

    # region Name Validation

    def _identifier(self, identifier):
        """Generalized validation for "identifier naming conventions".

        All other "identifiers" should probably be run through this function.
        See https://dev.mysql.com/doc/refman/8.0/en/identifiers.html
        """
        if not self._quote_identifier_format:
            raise ValueError('"Value quote" format is not defined. Should be one of [\', ", `].')

        # Run basic sanitation against provided param.
        if identifier is None:
            return (False, 'is None.')
        identifier = str(identifier).strip()

        # Check if value is quoted.
        is_quoted = self._is_quoted(identifier)
        if is_quoted:
            max_len = 66
        else:
            max_len = 64

        # Check minimum length.
        if (
            (is_quoted and len(identifier) < 3)
            or len(identifier) == 0
        ):
            return (False, 'is empty.')

        # Check against max possible length.
        if len(identifier) > max_len:
            return (False, """is longer than 64 characters.\n Identifier is: {0}""".format(identifier))

        # Check acceptable patterns.
        if is_quoted is False:
            # Check against "unquoted patterns".
            '0-9a-zA-Z$_'
            # Check against "quoted patterns".
            pattern = re.compile('^([0-9a-zA-Z$_])+$')
            if not re.match(pattern, identifier):
                return (False, """does not match acceptable characters.\n Identifier is: {0}""".format(identifier))
        else:
            # Check against "quoted patterns".
            pattern = re.compile(u'^([\u0001-\u007F])+$', flags=re.UNICODE)
            if not re.match(pattern, identifier):
                return (False, """does not match acceptable characters.\n Identifier is: {0}""".format(identifier))

        # Check for characters that we want to exclude.
        forbidden_chars = re.compile(
            u'((;)|(\u003B)|(\\\\)|(\\\u005C))',
            flags=re.UNICODE,
        )
        if forbidden_chars.search(identifier):
            return (False, """does not match acceptable characters.\n Identifier is: {0}""".format(identifier))

        # Passed all tests.
        return (True, '')

    def database_name(self, identifier):
        """Validates that provided database name uses set of acceptable characters.

        :param identifier: Potential name of database to validate.
        :return: True if valid | False otherwise.
        """
        # Run basic sanitation against provided param.
        if identifier is None:
            raise TypeError('Invalid database name. Is None.')
        identifier = str(identifier).strip()

        # Check if value is quoted.
        is_quoted = self._is_quoted(identifier)

        # Validate using "general identifier" logic.
        results = self._identifier(identifier)

        if results[0] is False:
            if is_quoted:
                raise ValueError(u'Invalid database name of {0}. Name {1}'.format(str(identifier), results[1]))
            else:
                raise ValueError(u'Invalid database name of "{0}". Name {1}'.format(str(identifier), results[1]))

        # Passed checks.
        return True

    def table_name(self, identifier):
        """Validates that provided table name uses set of acceptable characters.

        :param identifier: Potential name of table to validate.
        :return: True if valid | False otherwise.
        """
        # Run basic sanitation against provided param.
        if identifier is None:
            raise TypeError('Invalid table name. Is None.')
        identifier = str(identifier).strip()

        # Check if value is quoted.
        is_quoted = self._is_quoted(identifier)

        # Validate using "general identifier" logic.
        results = self._identifier(identifier)

        if results[0] is False:
            if is_quoted:
                raise ValueError(u'Invalid table name of {0}. Name {1}'.format(str(identifier), results[1]))
            else:
                raise ValueError(u'Invalid table name of "{0}". Name {1}'.format(str(identifier), results[1]))

        # Passed checks.
        return True

    def table_column(self, identifier):
        """Validates that provided table column uses set of acceptable characters.

        Differs from validate.table_columns() in that this checks a singular column, and that one checks a set.
        Aka, validate.table_columns() is a parent method that calls this function.

        :param identifier: Potential column of table to validate.
        :return: True if valid | False otherwise.
        """
        # Run basic sanitation against provided param.
        if identifier is None:
            raise TypeError('Invalid table column. Is None.')
        identifier = str(identifier).strip()

        # Check if value is quoted.
        is_quoted = self._is_quoted(identifier)

        # Validate using "general identifier" logic.
        results = self._identifier(identifier)

        if results[0] is False:
            if is_quoted:
                raise ValueError(u'Invalid table column of {0}. Column {1}'.format(str(identifier), results[1]))
            else:
                raise ValueError(u'Invalid table column of "{0}". Column {1}'.format(str(identifier), results[1]))

        # Passed checks.
        return True

    # endregion Name Validation

    def table_columns(self, columns):
        """Validates that provided column values match expected syntax.

        Differs from validate.table_column() in that this checks a set of columns, and that one checks a singular.
        Aka, validate.table_column() is a child method that is called by this function.

        :param columns: Str or dict of columns to validate.
        :return: True if columns are valid | False otherwise.
        """
        # NOTE: Table column cannot match:
        #   * desc
        #   * ??? Look into further "bad" values.

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
            orig_columns = copy.deepcopy(columns)

            # Ensure dict has at least one key-value pair.
            if len(columns) == 0:
                raise ValueError('Columns dict cannot be empty.')

            # Generate appropriate string from dict values.
            columns = '( '
            for key, value in orig_columns.items():

                # Separately validate provided key and value.
                key = str(key).strip()
                value = str(value).strip()
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

    # region Clause Validation

    def sanitize_select_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: SELECT clause to validate.
        :return: True if valid | False otherwise.
        """
        if not self._reserved_function_names:
            raise ValueError('Reserved keyword list is not defined.')

        if isinstance(clause, list) or isinstance(clause, tuple):
            # Format we want.
            pass
        else:
            # Handle for None type. Default to "all".
            if clause is None:
                clause = '*'
            else:
                # Handle for all other types.
                clause = str(clause)

            # Check for outer parens.
            if (
                len(clause) > 1
                and (
                    (clause[0] == '(' and clause[-1] == ')')
                    or (clause[0] == '[' and clause[-1] == ']')
                )
            ):
                clause = clause[1:-1]

            # Convert to list.
            clause = clause.split(',')
            for index in range(len(clause)):
                item = clause[index].strip()
                if item == '*':
                    clause[index] = item
                clause[index] = '{0}'.format(item)

        # Handle for "all" star.
        if len(clause) == 1 and clause[0] == '*':
            return '*'

        # Validate each item in clause, now that it's an array.
        new_clause = []
        for item in clause:
            found_functions = False
            item = str(item).strip()

            # Strip out function values.
            # First check against regex matches.
            func_call_regex = (r'\(*|'.join(self._reserved_function_names))

            matches = re.match(func_call_regex, item, flags=re.IGNORECASE)

            # Proceed if at least one match is found.
            stripped_left = ''
            stripped_right = ''
            if matches:
                index = 0
                while index < len(self._reserved_function_names):
                    func_call = self._reserved_function_names[index]
                    if re.match(r'^{0}\('.format(func_call), item, flags=re.IGNORECASE) and item[-1] == ')':
                        # Found a match. Update identifier and check for further matches.
                        found_functions = True
                        length = len(func_call) + 1
                        stripped_left += item[:length]
                        stripped_right += ')'
                        item = item[length:-1].strip()
                    index += 1

            # Error if "all" star. Should not pass this in addition to other values.
            if item == '*' and not found_functions:
                raise ValueError('SELECT clause provided * with other params. * is only valid alone.')

            # Validate individual identifier.
            if item != '*':
                results = self._identifier(item)
                if results[0] is False:
                    raise ValueError('Invalid SELECT identifier. Identifier {0}'.format(results[1]))

            # If we made it this far, item is valid. Escape with backticks and readd.
            is_quoted = self._is_quoted(item)
            if is_quoted:
                # Was already quoted, but may not be with expected format. Reformat to guaranteed use expected format.
                item = '{1}{0}{1}'.format(item[1:-1], self._quote_identifier_format)
            elif item == '*':
                pass
            else:
                # Was not quoted. Add quotes.
                item = '{1}{0}{1}'.format(item, self._quote_identifier_format)

            # Re-add function values.
            item = stripped_left.upper() + item + stripped_right

            # Append updated value to clause.
            new_clause.append(item)

        # All items in clause were valid. Re-concatenate into single expected str format.
        clause = ', '.join(new_clause)

        # Return validated and sanitized SELECT clause.
        return clause

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

    def _is_quoted(self, value):
        """Checks if provided value is quoted.

        Aka, these are three "quoted" values:   "id", `first_name`, 'last_name'
        These are three not "quoted" values:    id, first_name, last_name
        """
        is_quoted = False
        if isinstance(value, str):
            # Only attempt to check if str type.
            value = value.strip()

            # Must have matching outer quotes, plus at least one inner character.
            if len(value) > 1 and value[0] == value[-1] and value[0] in ['`', '"', "'"]:
                is_quoted = True

        return is_quoted

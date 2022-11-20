"""
Validation section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
import copy, re
from io import StringIO
from tokenize import (
    generate_tokens,
    ENDMARKER,
    NAME,
    NEWLINE,
    NUMBER,
    OP,
    STRING,
)

# Internal Imports.
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
        self._quote_identifier_format = None
        self._quote_order_by_format = None
        self._quote_str_literal_format = None
        self._reserved_function_names = None
        self._reserved_keywords = None

    # region Validation Functions

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
            pattern = re.compile('^([0-9a-zA-Z$_])+$')
            if not re.match(pattern, identifier):
                return (False, """does not match acceptable characters.\n Identifier is: {0}""".format(identifier))

            # Check against known keyword values. Cannot use keywords without quotes.
            if identifier.upper() in self._reserved_keywords:
                return (
                    False,
                    """matches a known keyword. Must be quoted to use this value. Identifier is: {0}""".format(
                        identifier,
                    ),
                )
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

    def table_columns(self, columns):
        """Validates that provided column values match expected syntax.

        Differs from validate.table_column() in that this checks a set of columns, and that function checks a singular.
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

    def validate_select_clause(self, identifier):
        """"""

    def validate_columns_clause(self, identifier):
        """"""
        # Ensure we have our reserved lists defined for this database type.
        if not self._reserved_function_names:
            raise ValueError('Reserved function list is not defined.')
        if not self._reserved_keywords:
            raise ValueError('Reserved keyword list is not defined.')

        # Ensure provided identifier is not null.
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

    def validate_where_clause(self, identifier):
        """"""

    def validate_values_clause(self, identifier):
        """"""

    def validate_order_by_clause(self, identifier):
        """"""
        # Ensure we have our reserved lists defined for this database type.
        if not self._reserved_function_names:
            raise ValueError('Reserved function list is not defined.')
        if not self._reserved_keywords:
            raise ValueError('Reserved keyword list is not defined.')

        # Ensure provided identifier is not null.
        if identifier is None:
            raise TypeError('Invalid table column. Is None.')
        identifier = str(identifier).strip()

        if identifier.upper().endswith(' ASC'):
            identifier = identifier[:-3].strip()
        elif identifier.upper().endswith(' DESC'):
            identifier = identifier[:-4].strip()

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

    def validate_limit_by_clause(self, identifier):
        """"""

    # endregion Validation Functions

    # region Sanitization Functions

    def sanitize_select_identifier_clause(self, clause, as_str=True):
        """
        Validates that provided clause follows acceptable format.
        :param clause: SELECT clause to validate.
        :param as_str: Bool indicating if return value should be formatted as a str. Otherwise is list.
        :return: Properly formatted clause if possible, otherwise error.
        """
        if not self._reserved_function_names:
            raise ValueError('Reserved keyword list is not defined.')

        # Sanitize overall clause.
        clause = self._inner_sanitize_columns(clause, allow_wildcard=True)

        # Check that each inner clause item is valid.
        for item in clause:
            self.validate_select_clause(item)

        # All items in clause were valid. Return validated and sanitized SELECT clause.
        if as_str:
            # Re-concatenate into single expected str format.
            return ', '.join(clause)
        else:
            # Return as list.
            return clause

    def sanitize_where_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: WHERE clause to validate.
        :return: Properly formatted clause if possible, otherwise error.
        """
        # TODO: Implement proper sanitization.

        # Handle if none.
        if clause is None:
            clause = ''

        # Convert to str.
        clause = str(clause).strip()

        # Remove prefix, if present.
        if clause.lower().startswith('where'):
            clause = clause[5:]

        # Strip now that prefix is gone.
        clause = clause.strip()

        # Put into expected format.
        if len(clause) > 1:
            clause = '\nWHERE {0}'.format(clause)

        return clause

    def sanitize_columns_clause(self, clause, as_str=True):
        """
        Validates that provided clause follows acceptable format.
        :param clause: COLUMNS clause to validate.
        :param as_str: Bool indicating if return value should be formatted as a str. Otherwise is list.
        :return: Properly formatted clause if possible, otherwise error.
        """
        if not self._reserved_function_names:
            raise ValueError('Reserved keyword list is not defined.')

        # Sanitize overall clause.
        clause = self._inner_sanitize_columns(clause, allow_wildcard=False)

        # Check that each inner clause item is valid.
        for item in clause:
            self.validate_columns_clause(item)

        # All items in clause were valid. Return validated and sanitized SELECT clause.
        if as_str:
            # Re-concatenate into single expected str format.
            return ', '.join(clause)
        else:
            # Return as list.
            return clause

    def sanitize_values_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.

        :param clause: VALUES clause to validate.
        :return: Properly formatted clause if possible, otherwise error.
        """
        # For now, always return as valid.
        return clause

        # # TODO: Attempted to have full, dynamic validation of entire clause and all inner values.
        # #   However, had too many cases where it would break, due to being able to essentially put in anything.
        # #   It may be possible to magically validate the "values clause", but it's too much time/work
        # #   to implement right now. Potentially look into again in the future.
        # #
        # #   Also, due to the nature of this logic, it almost seems like this should either do the
        # #   "full dynamic validation" or have no validation at all for this clause. Unsure how best to handle this
        # #   at the current date...
        # #
        # print('\n\n\n\n')
        # print('orig clause: "{0}"'.format(clause))
        #
        # if not self._reserved_function_names:
        #     raise ValueError('Reserved keyword list is not defined.')
        #
        # # Convert to array format.
        # if isinstance(clause, list) or isinstance(clause, tuple):
        #     # Format we want.
        #     pass
        # else:
        #     print('as str: {0}')
        #
        #     # Handle for None type.
        #     if clause is None:
        #         clause = ''
        #     else:
        #         clause = str(clause).strip()
        #
        #     # Remove clause starting value.
        #     if clause.lower().startswith('values'):
        #         clause = clause[6:].strip()
        #
        #     # Ensure not empty when prefix was provided.
        #     if len(clause) < 1:
        #         raise ValueError('Invalid VALUES clause. Must have one or more items.')
        #
        #     # Due to possible amount of variation (particularly in quoted string values),
        #     # we have to tokenize in order to attempt to properly parse.
        #     # Via tokenization, we can effectively avoid outer parens.
        #     tokens = generate_tokens(StringIO(clause).readline)
        #     print('\nas tokens:')
        #     clause = []
        #     for token in tokens:
        #         print('    {0}'.format(token))
        #         if token.exact_type == 1:
        #             # Direct value, missing quotes.
        #             token = str(token.string).strip()
        #             clause.append('{0}{1}{0}'.format(self._quote_str_literal_format, token))
        #         elif token.exact_type == 3:
        #             # String type. Convert to expected quote type.
        #             token = str(token.string).strip()[1:-1]
        #             clause.append('{0}{1}{0}'.format(self._quote_str_literal_format, token))
        #
        # print('as array: {0}'.format(clause))
        #
        # # Loop through each item in array and ensure proper formatting.
        # updated_clause = []
        # for index in range(len(clause)):
        #     item = clause[index]
        #     print('    type: {0}    val: {1}'.format(type(item), item))
        #
        #     # Sanitize for null.
        #     if item is None:
        #         item = 'Null'
        #
        #     # Sanitize str outer quoting.
        #     elif isinstance(item, str):
        #         print('    formatted: {0}'.format("""{0}""".format(item)))
        #
        #         # TODO: Unsure of if this part is required? Seemed to be having issues parsing when multiple quotes are
        #         # put in a row.
        #         tokens = generate_tokens(StringIO("""{0}""".format(item)).readline)
        #         print('    tokens:')
        #         for token in tokens:
        #             print('        {0}'.format(token))
        #
        #         if len(item) > 1:
        #             if item[0] != self._quote_str_literal_format or item[-1] != self._quote_str_literal_format:
        #                 item = '{0}{1}{0}'.format(self._quote_str_literal_format, item)
        #
        #     # Set all others to str equivalent.
        #     else:
        #         item = str(item)
        #
        #     # Append item.
        #     updated_clause.append(item)
        # clause = updated_clause
        #
        # # Handle empty clause.
        # if clause == '':
        #     return ''
        #
        # # Return formatted clause.
        # return ' VALUES ({0})'.format(', '.join(clause))

    def sanitize_order_by_clause(self, clause, as_str=True):
        """
        Validates that provided clause follows acceptable format.
        :param clause: ORDER_BY clause to validate.
        :param as_str: Bool indicating if return value should be formatted as a str. Otherwise is list.
        :return: Properly formatted clause if possible, otherwise error.
        """
        if not self._reserved_function_names:
            raise ValueError('Reserved keyword list is not defined.')

        # Quickly sanitize if string format.
        if isinstance(clause, str):
            clause = clause.strip()

            # Remove clause starting value.
            if clause.lower().startswith('order by'):
                clause = clause[8:].strip()

                # Ensure not empty when prefix was provided.
                if len(clause) < 1:
                    raise ValueError('Invalid ORDER BY clause.')

        # Validate.
        clause = self._inner_sanitize_columns(clause, allow_wildcard=False, order_by=True)

        # Handle empty clause.
        if clause == '':
            return ''

        # Check that each inner clause item is valid.
        for item in clause:
            self.validate_order_by_clause(item)

        # All items in clause were valid. Return validated and sanitized SELECT clause.
        if as_str:
            # Re-concatenate into single expected str format.
            clause = ', '.join(clause)
            return '\nORDER BY {0}'.format(clause)
        else:
            # Return as list.
            return clause

    def sanitize_limit_clause(self, clause):
        """
        Validates that provided clause follows acceptable format.
        :param clause: LIMIT clause to validate.
        :return: Properly formatted clause if possible, otherwise error.
        """
        if clause is None:
            clause = ''

        # Strip any potential whitespace.
        clause = str(clause).strip()

        # Handle if clause is not empty.
        if clause != '':
            # Remove prefix, if present.
            if clause.lower().startswith('limit'):
                clause = clause[5:]

            # Strip again, with prefix removed.
            clause = clause.strip()

            # Check that value can be safely converted to int.
            try:
                clause = int(clause)
            except ValueError:
                raise ValueError('The LIMIT clause expects a positive integer.')

            # Verify is a positive integer.
            if clause < 1:
                raise ValueError('The LIMIT clause must return at least one record.')

            # Put in expected format.
            clause = ' LIMIT {0}'.format(clause)

        # Return formatted clause.
        return clause

    # endregion Sanitization Functions

    # region Helper Functions

    def _is_quoted(self, value):
        """Checks if provided value is quoted.

        Aka, these are three "quoted" values: "id", `first_name`, 'last_name'
        These are not "quoted" values:
            id, first_name, last_name
            "id'
            'id"
            `id'
            etc...
        """
        is_quoted = False
        if isinstance(value, str):
            # Only attempt to check if str type.
            value = value.strip()

            # Must have matching outer quotes, plus at least one inner character.
            if len(value) > 1 and value[0] == value[-1] and value[0] in ['`', '"', "'"]:
                is_quoted = True

        return is_quoted

    def _inner_sanitize_columns(self, clause, allow_wildcard=False, order_by=False, as_str=False):
        """Common logic used by multiple functions to sanitize columns-like values.

        :param clause: Clause to sanitize.
        :param allow_wildcard: Bool indicating if wildcard is allowed for this instance.
        :param order_by: Bool indicating if this is an order_by instance.
        :param as_str: Bool indicating if return value should be formatted as a str. Otherwise is list.
        :return: Str or List of sanitized values.
        """
        if allow_wildcard:
            quote_format = self._quote_identifier_format
        elif order_by:
            quote_format = self._quote_order_by_format
        else:
            quote_format = self._quote_column_format

        # Convert to array format.
        if isinstance(clause, list) or isinstance(clause, tuple):
            # Format we want.
            pass
        else:

            # Handle for None type.
            if clause is None:
                # If wildcards allowed, then default to "all".
                if allow_wildcard:
                    clause = '*'
                else:
                    # Wildcard not allowed. Empty instead.
                    clause = ''
            else:
                # Handle for all other types.
                clause = str(clause).strip()

            # Check for descriptor values.
            if clause.upper().startswith('COLUMNS ') or clause.upper().startswith('COLUMNS('):
                clause = clause[7:].strip()
            if clause.upper().startswith('WHERE ') or clause.upper().startswith('WHERE('):
                clause = clause[5:].strip()
            if clause.upper().startswith('VALUES ') or clause.upper().startswith('VALUES('):
                clause = clause[6:].strip()
            if clause.upper().startswith('ORDER BY ') or clause.upper().startswith('ORDER BY('):
                clause = clause[8:].strip()
            if clause.upper().startswith('LIMIT ') or clause.upper().startswith('LIMIT('):
                clause = clause[5:].strip()

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
                clause[index] = str(clause[index]).strip()

            # Remove potential trailing deadspace.
            if len(clause) > 1 and clause[-1] == '':
                clause = clause[:-1]

        # Check if "all" star wildcard is allowed.
        if allow_wildcard:
            # Handle for SELECT all.
            if len(clause) == 1 and clause[0] == '*':
                return '*'
        # Handle for empty otherwise.
        elif len(clause) == 1 and clause[0] == '':
            return ''

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

            # Ignore potential type casting syntax.
            cast_identifier = ''
            if self._base._config.db_type == 'PostgreSQL':
                # Handle for PostgreSQL casting.
                cast_split = item.split('::')
                if len(cast_split) > 2:
                    raise ValueError('Invalid casting identifier "{0}"'.format(item))
                elif len(cast_split) > 1:
                    cast_identifier = cast_split[1]
                    if not re.match(r'[A-Za-z0-9]+', cast_identifier):
                        raise ValueError('Invalid casting identifier "{0}"'.format(cast_identifier))
                    cast_identifier = '::{0}'.format(cast_identifier)
                item = cast_split[0]

            # Errors on "all" wildcard star.
            if item == '*':
                # Wildcard only acceptable in SELECT clauses.
                if not allow_wildcard:
                    raise ValueError('The * identifier can only be used in a SELECT clause.')
                # Is SELECT clause. However, should not pass wildcard in addition to other values.
                if not found_functions:
                    raise ValueError('SELECT clause provided * with other params. * is only valid alone.')

            # Validate individual identifier.
            order_by_descriptor = ''
            if item != '*':
                if order_by:
                    # To check identifier, trim possible ASC/DESC values.
                    if item.lower().endswith(' asc'):
                        # Handle for ASC syntax.
                        item = item[:-4].rstrip()
                        order_by_descriptor = ' ASC'
                    if item.lower().endswith(' desc'):
                        # Handle for DESC syntax.
                        item = item[:-5].rstrip()
                        order_by_descriptor = ' DESC'

            # If we made it this far, item is valid. Escape with proper quote format and readd.
            is_quoted = self._is_quoted(item)
            if is_quoted:
                # Was already quoted, but may not be with expected format. Reformat to guaranteed use expected format.
                item = '{1}{0}{1}{2}{3}'.format(item[1:-1], quote_format, cast_identifier, order_by_descriptor)
            elif item == '*':
                pass
            else:
                # Was not quoted.
                # First double check that we don't have mismatched quotes.
                if len(item) > 1 and item[0] in ['\'', '"', '`'] and item[-1] in ['\'', '"', '`']:
                    raise ValueError('Found mismatching quotes for identifier {0}'.format(item))

                # Add quotes.
                item = '{1}{0}{1}{2}{3}'.format(item, quote_format, cast_identifier, order_by_descriptor)

            # Re-add function values.
            item = stripped_left.upper() + item + stripped_right

            # Append updated value to clause.
            new_clause.append(item)

        # All items in clause were valid. Return validated and sanitized SELECT clause.
        if as_str:
            # Re-concatenate into single expected str format.
            return ', '.join(new_clause)
        else:
            # Return as list.
            return new_clause

    # endregion Helper Functions

"""
Helper classes to build and store clause logic for queries.
"""

# System Imports.
import datetime, re
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


class BaseClauseBuilder(object):
    """"""
    def __init__(self, validation_class, clause_type, *args, **kwargs):
        # Call parent logic.
        super().__init__(*args, **kwargs)

        # Validate clause type.
        self._clause_type = str(clause_type).lower().strip()
        valid_clause_types = {
            'select': None,
            'where': None,
            'columns': None,
            'values': None,
            'order_by': None,
        }
        try:
            valid_clause_types[self._clause_type]
        except KeyError:
            raise ValueError('Invalid clause type of "{0}".'.format(clause_type))

        # Initialize values.
        self._parent = validation_class
        self._base = validation_class._base
        self._clause_array = []
        self._sanitized_clause = None
        self._print_parens = True
        self._always_quote = True
        self._allow_spaces = False

    def __str__(self):
        if len(self.array) > 0:
            # Non-empty clause. Format for str output.
            to_str = ', '.join('{}' for x in range(len(self.array)))
            to_str = to_str.format(*self.array)
            if self._print_parens:
                to_str = '{0}({1})'.format(self._print_prefix, to_str)
            else:
                to_str = '{0}{1}'.format(self._print_prefix, to_str)
            return to_str
        else:
            # Empty clause.
            return ''

    def __repr__(self):
        return str(tuple(self._clause_array))

    def __len__(self):
        return len(self.__str__())

    def __iter__(self):
        return iter(self.__str__())

    def split(self, *args, **kwargs):
        return self.__str__().split(*args, **kwargs)

    @property
    def array(self):
        return self._clause_array

    @array.setter
    def array(self, value):
        self._to_array(value)

    @property
    def context(self):
        if len(self.array) > 0:
            context = ', '.join('%s' for i in range(len(self.array)))
            return context
        else:
            return ''

    @property
    def data(self):
        single_depth_array = []
        for index in range(len(self.array)):
            single_depth_array.append(self.array[index])

        return single_depth_array

    def _to_array(self, value):
        """Converts clause to array format for initial parsing."""
        if self._clause_prefix is None:
            raise NotImplementedError('Query type {0} missing clause_prefix value.'.format(self.__class__))
        if self._print_prefix is None:
            raise NotImplementedError('Query type {0} missing print_prefix value.'.format(self.__class__))
        if self._quote_format is None:
            raise NotImplementedError('Query type {0} missing quote_format value.'.format(self.__class__))

        print('')
        print('original val: {0}'.format(value))

        if isinstance(value, list):
            # Already list format.
            clause = value
        elif isinstance(value, tuple):
            # Close to list format. Simply convert.
            clause = list(value)
        else:
            # Attempt to parse as str for all other formats.
            if value is None:
                # None type defaults to empty.
                clause = []
            else:
                clause = str(value).strip()

                # Trim prefix, if present.
                if len(self._clause_prefix) > 0:
                    # Check if starts with prefix, brackets, and space.
                    if (
                        clause.upper().startswith('{0} ('.format(self._clause_prefix)) and clause.endswith(')')
                        or clause.upper().startswith('{0} ['.format(self._clause_prefix)) and clause.endswith(']')
                    ):
                        clause = clause[(len(self._clause_prefix) + 2):-1]

                    # Check if starts with prefix, brackets, and no space.
                    elif (
                        clause.upper().startswith('{0}('.format(self._clause_prefix)) and clause.endswith(')')
                        or clause.upper().startswith('{0}['.format(self._clause_prefix)) and clause.endswith(']')
                    ):
                        clause = clause[(len(self._clause_prefix) + 1):-1]

                    # Check if starts with prefix and no brackets.
                    elif clause.upper().startswith('{0} '.format(self._clause_prefix)):
                        clause = clause[(len(self._clause_prefix) + 1):]

                    # Check if starts with brackets only and no prefix.
                    elif (
                        clause.startswith('(') and clause.endswith(')')
                        or clause.startswith('[') and clause.endswith(']')
                    ):
                        clause = clause[1:-1]

                # Convert to list.
                clause = clause.split(',')
                for index in range(len(clause)):
                    clause[index] = str(clause[index]).strip()

                # Remove potential trailing deadspace.
                if len(clause) > 1 and clause[-1] == '':
                    clause = clause[:-1]

        # Validate each item in clause, now that it's an array.
        if len(clause) == 1 and clause[0] == '*':
            # Save wildcard clause.
            self._clause_array = ['*']

        elif len(clause) > 0:
            # Handle any other clause that is non-empty.
            clause = self._validate_clause(clause)

            # Save validated clause.
            self._clause_array = clause
        else:
            # Save empty clause.
            self._clause_array = []

    def _validate_clause(self, original_clause):
        """Used to validate/sanitize an array of clause values."""
        new_clause = []
        for item in original_clause:

            # Handle various specific types.
            is_datetime = False
            if isinstance(item, datetime.datetime):
                # Is a datetime object. Convert to string.
                item = "'{0}'".format(item.strftime('%Y-%m-%d %H:%M:%S'))
                is_datetime = True

            elif isinstance(item, datetime.date):
                # Is a date object. Convert to string.
                item = "'{0}'".format(item.strftime('%Y-%m-%d'))
                is_datetime = True

            # Skip handling for other non-str items.
            elif not isinstance(item, str):
                new_clause.append(item)
                continue

            # If we made it this far, then item is a str (or converted to such).
            item = str(item).strip()

            # Strip out function values.
            # First check against regex matches.
            func_call_regex = (r'\(*|'.join(self._parent._reserved_function_names))
            matches = re.match(func_call_regex, item, flags=re.IGNORECASE)

            # Proceed if at least one match is found.
            stripped_left = ''
            stripped_right = ''
            if matches:
                index = 0
                while index < len(self._parent._reserved_function_names):
                    func_call = self._parent._reserved_function_names[index]
                    if (
                        re.match(r'^{0}\('.format(func_call), item, flags=re.IGNORECASE)
                        and item[-1] == ')'
                    ):
                        # Found a match. Update identifier and check for further matches.
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

            # Validate individual identifier.
            order_by_descriptor = ''
            if item != '*':
                # To check identifier, trim possible ASC/DESC values.
                if item.lower().endswith(' asc'):
                    # Handle for ASC syntax.
                    item = item[:-4].rstrip()
                    order_by_descriptor = ' ASC'
                if item.lower().endswith(' desc'):
                    # Handle for DESC syntax.
                    item = item[:-5].rstrip()
                    order_by_descriptor = ' DESC'

            # # Extra string handling for date/datetime objects.
            # if is_datetime:
            #     item = item[1:-1]

            print('')
            print('item: {0}'.format(item))

            # if (
            #     len(item) > 0
            #     and item != '*'
            #     and (
            #         item[0] not in ['"', "'", '`']
            #         or item[-1] not in ['"', "'", '`']
            #     )
            # ):
            #     item = """'{0}'""".format(item)

            # # Check if apostrophe in value.
            # if "'" in item:
            #     print('\n\n\n\n')
            #     print('replacing quote in {0}'.format(item))
            #     item.replace("'", '\0027')
            #     print('replaced quote in {0}'.format(item))

            # If we made it this far, item is valid. Escape with proper quote format and readd.
            is_quoted = False
            if self.is_quoted(item):
                item = item[1:-1].strip()
                is_quoted = True

            # Skip items that are empty. Otherwise append.
            if len(item) > 0:
                print('')
                print('item: {0}'.format(item))
                print('is_quoted: {0}'.format(is_quoted))
                if item != '*':
                    # Readd quotes in proper format.
                    # Account for statements that may have multiple parts (denoted by spaces).
                    if not self._allow_spaces:
                        item_split = item.split(' ')
                        if self._always_quote or is_quoted:
                            item = '{1}{0}{1}'.format(item_split.pop(0), self._quote_format)
                        while len(item_split) > 0:
                            item_split_part = item_split.pop(0).strip()
                            if len(item_split_part) > 0:
                                item = '{0} {1}'.format(item, item_split_part)
                    else:
                        if self._always_quote or is_quoted:
                            item = '{1}{0}{1}'.format(item, self._quote_format)

                # Readd identifiers in proper format.
                item = '{0}{1}{2}'.format(item, cast_identifier, order_by_descriptor)

                # Readd function calls if present.
                item = '{1}{0}{2}'.format(item, stripped_left.upper(), stripped_right)

                # Save item to clause.
                new_clause.append(item)

        print('final result: {0}'.format(item))

        return new_clause

    @staticmethod
    def is_quoted(value):
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
            if len(value) > 2 and value[0] == value[-1] and value[0] in ['`', '"', "'"]:
                is_quoted = True

        return is_quoted


class SelectClauseBuilder(BaseClauseBuilder):
    """"""
    def __init__(self, validation_class, clause, *args, clause_type='SELECT', **kwargs):
        # Pre-parent-call initialize values.
        self._clause_prefix = ''
        self._print_prefix = ''
        self._quote_format = '"'

        # Call parent logic.
        super().__init__(validation_class, *args, clause_type=clause_type, **kwargs)

        # Process and save provided clause.
        self.array = clause

    def __str__(self):
        # Handle for all-star return.
        if len(self.array) == 1 and self.array[0] == '*':
            return '*'

        # Handle for all other values.
        return super().__str__()

    def _to_array(self, value):
        # If none, set to all-star.
        if value is None:
            value = ['*']

        # Call parent logic.
        super()._to_array(value)

        # If validation returned empty set, set to all-star.
        if len(self.array) == 0:
            self.array = ['*']

        # Error if wildcard star used with any other values.
        elif len(self.array) > 1 and '*' in self.array:
            raise ValueError('SELECT clause provided * with other params. * is only valid alone.')


class WhereClauseBuilder(BaseClauseBuilder):
    """"""
    def __init__(self, validation_class, clause, *args, clause_type='WHERE', **kwargs):
        # Pre-parent-call initialize values.
        self._clause_prefix = 'WHERE'
        self._print_prefix = 'WHERE '
        self._quote_format = '"'

        # Call parent logic.
        super().__init__(validation_class, *args, clause_type=clause_type, **kwargs)

        # Process and save provided clause.
        self.array = clause

    def __str__(self):
        if len(self.array) > 0:
            # Non-empty clause. Format for str output.
            to_str = ' AND '.join('({})' for x in range(len(self.array)))
            to_str = to_str.format(*self.array)
            to_str = '\n{0}{1}'.format(self._print_prefix, to_str)
            return to_str
        else:
            # Empty clause.
            return ''

    def _to_array(self, value):
        """Converts clause to array format for initial parsing."""
        if self._clause_prefix is None:
            raise NotImplementedError('Query type {0} missing clause_prefix value.'.format(self.__class__))
        if self._quote_format is None:
            raise NotImplementedError('Query type {0} missing quote_format value.'.format(self.__class__))

        if isinstance(value, list):
            # Already list format.
            clause = value
        elif isinstance(value, tuple):
            # Close to list format. Simply convert.
            clause = list(value)
        else:
            # Attempt to parse as str for all other formats.
            if value is None:
                # None type defaults to empty.
                clause = []
            else:
                clause = str(value).strip()

                # Trim prefix, if present.
                if len(self._clause_prefix) > 0:
                    # Check if starts with prefix, brackets, and space.
                    if (
                        clause.upper().startswith('{0} ('.format(self._clause_prefix)) and clause.endswith(')')
                        or clause.upper().startswith('{0} ['.format(self._clause_prefix)) and clause.endswith(']')
                    ):
                        clause = clause[(len(self._clause_prefix) + 2):-1]

                    # Check if starts with prefix, brackets, and no space.
                    elif (
                        clause.upper().startswith('{0}('.format(self._clause_prefix)) and clause.endswith(')')
                        or clause.upper().startswith('{0}['.format(self._clause_prefix)) and clause.endswith(']')
                    ):
                        clause = clause[(len(self._clause_prefix) + 1):-1]

                    # Check if starts with prefix and no brackets.
                    elif clause.upper().startswith('{0} '.format(self._clause_prefix)):
                        clause = clause[(len(self._clause_prefix) + 1):]

                # Split into subsections, based on AND + OR delimiters.
                full_split = []
                # First separate by AND delimiters.
                and_split = clause.split(' AND ')
                for and_clause in and_split:
                    # For each inner section, also separate by OR delimiters.
                    or_split = and_clause.split(' OR ')
                    for or_clause in or_split:
                        # For each of these, strip spaces and add if non-empty.
                        or_clause = or_clause.strip()
                        if len(or_clause) > 0:
                            full_split.append(or_clause)

                # Use final result.
                clause = full_split

        # Validate each item in clause, now that it's an array.
        if len(clause) > 0:

            # Loop through each clause item. Correct quotes.
            # TODO: For now, we assume that the first item (separated by spaces) will always be a column.
            #  Fix this logic later.
            for index in range(len(clause)):
                clause_item = clause[index]

                # Split based on spaces. For now, we assume only the first item needs quotes.
                clause_split = clause_item.split(' ')
                first_item = clause_split[0]
                if self.is_quoted(first_item):
                    first_item = first_item[1:-1]
                first_item = '{1}{0}{1}'.format(first_item, self._quote_format)

                # Recombine into single string.
                clause_split[0] = first_item
                clause[index] = ' '.join(clause_split)

            # Save validated clause.
            self._clause_array = clause
        else:
            # Save empty clause.
            self._clause_array = []


class ColumnsClauseBuilder(BaseClauseBuilder):
    """"""
    def __init__(self, validation_class, clause, *args, clause_type='COLUMNS', **kwargs):
        # Pre-parent-call initialize values.
        self._clause_prefix = 'COLUMNS'
        self._print_prefix = ''
        self._quote_format = '"'

        # Call parent logic.
        super().__init__(validation_class, *args, clause_type=clause_type, **kwargs)

        # Process and save provided clause.
        self.array = clause

    def _to_array(self, value):
        # Call parent logic.
        super()._to_array(value)

        # Verify that wildcard star is not present.
        if '*' in self._clause_array:
            raise ValueError('The * identifier can only be used in a SELECT clause.')


class ValuesClauseBuilder(BaseClauseBuilder):
    """"""
    def __init__(self, validation_class, clause, *args, clause_type='VALUES', **kwargs):
        # Pre-parent-call initialize values.
        self._clause_prefix = 'VALUES'
        self._print_prefix = 'VALUES '
        self._quote_format = "'"

        # Call parent logic.
        super().__init__(validation_class, *args, clause_type=clause_type, **kwargs)

        # Post-parent-call initialize values.
        self._always_quote = False
        self._allow_spaces = True

        # Process and save provided clause.
        self.array = clause


class ValuesManyClauseBuilder(ValuesClauseBuilder):
    """"""

    def _validate_clause(self, original_clause):
        """Used to validate/sanitize an array of clause values."""

        # Handle the same as original logic, except there is one extra layer.
        # So loop through each inner item and hand that to validation.
        print('\n\n\n\n')
        print('original_clause:')
        print('{0}'.format(original_clause))

        if len(original_clause) > 0:
            for index in range(len(original_clause)):
                inner_clause = original_clause[index]
                print('    inner_clause:')
                print('    {0}'.format(inner_clause))
                original_clause[index] = super()._validate_clause(inner_clause)
                print('    updated inner_clause:')
                print('    {0}'.format(original_clause[index]))

            print('final result:')
            print('{0}'.format(original_clause))

            # Return validated clause.
            return original_clause

        else:
            # Return empty clause.
            return []

    def __str__(self):
        if len(self.array) > 0:
            # Non-empty clause. Format for str output.
            to_str = self.context
            all_values = []
            for inner_array in self.array:
                for value in inner_array:
                    all_values.append(value)
            print('all_values:')
            print('{0}'.format(all_values))
            print(to_str.format(*all_values))
            to_str = to_str.format(*all_values)
            print('to_str:')
            print('{0}'.format(to_str))
            if self._print_parens:
                to_str = '{0}({1})'.format(self._print_prefix, to_str)
            else:
                to_str = '{0}{1}'.format(self._print_prefix, to_str)
            return to_str
        else:
            # Empty clause.
            return ''

    @property
    def context(self):
        if len(self.array) > 0:
            context_line = ', '.join('%s' for i in range(len(self.array[0])))
            context_line = '    ({0})'.format(context_line)
            context = ',\n'.join(context_line for i in range(len(self.array)))
            context += '\n'
            return context
        else:
            return ''

    @property
    def orig_context(self):
        return super().context

    @property
    def data(self):
        single_depth_array = []
        for inner_array in self.array:
            for index in range(len(inner_array)):
                single_depth_array.append(inner_array[index])

        return single_depth_array


class SetClauseBuilder(BaseClauseBuilder):
    """"""
    def __init__(self, validation_class, clause, *args, clause_type='VALUES', **kwargs):
        # Pre-parent-call initialize values.
        self._clause_prefix = 'SET'
        self._print_prefix = 'SET '
        self._quote_format = '"'

        # Call parent logic.
        super().__init__(validation_class, *args, clause_type=clause_type, **kwargs)

        # Post-parent-call initialize values.
        self._print_parens = False
        self._always_quote = True
        self._allow_spaces = False

        # Process and save provided clause.
        self.array = clause


class OrderByClauseBuilder(BaseClauseBuilder):
    """"""
    def __init__(self, validation_class, clause, *args, clause_type='ORDER_BY', **kwargs):
        # Pre-parent-call initialize values.
        self._clause_prefix = 'ORDER BY'
        self._print_prefix = 'ORDER BY '
        self._quote_format = '"'

        # Call parent logic.
        super().__init__(validation_class, *args, clause_type=clause_type, **kwargs)

        # Post-parent-call initialize values.
        self._print_parens = False

        # Process and save provided clause.
        self.array = clause

    def __str__(self):
        if len(self.array) > 0:
            # Call parent logic.
            str_value = super().__str__()
            return '\n{0}'.format(str_value)
        else:
            return ''

    def _to_array(self, value):
        # Call parent logic.
        super()._to_array(value)

        if '*' in self._clause_array:
            raise ValueError('The * identifier can only be used in a SELECT clause.')

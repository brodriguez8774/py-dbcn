"""
Display section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
import copy
import textwrap

# Internal Imports.
from py_dbcn.constants import OUTPUT_QUERY, OUTPUT_RESULTS, OUTPUT_RESET
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseDisplay:
    """
    Abstract/generalized logic, for displaying queries and other project output in prettier format.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Display class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

        # Define connected children objects.
        self.tables = TableDisplay(self)
        self.records = RecordDisplay(self)

    def _get_longest(self, array, include_db_name=True):
        """Returns count of longest element in provided array.

        :param array: Iterable list/tuple object to get max of.
        :param include_db_name: Bool indicating if database name should also be considered. Defaults to True.
        """
        # Handle if empty.
        if len(array) < 1:
            array = ['']

        # Find longest element in provided array.
        max_count = max([len(str(i).strip()) for i in array])

        # Optionally compare against database name as well.
        curr_database = ''
        if include_db_name:
            curr_database = self._base.database.current(display_query=False)

        # Return max of all.
        return max(max_count, len(curr_database))

    def query(self, query_str):
        """Formats query output for display."""
        # Remove any whitespace created from standard code indentations.
        query_str = textwrap.dedent(query_str).strip()

        # Log results.
        logger.query('{0}{1}{2}'.format(OUTPUT_QUERY, query_str, OUTPUT_RESET))

    def results(self, result_str):
        """Formats result output for display."""
        # Remove any whitespace created from standard code indentations.
        result_str = textwrap.dedent(result_str).strip()

        # Log results.
        logger.results('{0}{1}{2}'.format(OUTPUT_RESULTS, result_str, OUTPUT_RESET))


class TableDisplay:
    """Display logic for table queries."""

    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating Table Display class.')

        # Define connector root object.
        self._base = parent._base

        # Define provided direct parent object.
        self._parent = parent

    def _get(self, results, logger):
        """Display logic for tables._get()."""
        if results:
            # Calculate base values.
            db_name = self._base.database.select(display_query=False)
            inner_row_len = self._parent._get_longest(results)
            if len(db_name) >= inner_row_len - 9:
                header_text_len = inner_row_len
                full_row_len = inner_row_len + 12
                inner_row_len = full_row_len - 2
            else:
                inner_row_len -= 2
                header_text_len = inner_row_len - 8
                full_row_len = inner_row_len + 4
                inner_row_len = full_row_len - 2

            # Generate strings to print out.
            divider = '{0}{1}{2}\n'.format('+', ('-' * full_row_len), '+')
            header = ('| Tables in {0:<' + '{0}'.format(header_text_len) + '} |').format(db_name)
            msg_str = '{0}{1}\n{0}'.format(divider, header)

            # Add results.
            base_row_str = '| {0:<' + '{0}'.format(inner_row_len) + '} |\n'
            for result in sorted(results):
                msg_str += base_row_str.format(str(result).strip())
            msg_str += divider

            # Finally display output.
            self._parent.results(msg_str)
        else:
            self._parent.results('Empty Set')

    def describe(self, results, logger):
        """Display logic for tables.describe()."""
        # Initialize record col sets.

        if self._base._config.db_type == 'MySQL':
            field_col_index = 0
            type_col_index = 1
            null_col_index = 2
            key_col_index = 3
            default_col_index = 4
            extra_col_index = 5
        elif self._base._config.db_type == 'PostgreSQL':
            field_col_index = 3
            type_col_index = 27
            null_col_index = 6
            key_col_index = None
            default_col_index = 5
            extra_col_index = None
        else:
            raise NotImplementedError('Please define expected index to find describe columns.')

        field_col_values = []
        type_col_values = []
        null_col_values = []
        key_col_values = []
        default_col_values = []
        extra_col_values = []

        field_col_max_len = 5
        type_col_max_len = 4
        null_col_max_len = 4
        key_col_max_len = 3
        default_col_max_len = 7
        extra_col_max_len = 5

        # Populate record col sets.
        undefined_value = '{0}__UNDEFINED'.format(self._base._config.db_type)
        for record in results:
            # Handle col "name".
            value = undefined_value
            if field_col_index is not None:
                value = record[field_col_index]
            if value == undefined_value:
                value = ''
            elif value is None:
                value = 'NULL'
            field_col_values.append(value)
            field_col_max_len = max(field_col_max_len, len(str(value)))

            # Handle col "type".
            value = undefined_value
            if type_col_index is not None:
                value = record[type_col_index]
            if value == undefined_value:
                value = 'UNKNOWN'
            elif value is None:
                value = 'NULL'
            type_col_values.append(value)
            type_col_max_len = max(type_col_max_len, len(str(value)))

            # Handle col "nullable".
            value = undefined_value
            if null_col_index is not None:
                value = record[null_col_index]
            if value == undefined_value:
                value = 'UNKNOWN'
            elif value is None:
                value = 'NULL'
            null_col_values.append(value)
            null_col_max_len = max(null_col_max_len, len(str(value)))

            # Handle col "key".
            value = undefined_value
            if key_col_index is not None:
                value = record[key_col_index]
            if value == undefined_value:
                value = 'UNKNOWN'
            elif value is None:
                value = 'NULL'
            key_col_values.append(value)
            key_col_max_len = max(key_col_max_len, len(str(value)))

            # Handle col "default".
            value = undefined_value
            if default_col_index is not None:
                value = record[default_col_index]
            if value == undefined_value:
                value = 'UNKNOWN'
            elif value is None:
                value = 'NULL'
            elif value.startswith('nextval('):
                # TODO: See https://stackoverflow.com/a/8148177
                pass
                # value = self._base.query.execute('SELECT {0}'.format(value), display_query=False)[0]
                # value = self._base.query.execute('SELECT {0}'.format(value))
            default_col_values.append(value)
            default_col_max_len = max(default_col_max_len, len(str(value)))

            # Handle col "extra".
            value = undefined_value
            if extra_col_index is not None:
                value = record[extra_col_index]
            if value == undefined_value:
                value = 'UNKNOWN'
            elif value is None:
                value = 'NULL'
            extra_col_values.append(value)
            extra_col_max_len = max(extra_col_max_len, len(str(value)))

        # Generate strings to print out.
        divider = '{0}{1}{0}{2}{0}{3}{0}{4}{0}{5}{0}{6}{0}\n'.format(
            '+',
            '-' * (field_col_max_len + 2),
            '-' * (type_col_max_len + 2),
            '-' * (null_col_max_len + 2),
            '-' * (key_col_max_len + 2),
            '-' * (default_col_max_len + 2),
            '-' * (extra_col_max_len + 2),
        )
        header = '{0} {1} {0} {2} {0} {3} {0} {4} {0} {5} {0} {6} {0}\n'.format(
            '|',
            ('{0:<' + '{0}'.format(field_col_max_len) + '}').format('Field'),
            ('{0:<' + '{0}'.format(type_col_max_len) + '}').format('Type'),
            ('{0:<' + '{0}'.format(null_col_max_len) + '}').format('Null'),
            ('{0:<' + '{0}'.format(key_col_max_len) + '}').format('Key'),
            ('{0:<' + '{0}'.format(default_col_max_len) + '}').format('Default'),
            ('{0:<' + '{0}'.format(extra_col_max_len) + '}').format('Extra'),
        )
        msg_str = '{0}{1}{0}'.format(divider, header)

        # Add results.
        base_row_str = '{0} {1} {0} {2} {0} {3} {0} {4} {0} {5} {0} {6} {0}\n'.format(
            '|',
            '{0:<' + '{0}'.format(field_col_max_len) + '}',
            '{1:<' + '{0}'.format(type_col_max_len) + '}',
            '{2:<' + '{0}'.format(null_col_max_len) + '}',
            '{3:<' + '{0}'.format(key_col_max_len) + '}',
            '{4:<' + '{0}'.format(default_col_max_len) + '}',
            '{5:<' + '{0}'.format(extra_col_max_len) + '}',
        )

        for index in range(len(results)):
            msg_str += base_row_str.format(
                str(field_col_values[index]).strip(),
                str(type_col_values[index]).strip(),
                str(null_col_values[index]).strip(),
                str(key_col_values[index]).strip(),
                str(default_col_values[index]).strip(),
                str(extra_col_values[index]).strip(),
            )
        msg_str += divider

        # Finally display output.
        self._parent.results(msg_str)


class RecordDisplay:
    """Display logic for record/row/entry queries."""

    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating Record Display class.')

        # Define connector root object.
        self._base = parent._base

        # Define provided direct parent object.
        self._parent = parent

    def select(self, results, logger, table_name, select_clause=None):
        """Display logic for records.select()."""
        if not self._base.validate._quote_column_format:
            raise ValueError('Column quote format is not defined.')

        if results:
            # Check select clause, which directly affects desired output columns.
            # First we initialize to a default str.
            if select_clause is None:
                select_clause = '*'
            else:
                select_clause = str(select_clause).strip()

            if self._base._config.db_type == 'MySQL':
                col_name_index = 0
            elif self._base._config.db_type == 'PostgreSQL':
                col_name_index = 3
            else:
                raise NotImplementedError('Please define expected index to find column name.')

            # Handle based on star or specific cols.
            # TODO: Probably need to tokenize this, to properly compare.
            if select_clause == '*' or '(*)' in select_clause:
                # Calculate column header values, using all columns.
                table_cols = [
                    x[col_name_index]
                    for x in self._base.tables.describe(table_name, display_query=False, display_results=False)
                ]
            else:
                select_clause = select_clause.split(',')
                table_cols = []
                table_describe = self._base.tables.describe(table_name, display_query=False, display_results=False)
                for index in range(len(select_clause)):
                    # Sanitize select clause values.
                    clause = select_clause[index].strip()
                    if len(clause) > 1 and clause[0] == clause[-1] and clause[0] in ['`', '"', "'"]:
                        clause = clause[1:-1]
                    select_clause[index] = clause

                # Calculate column header values, filtered by select clause.
                table_cols = copy.deepcopy(select_clause)

            col_len_array = []
            total_col_len = 0
            for table_col in table_cols:
                col_len = len(table_col)
                if not any(keyword_str in table_col for keyword_str in self._base.validate._reserved_function_names):
                    record_len = self._base.query.execute(
                        self._parent.max_col_length_query.format(
                            table_col,
                            table_name,
                            self._base.validate._quote_identifier_format,
                        ),
                        display_query=False,
                    )[0][0]
                else:
                    # Keyword found in str. For now, to prevent errors, default to size of 19 and skip query.
                    record_len = 19
                length = max(col_len, record_len or 0)
                col_len_array.append(length)
                total_col_len += length + 2

            # Generate divider.
            divider = ''
            for length in col_len_array:
                divider += '{0}{1}'.format('+', ('-' * (length + 2)))
            divider += '+'

            # Generate column header.
            header = ''
            for index in range(len(table_cols)):
                header += ('| {0:<' + '{0}'.format(col_len_array[index]) + '} ').format(table_cols[index])
            header += '|'

            # Generate record row output.
            record_str = ''
            for record in results:
                for index in range(len(record)):
                    if record[index] is None:
                        col_str = 'NULL'
                    else:
                        col_str = str(record[index])
                    record_str += ('| {0:<' + '{0}'.format(col_len_array[index]) + '} ').format(col_str)
                record_str += '|\n'

            # Combine final string.
            msg_str = '{0}\n{1}\n{0}\n{2}{0}'.format(divider, header, record_str)

            # Finally display output.
            self._parent.results(msg_str)
        else:
            self._parent.results('Empty Set')

"""
Display section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


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
            curr_database = self._base.database.current()

        # Return max of all.
        return max(max_count, len(curr_database))


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
            db_name = self._base.database.select()
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
            for result in results:
                msg_str += base_row_str.format(str(result).strip())
            msg_str += divider

            # Finally display output.
            logger.results('{0}'.format(msg_str))
        else:
            logger.results('Empty Set')

    def describe(self, results, logger):
        """Display logic for tables.describe()."""
        # Initialize record col sets.
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
        for record in results:
            # Handle col 1.
            value = record[0]
            if value is None:
                value = 'NULL'
            field_col_values.append(value)
            field_col_max_len = max(field_col_max_len, len(value))

            # Handle col 2.
            value = record[1]
            if value is None:
                value = 'NULL'
            type_col_values.append(value)
            type_col_max_len = max(type_col_max_len, len(value))

            # Handle col 3.
            value = record[2]
            if value is None:
                value = 'NULL'
            null_col_values.append(value)
            null_col_max_len = max(null_col_max_len, len(value))

            # Handle col 4.
            value = record[3]
            if value is None:
                value = 'NULL'
            key_col_values.append(value)
            key_col_max_len = max(key_col_max_len, len(value))

            # Handle col 5.
            value = record[4]
            if value is None:
                value = 'NULL'
            default_col_values.append(value)
            default_col_max_len = max(default_col_max_len, len(value))

            # Handle col 6.
            value = record[5]
            if value is None:
                value = 'NULL'
            extra_col_values.append(value)
            extra_col_max_len = max(extra_col_max_len, len(value))

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
        logger.results('{0}'.format(msg_str))


class RecordDisplay:
    """Display logic for record/row/entry queries."""

    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating Record Display class.')

        # Define connector root object.
        self._base = parent._base

        # Define provided direct parent object.
        self._parent = parent

    def select(self, results, logger, table_name):
        """Display logic for records.select()."""
        if results:
            # Calculate column header values.
            table_cols = [
                x[0]
                for x in self._base.tables.describe(table_name)
            ]
            col_len_array = []
            total_col_len = 0
            for table_col in table_cols:
                col_len = len(table_col)
                record_len = self._base.query.execute(
                    'SELECT MAX(LENGTH({0})) FROM {1};'.format(table_col, table_name)
                )[0][0]
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
                    record_str += ('| {0:<' + '{0}'.format(col_len_array[index]) + '} ').format(record[index])
                record_str += '|\n'

            # Combine final string.
            msg_str = '{0}\n{1}\n{0}\n{2}{0}'.format(divider, header, record_str)

            # Finally display output.
            logger.results('{0}'.format(msg_str))
        else:
            logger.results('Empty Set')

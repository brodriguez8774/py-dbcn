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

        self._base = parent
        self.tables = TableDisplay(self)

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

    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating Table Display class.')

        self._base = parent

    def _get(self, results, logger):
        """Display method for table._get()."""
        if results:
            # Calculate base values.
            db_name = self._base._base.database.select()
            inner_row_len = self._base._get_longest(results)
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
            logger.info('{0}'.format(msg_str))
        else:
            logger.info('Empty Set')

"""
Table section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
import textwrap

# Internal Imports.
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseTables:
    """
    Abstract/generalized logic, for making table queries.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Tables class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

        # Initialize required class query variables.
        self._show_tables_query = None
        self._describe_table_query = None

    def _get(self, display_query=False, display_results=False):
        """Gets list of all currently-available tables in database.

        :param display_query: Bool indicating if query should output to console. Defaults to False.
        :param display_results: Bool indicating if results should output to console. Used for "SHOW TABLES" query.
        """
        if not self._show_tables_query:
            raise ValueError('SHOW TABLES query is not defined.')

        # Generate and execute query.
        results = self._base.query.execute(self._show_tables_query, display_query=display_query)

        # Convert to more friendly format.
        formatted_results = []
        for result in results:
            formatted_results.append(result[0])
        results = formatted_results

        if display_results:
            self._base.display.tables._get(results, logger)

        # Return data.
        return results

    def show(self, display_query=True):
        """Displays all tables available in database.

        :param display_query: Bool indicating if query should output to console. Defaults to True.
        """
        return self._get(display_query=display_query, display_results=True)

    def describe(self, table_name, display_query=True, display_results=True):
        """Describes given table in database.

        :param table_name: Name of table to describe.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        if not self._describe_table_query:
            raise ValueError('DESCRIBE TABLE query is not defined.')

        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided table matches value in list.
        if table_name not in available_tables:
            raise ValueError(
                'Could not find table "{0}". Valid options are {1}.'.format(table_name, available_tables)
            )

        # Generate and execute query.
        query = self._describe_table_query.format(table_name)
        results = self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.tables.describe(results, logger)

        return results

    def create(self, table_name, table_columns, display_query=True, display_results=True):
        """Creates new table with provided name.

        :param table_name: Desired name of new table.
        :param table_columns: Column values for new table.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided columns are valid format.
        orig_table_columns = table_columns
        table_columns = self._base.validate.table_columns(table_columns)
        if table_columns is None:
            raise ValueError('Invalid table columns of "{0}"'.format(orig_table_columns))

        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided table matches value in list.
        if table_name in available_tables:
            # Table already exists. Raise error.
            raise ValueError('Table with name "{0}" already exists'.format(table_name))

        # Create new table.
        # raise NotImplemented('Function needs column-definition handling.')
        query = 'CREATE TABLE {0} {1};'.format(table_name, table_columns)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Created table "{0}".'.format(table_name))

    def modify(self, table_name, modify_clause, column_clause, display_query=True, display_results=True):
        """Modifies table column with provided name.

        :param table_name: Name of table to modify.
        :param modify_clause: Clause of values to apply.
        :param column_clause: Clause of columns to update.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        if str(modify_clause).upper() == 'ADD':
            modify_clause = 'ADD'
        elif str(modify_clause).upper() == 'DROP':
            modify_clause = 'DROP'
        elif str(modify_clause).upper() == 'MODIFY':
            modify_clause = 'MODIFY'
        else:
            err_msg = 'Invalid clause. Accepted values are ADD/DROP/MODIFY. Received "{0}".'.format(modify_clause)
            raise ValueError(err_msg)

        # Check that provided name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided COLUMNS clause is valid format.
        if not self._base.validate.table_columns(column_clause):
            raise ValueError('Invalid table columns of "{0}".'.format(column_clause))

        # Modify table.
        query = textwrap.dedent(
            """
            ALTER TABLE {0}
            {1} {2};
            """.format(table_name, modify_clause, column_clause)
        )
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Created table "{0}".'.format(table_name))

    def update(self, table_name, modify_clause, column_clause, display_query=True, display_results=True):
        """Alias for modify().

        :param table_name: Name of table to modify.
        :param modify_clause: Clause of values to apply.
        :param column_clause: Clause of columns to update.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        return self.modify(
            table_name,
            modify_clause,
            column_clause,
            display_query=display_query,
            display_results=display_results,
        )

    def add_column(self, table_name, column_clause, display_query=True, display_results=True):
        """Adds column to provided table.

        :param table_name: Name of table to modify.
        :param column_clause: Clause of columns to add.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        return self.modify(
            table_name,
            'ADD',
            column_clause,
            display_query=display_query,
            display_results=display_results,
        )

    def drop_column(self, table_name, column_clause, display_query=True, display_results=True):
        """Drops column from provided table.

        :param table_name: Name of table to modify.
        :param column_clause: Clause of columns to drop.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        return self.modify(
            table_name,
            'DROP',
            column_clause,
            display_query=display_query,
            display_results=display_results,
        )

    def modify_column(self, table_name, column_clause, display_query=True, display_results=True):
        """Modifies column in provided table.

        :param table_name: Name of table to modify.
        :param column_clause: Clause of columns to update.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        return self.modify(
            table_name,
            'MODIFY',
            column_clause,
            display_query=display_query,
            display_results=display_results,
        )

    def drop(self, table_name, display_query=True, display_results=True):
        """Deletes table with provided name.

        :param table_name: Name of table to delete.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided tables matches value in list.
        if table_name not in available_tables:
            # Table does not exist. Raise error.
            raise ValueError('Table with name "{0}" already exists'.format(table_name))

        # Remove table.
        query = 'DROP TABLE {0};'.format(table_name)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Dropped table "{0}".'.format(table_name))

    def delete(self, table_name, display_query=True, display_results=True):
        """Alias for table "drop" function.

        :param table_name: Name of table to delete.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        self.drop(table_name, display_query=display_query, display_results=display_results)

    def truncate(self, table_name, cascade=False, display_query=True, display_results=True):
        """Truncates all records from table with provided name.

        :param table_name: Name of table to truncate.
        :param cascade: Bool indicating if truncation should cascade to related tables. Defaults to False.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # First, check that provided name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided tables matches value in list.
        if table_name not in available_tables:
            # Table does not exist. Raise error.
            raise ValueError('Table with name "{0}" already exists'.format(table_name))

        # Get count of records in table, before operation.
        record_count = self.count(table_name, display_query=False, display_results=False)

        # Remove table.
        if cascade:
            cascade = ' CASCADE'
        else:
            cascade = ''
        query = 'TRUNCATE {0}{1};'.format(table_name, cascade)
        self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('Truncated {0} records from table "{1}".'.format(record_count, table_name))

    def count(self, table_name, display_query=True, display_results=True):
        """Returns number of all records present in provided table.

        :param table_name: Name of table to count.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Get list of valid tables.
        available_tables = self._get()

        # Check if provided table matches value in list.
        if table_name not in available_tables:
            raise ValueError(
                'Could not find table "{0}". Valid options are {1}.'.format(table_name, available_tables)
            )

        # Count records in table.
        result = self._base.records.select(table_name, 'COUNT(*)', display_query=display_query)
        result = result[0][0]

        if display_results:
            self._base.display.results('Found {0} records in table.'.format(result))

        return result

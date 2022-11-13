"""
Record/row/entry manipulation section of "PostgreSQL" DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.
import datetime

# Internal Imports.
from py_dbcn.connectors.core.records import BaseRecords
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlRecords(BaseRecords):
    """
    Logic for making record/row/entry queries, for PostgreSQL databases.
    """
    def __init__(self, parent, *args, **kwargs):
        # Call parent logic.
        super().__init__(parent, *args, **kwargs)

        logger.debug('Generating related (PostgreSQL) Records class.')

    def update_many(
        self,
        table_name, columns_clause, values_clause, where_columns_clause,
        column_types_clause=None,
        display_query=True, display_results=True,
    ):
        """Updates record in provided table.

        :param table_name: Name of table to insert into.
        :param columns_clause: Clause to specify columns to insert into.
        :param values_clause: Clause to specify values to insert.
        :param where_columns_clause: NOT STANDARD WHERE CLAUSE. Columns to use as WHERE in provided values.
        :param column_types_clause: Optional clause to provide type hinting for column types. Not required if all
                                    columns are basic types such as text or integer.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Check provided size.
        upper_limit = 10000  # 10,000 limit for now.
        if len(values_clause) > upper_limit:
            if display_query:
                print('Subdividing query.')
            # Exceeds upper limit. Recursively call self on smaller subsets.
            for index in range(0, len(values_clause), upper_limit):
                if display_query:
                    print('    Range [{0}:{1}]'.format(index, index + upper_limit))
                self.update_many(
                    table_name,
                    columns_clause,
                    values_clause[index:index + upper_limit],
                    where_columns_clause,
                    column_types_clause=column_types_clause,
                    display_query=display_query,
                    display_results=display_results,
                )

            # Terminate once all recursive calls have finished.
            return

        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided VALUES clause is valid format.
        # Must be array format.
        if not isinstance(values_clause, list) and not isinstance(values_clause, tuple):
            raise ValueError('VALUES clause for INSERT_MANY queries must be in list/tuple format.')
        if len(values_clause) < 1:
            raise ValueError('VALUES clause cannot be empty for UPDATE_MANY queries.')
        values_clause = self._base.validate.sanitize_values_clause(values_clause)

        # Check that provided WHERE clause is valid format.
        columns_clause = self._base.validate.sanitize_columns_clause(columns_clause)
        where_columns_clause = self._base.validate.sanitize_columns_clause(where_columns_clause)
        columns_clause = columns_clause.split(', ')
        where_columns_clause = where_columns_clause.split(', ')

        # Verify each "where column" is present in the base columns clause.
        for column in where_columns_clause:
            if column not in columns_clause:
                raise ValueError(
                    'All columns specified in WHERE_COLUMNS must also be present in COLUMNS.'
                    'Failed to find "{0}" in {1}'.format(
                        column,
                        columns_clause,
                    )
                )

        # Check for values that might need formatting.
        # For example, if we find date/datetime objects, we automatically convert to a str value that won't error.
        if isinstance(values_clause, list) or isinstance(values_clause, tuple):
            updated_values_clause = ()
            for value_set in values_clause:
                updated_values_set = ()
                for item in value_set:

                    if isinstance(item, datetime.datetime):
                        # Is a datetime object. Convert to string.
                        item = item.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(item, datetime.date):
                        # Is a date object. Convert to string.
                        item = item.strftime('%Y-%m-%d')

                    # Add item to updated inner set.
                    updated_values_set += (item,)

                # Add item to updated clause.
                updated_values_clause += (updated_values_set,)

            # Replace original clause.
            values_clause = updated_values_clause

        # Now format our clauses for query.
        if column_types_clause is not None:
            # Provide type hinting for columns.
            set_clause = ''
            for index in range(len(columns_clause)):
                if set_clause != '':
                    set_clause += ',\n'
                set_clause += '    {0} = pydbcn_temp.{0}::{1}'.format(
                    columns_clause[index].strip(self._base.validate._quote_column_format),
                    column_types_clause[index],
                )
        else:
            # No type hinting. Provide columns as-is.
            set_clause = ',\n'.join([
                '    {0} = pydbcn_temp.{0}'.format(x.strip(self._base.validate._quote_column_format))
                for x in columns_clause
            ])
        values_clause = ',\n'.join([
            '    {0}'.format(x)
            for x in values_clause
        ])
        columns_clause = ', '.join([
            x.strip(self._base.validate._quote_column_format)
            for x in columns_clause
        ])
        where_columns_clause = ' AND\n'.join([
            '    pydbcn_update_table.{0} = pydbcn_temp.{0}'.format(x.strip(self._base.validate._quote_column_format))
            for x in where_columns_clause
        ])

        # Update records.
        query = f'UPDATE {table_name} AS pydbcn_update_table SET\n'
        query += f'{set_clause}\n'
        query += f'FROM (VALUES\n'
        query += f'{values_clause}\n'
        query += f') AS pydbcn_temp ({columns_clause})\n'
        query += f'WHERE (\n'
        query += f'{where_columns_clause}\n'
        query += f');'
        results = self._base.query.execute(query, display_query=display_query)

        # # Do a select to get the updated values as results.
        # # TODO: Currently doesn't get any results. Not sure how to dynamically get them at this time.
        # results = self.select(
        #     table_name,
        #     where_clause=where_clause,
        #     display_query=False,
        #     display_results=display_results,
        # )

        return results

"""
Record/row/entry manipulation section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
import datetime
import textwrap

# Internal Imports.
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseRecords:
    """
    Abstract/generalized logic, for making record/row/entry queries.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Records class.')

        # Define connector root object.
        self._base = parent

        # Define provided direct parent object.
        self._parent = parent

    def select(
        self,
        table_name,
        select_clause=None, where_clause=None, order_by_clause=None, limit_clause=None,
        display_query=True, display_results=True,
    ):
        """Selects records from provided table.

        :param table_name: Name of table to select from.
        :param select_clause: Clause to choose selected columns.
        :param where_clause: Clause to limit selected records.
        :param order_by_clause: Clause to adjust sort order of records.
        :param limit_clause: Clause to limit query scope via number of records returned.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided SELECT clause is valid format.
        select_clause = self._base.validate.sanitize_select_identifier_clause(select_clause)

        # Check that provided WHERE clause is valid format.
        where_clause = self._base.validate.sanitize_where_clause(where_clause)

        # Check that provided ORDER BY clause is valid format.
        order_by_clause = self._base.validate.sanitize_order_by_clause(order_by_clause)

        # Check that provided LIMIT clause is valid format.
        limit_clause = self._base.validate.sanitize_limit_clause(limit_clause)

        # Select record.
        query = 'SELECT {0} FROM {1}{2}{3}{4};'.format(
            select_clause,
            table_name,
            where_clause,
            order_by_clause,
            limit_clause,
        )
        results = self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.records.select(results, logger, table_name, select_clause)

        return results

    def insert(self, table_name, values_clause, columns_clause=None, display_query=True, display_results=True):
        """Inserts record(s) into provided table.

        :param table_name: Name of table to insert into.
        :param values_clause: Clause to specify values to insert.
        :param columns_clause: Clause to specify columns to insert into.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided COLUMNS clause is valid format.
        columns_clause = self._base.validate.sanitize_columns_clause(columns_clause)

        # Check that provided VALUES clause is valid format.
        values_clause = self._base.validate.sanitize_values_clause(values_clause)

        # Check for values that might need formatting.
        # For example, if we find date/datetime objects, we automatically convert to a str value that won't error.
        if isinstance(values_clause, list) or isinstance(values_clause, tuple):
            updated_values_clause = ()
            for item in values_clause:

                if isinstance(item, datetime.datetime):
                    # Is a datetime object. Convert to string.
                    item = item.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(item, datetime.date):
                    # Is a date object. Convert to string.
                    item = item.strftime('%Y-%m-%d')

                # Add item to updated clause.
                updated_values_clause += (item,)

            # Replace original clause.
            values_clause = updated_values_clause

        # Insert record.
        query = textwrap.dedent(
            """
            INSERT INTO {0}{1}
            VALUES {2};
            """.format(table_name, columns_clause, values_clause)
        )
        results = self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('{0}'.format(results))

        return results

    def insert_many(self, table_name, values_clause, columns_clause=None, display_query=True, display_results=True):
        """"""
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided COLUMNS clause is valid format.
        columns_clause = self._base.validate.sanitize_columns_clause(columns_clause)

        # Check that provided VALUES clause is valid format.
        # Must be array format.
        if not isinstance(values_clause, list) and not isinstance(values_clause, tuple):
            raise ValueError('VALUES clause for INSERT_MANY queries must be in list/tuple format.')
        values_clause = self._base.validate.sanitize_values_clause(values_clause)

        # Check for values that might need formatting.
        # For example, if we find date/datetime objects, we automatically convert to a str value that won't error.
        if isinstance(values_clause, list) or isinstance(values_clause, tuple):
            updated_values_clause = ()

            # Check each sub-item.
            for item in values_clause:

                if isinstance(item, datetime.datetime):
                    # Is a datetime object. Convert to string.
                    item = item.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(item, datetime.date):
                    # Is a date object. Convert to string.
                    item = item.strftime('%Y-%m-%d')

                # Add item to updated clause.
                updated_values_clause += (item,)

            # Replace original clause.
            values_clause = updated_values_clause
        else:
            raise ValueError('In an execute_many, values clause must be a list or tuple.')

        values_context = ', '.join('%s' for i in range(len(values_clause[0])))

        # Insert record.
        query = textwrap.dedent(
            """
            INSERT INTO {0}{1}
            VALUES ({2});
            """.format(table_name, columns_clause, values_context)
        )
        results = self._base.query.execute_many(query, values_clause, display_query=display_query)
        if display_results:
            self._base.display.results('{0}'.format(results))

        return results

    def update(self, table_name, values_clause, where_clause, display_query=True, display_results=True):
        """Updates record in provided table.

        :param table_name: Name of table to insert into.
        :param values_clause: Clause to specify values to insert.
        :param where_clause: Clause to limit update scope.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided VALUES clause is valid format.
        values_clause = self._base.validate.sanitize_values_clause(values_clause)

        # Check that provided WHERE clause is valid format.
        where_clause = self._base.validate.sanitize_where_clause(where_clause)

        # Check for values that might need formatting.
        # For example, if we find date/datetime objects, we automatically convert to a str value that won't error.
        if isinstance(values_clause, list) or isinstance(values_clause, tuple):
            updated_values_clause = ()
            for item in values_clause:

                if isinstance(item, datetime.datetime):
                    # Is a datetime object. Convert to string.
                    item = item.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(item, datetime.date):
                    # Is a date object. Convert to string.
                    item = item.strftime('%Y-%m-%d')

                # Add item to updated clause.
                updated_values_clause += (item,)

            # Replace original clause.
            values_clause = updated_values_clause

        # Update record.
        query = textwrap.dedent(
            """
            UPDATE {0}
            SET {1}{2};
            """.format(table_name, values_clause, where_clause)
        )
        self._base.query.execute(query, display_query=display_query)

        # Do a select to get the updated values as results.
        results = self.select(
            table_name,
            where_clause=where_clause,
            display_query=False,
            display_results=display_results,
        )

        return results

    def update_many(
        self,
        table_name, columns_clause, values_clause, where_columns_clause,
        display_query=True, display_results=True,
    ):
        """Updates record in provided table.

        :param table_name: Name of table to insert into.
        :param columns_clause: Clause to specify columns to insert into.
        :param values_clause: Clause to specify values to insert.
        :param where_columns_clause: NOT STANDARD WHERE CLAUSE. Columns to use as WHERE in provided values.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided VALUES clause is valid format.
        # Must be array format.
        if not isinstance(values_clause, list) and not isinstance(values_clause, tuple):
            raise ValueError('VALUES clause for INSERT_MANY queries must be in list/tuple format.')
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
            for item in values_clause:

                if isinstance(item, datetime.datetime):
                    # Is a datetime object. Convert to string.
                    item = item.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(item, datetime.date):
                    # Is a date object. Convert to string.
                    item = item.strftime('%Y-%m-%d')

                # Add item to updated clause.
                updated_values_clause += (item,)

            # Replace original clause.
            values_clause = updated_values_clause

        # Now format our clauses for query.
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
        where_columns_clause = ',\n'.join([
            '    pydbcn_update_table.{0} = pydbcn_temp.{0}'.format(x.strip(self._base.validate._quote_column_format))
            for x in where_columns_clause
        ])

        # print('\n\n\n\n')
        # print('\ntable_name:\n{0}'.format(table_name))
        # print('\nset_clause:\n{0}'.format(set_clause))
        # print('\nvalues_clause:\n{0}'.format(values_clause))
        # print('\nwhere_columns_clause:\n{0}'.format(where_columns_clause))
        # print('\ncolumns_clause:\n{0}'.format(columns_clause))

        # Update records.
        query = textwrap.dedent(
            """
            UPDATE {0} AS pydbcn_update_table SET
            {1}
            FROM (VALUES
            {2}
            ) AS pydbcn_temp ({3})
            WHERE (
            {4}
            );
            """.format(table_name, set_clause, values_clause, columns_clause, where_columns_clause)
        )

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

    def delete(self, table_name, where_clause, display_query=True, display_results=True):
        """Deletes record(s) in given table.

        :param table_name: Name of table to insert into.
        :param where_clause: Clause to limit delete scope.
        :param display_query: Bool indicating if query should output to console. Defaults to True.
        :param display_results: Bool indicating if results should output to console. Defaults to True.
        """
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided WHERE clause is valid format.
        where_clause = self._base.validate.sanitize_where_clause(where_clause)

        # Delete record.
        query = 'DELETE FROM {0}{1};'.format(table_name, where_clause)
        results = self._base.query.execute(query, display_query=display_query)
        if display_results:
            self._base.display.results('{0}'.format(results))

        return results

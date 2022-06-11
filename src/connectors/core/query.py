"""
Query section of "Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.

# User Imports.
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class BaseQuery():
    """
    Abstract/generalized logic, for making row queries.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    def __init__(self, parent, *args, **kwargs):
        logger.debug('Generating related (core) Query class.')

        self._base = parent

    def execute(self, query, display_query=True):
        """"""
        if display_query:
            logger.query(query)

        # Create connection and execute query.
        cursor = self._base.connection.cursor()
        cursor.execute(query)

        # Get results.
        results = cursor.fetchall()

        # Close connection.
        self._base.connection.commit()
        cursor.close()

        # Return results.
        if results is None:
            results = []
        return results

    def select(self, table_name, select_clause=None):
        """"""
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided SELECT clause is valid format.
        if select_clause is None:
            select_clause = '*'
        if not self._base.validate.table_name(select_clause):
            raise ValueError('Invalid SELECT clause of "{0}".'.format(select_clause))

        # Select record.
        query = 'SELECT {0} FROM {1};'.format(select_clause, table_name)
        results = self.execute(query)
        logger.info('{0}'.format(query))
        logger.info('{0}'.format(results))

        return results

    def insert(self, table_name, values_clause, columns_clause=None):
        """"""
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided COLUMNS clause is valid format.
        if columns_clause is None:
            columns_clause = ''
        columns_clause = str(columns_clause).strip()
        if not self._base.validate.columns_clause(columns_clause):
            raise ValueError('Invalid COLUMNS clause of "{0}".'.format(columns_clause))

        # Check that provided VALUES clause is valid format.
        if not self._base.validate.values_clause(values_clause):
            raise ValueError('Invalid VALUES clause of "{0}".'.format(values_clause))

        # Insert record.
        query = """
        INSERT INTO {0}{1}
        VALUES {2};
        """.format(table_name, columns_clause, values_clause)
        results = self.execute(query)
        logger.info('{0}'.format(query))
        logger.info('{0}'.format(results))

        return results

    def update(self, table_name, values_clause, where_clause):
        """"""
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided VALUES clause is valid format.
        if not self._base.validate.values_clause(values_clause):
            raise ValueError('Invalid VALUES clause of "{0}".'.format(values_clause))

        # Check that provided WHERE clause is valid format.
        if not self._base.validate.columns_clause(where_clause):
            raise ValueError('Invalid WHERE clause of "{0}".'.format(where_clause))

        # Update record.
        query = """
        UPDATE {0}
        SET {1}
        WHERE {2};
        """.format(table_name, values_clause, where_clause)
        results = self.execute(query)
        logger.info('{0}'.format(query))
        logger.info('{0}'.format(results))

        return results

    def delete(self, table_name, where_clause):
        """"""
        # Check that provided table name is valid format.
        if not self._base.validate.table_name(table_name):
            raise ValueError('Invalid table name of "{0}".'.format(table_name))

        # Check that provided WHERE clause is valid format.
        if not self._base.validate.columns_clause(where_clause):
            raise ValueError('Invalid WHERE clause of "{0}".'.format(where_clause))

        # Delete record.
        query = 'DELETE FROM {0} WHERE {1};'.format(table_name, where_clause)
        results = self.execute(query)
        logger.info('{0}'.format(query))
        logger.info('{0}'.format(results))

        return results
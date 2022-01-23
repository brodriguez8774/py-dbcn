"""
Entrypoint for manually testing project logic.
"""

# System Imports.

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


def main():
    """
    Logic entrypoint for building logic + manual testing.
    """
    # Initialize db connection objects.
    mysql_connector = MysqlDbConnector(
        mysql_config['host'],
        mysql_config['port'],
        mysql_config['user'],
        mysql_config['password'],
        mysql_config['name'],
        debug=True,
    )
    postgres_connector = PostgresqlDbConnector(sqlite_config['location'], debug=True)
    sqlite_connector = SqliteDbConnector(sqlite_config['location'], debug=True)

    # Manually test logic for mysql connector.
    # mysql_connector.database._get()
    mysql_connector.database.show()
    # mysql_connector.database.use('test_database')
    # mysql_connector.database.create('this_is_test_aaa')
    # mysql_connector.database.drop('this_is_test_aaa')

    # mysql_connector.tables._get()
    # mysql_connector.tables.show()
    # mysql_connector.tables.describe('category')


if __name__ == '__main__':
    logger.info('Initializing program.')
    main()
    logger.info('Terminating program.')

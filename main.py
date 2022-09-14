"""
Entrypoint for manually testing project logic.
"""

# System Imports.

# Internal Imports.
from config import mysql_config, postgresql_config, sqlite_config
from py_dbcn.connectors import MysqlDbConnector, PostgresqlDbConnector, SqliteDbConnector
from py_dbcn.logging import init_logging


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
    postgres_connector = PostgresqlDbConnector(
        postgresql_config['host'],
        postgresql_config['port'],
        postgresql_config['user'],
        postgresql_config['password'],
        postgresql_config['name'],
        debug=True,
    )
    # sqlite_connector = SqliteDbConnector(sqlite_config['location'], debug=True)

    columns = """(
        id INT NOT NULL AUTO_INCREMENT,
        name VARCHAR(100),
        description VARCHAR(100),
        PRIMARY KEY ( id )
    )"""

    # Manually test connector logic.
    mysql_connector.database.show()
    postgres_connector.database.show()

    mysql_connector.tables.show()
    postgres_connector.tables.show()

    # # Create "category" table if not present.
    # tables = mysql_connector.tables.show()
    # if 'category' not in tables:
    #     mysql_connector.tables.create('category', columns)
    #
    # # Describe category table.
    # mysql_connector.tables.describe('category')
    #
    # # Select from category table.
    # mysql_connector.records.select('category')


if __name__ == '__main__':
    logger.info('Initializing program.')
    main()
    logger.info('Terminating program.')

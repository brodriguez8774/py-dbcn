"""
Entrypoint for building project.
"""

# System Imports.

# User Imports.
from config import mysql_config, sqlite_config
from src.connectors import MySqlConnector, SqliteConnector
from src.logging import init_logging


# Import logger.
logger = init_logging(__name__)


def main():
    """
    Logic entrypoint for building logic + manual testing.
    """
    # Initialize db connection objects.
    mysql_connector = MySqlConnector(
        mysql_config['host'],
        mysql_config['port'],
        mysql_config['user'],
        mysql_config['password'],
        mysql_config['name'],
        debug=True,
    )
    sqlite_connector = SqliteConnector(sqlite_config['location'], debug=True)


if __name__ == '__main__':
    logger.info('Initializing program.')
    main()
    logger.info('Terminating program.')

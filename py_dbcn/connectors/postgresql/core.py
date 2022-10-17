"""
PostgreSQL DB Connector class.

Contains database connection logic specific to PostgreSQL databases.
"""

# System Imports.

# Third-party Imports.
import psycopg2

# Internal Imports.
from .database import PostgresqlDatabase
from .display import PostgresqlDisplay
from .query import PostgresqlQuery
from .records import PostgresqlRecords
from .tables import PostgresqlTables
from .validate import PostgresqlValidate
from py_dbcn.connectors.core import AbstractDbConnector
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class PostgresqlDbConnector(AbstractDbConnector):
    """
    Database connector logic for PostgreSQL databases.
    """
    def __init__(self, *args, **kwargs):

        # Call parent logic.
        super().__init__(*args, **kwargs)

        # Initialize error handlers.
        self.errors.handler = psycopg2.errors
        self.errors.database_does_not_exist = self.errors.handler.InvalidCatalogName
        self.errors.database_already_exists = self.errors.handler.DuplicateDatabase
        self.errors.table_does_not_exist = self.errors.handler.UndefinedTable
        self.errors.table_already_exists = self.errors.handler.DuplicateTable

        # Initialize database connection.
        self._config.db_type = 'PostgreSQL'
        self.create_connection()

    def create_connection(self, db_name=None):
        """Attempts to create database connection, using config values.

        :param db_name: Name of database to connect to.
        """
        if db_name is None or str(db_name).strip() == '':
            # Empty value provided. Fallback to config value.
            db_name = self._config.db_name
        else:
            # Update selected db in config.
            self._config.db_name = db_name

        self._connection = psycopg2.connect(
            host=self._config.db_host,
            port=self._config.db_port,
            user=self._config.db_user,
            password=self._config.db_pass,
            dbname=db_name,
        )

        # Set to correct transaction errors.
        # Unsure if we want this set for all queries, but it seems to work at least for now.
        # https://stackoverflow.com/a/68112827
        self._connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        if self._config.display_connection_output:
            logger.info('Created PostgreSQL database connection.')

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return PostgresqlDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return PostgresqlDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return PostgresqlQuery(self)

    def _get_related_records_class(self):
        """
        Overridable method to get the related "records functionality" class.
        """
        return PostgresqlRecords(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return PostgresqlTables(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return PostgresqlValidate(self)

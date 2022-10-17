"""
MySQL DB Connector class.

Contains database connection logic specific to MySQL databases.
"""

# System Imports.

# Third-party Imports.
import MySQLdb

# Internal Imports.
from .database import MysqlDatabase
from .display import MysqlDisplay
from .query import MysqlQuery
from .records import MysqlRecords
from .tables import MysqlTables
from .utils import MysqlUtils
from .validate import MysqlValidate
from py_dbcn.connectors.core import AbstractDbConnector
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class MysqlDbConnector(AbstractDbConnector):
    """
    Database connector logic for MySQL databases.
    """
    def __init__(self, *args, **kwargs):
        # Call parent logic.
        super().__init__(*args, **kwargs)

        # Initialize error handlers.
        self.errors.handler = MySQLdb
        self.errors.database_does_not_exist = self.errors.handler.OperationalError
        self.errors.database_already_exists = self.errors.handler.ProgrammingError
        self.errors.table_does_not_exist = self.errors.handler.OperationalError
        self.errors.table_already_exists = self.errors.handler.OperationalError

        # Initialize database connection.
        self._config.db_type = 'MySQL'
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

        self._connection = MySQLdb.connect(
            host=self._config.db_host,
            port=self._config.db_port,
            user=self._config.db_user,
            password=self._config.db_pass,
            db=db_name,
        )

        if self._config.display_connection_output:
            logger.info('Created MySQL database connection.')

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return MysqlDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return MysqlDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return MysqlQuery(self)

    def _get_related_records_class(self):
        """
        Overridable method to get the related "records functionality" class.
        """
        return MysqlRecords(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return MysqlTables(self)

    def _get_related_utils_class(self):
        """
        Overridable method to get the related "utils functionality" class.
        """
        return MysqlUtils(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return MysqlValidate(self)

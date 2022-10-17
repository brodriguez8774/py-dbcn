"""
"Core" DB Connector class.

Contains generalized database connection logic.
Should be inherited by language-specific connectors.
"""

# System Imports.
from abc import ABC, abstractmethod

# Internal Imports.
from .database import BaseDatabase
from .display import BaseDisplay
from .query import BaseQuery
from .records import BaseRecords
from .tables import BaseTables
from .utils import BaseUtils
from .validate import BaseValidate
from py_dbcn.logging import init_logging


# Import logger.
logger = init_logging(__name__)


class AbstractDbConnector(ABC):
    """
    Abstract/generalized database connector logic, that is universal to all database classes.

    (As this project develops, logic will likely start here,
    and then be gradually moved to specific connectors as needed.)
    """
    @abstractmethod
    def __init__(
        self,
        db_host, db_port, db_user, db_pass, db_name, *args,
        display_connection_output=True, debug=False, **kwargs,
    ):
        logger.debug('Generating (core) Connector class.')
        db_port = int(db_port)

        self._connection = None
        self._debug = debug

        # region Config Initialization

        # Define class to hold config values.
        class Config:
            pass

        # Initialize config.
        self._config = Config()
        # Values for connecting.
        self._config.display_connection_output = display_connection_output
        self._config.db_host = db_host
        self._config.db_port = db_port
        self._config.db_user = db_user
        self._config.db_pass = db_pass
        self._config.db_name = db_name
        # Values for managing connector state.
        self._config.db_type = None
        self._config._implemented_db_types = ['MySQL', 'PostgreSQL']

        # endregion Config Initialization

        # region Error Handler Setup

        # Define class to hold error handler references.
        class Errors:
            pass

        self.errors = Errors()
        self.errors.handler = None
        self.errors.database_does_not_exist = None
        self.errors.database_already_exists = None
        self.errors.table_does_not_exist = None
        self.errors.table_already_exists = None

        # endregion Error Handler Setup

        # region Child Sub-Class Initialization

        # Create references to related subclasses.
        self.database = self._get_related_database_class()
        self.databases = self._get_related_database_class()
        self.display = self._get_related_display_class()
        self.query = self._get_related_query_class()
        self.record = self._get_related_records_class()
        self.records = self._get_related_records_class()
        self.table = self._get_related_tables_class()
        self.tables = self._get_related_tables_class()
        self.utils = self._get_related_utils_class()
        self.validate = self._get_related_validate_class()

        # endregion Child Sub-Class Initialization

    def __del__(self):
        """
        Close database connection on exit.
        """
        self.close_connection()

    def create_connection(self, db_name=None):
        """Attempts to create database connection, using config values."""
        raise NotImplementedError('Please override the connection.create_connection() function.')

    def close_connection(self):
        """Attempts to close database connection, if open.

        :param display_output: Bool indicating if output should display.
        """
        try:
            self._connection.close()
        except:
            pass

        if self._config.display_connection_output:
            logger.info('Closed {0} database connection.'.format(self._config.db_type))

    def _get_related_database_class(self):
        """
        Overridable method to get the related "database functionality" class.
        """
        return BaseDatabase(self)

    def _get_related_display_class(self):
        """
        Overridable method to get the related "display functionality" class.
        """
        return BaseDisplay(self)

    def _get_related_query_class(self):
        """
        Overridable method to get the related "query functionality" class.
        """
        return BaseQuery(self)

    def _get_related_records_class(self):
        """
        Overridable method to get the related "record functionality" class.
        """
        return BaseRecords(self)

    def _get_related_tables_class(self):
        """
        Overridable method to get the related "tables functionality" class.
        """
        return BaseTables(self)

    def _get_related_utils_class(self):
        """
        Overridable method to get the related "utility functionality" class.
        """
        return BaseUtils(self)

    def _get_related_validate_class(self):
        """
        Overridable method to get the related "validation functionality" class.
        """
        return BaseValidate(self)

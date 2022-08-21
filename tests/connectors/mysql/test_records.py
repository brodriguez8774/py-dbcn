"""
Tests for "records" logic of "MySQL" DB Connector class.
"""

# System Imports.
import textwrap

# User Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_records import CoreRecordsTestMixin


class TestMysqlRecords(TestMysqlDatabaseParent, CoreRecordsTestMixin):
    """
    Tests "MySQL" DB Connector class record logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_records'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Define default table columns.
        cls._columns_query__basic = textwrap.dedent(
            """
            (
                id INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(100),
                description VARCHAR(100),
                PRIMARY KEY ( id )
            )
            """
        ).strip()
        cls._columns_query__datetime = textwrap.dedent(
            """
            (
                id INT NOT NULL AUTO_INCREMENT,
                test_datetime DATETIME,
                test_date DATE,
                PRIMARY KEY ( id )
            )
            """
        ).strip()

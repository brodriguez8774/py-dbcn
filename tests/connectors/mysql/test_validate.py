"""
Tests for "validate" logic of "MySQL" DB Connector class.
"""

# System Imports.

# Internal Imports.
from .test_core import TestMysqlDatabaseParent
from tests.connectors.core.test_validate import CoreValidateTestMixin


class TestMysqlValidate(TestMysqlDatabaseParent, CoreValidateTestMixin):
    """
    Tests "MySQL" DB Connector class validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Also call CoreTestMixin setup logic.
        cls.set_up_class()

        # Define database name to use in tests.
        cls.test_db_name = '{0}test_validate'.format(cls.test_db_name_start)

        # Initialize database for tests.
        cls.connector.database.create(cls.test_db_name)
        cls.connector.database.use(cls.test_db_name)

        # Check that database has no tables.
        results = cls.connector.tables.show()
        if len(results) > 0:
            for result in results:
                cls.connector.tables.drop(result)

        # Import here to prevent errors if database type is not installed on system.
        from py_dbcn.connectors.mysql.validate import QUOTE_IDENTIFIER_FORMAT

        # Initialize variables.
        cls._identifier_str = '{0}{1}{0}'.format(QUOTE_IDENTIFIER_FORMAT, '{0}')

    def test__sanitize_select_clause__success(self):
        """
        Test sanitizing a SELECT clause, in cases when it should succeed.
        """
        # Verify identifier str is as we expect.
        self.assertText('`{0}`', self._identifier_str)

        # Call parent logic.
        super().test__sanitize_select_clause__success()

"""
Initialization of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.
import re, unittest
from colorama import Fore, Style

# User Imports.
from py_dbcn.connectors.core.core import AbstractDbConnector


class CoreTestParent(unittest.TestCase):
    """
    Initialization of "Core" DB Connector class logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Child inheriting class must initialize their own connector and variables.
        cls.connector = None
        cls.db_type = None
        cls.test_db_name_start = 'pydbcn__{0}_unittest__'
        cls.test_db_name = None
        cls.db_error_handler = None

    def setUp(self):
        # Run parent setup logic.
        super().setUp()

        db_name_start = 'pydbcn__{0}_unittest__'

        # Verify connector is established and variables are initialized.
        if not isinstance(self.connector, AbstractDbConnector):
            raise SystemError('Database connector does not appear to be instantiated. Cannot run tests.')

        if self.db_type is None or str(self.db_type).strip() == '':
            raise ValueError('Database type not provided. Ex: "MySQL", "SqLite", etc.')

        if self.test_db_name_start == db_name_start:
            raise ValueError(
                'Test database name not fully initialized. '
                'Please define test_db_name_start in the set_up_class() Mixin method.'
            )

        if self.test_db_name is None:
            raise ValueError(
                'Test database name not fully initialized. Please define test_db_name in child setUpClass() method.'
            )

        # Values are populated. Validate and sanitize.
        self.db_type = str(self.db_type).strip()
        self.test_db_name_start = str(self.test_db_name_start).strip()
        self.test_db_name = str(self.test_db_name).strip()

        if self.db_type not in self._implemented_db_types:
            raise ValueError('Unknown db_type provided. Please select one of: {0}'.format(self._implemented_db_types))

        if not self.test_db_name.startswith('pydbcn__'):
            raise ValueError(
                'Test database name provided, but does not start with "pydbcn__". '
                'To help avoid potential naming conflicts with pre-existing local databases, please update the name.'
            )

        if self.db_error_handler is None:
            raise ValueError(
                'To properly handle expected database query errors (for testing), please set db_error_handler as the '
                'database error management class.'
            )

    @classmethod
    def tearDownClass(cls):
        # Destroy all leftover databases created during tests.
        results = cls.connector.database.show()
        for result in results:
            if result.startswith('pydbcn__'):
                cls.connector.database.drop(result)

        # Run parent teardown logic.
        super().tearDownClass()

    def assertText(self, actual_text, expected_text):
        """Wrapper for assertEquals, that prints full values to console on mismatch.

        Note that this also strips any colored text output, to directly compare the actual text itself, not formatting.
        """

        # Strip any initial whitespace.
        actual_text = str(actual_text).strip()
        expected_text = str(expected_text).strip()

        # Strip any colorama colorings.
        actual_text = actual_text.lstrip(Fore.BLUE).lstrip(Fore.MAGENTA).rstrip(Style.RESET_ALL)
        expected_text = expected_text.lstrip(Fore.BLUE).lstrip(Fore.MAGENTA).rstrip(Style.RESET_ALL)

        # Strip any unintentional "whitespace" caused by colorama + code indentations.
        actual_text = actual_text.strip()
        expected_text = expected_text.strip()

        # Attempt assertion.
        try:
            self.assertEqual(actual_text, expected_text)
        except AssertionError as err:
            # Assertion failed. Provide debug output.
            print('\n\n\n\n')
            print('ACTUAL:')
            print(actual_text)
            print('\n')
            print('EXPECTED:')
            print(expected_text)
            print('\n\n\n\n')

            # Raise original error.
            raise AssertionError(err)

    def get_logging_output(self, log_capture, record_num):
        """Helper function to read captured logging output."""
        return str(log_capture.records[record_num].message).strip()

"""
Initialization of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.
import unittest

# Internal Imports.
from py_dbcn.connectors.core.core import AbstractDbConnector
from py_dbcn.constants import (
    OUTPUT_ACTUALS_ERROR,
    OUTPUT_ACTUALS_MATCH,
    OUTPUT_ERROR,
    OUTPUT_EXPECTED_ERROR,
    OUTPUT_EXPECTED_MATCH,
    OUTPUT_RESET,
)


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

    def assertText(self, expected_text, actual_text, strip=True):
        """Wrapper for assertEqual(), that prints full values to console on mismatch.

        :param expected_text: Expected text value to check against.
        :param actual_text: Actual text value to compare.
        :param strip: Bool indicating if outer whitespace should be stripped. Defaults to True.
        """
        # Enforce str type.
        expected_text = str(expected_text)
        actual_text = str(actual_text)

        # Handle optional cleaning params.
        if strip:
            expected_text = expected_text.strip()
            actual_text = actual_text.strip()

        # Attempt assertion.
        try:
            self.assertEqual(expected_text, actual_text)
        except AssertionError as err:
            # Assertion failed. Provide debug output.

            # Loop through to calculate color output differences.
            # First split on newlines.
            split_expected = expected_text.split('\n')
            split_actual = actual_text.split('\n')
            append_newline = False

            # Handle if either is empty.
            if len(split_expected) == 1 and split_expected[0].strip() == '':
                split_expected = []
            if len(split_actual) == 1 and split_actual[0].strip() == '':
                split_actual = []

            # Determine which one is longer.
            if len(split_actual) > len(split_expected):
                max_lines = len(split_actual)
            else:
                max_lines = len(split_expected)

            formatted_expected_output = ''
            formatted_actual_output = ''
            for line_index in range(max_lines):
                try:
                    curr_expected_line = split_expected[line_index]
                    if append_newline:
                        curr_expected_line = '\n{0}'.format(curr_expected_line)
                except IndexError:
                    curr_expected_line = None
                try:
                    curr_actual_line = split_actual[line_index]
                    if append_newline:
                        curr_actual_line = '\n{0}'.format(curr_actual_line)
                except IndexError:
                    curr_actual_line = None
                append_newline = False

                if curr_expected_line == curr_actual_line:
                    # Line is full match and correct.
                    curr_expected_line = '{0}{1}{2}\n'.format(OUTPUT_EXPECTED_MATCH, curr_expected_line, OUTPUT_RESET)
                    curr_actual_line = '{0}{1}{2}\n'.format(OUTPUT_ACTUALS_MATCH, curr_actual_line, OUTPUT_RESET)
                elif curr_expected_line is None:
                    # "Actual" output is longer than "expected" output. Impossible to match current line.
                    curr_expected_line = ''
                    curr_actual_line = '{0}{1}{2}\n'.format(
                        OUTPUT_ACTUALS_ERROR,
                        curr_actual_line,
                        OUTPUT_RESET,
                    )
                elif curr_actual_line is None:
                    # "Expected" output is longer than "actual" output. Impossible to match current line.
                    curr_expected_line = '{0}{1}{2}\n'.format(
                        OUTPUT_EXPECTED_ERROR,
                        curr_expected_line,
                        OUTPUT_RESET,
                    )
                    curr_actual_line = ''
                else:
                    # Both lines are populated but do not match.
                    # Determine which one is longer.
                    if len(curr_actual_line) > len(curr_expected_line):
                        max_chars = len(curr_actual_line)
                    else:
                        max_chars = len(curr_expected_line)

                    # Check each character and determine where non-match happens.
                    curr_expected_color = OUTPUT_RESET
                    curr_actual_color = OUTPUT_RESET
                    curr_expected_char_line = ''
                    curr_actual_char_line = ''
                    for char_index in range(max_chars):
                        # Grab current character.
                        try:
                            expected_char = curr_expected_line[char_index]
                        except IndexError:
                            expected_char = ''
                        try:
                            actual_char = curr_actual_line[char_index]
                        except IndexError:
                            actual_char = ''

                        # Format based on match.
                        if expected_char == actual_char:
                            # Match.
                            if curr_expected_color != OUTPUT_EXPECTED_MATCH:
                                curr_expected_color = OUTPUT_EXPECTED_MATCH
                                curr_expected_char_line += curr_expected_color
                            if curr_actual_color != OUTPUT_ACTUALS_MATCH:
                                curr_actual_color = OUTPUT_ACTUALS_MATCH
                                curr_actual_char_line += curr_actual_color
                        else:
                            # Non-match.
                            if curr_expected_color != OUTPUT_EXPECTED_ERROR:
                                curr_expected_color = OUTPUT_EXPECTED_ERROR
                                curr_expected_char_line += curr_expected_color
                            if curr_actual_color != OUTPUT_ACTUALS_ERROR:
                                curr_actual_color = OUTPUT_ACTUALS_ERROR
                                curr_actual_char_line += curr_actual_color

                        curr_expected_char_line += '{0}'.format(expected_char)
                        curr_actual_char_line += '{0}'.format(actual_char)

                    # Update output strings.
                    append_newline = True
                    formatted_expected_output += curr_expected_char_line
                    formatted_actual_output += curr_actual_char_line
                    continue

                # Update output strings.
                formatted_expected_output += curr_expected_line
                formatted_actual_output += curr_actual_line

            # Finally print actual debug output.
            print('')
            print('')
            print('{0}EXPECTED:{1}'.format(OUTPUT_EXPECTED_MATCH, OUTPUT_RESET))
            print(formatted_expected_output)
            print('')
            print('')
            print('{0}ACTUAL:{1}'.format(OUTPUT_ACTUALS_MATCH, OUTPUT_RESET))
            print(formatted_actual_output)
            print('')
            print('')

            # Raise original error.
            raise AssertionError(err) from err

    def get_logging_output(self, log_capture, record_num):
        """Helper function to read captured logging output."""
        return str(log_capture.records[record_num].message).strip()

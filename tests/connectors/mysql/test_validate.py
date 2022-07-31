"""
Tests for "validate" logic of "MySQL" DB Connector class.
"""

# System Imports.
import re

# User Imports.
from .test_core import TestMysqlDatabaseParent


class TestMysqlValidate(TestMysqlDatabaseParent):
    """
    Tests "MySQL" DB Connector class validation logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        cls.unallowed_char_list = [';', '\\']
        cls.unallowed_unicode_index_list = [59, 92]

    def test__identifier__success(self):
        """
        Test "general identifier" validation, when it should succeed.
        """
        with self.subTest('"Permitted characters in unquoted Identifiers"'):
            # Ensure capital letters validate.
            result = self.connector.validate._identifier('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            self.assertTrue(result[0])
            self.assertEqual(result[1], '')

            # Ensure lowercase characters validate.
            result = self.connector.validate._identifier('abcdefghijklmnopqrstuvwxyz')
            self.assertTrue(result[0])
            self.assertEqual(result[1], '')

            # Ensure integer characters validate.
            result = self.connector.validate._identifier('0123456789')
            self.assertTrue(result[0])
            self.assertEqual(result[1], '')

            # Ensure dollar and underscore validate.
            result = self.connector.validate._identifier('_$')
            self.assertTrue(result[0])
            self.assertEqual(result[1], '')

        with self.subTest('At max length - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 64)
            result = self.connector.validate._identifier(test_str)
            self.assertTrue(result[0])
            self.assertEqual(result[1], '')

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 66)
            result = self.connector.validate._identifier(test_str)
            self.assertTrue(result[0])
            self.assertEqual(result[1], '')

        with self.subTest(
            '"Permitted characters in quoted identifiers include the full Unicode Basic Multilingual Plane (BMP), '
            'except U+0000"'
        ):
            for index in range(127):
                # Skip "unacceptable" values.
                if (index + 1) in self.unallowed_unicode_index_list:
                    continue

                # Test value.
                test_str = u'`' + chr(index + 1) + u'`'
                result = self.connector.validate._identifier(test_str)
                self.assertTrue(result[0])
                self.assertEqual(result[1], '')

    def test__identifier__failure(self):
        """
        Test "general identifier" validation, when it should fail.
        """
        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 65)
            result = self.connector.validate._identifier(test_str)
            self.assertFalse(result[0])
            self.assertEqual(result[1], 'is longer than 64 characters.')

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 67)
            result = self.connector.validate._identifier(test_str)
            self.assertFalse(result[0])
            self.assertEqual(result[1], 'is longer than 64 characters.')

        with self.subTest('Invalid characters - unquoted'):
            # Check basic "unquoted problem characters".
            test_str = '!@#%^&*()-+=~\'"[]{}<>|\\/:;,.?'
            for item in test_str:
                result = self.connector.validate._identifier(item)
                self.assertFalse(result[0])
                self.assertEqual(result[1], 'does not match acceptable characters.')

            # Check project-specific "bad characters".
            for item in self.unallowed_char_list:
                result = self.connector.validate._identifier(item)
                self.assertFalse(result[0])
                self.assertEqual(result[1], 'does not match acceptable characters.')

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):

                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'{0}'.format(chr(index + 1))
                result = self.connector.validate._identifier(test_str)
                self.assertFalse(result[0])
                self.assertEqual(result[1], 'does not match acceptable characters.')

        with self.subTest('Invalid characters - quoted'):
            # Check that hex 0 is invalid.
            result = self.connector.validate._identifier(u'`' + chr(0) + u'`')
            self.assertFalse(result[0])
            self.assertEqual(result[1], 'does not match acceptable characters.')

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):
                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'`' + chr(index + 1) + u'`'
                result = self.connector.validate._identifier(test_str)
                self.assertFalse(result[0])
                self.assertEqual(result[1], 'does not match acceptable characters.')

    def test__database_name__success(self):
        """
        Test "database name" validation, when it should succeed.
        """
        with self.subTest('"Permitted characters in unquoted Identifiers"'):
            # Ensure capital letters validate.
            self.assertTrue(self.connector.validate.database_name('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

            # Ensure lowercase characters validate.
            self.assertTrue(self.connector.validate.database_name('abcdefghijklmnopqrstuvwxyz'))

            # Ensure integer characters validate.
            self.assertTrue(self.connector.validate.database_name('0123456789'))

            # Ensure dollar and underscore validate.
            self.assertTrue(self.connector.validate.database_name('_$'))

        with self.subTest('At max length - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 64)
            self.assertTrue(self.connector.validate.database_name(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 66)
            self.assertTrue(self.connector.validate.database_name(test_str))

        with self.subTest(
            '"Permitted characters in quoted identifiers include the full Unicode Basic Multilingual Plane (BMP), '
            'except U+0000"'
        ):
            for index in range(127):
                # Skip "unacceptable" values.
                if (index + 1) in self.unallowed_unicode_index_list:
                    continue

                # Test value.
                test_str = u'`' + chr(index + 1) + u'`'
                self.assertTrue(self.connector.validate.database_name(test_str))

    def test__database_name__failure(self):
        """
        Test "database name" validation, when it should fail.
        """
        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 65)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name(test_str)
            self.assertIn('Invalid database name of "', str(err.exception))
            self.assertIn('". Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 67)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name(test_str)
            self.assertIn('Invalid database name of ', str(err.exception))
            self.assertIn('. Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Invalid characters - unquoted'):
            # Check basic "unquoted problem characters".
            test_str = '!@#%^&*()-+=~\'"[]{}<>|\\/:;,.?'
            for item in test_str:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.database_name(item)
                self.assertIn('Invalid database name of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

            # Check project-specific "bad characters".
            for item in self.unallowed_char_list:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.database_name(item)
                self.assertIn('Invalid database name of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):

                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'{0}'.format(chr(index + 1))
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.database_name(test_str)
                self.assertIn('Invalid database name of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

        with self.subTest('Invalid characters - quoted'):
            # Check that hex 0 is invalid.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name(u'`' + chr(0) + u'`')
            self.assertIn('Invalid database name of ', str(err.exception))
            self.assertIn('. Name does not match acceptable characters.', str(err.exception))

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):
                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'`' + chr(index + 1) + u'`'
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.database_name(test_str)
                self.assertIn('Invalid database name of ', str(err.exception))
                self.assertIn('. Name does not match acceptable characters.', str(err.exception))

    def test__table_name__success(self):
        """
        Test "table name" validation, when it should succeed.
        """
        with self.subTest('"Permitted characters in unquoted Identifiers"'):
            # Ensure capital letters validate.
            self.assertTrue(self.connector.validate.table_name('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

            # Ensure lowercase characters validate.
            self.assertTrue(self.connector.validate.table_name('abcdefghijklmnopqrstuvwxyz'))

            # Ensure integer characters validate.
            self.assertTrue(self.connector.validate.table_name('0123456789'))

            # Ensure dollar and underscore validate.
            self.assertTrue(self.connector.validate.table_name('_$'))

        with self.subTest('At max length - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 64)
            self.assertTrue(self.connector.validate.table_name(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 66)
            self.assertTrue(self.connector.validate.table_name(test_str))

        with self.subTest(
            '"Permitted characters in quoted identifiers include the full Unicode Basic Multilingual Plane (BMP), '
            'except U+0000"'
        ):
            for index in range(127):
                # Skip "unacceptable" values.
                if (index + 1) in self.unallowed_unicode_index_list:
                    continue

                # Test value.
                test_str = u'`' + chr(index + 1) + u'`'
                self.assertTrue(self.connector.validate.table_name(test_str))

    def test__table_name__failure(self):
        """
        Test "table name" validation, when it should fail.
        """
        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 65)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name(test_str)
            self.assertIn('Invalid table name of "', str(err.exception))
            self.assertIn('". Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 67)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name(test_str)
            self.assertIn('Invalid table name of ', str(err.exception))
            self.assertIn('. Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Invalid characters - unquoted'):
            # Check basic "unquoted problem characters".
            test_str = '!@#%^&*()-+=~\'"[]{}<>|\\/:;,.?'
            for item in test_str:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_name(item)
                self.assertIn('Invalid table name of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

            # Check project-specific "bad characters".
            for item in self.unallowed_char_list:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_name(item)
                self.assertIn('Invalid table name of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):

                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'{0}'.format(chr(index + 1))
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_name(test_str)
                self.assertIn('Invalid table name of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

        with self.subTest('Invalid characters - quoted'):
            # Check that hex 0 is invalid.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name(u'`' + chr(0) + u'`')
            self.assertIn('Invalid table name of ', str(err.exception))
            self.assertIn('. Name does not match acceptable characters.', str(err.exception))

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):
                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'`' + chr(index + 1) + u'`'
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_name(test_str)
                self.assertIn('Invalid table name of ', str(err.exception))
                self.assertIn('. Name does not match acceptable characters.', str(err.exception))

    def test__table_column__success(self):
        """
        Test "table column" validation, when it should succeed.
        """
        with self.subTest('"Permitted characters in unquoted Identifiers"'):
            # Ensure capital letters validate.
            self.assertTrue(self.connector.validate.table_column('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

            # Ensure lowercase characters validate.
            self.assertTrue(self.connector.validate.table_column('abcdefghijklmnopqrstuvwxyz'))

            # Ensure integer characters validate.
            self.assertTrue(self.connector.validate.table_column('0123456789'))

            # Ensure dollar and underscore validate.
            self.assertTrue(self.connector.validate.table_column('_$'))

        with self.subTest('At max length - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 64)
            self.assertTrue(self.connector.validate.table_column(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 66)
            self.assertTrue(self.connector.validate.table_column(test_str))

        with self.subTest(
            '"Permitted characters in quoted identifiers include the full Unicode Basic Multilingual Plane (BMP), '
            'except U+0000"'
        ):
            for index in range(127):
                # Skip "unacceptable" values.
                if (index + 1) in self.unallowed_unicode_index_list:
                    continue

                # Test value.
                test_str = u'`' + chr(index + 1) + u'`'
                self.assertTrue(self.connector.validate.table_column(test_str))

    def test__table_column__failure(self):
        """
        Test "table column" validation, when it should fail.
        """
        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertEqual(len(test_str), 65)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column(test_str)
            self.assertIn('Invalid table column of "', str(err.exception))
            self.assertIn('". Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertEqual(len(test_str), 67)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column(test_str)
            self.assertIn('Invalid table column of ', str(err.exception))
            self.assertIn('. Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Invalid characters - unquoted'):
            # Check basic "unquoted problem characters".
            test_str = '!@#%^&*()-+=~\'"[]{}<>|\\/:;,.?'
            for item in test_str:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_column(item)
                self.assertIn('Invalid table column of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

            # Check project-specific "bad characters".
            for item in self.unallowed_char_list:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_column(item)
                self.assertIn('Invalid table column of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):

                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'{0}'.format(chr(index + 1))
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_column(test_str)
                self.assertIn('Invalid table column of "', str(err.exception))
                self.assertIn('". Name does not match acceptable characters.', str(err.exception))

        with self.subTest('Invalid characters - quoted'):
            # Check that hex 0 is invalid.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column(u'`' + chr(0) + u'`')
            self.assertIn('Invalid table column of ', str(err.exception))
            self.assertIn('. Name does not match acceptable characters.', str(err.exception))

            # For now, "extended" range is considered invalid.
            # Not sure if we'll want to enable this at some point?
            for index in range(65535):
                # Skip "acceptable" values.
                if index + 1 <= 127:
                    continue

                # Check len of str with new value added.
                test_str = u'`' + chr(index + 1) + u'`'
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_column(test_str)
                self.assertIn('Invalid table column of ', str(err.exception))
                self.assertIn('. Name does not match acceptable characters.', str(err.exception))

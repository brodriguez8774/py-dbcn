"""
Initialization of "validate" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# User Imports.


class CoreValidateTestMixin:
    """
    Tests "Core" DB Connector class validation logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)

        # Initialize variables.
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
            self.assertText(result[1], '')

            # Ensure lowercase characters validate.
            result = self.connector.validate._identifier('abcdefghijklmnopqrstuvwxyz')
            self.assertTrue(result[0])
            self.assertText(result[1], '')

            # Ensure integer characters validate.
            result = self.connector.validate._identifier('0123456789')
            self.assertTrue(result[0])
            self.assertText(result[1], '')

            # Ensure dollar and underscore validate.
            result = self.connector.validate._identifier('_$')
            self.assertTrue(result[0])
            self.assertText(result[1], '')

        with self.subTest('At max length - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertText(len(test_str), 64)
            result = self.connector.validate._identifier(test_str)
            self.assertTrue(result[0])
            self.assertText(result[1], '')

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 66)
            result = self.connector.validate._identifier(test_str)
            self.assertTrue(result[0])
            self.assertText(result[1], '')

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
                self.assertText(result[1], '')

    def test__identifier__failure(self):
        """
        Test "general identifier" validation, when it should fail.
        """
        with self.subTest('Identifier is null'):
            result = self.connector.validate._identifier(None)
            self.assertFalse(result[0])
            self.assertText(result[1], 'is None.')

        with self.subTest('Identifier too short - unquoted'):
            # Actually empty.
            result = self.connector.validate._identifier('')
            self.assertFalse(result[0])
            self.assertText(result[1], 'is empty.')

            # Empty after strip().
            result = self.connector.validate._identifier('   ')
            self.assertFalse(result[0])
            self.assertText(result[1], 'is empty.')

        with self.subTest('Identifier too short - quoted'):
            # Actually empty.
            result = self.connector.validate._identifier('``')
            self.assertFalse(result[0])
            self.assertText(result[1], 'is empty.')

        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertText(len(test_str), 65)
            result = self.connector.validate._identifier(test_str)
            self.assertFalse(result[0])
            self.assertText(result[1], 'is longer than 64 characters.\n Identifier is: {0}'.format(test_str))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 67)
            result = self.connector.validate._identifier(test_str)
            self.assertFalse(result[0])
            self.assertText(result[1], 'is longer than 64 characters.\n Identifier is: {0}'.format(test_str))

        with self.subTest('Invalid characters - unquoted'):
            # Check basic "unquoted problem characters".
            test_str = '!@#%^&*()-+=~\'"[]{}<>|\\/:;,.?'
            for item in test_str:
                result = self.connector.validate._identifier(item)
                self.assertFalse(result[0])
                self.assertText(
                    result[1],
                    'does not match acceptable characters.\n Identifier is: {0}'.format(item),
                )

            # Check project-specific "bad characters".
            for item in self.unallowed_char_list:
                result = self.connector.validate._identifier(item)
                self.assertFalse(result[0])
                self.assertText(
                    result[1],
                    'does not match acceptable characters.\n Identifier is: {0}'.format(item),
                )

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
                # Message changes based on if value was stripped away or not.
                if len(test_str.strip()) > 0:
                    self.assertText(result[1], 'does not match acceptable characters.\n Identifier is: {0}'.format(test_str))
                else:
                    self.assertText(result[1], 'is empty.')

        with self.subTest('Invalid characters - quoted'):
            # Check that hex 0 is invalid.
            result = self.connector.validate._identifier(u'`' + chr(0) + u'`')
            self.assertFalse(result[0])
            self.assertIn('does not match acceptable characters.\n Identifier is: ', result[1])

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
                self.assertText(result[1], 'does not match acceptable characters.\n Identifier is: {0}'.format(test_str))

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
            self.assertText(len(test_str), 64)
            self.assertTrue(self.connector.validate.database_name(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 66)
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
        with self.subTest('Identifier is null'):
            with self.assertRaises(TypeError) as err:
                self.connector.validate.database_name(None)
            self.assertText('Invalid database name. Is None.', str(err.exception))

        with self.subTest('Identifier too short - unquoted'):
            # Actually empty.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name('')
            self.assertIn('Invalid database name of ', str(err.exception))
            self.assertIn('. Name is empty.', str(err.exception))

            # Empty after strip().
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name('   ')
            self.assertIn('Invalid database name of ', str(err.exception))
            self.assertIn('. Name is empty.', str(err.exception))

        with self.subTest('Identifier too short - quoted'):
            # Actually empty.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name('``')
            self.assertIn('Invalid database name of ', str(err.exception))
            self.assertIn('. Name is empty.', str(err.exception))

        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertText(len(test_str), 65)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.database_name(test_str)
            self.assertIn('Invalid database name of "', str(err.exception))
            self.assertIn('". Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 67)
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
                # Message changes based on if value was stripped away or not.
                if len(test_str.strip()) > 0:
                    self.assertIn('Invalid database name of "', str(err.exception))
                    self.assertIn('". Name does not match acceptable characters.', str(err.exception))
                else:
                    self.assertIn('Invalid database name of "', str(err.exception))
                    self.assertIn('". Name is empty.', str(err.exception))

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
            self.assertText(len(test_str), 64)
            self.assertTrue(self.connector.validate.table_name(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 66)
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
        with self.subTest('Identifier is null'):
            with self.assertRaises(TypeError) as err:
                self.connector.validate.table_name(None)
            self.assertText('Invalid table name. Is None.', str(err.exception))

        with self.subTest('Identifier too short - unquoted'):
            # Actually empty.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name('')
            self.assertIn('Invalid table name of ', str(err.exception))
            self.assertIn('. Name is empty.', str(err.exception))

            # Empty after strip().
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name('   ')
            self.assertIn('Invalid table name of ', str(err.exception))
            self.assertIn('. Name is empty.', str(err.exception))

        with self.subTest('Identifier too short - quoted'):
            # Actually empty.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name('``')
            self.assertIn('Invalid table name of ', str(err.exception))
            self.assertIn('. Name is empty.', str(err.exception))

        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertText(len(test_str), 65)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_name(test_str)
            self.assertIn('Invalid table name of "', str(err.exception))
            self.assertIn('". Name is longer than 64 characters.', str(err.exception))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 67)
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
                # Message changes based on if value was stripped away or not.
                if len(test_str.strip()) > 0:
                    self.assertIn('Invalid table name of "', str(err.exception))
                    self.assertIn('". Name does not match acceptable characters.', str(err.exception))
                else:
                    self.assertIn('Invalid table name of "', str(err.exception))
                    self.assertIn('". Name is empty.', str(err.exception))

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
            self.assertText(len(test_str), 64)
            self.assertTrue(self.connector.validate.table_column(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 66)
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
        with self.subTest('Identifier is null'):
            with self.assertRaises(TypeError) as err:
                self.connector.validate.table_column(None)
            self.assertText('Invalid table column. Is None.', str(err.exception))

        with self.subTest('Identifier too short - unquoted'):
            # Actually empty.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column('')
            self.assertIn('Invalid table column of ', str(err.exception))
            self.assertIn('. Column is empty.', str(err.exception))

            # Empty after strip().
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column('   ')
            self.assertIn('Invalid table column of ', str(err.exception))
            self.assertIn('. Column is empty.', str(err.exception))

        with self.subTest('Identifier too short - quoted'):
            # Actually empty.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column('``')
            self.assertIn('Invalid table column of', str(err.exception))
            self.assertIn('. Column is empty.', str(err.exception))

        with self.subTest('Identifier too long - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertText(len(test_str), 65)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column(test_str)
            self.assertIn('Invalid table column of "', str(err.exception))
            self.assertIn('". Column is longer than 64 characters.', str(err.exception))

        with self.subTest('Identifier too long - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 67)
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column(test_str)
            self.assertIn('Invalid table column of ', str(err.exception))
            self.assertIn('. Column is longer than 64 characters.', str(err.exception))

        with self.subTest('Invalid characters - unquoted'):
            # Check basic "unquoted problem characters".
            test_str = '!@#%^&*()-+=~\'"[]{}<>|\\/:;,.?'
            for item in test_str:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_column(item)
                self.assertIn('Invalid table column of "', str(err.exception))
                self.assertIn('". Column does not match acceptable characters.', str(err.exception))

            # Check project-specific "bad characters".
            for item in self.unallowed_char_list:
                with self.assertRaises(ValueError) as err:
                    self.connector.validate.table_column(item)
                self.assertIn('Invalid table column of "', str(err.exception))
                self.assertIn('". Column does not match acceptable characters.', str(err.exception))

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
                # Message changes based on if value was stripped away or not.
                if len(test_str.strip()) > 0:
                    self.assertIn('Invalid table column of "', str(err.exception))
                    self.assertIn('". Column does not match acceptable characters.', str(err.exception))
                else:
                    self.assertIn('Invalid table column of "', str(err.exception))
                    self.assertIn('". Column is empty.', str(err.exception))

        with self.subTest('Invalid characters - quoted'):
            # Check that hex 0 is invalid.
            with self.assertRaises(ValueError) as err:
                self.connector.validate.table_column(u'`' + chr(0) + u'`')
            self.assertIn('Invalid table column of ', str(err.exception))
            self.assertIn('. Column does not match acceptable characters.', str(err.exception))

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
                self.assertIn('. Column does not match acceptable characters.', str(err.exception))

    def test__validate_columns__invalid_type(self):
        """
        Tests column validation logic, using invalid type.
        """
        with self.subTest('With None type'):
            with self.assertRaises(TypeError):
                self.connector.validate.table_columns(None)

        with self.subTest('With int type'):
            with self.assertRaises(TypeError):
                self.connector.validate.table_columns(1)

        with self.subTest('With list type'):
            with self.assertRaises(TypeError):
                self.connector.validate.table_columns(['id INT'])

        with self.subTest('With tuple type'):
            with self.assertRaises(TypeError):
                self.connector.validate.table_columns(('id INT',))

    def test__validate_columns__str(self):
        """
        Tests column validation logic, using str object.
        """
        with self.subTest('Minimal value'):
            self.assertEqual(
                self.connector.validate.table_columns('id INT'),
                '( id INT )',
            )

        with self.subTest('Multi-value'):
            self.assertEqual(
                self.connector.validate.table_columns(
                    'id INT NOT NULL AUTO_INCREMENT, '
                    'title VARCHAR(100) NOT NULL, '
                    'description VARCHAR(255) NOT NULL'
                ),
                '( '
                'id INT NOT NULL AUTO_INCREMENT, '
                'title VARCHAR(100) NOT NULL, '
                'description VARCHAR(255) NOT NULL '
                ')'
            )

        with self.subTest('With bad value'):
            with self.assertRaises(ValueError):
                self.connector.validate.table_columns('id INT;')

    def test__validate_columns__dict(self):
        """
        Tests column validation logic, using dict object.
        """
        with self.subTest('Minimal value'):
            self.assertEqual(
                self.connector.validate.table_columns({'id': 'INT'}),
                '( id INT )',
            )

        with self.subTest('Multi-value'):
            self.assertEqual(
                self.connector.validate.table_columns({
                    'id': 'INT NOT NULL AUTO_INCREMENT',
                    'title': 'VARCHAR(100) NOT NULL',
                    'description': 'VARCHAR(255) NOT NULL',
                }),
                '( '
                'id INT NOT NULL AUTO_INCREMENT, '
                'title VARCHAR(100) NOT NULL, '
                'description VARCHAR(255) NOT NULL '
                ')'
            )

        with self.subTest('With bad key'):
            with self.assertRaises(ValueError):
                self.connector.validate.table_columns({'id;': 'INT'})

        with self.subTest('With bad value'):
            with self.assertRaises(ValueError):
                self.connector.validate.table_columns({'id': 'INT;'})

    def test__sanitize_select_clause__success(self):
        """"""
        # None provided. Defaults back to "*".
        result = self.connector.validate.sanitize_select_clause(None)
        self.assertEqual(result, '*')

        # All flag provided.
        result = self.connector.validate.sanitize_select_clause('*')
        self.assertEqual(result, '*')

        with self.subTest('Values as str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause('id')
            self.assertEqual(result, '`id`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause(' id ')
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause('id, name')
            self.assertEqual(result, '`id`, `name`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause(' id ,  name ')
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause('id, name, code')
            self.assertEqual(result, '`id`, `name`, `code`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause(' id ,  name ,  code ')
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as triple str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause("""id""")
            self.assertEqual(result, '`id`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause(""" id """)
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause("""id, name""")
            self.assertEqual(result, '`id`, `name`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause(""" id ,  name """)
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause("""id, name, code""")
            self.assertEqual(result, '`id`, `name`, `code`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause(""" id ,  name ,  code """)
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as list - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(['id'])
            self.assertEqual(result, '`id`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause([' id '])
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(['id', 'name'])
            self.assertEqual(result, '`id`, `name`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause([' id ', ' name '])
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(['id', 'name', 'code'])
            self.assertEqual(result, '`id`, `name`, `code`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause([' id ', ' name ', ' code '])
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as tuple - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(('id',))
            self.assertEqual(result, '`id`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause((' id ',))
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(('id', 'name'))
            self.assertEqual(result, '`id`, `name`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause((' id ', ' name '))
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(('id', 'name', 'code'))
            self.assertEqual(result, '`id`, `name`, `code`')
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_clause((' id ', ' name ', ' code '))
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as str - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause("'id'")
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause("'id', 'name'")
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause("'id', 'name', 'code'")
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as list - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(["'id'"])
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(["'id'", "'name'"])
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(["'id'", "'name'", "'code'"])
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as tuple - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(("'id'",))
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(("'id'", "'name'"))
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(("'id'", "'name'", "'code'"))
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as str - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause('"id"')
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause('"id", "name"')
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause('"id", "name", code')
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as list - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(['"id"'])
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(['"id"', '"name"'])
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(['"id"', '"name"', '"code"'])
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as tuple - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(('"id"',))
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(('"id"', '"name"'))
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(('"id"', '"name"', '"code"'))
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as str - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause('`id`')
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause('`id`, `name`')
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause('`id`, `name`, `code`')
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as list - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(['`id`'])
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(['`id`', '`name`'])
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(['`id`', '`name`', '`code`'])
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as tuple - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_clause(('`id`',))
            self.assertEqual(result, '`id`')

            # Two vals provided.
            result = self.connector.validate.sanitize_select_clause(('`id`', '`name`'))
            self.assertEqual(result, '`id`, `name`')

            # Three vals provided.
            result = self.connector.validate.sanitize_select_clause(('`id`', '`name`', '`code`'))
            self.assertEqual(result, '`id`, `name`, `code`')

        with self.subTest('Values as non-standard types'):
            result = self.connector.validate.sanitize_select_clause((1, True))
            self.assertEqual(result, '`1`, `True`')

        with self.subTest('Values with function calls'):
            # Uppercase.
            result = self.connector.validate.sanitize_select_clause('COUNT(*)')
            self.assertEqual(result, 'COUNT(*)')

            # Lowercase.
            result = self.connector.validate.sanitize_select_clause('count(*)')
            self.assertEqual(result, 'COUNT(*)')

    def test__sanitize_select_clause__failure(self):
        """"""
        # Param "*" provided with other values.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause('* , id')
        self.assertEqual('SELECT clause provided * with other params. * is only valid alone.', str(err.exception))

        # Mistmatching quotes - double then single.
        identifier = """\"id'"""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause(identifier)
        self.assertEqual(
            'Invalid SELECT identifier. Identifier does not match acceptable characters.\n Identifier is: "id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then double.
        identifier = """'id\""""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause(identifier)
        self.assertEqual(
            'Invalid SELECT identifier. Identifier does not match acceptable characters.\n Identifier is: \'id"',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then single.
        identifier = "`id'"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause(identifier)
        self.assertEqual(
            'Invalid SELECT identifier. Identifier does not match acceptable characters.\n Identifier is: `id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then backtick.
        identifier = "'id`"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause(identifier)
        self.assertEqual(
            'Invalid SELECT identifier. Identifier does not match acceptable characters.\n Identifier is: \'id`',
            str(err.exception),
        )

        # Mistmatching quotes - double then backtick.
        identifier = '"id`'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause(identifier)
        self.assertEqual(
            'Invalid SELECT identifier. Identifier does not match acceptable characters.\n Identifier is: "id`',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then double.
        identifier = '`id"'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_clause(identifier)
        self.assertEqual(
            'Invalid SELECT identifier. Identifier does not match acceptable characters.\n Identifier is: `id"',
            str(err.exception),
        )

    def test__is_quoted__true(self):
        """
        Tests is_quoted() function, when return value should be True.
        """
        # Basic strings.
        self.assertTrue(self.connector.validate._is_quoted('"True"'))
        self.assertTrue(self.connector.validate._is_quoted("'True'"))
        self.assertTrue(self.connector.validate._is_quoted('`True`'))

        # With spaces.
        self.assertTrue(self.connector.validate._is_quoted('"True False"'))
        self.assertTrue(self.connector.validate._is_quoted("'True False'"))
        self.assertTrue(self.connector.validate._is_quoted('`True False`'))

        # And commas.
        self.assertTrue(self.connector.validate._is_quoted('"True, False"'))
        self.assertTrue(self.connector.validate._is_quoted("'True, False'"))
        self.assertTrue(self.connector.validate._is_quoted('`True, False`'))

    def test__is_quoted__false(self):
        """
        Tests is_quoted() function, when return val should be False.
        """
        # Boolean type.
        self.assertFalse(self.connector.validate._is_quoted(True))

        # Integer type.
        self.assertFalse(self.connector.validate._is_quoted(1))

        # Basic strings.
        self.assertFalse(self.connector.validate._is_quoted('True'))

        # With spaces.
        self.assertFalse(self.connector.validate._is_quoted('True False'))

        # And commas.
        self.assertFalse(self.connector.validate._is_quoted('True, False'))


"""
Initialization of "validate" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# Internal Imports.


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
        cls._quote_columns_format = None
        cls._quote_select_identifier_format = None
        cls._quote_str_literal_format = None

    # def sql_injection(self):
    #     with self.subTest('SQL Injection - Drop database'):
    #         with self.assertRaises():
    #             self.connector.
    #             self.connector.validate.validate_select_clause('DROP DATABASE {0}'.format(self.test_db_name_start))
    #
    #     with self.subTest('SQL Injection - Drop table'):
    #         with self.assertRaises():
    #             self.connector.validate.validate_select_clause('DROP DATABASE {0}'.format(self.test_db_name_start))



    def test__column_quote_format(self):
        raise NotImplementedError('Check for column quote formatting not implemented.')

    def test__select_identifier_quote_format(self):
        raise NotImplementedError('Check for SELECT identifier quote formatting not implemented.')

    def test__order_by_quote_format(self):
        raise NotImplementedError('Check for order by quote formatting not implemented.')

    def test__str_literal_quote_format(self):
        raise NotImplementedError('Check for str literal quote formatting not implemented.')

    # region Validation Functions

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
            self.assertText(
                self.connector.validate.table_columns('id INT'),
                '( id INT )',
            )

        with self.subTest('Multi-value'):
            self.assertText(
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
            self.assertText(
                self.connector.validate.table_columns({'id': 'INT'}),
                '( id INT )',
            )

        with self.subTest('Multi-value'):
            self.assertText(
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

    def test__validate_select_clause__success(self):
        """"""

    def test__validate_select_clause__failure(self):
        """"""

    def test__validate_columns_clause__success(self):
        """
        Test "table column" individual value validation, when it should succeed.
        """
        with self.subTest('"Permitted characters in unquoted Identifiers"'):
            # Ensure capital letters validate.
            self.assertTrue(self.connector.validate.validate_columns_clause('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))

            # Ensure lowercase characters validate.
            self.assertTrue(self.connector.validate.validate_columns_clause('abcdefghijklmnopqrstuvwxyz'))

            # Ensure integer characters validate.
            self.assertTrue(self.connector.validate.validate_columns_clause('0123456789'))

            # Ensure dollar and underscore validate.
            self.assertTrue(self.connector.validate.validate_columns_clause('_$'))

        with self.subTest('At max length - unquoted'):
            test_str = 'Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
            self.assertText(len(test_str), 64)
            self.assertTrue(self.connector.validate.validate_columns_clause(test_str))

        with self.subTest('At max length - quoted'):
            test_str = '`Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`'
            self.assertText(len(test_str), 66)
            self.assertTrue(self.connector.validate.validate_columns_clause(test_str))

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
                self.assertTrue(self.connector.validate.validate_columns_clause(test_str))

        with self.subTest('Basic common column values - As-is'):
            self.assertTrue(self.connector.validate.validate_columns_clause('name'))
            self.assertTrue(self.connector.validate.validate_columns_clause('description'))
            self.assertTrue(self.connector.validate.validate_columns_clause('id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('code'))
            self.assertTrue(self.connector.validate.validate_columns_clause('size'))
            self.assertTrue(self.connector.validate.validate_columns_clause('type'))
            self.assertTrue(self.connector.validate.validate_columns_clause('quantity'))
            self.assertTrue(self.connector.validate.validate_columns_clause('qty'))
            self.assertTrue(self.connector.validate.validate_columns_clause('status'))
            self.assertTrue(self.connector.validate.validate_columns_clause('order'))
            self.assertTrue(self.connector.validate.validate_columns_clause('order_id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('invoice'))
            self.assertTrue(self.connector.validate.validate_columns_clause('invoice_id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('load'))
            self.assertTrue(self.connector.validate.validate_columns_clause('load_id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('location'))
            self.assertTrue(self.connector.validate.validate_columns_clause('location_id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('product'))
            self.assertTrue(self.connector.validate.validate_columns_clause('product_id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('item'))
            self.assertTrue(self.connector.validate.validate_columns_clause('item_id'))
            self.assertTrue(self.connector.validate.validate_columns_clause('date_created'))
            self.assertTrue(self.connector.validate.validate_columns_clause('date_modified'))
            self.assertTrue(self.connector.validate.validate_columns_clause('last_edited'))
            self.assertTrue(self.connector.validate.validate_columns_clause('last_active'))
            self.assertTrue(self.connector.validate.validate_columns_clause('last_activity'))
            self.assertTrue(self.connector.validate.validate_columns_clause('active'))
            self.assertTrue(self.connector.validate.validate_columns_clause('is_active'))

        with self.subTest('Basic common column values - With Single Quotes'):
            # Standard Values.
            self.assertTrue(self.connector.validate.validate_columns_clause("'name'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'description'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'code'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'size'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'type'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'quantity'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'qty'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'status'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'order'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'order_id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'invoice'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'invoice_id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'load'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'load_id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'location'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'location_id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'product'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'product_id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'item'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'item_id'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'date_created'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'date_modified'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'last_edited'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'last_active'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'last_activity'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'active'"))
            self.assertTrue(self.connector.validate.validate_columns_clause("'is_active'"))

            # Keyword values that fail without quotes, but succeed here.
            self.assertTrue(self.connector.validate.validate_columns_clause("'desc'"))

        with self.subTest('Basic common column values - With Double Quotes'):
            # Standard values.
            self.assertTrue(self.connector.validate.validate_columns_clause('"name"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"description"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"code"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"size"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"type"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"quantity"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"qty"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"status"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"order"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"order_id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"invoice"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"invoice_id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"load"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"load_id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"location"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"location_id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"product"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"product_id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"item"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"item_id"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"date_created"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"date_modified"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"last_edited"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"last_active"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"last_activity"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"active"'))
            self.assertTrue(self.connector.validate.validate_columns_clause('"is_active"'))

            # Keyword values that fail without quotes, but succeed here.
            self.assertTrue(self.connector.validate.validate_columns_clause('"desc"'))

        with self.subTest('Basic common column values - With Backtick Quotes'):
            # Standard values.
            self.assertTrue(self.connector.validate.validate_columns_clause('`name`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`description`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`code`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`size`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`type`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`quantity`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`qty`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`status`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`order`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`order_id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`invoice`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`invoice_id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`load`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`load_id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`location`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`location_id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`product`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`product_id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`item`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`item_id`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`date_created`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`date_modified`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`last_edited`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`last_active`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`last_activity`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`active`'))
            self.assertTrue(self.connector.validate.validate_columns_clause('`is_active`'))

            # Keyword values that fail without quotes, but succeed here.
            self.assertTrue(self.connector.validate.validate_columns_clause('`desc`'))

        with self.subTest('Special cases'):
            # Contains space.
            self.assertTrue(self.connector.validate.validate_columns_clause('"test value"'))

            # Contains inner apostraphe.
            self.assertTrue(self.connector.validate.validate_columns_clause('"Customer\'s Price"'))

            # Contains inner quotes.
            self.assertTrue(self.connector.validate.validate_columns_clause('"John "Spaceman" Johnny"'))

    def test__validate_columns_clause__failure(self):
        """"""
        # # Test none.
        # self.assertFalse(self.connector.validate.validate_columns_clause(None))
        #
        # # Test empty str.
        # self.assertFalse(self.connector.validate.validate_columns_clause(''))

        with self.subTest('Common column keyword values that will fail without quotes'):
            with self.assertRaises(ValueError) as err:
                self.assertFalse(self.connector.validate.validate_columns_clause('desc'))
            self.assertText(
                (
                    'Invalid table column of "desc". Column matches a known keyword. '
                    'Must be quoted to use this value. Identifier is: desc'
                ),
                str(err.exception)
            )

    def test__validate_where_clause__success(self):
        """"""

    def test__validate_where_clause__failure(self):
        """"""

    def test__validate_values_clause__success(self):
        """"""

    def test__validate_values_clause__failure(self):
        """"""

    def test__validate_order_by_clause__success(self):
        """"""

    def test__validate_order_by_clause__failure(self):
        """"""

    def test__validate_limit_by_clause__success(self):
        """"""

    def test__validate_limit_by_clause__failure(self):
        """"""

    # endregion Validation Functions


    # region Sanitization Functions

    def test__sanitize_select_identifier_clause__success(self):
        """
        Test sanitizing a SELECT clause, in cases when it should succeed.

        For the most part, we test that the library gracefully handles any of
        the "standard" database quote types (', ", and `), and then properly
        converts it to the actual type/format as expected by the given database.
        """
        if self._quote_select_identifier_format is None:
            TypeError('Invalid _select_identifier_clause_format_str variable. Is None.')

        # None provided. Defaults back to "*".
        result = self.connector.validate.sanitize_select_identifier_clause(None)
        self.assertText(result, '*')

        # All flag provided.
        result = self.connector.validate.sanitize_select_identifier_clause('*')
        self.assertText(result, '*')

        with self.subTest('Values as str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause('id')
            self.assertText(result, self._quote_select_identifier_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause(' id ')
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause('id, name')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name')
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause(' id ,  name ')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause('id, name, code')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause(' id ,  name ,  code ')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as triple str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause("""id""")
            self.assertText(result, self._quote_select_identifier_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause(""" id """)
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause("""id, name""")
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause(""" id ,  name """)
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause("""id, name, code""")
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause(""" id ,  name ,  code """)
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as list - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['id'])
            self.assertText(result, self._quote_select_identifier_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause([' id '])
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['id', 'name'])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause([' id ', ' name '])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['id', 'name', 'code'])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause([' id ', ' name ', ' code '])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('id',))
            self.assertText(result, self._quote_select_identifier_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause((' id ',))
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('id', 'name'))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause((' id ', ' name '))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('id', 'name', 'code'))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_select_identifier_clause((' id ', ' name ', ' code '))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause("'id'")
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause("'id', 'name'")
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause("'id', 'name', 'code'")
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code')
                ),
            )

        with self.subTest('Values as list - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(["'id'"])
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(["'id'", "'name'"])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(["'id'", "'name'", "'code'"])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(("'id'",))
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(("'id'", "'name'"))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(("'id'", "'name'", "'code'"))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause('"id"')
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause('"id", "name"')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause('"id", "name", code')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as list - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['"id"'])
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['"id"', '"name"'])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['"id"', '"name"', '"code"'])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('"id"',))
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('"id"', '"name"'))
            self.assertText(
                result, '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('"id"', '"name"', '"code"'))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause('`id`')
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause('`id`, `name`')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause('`id`, `name`, `code`')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as list - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['`id`'])
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['`id`', '`name`'])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(['`id`', '`name`', '`code`'])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('`id`',))
            self.assertText(result, self._quote_select_identifier_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('`id`', '`name`'))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_select_identifier_clause(('`id`', '`name`', '`code`'))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_select_identifier_format.format('id'),
                    self._quote_select_identifier_format.format('name'),
                    self._quote_select_identifier_format.format('code'),
                ),
            )

        with self.subTest('Values as non-standard types'):
            result = self.connector.validate.sanitize_select_identifier_clause((1, True))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_select_identifier_format.format(1),
                    self._quote_select_identifier_format.format(True),
                ),
            )

        with self.subTest('Values with function calls'):
            # Uppercase.
            result = self.connector.validate.sanitize_select_identifier_clause('COUNT(*)')
            self.assertText(result, 'COUNT(*)')

            # Lowercase.
            result = self.connector.validate.sanitize_select_identifier_clause('count(*)')
            self.assertText(result, 'COUNT(*)')

    def test__sanitize_select_identifier_clause__failure(self):
        """
        Test sanitizing a SELECT clause, in cases when it should fail.
        """
        # Param "*" provided with other values.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause('* , id')
        self.assertText('SELECT clause provided * with other params. * is only valid alone.', str(err.exception))

        # Mistmatching quotes - double then single.
        identifier = """\"id'"""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier "id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then double.
        identifier = """'id\""""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier \'id"',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then single.
        identifier = "`id'"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier `id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then backtick.
        identifier = "'id`"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier \'id`',
            str(err.exception),
        )

        # Mistmatching quotes - double then backtick.
        identifier = '"id`'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier "id`',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then double.
        identifier = '`id"'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_select_identifier_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier `id"',
            str(err.exception),
        )

    def test__sanitize_columns_clause__success(self):
        """
        Test sanitizing a COLUMNS clause, in cases when it should succeed.

        For the most part, we test that the library gracefully handles any of
        the "standard" database quote types (', ", and `), and then properly
        converts it to the actual type/format as expected by the given database.
        """
        if self._quote_columns_format is None:
            TypeError('Invalid _columns_clause_format_str variable. Is None.')

        # None provided. Defaults back to empty string.
        result = self.connector.validate.sanitize_columns_clause(None)
        self.assertText(result, '')

        # Empty string provided (single-quote str).
        result = self.connector.validate.sanitize_columns_clause('')
        self.assertText(result, '')

        # Empty string provided (double-quote str).
        result = self.connector.validate.sanitize_columns_clause("")
        self.assertText(result, '')

        # Empty string provided (triple double-quote str).
        result = self.connector.validate.sanitize_columns_clause("""""")
        self.assertText(result, '')

        with self.subTest('Values as str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause('id')
            self.assertText(result, self._quote_columns_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(' id ')
            self.assertText(result, self._quote_columns_format.format('id'))

            # Single val provided and COLUMNS.
            result = self.connector.validate.sanitize_columns_clause('COLUMNS (id)')
            self.assertText(result, self._quote_columns_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(' COLUMNS ( id ) ')
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause('id, name')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name')
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(' id ,  name ')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause('id, name, code')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(' id ,  name ,  code ')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as triple str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause("""id""")
            self.assertText(result, self._quote_columns_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(""" id """)
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause("""id, name""")
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(""" id ,  name """)
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause("""id, name, code""")
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause(""" id ,  name ,  code """)
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as list - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(['id'])
            self.assertText(result, self._quote_columns_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause([' id '])
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(['id', 'name'])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause([' id ', ' name '])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(['id', 'name', 'code'])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause([' id ', ' name ', ' code '])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(('id',))
            self.assertText(result, self._quote_columns_format.format('id'))
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause((' id ',))
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(('id', 'name'))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause((' id ', ' name '))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(('id', 'name', 'code'))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_columns_clause((' id ', ' name ', ' code '))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause("'id'")
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause("'id', 'name'")
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause("'id', 'name', 'code'")
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code')
                ),
            )

        with self.subTest('Values as list - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(["'id'"])
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(["'id'", "'name'"])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(["'id'", "'name'", "'code'"])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(("'id'",))
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(("'id'", "'name'"))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(("'id'", "'name'", "'code'"))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause('"id"')
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause('"id", "name"')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause('"id", "name", code')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as list - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(['"id"'])
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(['"id"', '"name"'])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(['"id"', '"name"', '"code"'])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(('"id"',))
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(('"id"', '"name"'))
            self.assertText(
                result, '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(('"id"', '"name"', '"code"'))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause('`id`')
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause('`id`, `name`')
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause('`id`, `name`, `code`')
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as list - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(['`id`'])
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(['`id`', '`name`'])
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(['`id`', '`name`', '`code`'])
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_columns_clause(('`id`',))
            self.assertText(result, self._quote_columns_format.format('id'))

            # Two vals provided.
            result = self.connector.validate.sanitize_columns_clause(('`id`', '`name`'))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_columns_clause(('`id`', '`name`', '`code`'))
            self.assertText(
                result,
                '{0}, {1}, {2}'.format(
                    self._quote_columns_format.format('id'),
                    self._quote_columns_format.format('name'),
                    self._quote_columns_format.format('code'),
                ),
            )

        with self.subTest('Values as non-standard types'):
            # TODO: Should these fail? These probably should fail.
            #  I think only literal column names should work.
            result = self.connector.validate.sanitize_columns_clause((1, True))
            self.assertText(
                result,
                '{0}, {1}'.format(
                    self._quote_columns_format.format(1),
                    self._quote_columns_format.format(True),
                ),
            )

    def test__sanitize_columns_clause__failure(self):
        """
        Test sanitizing a COLUMNS clause, in cases when it should fail.
        """
        # Param "*" provided.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause('*')
        self.assertText('The * identifier can only be used in a SELECT clause.', str(err.exception))

        # Param "*" provided with other values.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause('* , id')
        self.assertText('The * identifier can only be used in a SELECT clause.', str(err.exception))

        # Mistmatching quotes - double then single.
        identifier = """\"id'"""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier "id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then double.
        identifier = """'id\""""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier \'id"',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then single.
        identifier = "`id'"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier `id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then backtick.
        identifier = "'id`"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier \'id`',
            str(err.exception),
        )

        # Mistmatching quotes - double then backtick.
        identifier = '"id`'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier "id`',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then double.
        identifier = '`id"'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_columns_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier `id"',
            str(err.exception),
        )

    # def test__sanitize_values_clause__success(self):
    #     """
    #     Test sanitizing a VALUES clause, in cases when it should succeed.
    #
    #     For the most part, we test that the library gracefully handles any of
    #     the "standard" database quote types (', ", and `), and then properly
    #     converts it to the actual type/format as expected by the given database.
    #     """
    #     if self._quote_columns_format is None:
    #         TypeError('Invalid _columns_clause_format_str variable. Is None.')
    #
    #     with self.subTest('Values as str - Without quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause('id')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(' id ')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES id')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause('values id')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES (id)')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause('values (id)')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause('id, name')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(' id ,  name ')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES id, name')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause('values id, name')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES (id, name)')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause('values (id, name)')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause('id, name, code')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(' id ,  name ,  code ')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES id, name, code')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause('values id, name, code')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES (id, name, code)')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause('values (id, name, code)')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #     with self.subTest('Values as triple str - Without quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause("""id""")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(""" id """)
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause("""VALUES id""")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause("""values id""")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause("""VALUES (id)""")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause("""values (id)""")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause("""id, name""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(""" id , name """)
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause("""VALUES id, name""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause("""values id, name""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause("""VALUES (id, name)""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause("""values (id, name)""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause("""id, name, code""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(""" id , name , code """)
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause("""VALUES id, name, code""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause("""values id, name, code""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause("""VALUES (id, name, code)""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause("""values (id, name, code)""")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #     with self.subTest('Values as list - Without quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(['id'])
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause([' id '])
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' id ')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(['id', 'name'])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause([' id ', ' name '])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(['id', 'name', 'code'])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause([' id ', ' name ', ' code '])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                     self._quote_str_literal_format.format(' code '),
    #                 ),
    #             )
    #
    #     with self.subTest('Values as tuple - Without quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(('id',))
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause((' id ',))
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' id ')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(('id', 'name'))
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause((' id ', ' name '))
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(('id', 'name', 'code'))
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause((' id ', ' name ', ' code '))
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                     self._quote_str_literal_format.format(' code '),
    #                 ),
    #             )
    #
    #     with self.subTest('Values as str - With single quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause("'id'")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(" ' id ' ")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' id ')))
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause("VALUES 'id'")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause("values 'id'")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause("VALUES ('id')")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause("values ('id')")
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause("'id', 'name'")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(" ' id ' , ' name ' ")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause("VALUES 'id', 'name',")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause("values 'id', 'name'")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause("VALUES ('id', 'name')")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause("values ('id', 'name')")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause("'id', 'name', 'code'")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(" ' id ' , ' name ' , ' code ' ")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                     self._quote_str_literal_format.format(' code '),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause("VALUES 'id', 'name', 'code'")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause("values 'id', 'name', 'code'")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause("VALUES ('id', 'name', 'code')")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause("values ('id', 'name', 'code')")
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #     # with self.subTest('Values as list - With single quotes'):
    #     #
    #     #     with self.subTest('Single val provided'):
    #     #         # Base value.
    #     #         print('\n\n\n\n\n\n\n\n\n\n\n\n\n')
    #     #         # All of these tokenize to the same thing? Okay then...
    #     #         # TODO: Figure out how to tokenize this as expected.
    #     #         result = self.connector.validate.sanitize_values_clause('id')
    #     #         result = self.connector.validate.sanitize_values_clause("id")
    #     #         result = self.connector.validate.sanitize_values_clause("'id'")
    #     #         result = self.connector.validate.sanitize_values_clause(["'id'"])
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format("'id'")))
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause([" ' id ' "])
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(" ' id ' ")))
    #     #
    #     #     with self.subTest('Two vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(["'id'", "'name'"])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format("'id'"),
    #     #                 self._quote_str_literal_format.format("'name'"),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause([" ' id ' ", " ' name ' "])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format(" ' id ' "),
    #     #                 self._quote_str_literal_format.format(" ' name ' "),
    #     #             ),
    #     #         )
    #     #
    #     #     with self.subTest('Three vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(["'id'", "'name'", "'code'"])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format("'id'"),
    #     #                 self._quote_str_literal_format.format("'name'"),
    #     #                 self._quote_str_literal_format.format("'code'"),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause([" ' id ' ", " ' name ' ", " ' code ' "])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format(" ' id ' "),
    #     #                 self._quote_str_literal_format.format(" ' name ' "),
    #     #                 self._quote_str_literal_format.format(" ' code ' "),
    #     #             ),
    #     #         )
    #
    #     # with self.subTest('Values as tuple - With single quotes'):
    #     #
    #     #     with self.subTest('Single val provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(("'id'",))
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format("'id'")))
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause((" ' id ' ",))
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(" ' id ' ")))
    #     #
    #     #     with self.subTest('Two vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(("'id'", "'name'"))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format("'id'"),
    #     #                 self._quote_str_literal_format.format("'name'"),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause((" ' id ' ", " ' name ' "))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format(" ' id ' "),
    #     #                 self._quote_str_literal_format.format(" ' name ' "),
    #     #             ),
    #     #         )
    #     #
    #     #     with self.subTest('Three vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(("'id'", "'name'", "'code'"))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format("'id'"),
    #     #                 self._quote_str_literal_format.format("'name'"),
    #     #                 self._quote_str_literal_format.format("'code'"),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause((" ' id ' ", " ' name ' ", " ' code ' "))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format(" ' id ' "),
    #     #                 self._quote_str_literal_format.format(" ' name ' "),
    #     #                 self._quote_str_literal_format.format(" ' code ' "),
    #     #             ),
    #     #         )
    #
    #     with self.subTest('Values as str - With double quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause('"id"')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(' " id " ')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' id ')))
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES "id"')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause('values "id"')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES ("id")')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause('values ("id")')
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('id')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause('"id", "name"')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(' " id " , " name " ')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES "id", "name"')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause('values "id", "name"')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES ("id", "name")')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause('values ("id", "name")')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause('"id", "name", "code"')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause(' " id " , " name " , " code " ')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format(' id '),
    #                     self._quote_str_literal_format.format(' name '),
    #                     self._quote_str_literal_format.format(' code '),
    #                 ),
    #             )
    #
    #             # With full statement - upper, no parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES "id", "name", "code"')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, no parens.
    #             result = self.connector.validate.sanitize_values_clause('values "id", "name", "code"')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - upper, with parens.
    #             result = self.connector.validate.sanitize_values_clause('VALUES ("id", "name", "code")')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #             # With full statement - lower, with parens.
    #             result = self.connector.validate.sanitize_values_clause('values ("id", "name", "code")')
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('id'),
    #                     self._quote_str_literal_format.format('name'),
    #                     self._quote_str_literal_format.format('code'),
    #                 ),
    #             )
    #
    #     with self.subTest('Values as list - With double quotes'):
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(['"id"'])
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('"id"')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause([' " id " '])
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' " id " ')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(['"id"', '"name"'])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('"id"'),
    #                     self._quote_str_literal_format.format('"name"'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause([' " id " ', ' " name " '])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format(' " id " '),
    #                     self._quote_str_literal_format.format(' " name " '),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(['"id"', '"name"', '"code"'])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('"id"'),
    #                     self._quote_str_literal_format.format('"name"'),
    #                     self._quote_str_literal_format.format('"code"'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause([' " id " ', ' " name " ', ' " code " '])
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format(' " id " '),
    #                     self._quote_str_literal_format.format(' " name " '),
    #                     self._quote_str_literal_format.format(' " code " '),
    #                 ),
    #             )
    #
    #     with self.subTest('Values as tuple - With double quotes'):
    #
    #         with self.subTest('Single val provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(('"id"',))
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('"id"')))
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause((' " id " ',))
    #             self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' " id " ')))
    #
    #         with self.subTest('Two vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(('"id"', '"name"'))
    #             self.assertText(
    #                 result, '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format('"id"'),
    #                     self._quote_str_literal_format.format('"name"'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause((' " id " ', ' " name " '))
    #             self.assertText(
    #                 result, '\nVALUES ({0}, {1})'.format(
    #                     self._quote_str_literal_format.format(' " id " '),
    #                     self._quote_str_literal_format.format(' " name " '),
    #                 ),
    #             )
    #
    #         with self.subTest('Three vals provided'):
    #             # Base value.
    #             result = self.connector.validate.sanitize_values_clause(('"id"', '"name"', '"code"'))
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format('"id"'),
    #                     self._quote_str_literal_format.format('"name"'),
    #                     self._quote_str_literal_format.format('"code"'),
    #                 ),
    #             )
    #
    #             # With extra whitespace.
    #             result = self.connector.validate.sanitize_values_clause((' " id " ', ' " name " ', ' " code " '))
    #             self.assertText(
    #                 result,
    #                 '\nVALUES ({0}, {1}, {2})'.format(
    #                     self._quote_str_literal_format.format(' " id " '),
    #                     self._quote_str_literal_format.format(' " name " '),
    #                     self._quote_str_literal_format.format(' " code " '),
    #                 ),
    #             )
    #
    #     # with self.subTest('Values as str - With backtick quotes'):
    #     #
    #     #     with self.subTest('Single val provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause('`id`')
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause(' ` id ` ')
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('` id `')))
    #     #
    #     #         # With full statement - upper, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('VALUES `id`')
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #         # With full statement - lower, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('values `id`')
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #         # With full statement - upper, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('VALUES `id`')
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #         # With full statement - lower, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('values `id`')
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #     with self.subTest('Two vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause('`id`, `name`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause(' ` id ` , ` name ` ')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('` id `'),
    #     #                 self._quote_str_literal_format.format('` name `'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - upper, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('VALUES `id`, `name`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - lower, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('values `id`, `name`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - upper, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('VALUES `id`, `name`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - lower, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('values `id`, `name`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #     with self.subTest('Three vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause('`id`, `name`, `code`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause(' ` id ` ,  ` name ` , ` code ` ')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - upper, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('VALUES `id`, `name`, `code`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - lower, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('values `id`, `name`, `code`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - upper, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('VALUES `id`, `name`, `code`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With full statement - lower, no parens.
    #     #         result = self.connector.validate.sanitize_values_clause('values `id`, `name`, `code`')
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #
    #     # with self.subTest('Values as list - With backtick quotes'):
    #     #
    #     #     with self.subTest('Single val provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(['`id`'])
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause([' ` id ` '])
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('` id `')))
    #     #
    #     #     with self.subTest('Two vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(['`id`', '`name`'])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause([' ` id ` ', ' ` name ` '])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format(' ` id ` '),
    #     #                 self._quote_str_literal_format.format(' ` name ` '),
    #     #             ),
    #     #         )
    #     #
    #     #     with self.subTest('Three vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(['`id`', '`name`', '`code`'])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause([' ` id ` ', ' ` name ` ', ' ` code ` '])
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format(' ` id ` '),
    #     #                 self._quote_str_literal_format.format(' ` name ` '),
    #     #                 self._quote_str_literal_format.format(' ` code ` '),
    #     #             ),
    #     #         )
    #
    #     # with self.subTest('Values as tuple - With backtick quotes'):
    #     #
    #     #     with self.subTest('Single val provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(('`id`',))
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format('`id`')))
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause((' ` id ` ',))
    #     #         self.assertText(result, '\nVALUES ({0})'.format(self._quote_str_literal_format.format(' ` id ` ')))
    #     #
    #     #     with self.subTest('Two vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(('`id`', '`name`'))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause((' ` id ` ', ' ` name ` '))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1})'.format(
    #     #                 self._quote_str_literal_format.format(' ` id ` '),
    #     #                 self._quote_str_literal_format.format(' ` name ` '),
    #     #             ),
    #     #         )
    #     #
    #     #     with self.subTest('Three vals provided'):
    #     #         # Base value.
    #     #         result = self.connector.validate.sanitize_values_clause(('`id`', '`name`', '`code`'))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format('`id`'),
    #     #                 self._quote_str_literal_format.format('`name`'),
    #     #                 self._quote_str_literal_format.format('`code`'),
    #     #             ),
    #     #         )
    #     #
    #     #         # With extra whitespace.
    #     #         result = self.connector.validate.sanitize_values_clause((' ` id ` ', ' ` name ` ', ' ` code ` '))
    #     #         self.assertText(
    #     #             result,
    #     #             '\nVALUES ({0}, {1}, {2})'.format(
    #     #                 self._quote_str_literal_format.format(' ` id ` '),
    #     #                 self._quote_str_literal_format.format(' ` name ` '),
    #     #                 self._quote_str_literal_format.format(' ` code ` '),
    #     #             ),
    #     #         )
    #
    #     with self.subTest('Values as non-standard types'):
    #         result = self.connector.validate.sanitize_values_clause((1, True))
    #         self.assertText(
    #             result,
    #             '\nVALUES ({0}, {1})'.format(
    #                 1,
    #                 True,
    #             ),
    #         )
    #
    #     # # Mistmatching quotes - double then single.
    #     # identifier = """\"id'"""
    #     # result = self.connector.validate.sanitize_values_clause(identifier)
    #     # self.assertText(
    #     #     'Found mismatching quotes for identifier "id\'',
    #     #     result,
    #     # )
    #     #
    #     # # Mistmatching quotes - single then double.
    #     # identifier = """'id\""""
    #     # result = self.connector.validate.sanitize_values_clause(identifier)
    #     # self.assertText(
    #     #     'Found mismatching quotes for identifier \'id"',
    #     #     result,
    #     # )
    #     #
    #     # # Mistmatching quotes - backtick then single.
    #     # identifier = "`id'"
    #     # result = self.connector.validate.sanitize_values_clause(identifier)
    #     # self.assertText(
    #     #     'Found mismatching quotes for identifier `id\'',
    #     #     result,
    #     # )
    #     #
    #     # # Mistmatching quotes - single then backtick.
    #     # identifier = "'id`"
    #     # result = self.connector.validate.sanitize_values_clause(identifier)
    #     # self.assertText(
    #     #     'Found mismatching quotes for identifier \'id`',
    #     #     result,
    #     # )
    #     #
    #     # # Mistmatching quotes - double then backtick.
    #     # identifier = '"id`'
    #     # result = self.connector.validate.sanitize_values_clause(identifier)
    #     # self.assertText(
    #     #     'Found mismatching quotes for identifier "id`',
    #     #     result,
    #     # )
    #     #
    #     # # Mistmatching quotes - backtick then double.
    #     # identifier = '`id"'
    #     # result = self.connector.validate.sanitize_values_clause(identifier)
    #     # self.assertText(
    #     #     'Found mismatching quotes for identifier `id"',
    #     #     result,
    #     # )

    # def test__sanitize_values_clause__failure(self):
    #     """
    #     Test sanitizing a VALUES clause, in cases when it should fail.
    #     """
    #     # None provided.
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause(None)
    #     self.assertText('Invalid VALUES clause. Must have one or more items.', str(err.exception))
    #
    #     # Empty string provided (single-quote str).
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause('')
    #     self.assertText('Invalid VALUES clause. Must have one or more items.', str(err.exception))
    #
    #     # Empty string provided (double-quote str).
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause("")
    #     self.assertText('Invalid VALUES clause. Must have one or more items.', str(err.exception))
    #
    #     # Empty string provided (triple double-quote str).
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause("""""")
    #     self.assertText('Invalid VALUES clause. Must have one or more items.', str(err.exception))
    #
    #     # "VALUES" provided without any additional values.
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause('VALUES')
    #     self.assertText('Invalid VALUES clause. Must have one or more items.', str(err.exception))
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause('   VALUES   ')
    #     self.assertText('Invalid VALUES clause. Must have one or more items.', str(err.exception))
    #
    #     # Param "*" provided.
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause('*')
    #     self.assertText('The * identifier can only be used in a SELECT clause.', str(err.exception))
    #
    #     # Param "*" provided with other values.
    #     with self.assertRaises(ValueError) as err:
    #         self.connector.validate.sanitize_values_clause('* , id')
    #     self.assertText('The * identifier can only be used in a SELECT clause.', str(err.exception))

    def test__sanitize_order_by_clause__success(self):
        """
        Test sanitizing an ORDER BY clause, in cases when it should succeed.

        For the most part, we test that the library gracefully handles any of
        the "standard" database quote types (', ", and `), and then properly
        converts it to the actual type/format as expected by the given database.
        """
        if self._quote_columns_format is None:
            TypeError('Invalid _columns_clause_format_str variable. Is None.')

        # None provided. Defaults back to empty string.
        result = self.connector.validate.sanitize_order_by_clause(None)
        self.assertText(result, '')

        # Empty string provided (single-quote str).
        result = self.connector.validate.sanitize_order_by_clause('')
        self.assertText(result, '')

        # Empty string provided (double-quote str).
        result = self.connector.validate.sanitize_order_by_clause("")
        self.assertText(result, '')

        # Empty string provided (triple double-quote str).
        result = self.connector.validate.sanitize_order_by_clause("""""")
        self.assertText(result, '')

        with self.subTest('Values as str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause('id')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause(' id ')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - upper.
            result = self.connector.validate.sanitize_order_by_clause('ORDER BY id')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - lower.
            result = self.connector.validate.sanitize_order_by_clause('order by id')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause('id, name')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name')
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause(' id ,  name ')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause('id, name, code')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause(' id ,  name ,  code ')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as triple str - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause("""id""")
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause(""" id """)
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - upper.
            result = self.connector.validate.sanitize_order_by_clause("""ORDER BY id""")
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - lower.
            result = self.connector.validate.sanitize_order_by_clause("""order by id""")
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause("""id, name""")
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause(""" id ,  name """)
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause("""id, name, code""")
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause(""" id ,  name ,  code """)
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as list - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(['id'])
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause([' id '])
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(['id', 'name'])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause([' id ', ' name '])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(['id', 'name', 'code'])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause([' id ', ' name ', ' code '])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - Without quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(('id',))
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause((' id ',))
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(('id', 'name'))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause((' id ', ' name '))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(('id', 'name', 'code'))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )
            # With extra whitespace.
            result = self.connector.validate.sanitize_order_by_clause((' id ', ' name ', ' code '))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause("'id'")
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - upper.
            result = self.connector.validate.sanitize_order_by_clause("ORDER BY 'id'")
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - lower.
            result = self.connector.validate.sanitize_order_by_clause("order by 'id'")
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause("'id', 'name'")
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause("'id', 'name', 'code'")
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code')
                ),
            )

        with self.subTest('Values as list - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(["'id'"])
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(["'id'", "'name'"])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(["'id'", "'name'", "'code'"])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With single quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(("'id'",))
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(("'id'", "'name'"))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(("'id'", "'name'", "'code'"))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause('"id"')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - upper.
            result = self.connector.validate.sanitize_order_by_clause('ORDER BY "id"')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - lower.
            result = self.connector.validate.sanitize_order_by_clause('order by "id"')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause('"id", "name"')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause('"id", "name", code')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as list - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(['"id"'])
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(['"id"', '"name"'])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(['"id"', '"name"', '"code"'])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With double quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(('"id"',))
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(('"id"', '"name"'))
            self.assertText(
                result, '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(('"id"', '"name"', '"code"'))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as str - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause('`id`')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - upper.
            result = self.connector.validate.sanitize_order_by_clause('ORDER BY `id`')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))
            # With full statement - lower.
            result = self.connector.validate.sanitize_order_by_clause('order by `id`')
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause('`id`, `name`')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause('`id`, `name`, `code`')
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as list - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(['`id`'])
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(['`id`', '`name`'])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(['`id`', '`name`', '`code`'])
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as tuple - With backtick quotes'):
            # Single val provided.
            result = self.connector.validate.sanitize_order_by_clause(('`id`',))
            self.assertText(result, '\nORDER BY {0}'.format(self._quote_order_by_format.format('id')))

            # Two vals provided.
            result = self.connector.validate.sanitize_order_by_clause(('`id`', '`name`'))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                ),
            )

            # Three vals provided.
            result = self.connector.validate.sanitize_order_by_clause(('`id`', '`name`', '`code`'))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}, {2}'.format(
                    self._quote_order_by_format.format('id'),
                    self._quote_order_by_format.format('name'),
                    self._quote_order_by_format.format('code'),
                ),
            )

        with self.subTest('Values as non-standard types'):
            # TODO: Should these fail? These probably should fail.
            #  I think only literal column names should work.
            result = self.connector.validate.sanitize_order_by_clause((1, True))
            self.assertText(
                result,
                '\nORDER BY {0}, {1}'.format(
                    self._quote_order_by_format.format(1),
                    self._quote_order_by_format.format(True),
                ),
            )

    def test__sanitize_order_by_clause__failure(self):
        """
        Test sanitizing an ORDER BY clause, in cases when it should fail.
        """
        # "ORDER BY" provided without any additional values.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause('ORDER BY')
        self.assertText('Invalid ORDER BY clause.', str(err.exception))
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause('   ORDER BY   ')
        self.assertText('Invalid ORDER BY clause.', str(err.exception))

        # Param "*" provided.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause('*')
        self.assertText('The * identifier can only be used in a SELECT clause.', str(err.exception))

        # Param "*" provided with other values.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause('* , id')
        self.assertText('The * identifier can only be used in a SELECT clause.', str(err.exception))

        # Mistmatching quotes - double then single.
        identifier = """\"id'"""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier "id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then double.
        identifier = """'id\""""
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier \'id"',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then single.
        identifier = "`id'"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier `id\'',
            str(err.exception),
        )

        # Mistmatching quotes - single then backtick.
        identifier = "'id`"
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier \'id`',
            str(err.exception),
        )

        # Mistmatching quotes - double then backtick.
        identifier = '"id`'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier "id`',
            str(err.exception),
        )

        # Mistmatching quotes - backtick then double.
        identifier = '`id"'
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_order_by_clause(identifier)
        self.assertText(
            'Found mismatching quotes for identifier `id"',
            str(err.exception),
        )

    def test__sanitize_limit_clause__success(self):
        """
        Test sanitizing a LIMIT clause, in cases when it should succeed.
        """
        # None provided. Defaults back to empty string.
        result = self.connector.validate.sanitize_limit_clause(None)
        self.assertText(result, '')

        # Empty string provided (single-quote str).
        result = self.connector.validate.sanitize_limit_clause('')
        self.assertText(result, '')

        # Empty string provided (double-quote str).
        result = self.connector.validate.sanitize_limit_clause("")
        self.assertText(result, '')

        # Empty string provided (triple double-quote str).
        result = self.connector.validate.sanitize_limit_clause("""""")
        self.assertText(result, '')

        with self.subTest('Limit of 1 (lowest acceptable limit)'):
            # As int.
            result = self.connector.validate.sanitize_limit_clause(1)
            self.assertText(result, ' LIMIT 1')

            # As str.
            result = self.connector.validate.sanitize_limit_clause('1')
            self.assertText(result, ' LIMIT 1')

            # As full str (upper).
            result = self.connector.validate.sanitize_limit_clause('LIMIT 1')
            self.assertText(result, ' LIMIT 1')

            # As full str (lower).
            result = self.connector.validate.sanitize_limit_clause('limit 1')
            self.assertText(result, ' LIMIT 1')

        with self.subTest('Limit of 2'):
            # As int.
            result = self.connector.validate.sanitize_limit_clause(2)
            self.assertText(result, ' LIMIT 2')

            # As str.
            result = self.connector.validate.sanitize_limit_clause('2')
            self.assertText(result, ' LIMIT 2')

            # As full str (upper).
            result = self.connector.validate.sanitize_limit_clause('LIMIT 2')
            self.assertText(result, ' LIMIT 2')

            # As full str (lower).
            result = self.connector.validate.sanitize_limit_clause('limit 2')
            self.assertText(result, ' LIMIT 2')

        with self.subTest('Limit of 100'):
            # As int.
            result = self.connector.validate.sanitize_limit_clause(100)
            self.assertText(result, ' LIMIT 100')

            # As str.
            result = self.connector.validate.sanitize_limit_clause('100')
            self.assertText(result, ' LIMIT 100')

            # As full str (upper).
            result = self.connector.validate.sanitize_limit_clause('LIMIT 100')
            self.assertText(result, ' LIMIT 100')

            # As full str (lower).
            result = self.connector.validate.sanitize_limit_clause('limit 100')
            self.assertText(result, ' LIMIT 100')

    def test__sanitize_limit_clause__failure(self):
        """
        Test sanitizing a LIMIT clause, in cases when it should fail.
        """
        # Zero provided.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_limit_clause(0)
        self.assertText('The LIMIT clause must return at least one record.', str(err.exception))

        # Negative provided.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_limit_clause(-1)
        self.assertText('The LIMIT clause must return at least one record.', str(err.exception))

        # Non-integer.
        with self.assertRaises(ValueError) as err:
            self.connector.validate.sanitize_limit_clause('abc')
        self.assertText('The LIMIT clause expects a positive integer.', str(err.exception))

    # endregion Sanitization Functions


    # region Helper Functions

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

        # With commas.
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

        with self.subTest('Str defined by single quotes'):
            # Basic strings.
            self.assertFalse(self.connector.validate._is_quoted('True'))

            # With spaces.
            self.assertFalse(self.connector.validate._is_quoted('True False'))

            # With commas.
            self.assertFalse(self.connector.validate._is_quoted('True, False'))

            # With mismatching quote types.
            self.assertFalse(self.connector.validate._is_quoted('\'True"'))
            self.assertFalse(self.connector.validate._is_quoted('"True\''))
            self.assertFalse(self.connector.validate._is_quoted('`True"'))
            self.assertFalse(self.connector.validate._is_quoted('"True`'))
            self.assertFalse(self.connector.validate._is_quoted('`True\''))
            self.assertFalse(self.connector.validate._is_quoted('\'True`'))

            # With value mid-string.
            self.assertFalse(self.connector.validate._is_quoted('we\'re'))
            self.assertFalse(self.connector.validate._is_quoted('\'twas'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus\''))
            self.assertFalse(self.connector.validate._is_quoted('Marcus\' Market'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus \'Fresh\' Market'))
            self.assertFalse(self.connector.validate._is_quoted('we"re'))
            self.assertFalse(self.connector.validate._is_quoted('"twas'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus"'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus" Market'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus "Fresh" Market'))
            self.assertFalse(self.connector.validate._is_quoted('we`re'))
            self.assertFalse(self.connector.validate._is_quoted('`twas'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus`'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus` Market'))
            self.assertFalse(self.connector.validate._is_quoted('Marcus `Fresh` Market'))

        with self.subTest('Str defined by double quotes'):
            # Basic strings.
            self.assertFalse(self.connector.validate._is_quoted("True"))

            # With spaces.
            self.assertFalse(self.connector.validate._is_quoted("True False"))

            # With commas.
            self.assertFalse(self.connector.validate._is_quoted("True, False"))

            # With mismatching quote types.
            self.assertFalse(self.connector.validate._is_quoted("'True\""))
            self.assertFalse(self.connector.validate._is_quoted("\"True'"))
            self.assertFalse(self.connector.validate._is_quoted("`True\""))
            self.assertFalse(self.connector.validate._is_quoted("\"True`"))
            self.assertFalse(self.connector.validate._is_quoted("`True\'"))
            self.assertFalse(self.connector.validate._is_quoted("'True`"))

            # With value mid-string.
            self.assertFalse(self.connector.validate._is_quoted("we're"))
            self.assertFalse(self.connector.validate._is_quoted("'twas"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus'"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus' Market"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus 'Fresh' Market"))
            self.assertFalse(self.connector.validate._is_quoted("we\"re"))
            self.assertFalse(self.connector.validate._is_quoted("\"twas"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus\""))
            self.assertFalse(self.connector.validate._is_quoted("Marcus\" Market"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus \"Fresh\" Market"))
            self.assertFalse(self.connector.validate._is_quoted("we`re"))
            self.assertFalse(self.connector.validate._is_quoted("`twas"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus`"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus` Market"))
            self.assertFalse(self.connector.validate._is_quoted("Marcus `Fresh` Market"))

        with self.subTest('Str defined by triple quotes'):
            # Basic strings.
            self.assertFalse(self.connector.validate._is_quoted("""True"""))

            # With spaces.
            self.assertFalse(self.connector.validate._is_quoted("""True False"""))

            # With commas.
            self.assertFalse(self.connector.validate._is_quoted("""True, False"""))

            # With mismatching quote types.
            self.assertFalse(self.connector.validate._is_quoted("""'True\""""))
            self.assertFalse(self.connector.validate._is_quoted("""\"True'"""))
            self.assertFalse(self.connector.validate._is_quoted("""`True\""""))
            self.assertFalse(self.connector.validate._is_quoted("""\"True`"""))
            self.assertFalse(self.connector.validate._is_quoted("""`True\'"""))
            self.assertFalse(self.connector.validate._is_quoted("""'True`"""))

            # With value mid-string.
            self.assertFalse(self.connector.validate._is_quoted("""we're"""))
            self.assertFalse(self.connector.validate._is_quoted("""'twas"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus'"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus' Market"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus 'Fresh' Market"""))
            self.assertFalse(self.connector.validate._is_quoted("""we"re"""))
            self.assertFalse(self.connector.validate._is_quoted(""""twas"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus\""""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus" Market"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus "Fresh" Market"""))
            self.assertFalse(self.connector.validate._is_quoted("""we`re"""))
            self.assertFalse(self.connector.validate._is_quoted("""`twas"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus`"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus` Market"""))
            self.assertFalse(self.connector.validate._is_quoted("""Marcus `Fresh` Market"""))

    # endregion Helper Functions

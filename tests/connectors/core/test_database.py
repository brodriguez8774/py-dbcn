"""
Initialization of "database" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# Internal Imports.


class CoreDatabaseTestMixin:
    """
    Tests "Core" DB Connector class database logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)

    def test_error_catch_types(self):
        """Tests to ensure database ERROR types are properly caught.

        For example, MySQL and PostgreSQL interfaces do not catch "Database Does Not Exist" errors the same way.
        These tests make sure this error (and others) are properly caught, regardless of what database is being called.
        """
        # Ensure error types are first defined.
        if not self.connector.errors.database_does_not_exist:
            raise ValueError('Please define error handler for "Database Does Not Exist" error type.')
        if not self.connector.errors.database_already_exists:
            raise ValueError('Please define error handler for "Database Already Exists" error type.')

    def test__select(self):
        """
        Test logic for `SELECT;` query.
        """
        with self.subTest('With default database selected'):
            # Varify default database name is returned.
            result = self.connector.database.select()
            self.assertEqual(result.casefold(), self.test_db_name.casefold())

            # Verify alias func returns same result.
            result = self.connector.database.current()
            self.assertEqual(result.casefold(), self.test_db_name.casefold())

        with self.subTest('With select_1 database selected'):
            db_name = '{0}__select_1'.format(self.test_db_name)

            # Verify database exists.
            try:
                self.connector.database.create(db_name)
            except self.connector.errors.database_already_exists:
                # Database already exists, as we want.
                pass

            # Switch databases and verify select changed.
            self.connector.database.use(db_name)
            result = self.connector.database.select()
            self.assertEqual(result.casefold(), db_name.casefold())

            # Verify alias func returns same result.
            result = self.connector.database.current()
            self.assertEqual(result.casefold(), db_name.casefold())

        with self.subTest('With select_2 database selected'):
            db_name = '{0}__select_2'.format(self.test_db_name)

            # Verify database exists.
            try:
                self.connector.database.create(db_name)
            except self.connector.errors.database_already_exists:
                # Database already exists, as we want.
                pass

            # Switch databases and verify select changed.
            self.connector.database.use(db_name)
            result = self.connector.database.select()
            self.assertEqual(result.casefold(), db_name.casefold())

            # Verify alias func returns same result.
            result = self.connector.database.current()
            self.assertEqual(result.casefold(), db_name.casefold())

    def test__show_database(self):
        """
        Test logic for `SHOW DATABASES;` query.
        """
        db_name = '{0}__show'.format(self.test_db_name)

        with self.subTest('SHOW query when database exists'):
            # Verify database exists.
            try:
                self.connector.database.create(db_name)
            except self.connector.errors.database_already_exists:
                # Database already exists, as we want.
                pass

            # Run test query.
            results = self.connector.database.show()

            # Verify at least one database returned.
            self.assertGreaterEqual(len(results), 1)

            # Verify expected database returned.
            self.assertIn(db_name.casefold(), (str(x).casefold() for x in results))

        # Remove database and verify expected results changed.
        with self.subTest('SHOW query when database does not exist'):
            # Verify database does not exist.
            try:
                self.connector.database.drop(db_name)
            except self.connector.errors.database_does_not_exist:
                # Database does not yet exist, as we want.
                pass

            # Run test query.
            results = self.connector.database.show()

            # Verify expected database did not return.
            self.assertNotIn(db_name.casefold(), (str(x).casefold() for x in results))

    def test__create_database__success(self):
        """
        Test `CREATE DATABASE` query, when database does not exist.
        """
        db_name = '{0}__create__success'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.database.drop(db_name)
        except ValueError:
            # Database does not yet exist, as we want.
            pass

        # Check databases prior to test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertNotIn(db_name.casefold(), (str(x).casefold() for x in results))

        # Run test query.
        self.connector.database.create(db_name)

        # Check databases after test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name.casefold(), (str(x).casefold() for x in results))

    def test__create_database__failure(self):
        """
        Test `CREATE DATABASE` query, when database exists.
        """
        db_name = '{0}__create__failure'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.database.create(db_name)
        except self.connector.errors.database_already_exists:
            # Database already exists, as we want.
            pass

        # Check databases prior to test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name.casefold(), (str(x).casefold() for x in results))

        # Run test query.
        error_type = None
        if self.connector._config.db_type == 'MySQL':
            error_type = ValueError
        elif self.connector._config.db_type == 'PostgreSQL':
            error_type = self.connector.errors.database_already_exists
        with self.assertRaises(error_type):
            self.connector.database.create(db_name)

    def test__use_database__success(self):
        """
        Test `USE DATABASE` query, when database exists.
        """
        db_name = '{0}__use__success'.format(self.test_db_name)

        # Verify database exists.
        try:
            self.connector.database.create(db_name)
        except self.connector.errors.database_already_exists:
            # Database already exists, as we want.
            pass

        # Check databases prior to test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name.casefold(), (str(x).casefold() for x in results))

        # Run test query.
        self.connector.database.use(db_name)

        # Check results of test query.
        results = self.connector.database.current()

        # Verify expected database returned.
        self.assertEqual(len(results), len(db_name))
        self.assertEqual(results.casefold(), db_name.casefold())

    def test__use_database__failure(self):
        """
        Test `USE DATABASE` query, when database does not exist.
        """
        db_name = '{0}__use__failure'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.database.drop(db_name)
        except ValueError:
            # Database does not exist, as we want.
            pass

        # Check databases prior to test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertNotIn(db_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.database.use(db_name)

    def test__delete_database__success(self):
        """
        Test `DROP DATABASE` query, when database exists.
        """
        db_name = '{0}__delete__success'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.database.create(db_name)
        except self.connector.errors.database_already_exists:
            # Database already exists, as we want.
            pass

        # Check databases prior to test query. Verify expected database returned.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertIn(db_name.casefold(), (str(x).casefold() for x in results))

        # Run test query.
        self.connector.database.delete(db_name)

        # Check databases after test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertGreaterEqual(len(results), 1)
        self.assertNotIn(db_name.casefold(), (str(x).casefold() for x in results))

    def test__delete_database__failure(self):
        """
        Test `DROP DATABASE` query, when database does not exist.
        """
        db_name = '{0}__delete__failure'.format(self.test_db_name)

        # Verify database does not yet exist.
        try:
            self.connector.database.drop(db_name)
        except ValueError:
            # Database does not yet exist, as we want.
            pass

        # Check databases prior to test query. Verify expected database did not return.
        results = self.connector.database.show()
        self.assertNotIn(db_name, results)

        # Run test query.
        with self.assertRaises(ValueError):
            self.connector.database.delete(db_name)

"""
Initialization of "tables" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# User Imports.


class CoreTablesTestMixin:
    """
    Tests "Core" DB Connector class table logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)

    def test__create_table___col_str(self):
        """
        Tests that connector object properly creates new tables, via str of column data.
        """
        table_name = 'test_create_table'

        # Check that expected table DOES NOT yet exist in database.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

        # Attempt to generate table.
        self.connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')

        # Check that expected table now exists in database.
        results = self.connector.tables.show()
        self.assertIn(table_name, results)

    # def test__create_table___col_dict(self):
    #     """
    #     Tests that connector object properly creates new tables, via dict of column data.
    #     """
    #     table_name = 'test_create_table'
    #
    #     # Check that expected table DOES NOT yet exist in database.
    #     results = self.connector.tables.show()
    #     self.assertNotIn(table_name, results)
    #
    #     # Attempt to generate table.
    #     self.connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')
    #
    #     # Check that expected table now exists in database.
    #     results = self.connector.tables.show()
    #     self.assertIn(table_name, results)

    def test__drop_table(self):
        """
        Tests that connector object properly drops tables.
        """
        table_name = 'test_drop_table'

        # Check that expected table DOES NOT yet exist in database.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

        # Attempt to generate table.
        self.connector.tables.create(table_name, 'id INT(11) NOT NULL AUTO_INCREMENT, PRIMARY KEY (id)')

        # Check that expected table now exists in database.
        results = self.connector.tables.show()
        self.assertIn(table_name, results)

        # Attempt to remove table.
        self.connector.tables.drop(table_name)

        # Check that expected table was removed.
        results = self.connector.tables.show()
        self.assertNotIn(table_name, results)

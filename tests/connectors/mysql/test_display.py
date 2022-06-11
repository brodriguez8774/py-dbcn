"""
Tests for "display" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
from .test_core import TestMysqlDatabaseParent


EXPECTED__TABLE__SHOW__DB_LONGER__PT_1 = """
+------------------------------------------------------+
| Tables in python__db_connector__test_display__tables |
+------------------------------------------------------+
| category                                             |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__DB_LONGER__PT_2 = """
+------------------------------------------------------+
| Tables in python__db_connector__test_display__tables |
+------------------------------------------------------+
| category                                             |
| priority                                             |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__DB_LONGER__PT_3 = """
+------------------------------------------------------+
| Tables in python__db_connector__test_display__tables |
+------------------------------------------------------+
| a                                                    |
| category                                             |
| priority                                             |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__EQUAL_LENGTH = """
+------------------------------------------------------+
| Tables in python__db_connector__test_display__tables |
+------------------------------------------------------+
| a                                                    |
| category                                             |
| priority                                             |
| test__testing__this_is__really_long_table_name__test |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_1 = """
+-------------------------------------------------------+
| Tables in python__db_connector__test_display__tables  |
+-------------------------------------------------------+
| a                                                     |
| category                                              |
| priority                                              |
| test__testing__this_is__really_long_table_name__test  |
| test__testing__this_is_a_really_long_table_name__test |
+-------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_2 = """
+-------------------------------------------------------+
| Tables in python__db_connector__test_display__tables  |
+-------------------------------------------------------+
| a                                                     |
| category                                              |
| priority                                              |
| test__testing__this_is__really_long_table_name__test  |
| test__testing__this_is_a_really_long_table_name__test |
| zzz                                                   |
+-------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_3 = """
+----------------------------------------------------------+
| Tables in python__db_connector__test_display__tables     |
+----------------------------------------------------------+
| a                                                        |
| category                                                 |
| priority                                                 |
| test__testing__this_is__really_long_table_name__test     |
| test__testing__this_is_a_really_long_table_name__test    |
| test__testing__this_is_a_really_long_table_name__testing |
| zzz                                                      |
+----------------------------------------------------------+
""".strip()


class TestMysqlDisplay(TestMysqlDatabaseParent):
    """
    Tests "MySQL" DB Connector class display logic.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize database for tests.
        db_name = 'python__db_connector__test_display'
        cls.connector.database.create(db_name)
        cls.connector.database.use(db_name)

    def get_output(self, log_capture, record_num):
        """Helper function to read captured logging output."""
        return str(log_capture.records[record_num].message).strip()

    def test__get_longest(self):
        with self.subTest('With no entry'):
            test_list = []
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 0)

        with self.subTest('With one entry'):
            # Test with len 0.
            test_list = ['']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 0)

            # Test with len 1.
            test_list = ['a']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 1)

            # Test with len 2.
            test_list = ['aa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 2)

            # Test with len 3.
            test_list = ['aaa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 3)

        with self.subTest('With two entries'):
            # Test with first as longest, at length of 1.
            test_list = ['a', '']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 1)

            # Test with second as longest, at length of 2.
            test_list = ['a', 'aa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 2)

            # Test with first as longest, at length of 3.
            test_list = ['aaa', 'a']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 3)

            # Test with second as longest, at length of 4.
            test_list = ['aa', 'aaaa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 4)

        with self.subTest('With two entries, including whitespace'):
            # Test with first as longest, at length of 1.
            test_list = ['a', '  ']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 1)

            # Test with second as longest, at length of 2.
            test_list = ['a   ', 'aa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 2)

            # Test with first as longest, at length of 3.
            test_list = ['  aaa', 'a    ']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 3)

            # Test with second as longest, at length of 4.
            test_list = ['  aa ', '    aaaa     ']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 4)

        with self.subTest('With three entries'):
            # Test with last as longest, at length of 3.
            test_list = ['a', 'aa', 'aaa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 3)

            # Test with second as longest, at length of 4.
            test_list = ['a', 'aaaa', 'aaa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 4)

            # Test with first as longest, at length of 5.
            test_list = ['aaaaa', 'aaaa', 'aaa']
            return_val = self.connector.display._get_longest(test_list, include_db_name=False)
            self.assertEqual(return_val, 5)

        with self.subTest('With db_name included'):
            test_list = []

            # Test with direct value.
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 34)

            # Test with select function.
            db_name_len = len(self.connector.database.select())
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, db_name_len)

            # Test with list being larger.
            test_list = ['python__db_connector__test_display__plus_ten']
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 44)


class TestMysqlDisplayTable(TestMysqlDatabaseParent):
    """
    Tests "MySQL" DB Connector class display logic.
    """

    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize database for tests.
        db_name = 'python__db_connector__test_display__tables'
        cls.connector.database.create(db_name)
        cls.connector.database.use(db_name)

    def get_output(self, log_capture, record_num):
        """Helper function to read captured logging output."""
        return str(log_capture.records[record_num].message).strip()

    def test__display__show_tables__db_name_longer(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            description VARCHAR(100),
            PRIMARY KEY ( id )
        )"""

        with self.subTest('With no tables present'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), 'Empty Set')

        with self.subTest('Db name longer - Pt 1'):
            # Create table.
            self.connector.tables.create('category', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__DB_LONGER__PT_1)

        with self.subTest('Db name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('priority', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__DB_LONGER__PT_2)

        with self.subTest('Db name longer - Pt 3'):
            # Create table.
            self.connector.tables.create('a', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__DB_LONGER__PT_3)

        with self.subTest('Db name and table name equal length'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is__really_long_table_name__test',
                columns,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__EQUAL_LENGTH)

        with self.subTest('Table name longer - Pt 1'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__test',
                columns,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_1)

        with self.subTest('Table name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('zzz', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_2)

        with self.subTest('Table name longer - Pt 3'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__testing',
                columns,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertEqual(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertEqual(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_3)


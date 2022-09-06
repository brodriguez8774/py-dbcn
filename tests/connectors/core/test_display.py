"""
Initialization of "display" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# User Imports.


class CoreDisplayBaseTestMixin:
    """
    Tests "Core" DB Connector class display logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)
        cls.expected_output = None

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

            # Test with empty value. Should equal length of database name.
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 42)

            # Test with select function. Aka, verify that it equals length of database name.
            db_name_len = len(self.connector.database.select())
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, db_name_len)

            # Test with list being larger.
            test_list = ['{0}__plus_ten'.format(self.test_db_name)]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 52)

            # Test with multiple list values, all smaller.
            test_list = ['a', 'bb', 'ccc']
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 42)

            # Test with multiple list values, one equal.
            test_list = [
                'a',
                'bb',
                'd' * 42,
                'ccc',
            ]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 42)

            # Test with multiple list values, one larger.
            test_list = [
                'a',
                'bb',
                'd' * 42,
                'e' * 47,
                'ccc',
            ]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 47)

            # Test with multiple list values, multiple larger.
            test_list = [
                'a',
                'h' * 49,
                'f' * 45,
                'bb',
                'd' * 42,
                'e' * 47,
                'ccc',
                'g' * 46,
            ]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 49)


class CoreDisplayTablesTestMixin:
    """
    Tests "Core" DB Connector class display logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)
        cls.expected_output = None

    def test__display__show_tables(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            description VARCHAR(100),
            PRIMARY KEY ( id )
        )"""

        # Since this directly tests display of tables, ensure we use a fresh database.
        db_name = '{0}d__tables__show'.format(self.test_db_name[0:-15])
        self.connector.database.create(db_name, display_query=False)
        self.connector.database.use(db_name, display_query=False)

        with self.subTest('With no tables present'):
            # Capture logging output.
            with self.assertLogs(None, 'QUERY') as qlog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(qlog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(qlog, 1), 'Empty Set')

        with self.subTest('Db name longer - Pt 1'):
            # Create table.
            self.connector.tables.create('category', columns, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__DB_LONGER__PT_1)

        with self.subTest('Db name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('priority', columns, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__DB_LONGER__PT_2)

        with self.subTest('Db name longer - Pt 3'):
            # Create table.
            self.connector.tables.create('a', columns, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__DB_LONGER__PT_3)

        with self.subTest('Db name and table name equal length'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__test_',
                columns,
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__EQUAL_LENGTH)

        with self.subTest('Table name longer - Pt 1'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__test__',
                columns,
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__TABLE_LONGER__PT_1)

        with self.subTest('Table name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('zzz', columns, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__TABLE_LONGER__PT_2)

        with self.subTest('Table name longer - Pt 3'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__testing__',
                columns,
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.SHOW__TABLE_LONGER__PT_3)

    def test__display__describe_tables(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            PRIMARY KEY ( id )
        )"""

        # Since this directly tests display of tables, ensure we use a fresh database.
        db_name = '{0}d__tables__desc'.format(self.test_db_name[0:-15])
        self.connector.database.create(db_name, display_query=False)
        self.connector.database.use(db_name, display_query=False)

        # Create initial table to describe.
        self.connector.tables.create('category', columns, display_query=False)

        with self.subTest('With only id'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_logging_output(ilog, 0), 'DESCRIBE category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.DESCRIBE__COLS_ID)

        with self.subTest('With id, name'):
            # Add new table column.
            self.connector.tables.add_column('category', 'name VARCHAR(100)', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_logging_output(ilog, 0), 'DESCRIBE category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.DESCRIBE__COLS_ID_NAME)

        with self.subTest('With id, name, desc'):
            # Add new table column.
            self.connector.tables.add_column('category', 'description VARCHAR(100)', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_logging_output(ilog, 0), 'DESCRIBE category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.tables.DESCRIBE__COLS_ID_NAME_DESC)


class CoreDisplayRecordsMixin:
    """
    Tests "Core" DB Connector class display logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)
        cls.expected_output = None

    def test__display__select_records__basic(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            description VARCHAR(100),
            PRIMARY KEY ( id )
        )"""

        self.connector.tables.create('category', columns, display_query=False)

        with self.subTest('With no records present'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), 'Empty Set')

        with self.subTest('With 1 record present'):
            # Create record.
            self.connector.records.insert('category', '(1, "tn", "td")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_1)

        with self.subTest('With 2 records present'):
            # Create record.
            self.connector.records.insert('category', '(2, "t n", "t d")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_2)

        with self.subTest('With 3 records present'):
            # Create record.
            self.connector.records.insert('category', '(3, "te n", "te d")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_3)

        with self.subTest('With 4 records present'):
            # Create record.
            self.connector.records.insert('category', '(4, "tes n", "tes d")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_4)

        with self.subTest('With 5 records present'):
            # Create record.
            self.connector.records.insert('category', '(5, "test n", "test d")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_5)

        with self.subTest('With 6 records present'):
            # Create record.
            self.connector.records.insert('category', '(6, "test na", "test de")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_6)

        with self.subTest('With 7 records present'):
            # Create record.
            self.connector.records.insert('category', '(7, "test nam", "test des")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_7)

        with self.subTest('With 8 records present'):
            # Create record.
            self.connector.records.insert('category', '(8, "test name", "test desc")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_8)

        with self.subTest('With 9 records present'):
            # Create record.
            self.connector.records.insert('category', '(9, "test name", "test descr")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_9)

        with self.subTest('With 10 records present'):
            # Create record.
            self.connector.records.insert('category', '(10, "test name", "test descri")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_10)

        with self.subTest('With 11 records present'):
            # Create record.
            self.connector.records.insert('category', '(101, "test name", "test descrip")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_11)

        with self.subTest('With 12 records present'):
            # Create record.
            self.connector.records.insert('category', '(1010, "test name", "test descript")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_12)

        with self.subTest('With 13 records present'):
            # Create record.
            self.connector.records.insert('category', '(10101, "test name", "test descripti")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_13)

        with self.subTest('With 14 records present'):
            # Create record.
            self.connector.records.insert('category', '(101010, "test name", "test descriptio")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_14)

        with self.subTest('With 15 records present'):
            # Create record.
            self.connector.records.insert('category', '(1010101, "test name", "test description")', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_logging_output(ilog, 1), self.expected_output.records.SELECT__PT_15)

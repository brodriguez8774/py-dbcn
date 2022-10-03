"""
Initialization of "display" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.
from datetime import datetime

# Internal Imports.
from py_dbcn.constants import (
    OUTPUT_QUERY,
    OUTPUT_RESULTS,
    OUTPUT_RESET,
)


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
            self.assertEqual(return_val, 37 + len(self.db_type))

            # Test with select function. Aka, verify that it equals length of database name.
            db_name_len = len(self.connector.database.select())
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, db_name_len)

            # Test with list being larger.
            test_list = ['{0}__plus_ten'.format(self.test_db_name)]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 47 + len(self.db_type))

            # Test with multiple list values, all smaller.
            test_list = ['a', 'bb', 'ccc']
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 37 + len(self.db_type))

            # Test with multiple list values, one equal.
            test_list = [
                'a',
                'bb',
                'd' * (37 + len(self.db_type)),
                'ccc',
            ]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 37 + len(self.db_type))

            # Test with multiple list values, one larger.
            test_list = [
                'a',
                'bb',
                'd' * (37 + len(self.db_type)),
                'e' * (42 + len(self.db_type)),
                'ccc',
            ]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 42 + len(self.db_type))

            # Test with multiple list values, multiple larger.
            test_list = [
                'a',
                'h' * (44 + len(self.db_type)),
                'f' * (40 + len(self.db_type)),
                'bb',
                'd' * (37 + len(self.db_type)),
                'e' * (42 + len(self.db_type)),
                'ccc',
                'g' * (41 + len(self.db_type)),
            ]
            return_val = self.connector.display._get_longest(test_list)
            self.assertEqual(return_val, 44 + len(self.db_type))


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
        show_tables_query = '{0}{1}{2}'.format(OUTPUT_QUERY, self._show_tables_query, OUTPUT_RESET)

        # Since this directly tests display of tables, ensure we use a fresh database.
        db_name = '{0}d__tables__show'.format(self.test_db_name[0:-15])
        self.connector.database.create(db_name, display_query=False)
        self.connector.database.use(db_name, display_query=False)

        with self.subTest('With no tables present'):
            # Capture logging output.
            with self.assertLogs(None, 'QUERY') as qlog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(qlog, 0), show_tables_query)
            self.assertText(self.get_logging_output(qlog, 1), '{0}Empty Set{1}'.format(OUTPUT_RESULTS, OUTPUT_RESET))

        with self.subTest('Db name longer - Pt 1'):
            # Create table.
            self.connector.tables.create('category', self._columns_clause__basic, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__DB_LONGER__PT_1, OUTPUT_RESET),
            )

        with self.subTest('Db name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('priority', self._columns_clause__basic, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__DB_LONGER__PT_2, OUTPUT_RESET),
            )

        with self.subTest('Db name longer - Pt 3'):
            # Create table.
            self.connector.tables.create('a', self._columns_clause__basic, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__DB_LONGER__PT_3, OUTPUT_RESET),
            )

        with self.subTest('Db name and table name equal length'):
            # Create table.
            self.connector.tables.create(
                'test___{0}___this_is_a_really_long_table_name__test_'.format(self.db_type.lower()),
                self._columns_clause__basic,
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__EQUAL_LENGTH, OUTPUT_RESET),
            )

        with self.subTest('Table name longer - Pt 1'):
            # Create table.
            self.connector.tables.create(
                'test___{0}___this_is_a_really_long_table_name__test__'.format(self.db_type.lower()),
                self._columns_clause__basic,
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__TABLE_LONGER__PT_1, OUTPUT_RESET),
            )

        with self.subTest('Table name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('zzz', self._columns_clause__basic, display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__TABLE_LONGER__PT_2, OUTPUT_RESET),
            )

        with self.subTest('Table name longer - Pt 3'):
            # Create table.
            self.connector.tables.create(
                'test___{0}___this_is_a_really_long_table_name__testing__'.format(self.db_type.lower()),
                self._columns_clause__basic,
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_logging_output(ilog, 0), show_tables_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.SHOW__TABLE_LONGER__PT_3, OUTPUT_RESET),
            )

    def test__display__describe_tables(self):
        """"""
        describe_table_query = '{0}{1}{2}'.format(OUTPUT_QUERY, self._describe_table_query, OUTPUT_RESET)

        # Since this directly tests display of tables, ensure we use a fresh database.
        db_name = '{0}d__tables__desc'.format(self.test_db_name[0:-15])
        self.connector.database.create(db_name, display_query=False)
        self.connector.database.use(db_name, display_query=False)

        # Create initial table to describe.
        self.connector.tables.create('category', self._columns_clause__minimal, display_query=False)

        with self.subTest('With only id'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_logging_output(ilog, 0), describe_table_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.DESCRIBE__COLS_ID, OUTPUT_RESET),
            )

        with self.subTest('With id, name'):
            # Add new table column.
            self.connector.tables.add_column('category', 'name VARCHAR(100)', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_logging_output(ilog, 0), describe_table_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.DESCRIBE__COLS_ID_NAME, OUTPUT_RESET),
            )

        with self.subTest('With id, name, desc'):
            # Add new table column.
            self.connector.tables.add_column('category', 'description VARCHAR(100)', display_query=False)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_logging_output(ilog, 0), describe_table_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.tables.DESCRIBE__COLS_ID_NAME_DESC, OUTPUT_RESET),
            )


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
        select_from_query = '{0}SELECT * FROM category;{1}'.format(OUTPUT_QUERY, OUTPUT_RESET)

        self.connector.tables.create('category', self._columns_clause__basic, display_query=False)

        with self.subTest('With no records present'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}Empty Set{1}'.format(OUTPUT_RESULTS, OUTPUT_RESET),
            )

        with self.subTest('With 1 record present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(1, {0}tn{0}, {0}td{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_1, OUTPUT_RESET),
            )

        with self.subTest('With 2 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(2, {0}t n{0}, {0}t d{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_2, OUTPUT_RESET),
            )

        with self.subTest('With 3 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(3, {0}te n{0}, {0}te d{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_3, OUTPUT_RESET),
            )

        with self.subTest('With 4 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(4, {0}tes n{0}, {0}tes d{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_4, OUTPUT_RESET),
            )

        with self.subTest('With 5 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(5, {0}test n{0}, {0}test d{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_5, OUTPUT_RESET),
            )

        with self.subTest('With 6 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(6, {0}test na{0}, {0}test de{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_6, OUTPUT_RESET),
            )

        with self.subTest('With 7 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(7, {0}test nam{0}, {0}test des{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_7, OUTPUT_RESET),
            )

        with self.subTest('With 8 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(8, {0}test name{0}, {0}test desc{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_8, OUTPUT_RESET),
            )

        with self.subTest('With 9 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(9, {0}test name{0}, {0}test descr{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_9, OUTPUT_RESET),
            )

        with self.subTest('With 10 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(10, {0}test name{0}, {0}test descri{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_10, OUTPUT_RESET),
            )

        with self.subTest('With 11 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(101, {0}test name{0}, {0}test descrip{0})'.format(self.connector.validate._quote_str_literal_format),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_11, OUTPUT_RESET),
            )

        with self.subTest('With 12 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(1010, {0}test name{0}, {0}test descript{0})'.format(
                    self.connector.validate._quote_str_literal_format,
                ),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_12, OUTPUT_RESET),
            )

        with self.subTest('With 13 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(10101, {0}test name{0}, {0}test descripti{0})'.format(
                    self.connector.validate._quote_str_literal_format,
                ),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_13, OUTPUT_RESET),
            )

        with self.subTest('With 14 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(101010, {0}test name{0}, {0}test descriptio{0})'.format(
                    self.connector.validate._quote_str_literal_format,
                ),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_14, OUTPUT_RESET),
            )

        with self.subTest('With 15 records present'):
            # Create record.
            self.connector.records.insert(
                'category',
                '(1010101, {0}test name{0}, {0}test description{0})'.format(
                    self.connector.validate._quote_str_literal_format,
                ),
                display_query=False,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(OUTPUT_RESULTS, self.expected_output.records.SELECT__PT_15, OUTPUT_RESET),
            )

    def test__display__select_records__limited(self):
        """"""
        select_from_query = '{0}SELECT {1} FROM category2;{2}'.format(OUTPUT_QUERY, '{0}', OUTPUT_RESET)
        quoted_id = '{0}id{0}'.format(self.connector.validate._quote_identifier_format)
        quoted_name = '{0}name{0}'.format(self.connector.validate._quote_identifier_format)
        quoted_desc = '{0}description{0}'.format(self.connector.validate._quote_identifier_format)

        # Create table.
        self.connector.tables.create('category2', self._columns_clause__basic, display_query=False)

        # Create record.
        self.connector.records.insert(
            'category2',
            '(1, {0}longer name value{0}, {0}short desc{0})'.format(
                self.connector.validate._quote_str_literal_format,
            ),
            display_query=False,
        )

        with self.subTest('With basic column types - Pull all'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query.format('*'))
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__ALL,
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With basic column types - Exclude id'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'name, description')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_name, quoted_desc))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__OMIT_ID,
                    OUTPUT_RESET
                ),
            )

        with self.subTest('With basic column types - Exclude name'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'id, description')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_id, quoted_desc))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__OMIT_NAME,
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With basic column types - Exclude description'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'id, name')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_id, quoted_name))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__OMIT_DESC,
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With basic column types - Pull all reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'description, name, id')
            curr_select_clause = select_from_query.format('{0}, {1}, {2}'.format(quoted_desc, quoted_name, quoted_id))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__REVERSED_ALL,
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With basic column types - Exclude id reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'description, name')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_desc, quoted_name))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__REVERSED_OMIT_ID,
                    OUTPUT_RESET
                ),
            )

        with self.subTest('With basic column types - Exclude name reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'description, id')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_desc, quoted_id))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__REVERSED_OMIT_NAME,
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With basic column types - Exclude description reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category2', 'name, id')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_name, quoted_id))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__BASIC__REVERSED_OMIT_DESC,
                    OUTPUT_RESET,
                ),
            )

        datetime_now = datetime.now()
        select_from_query = '{0}SELECT {1} FROM category3;{2}'.format(OUTPUT_QUERY, '{0}', OUTPUT_RESET)
        quoted_datetime = '{0}test_datetime{0}'.format(self.connector.validate._quote_identifier_format)
        quoted_date = '{0}test_date{0}'.format(self.connector.validate._quote_identifier_format)

        # Create table.
        self.connector.tables.create('category3', self._columns_clause__datetime, display_query=False)

        # Create record.
        self.connector.records.insert('category3', [1, datetime_now, datetime_now], display_query=False)

        with self.subTest('With datetime column types - Pull all'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3')
            self.assertText(self.get_logging_output(ilog, 0), select_from_query.format('*'))
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__ALL.format(
                        datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
                        datetime_now.date(),
                    ),
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With datetime column types - Exclude id'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'test_datetime, test_date')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_datetime, quoted_date))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__OMIT_ID.format(
                        datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
                        datetime_now.date(),
                    ),
                    OUTPUT_RESET
                ),
            )

        with self.subTest('With datetime column types - Exclude datetime'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'id, test_date')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_id, quoted_date))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__OMIT_DATETIME.format(
                        datetime_now.date(),
                    ),
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With datetime column types - Exclude date'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'id, test_datetime')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_id, quoted_datetime))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__OMIT_DATE.format(
                        datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
                    ),
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With datetime column types - Pull all reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'test_date, test_datetime, id')
            curr_select_clause = select_from_query.format(
                '{0}, {1}, {2}'.format(quoted_date, quoted_datetime, quoted_id),
            )
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__REVERSED_ALL.format(
                        datetime_now.date(),
                        datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
                    ),
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With datetime column types - Exclude id reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'test_date, test_datetime')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_date, quoted_datetime))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__REVERSED_OMIT_ID.format(
                        datetime_now.date(),
                        datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
                    ),
                    OUTPUT_RESET
                ),
            )

        with self.subTest('With datetime column types - Exclude datetime reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'test_date, id')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_date, quoted_id))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATETIME.format(
                        datetime_now.date(),
                    ),
                    OUTPUT_RESET,
                ),
            )

        with self.subTest('With datetime column types - Exclude date reversed'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category3', 'test_datetime, id')
            curr_select_clause = select_from_query.format('{0}, {1}'.format(quoted_datetime, quoted_id))
            self.assertText(self.get_logging_output(ilog, 0), curr_select_clause)
            self.assertText(
                self.get_logging_output(ilog, 1),
                '{0}{1}{2}'.format(
                    OUTPUT_RESULTS,
                    self.expected_output.records.LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATE.format(
                        datetime_now.strftime('%Y-%m-%d %H:%M:%S'),
                    ),
                    OUTPUT_RESET,
                ),
            )

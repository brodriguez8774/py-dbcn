"""
Tests for "display" logic of "MySQL" DB Connector class.
"""

# System Imports.

# User Imports.
from .test_core import TestMysqlDatabaseParent


EXPECTED__TABLE__SHOW__DB_LONGER__PT_1 = """
+------------------------------------------------------+
| Tables in python__db_connector__test_d__tables__show |
+------------------------------------------------------+
| category                                             |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__DB_LONGER__PT_2 = """
+------------------------------------------------------+
| Tables in python__db_connector__test_d__tables__show |
+------------------------------------------------------+
| category                                             |
| priority                                             |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__DB_LONGER__PT_3 = """
+------------------------------------------------------+
| Tables in python__db_connector__test_d__tables__show |
+------------------------------------------------------+
| a                                                    |
| category                                             |
| priority                                             |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__EQUAL_LENGTH = """
+------------------------------------------------------+
| Tables in python__db_connector__test_d__tables__show |
+------------------------------------------------------+
| a                                                    |
| category                                             |
| priority                                             |
| test__testing__this_is__really_long_table_name__test |
+------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_1 = """
+-------------------------------------------------------+
| Tables in python__db_connector__test_d__tables__show  |
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
| Tables in python__db_connector__test_d__tables__show  |
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
| Tables in python__db_connector__test_d__tables__show     |
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


EXPECTED__TABLE__DESCRIBE__COLS_ID = """
+-------+------+------+-----+---------+----------------+
| Field | Type | Null | Key | Default | Extra          |
+-------+------+------+-----+---------+----------------+
| id    | int  | NO   | PRI | NULL    | auto_increment |
+-------+------+------+-----+---------+----------------+
"""


EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME = """
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | YES  |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
"""


EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME_DESC = """
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int          | NO   | PRI | NULL    | auto_increment |
| name        | varchar(100) | YES  |     | NULL    |                |
| description | varchar(100) | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
"""


EXPECTED__RECORD__SELECT__PT_1 = """
+----+------+-------------+
| id | name | description |
+----+------+-------------+
| 1  | tn   | td          |
+----+------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_2 = """
+----+------+-------------+
| id | name | description |
+----+------+-------------+
| 1  | tn   | td          |
| 2  | t n  | t d         |
+----+------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_3 = """
+----+------+-------------+
| id | name | description |
+----+------+-------------+
| 1  | tn   | td          |
| 2  | t n  | t d         |
| 3  | te n | te d        |
+----+------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_4 = """
+----+-------+-------------+
| id | name  | description |
+----+-------+-------------+
| 1  | tn    | td          |
| 2  | t n   | t d         |
| 3  | te n  | te d        |
| 4  | tes n | tes d       |
+----+-------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_5 = """
+----+--------+-------------+
| id | name   | description |
+----+--------+-------------+
| 1  | tn     | td          |
| 2  | t n    | t d         |
| 3  | te n   | te d        |
| 4  | tes n  | tes d       |
| 5  | test n | test d      |
+----+--------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_6 = """
+----+---------+-------------+
| id | name    | description |
+----+---------+-------------+
| 1  | tn      | td          |
| 2  | t n     | t d         |
| 3  | te n    | te d        |
| 4  | tes n   | tes d       |
| 5  | test n  | test d      |
| 6  | test na | test de     |
+----+---------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_7 = """
+----+----------+-------------+
| id | name     | description |
+----+----------+-------------+
| 1  | tn       | td          |
| 2  | t n      | t d         |
| 3  | te n     | te d        |
| 4  | tes n    | tes d       |
| 5  | test n   | test d      |
| 6  | test na  | test de     |
| 7  | test nam | test des    |
+----+----------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_8 = """
+----+-----------+-------------+
| id | name      | description |
+----+-----------+-------------+
| 1  | tn        | td          |
| 2  | t n       | t d         |
| 3  | te n      | te d        |
| 4  | tes n     | tes d       |
| 5  | test n    | test d      |
| 6  | test na   | test de     |
| 7  | test nam  | test des    |
| 8  | test name | test desc   |
+----+-----------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_9 = """
+----+-----------+-------------+
| id | name      | description |
+----+-----------+-------------+
| 1  | tn        | td          |
| 2  | t n       | t d         |
| 3  | te n      | te d        |
| 4  | tes n     | tes d       |
| 5  | test n    | test d      |
| 6  | test na   | test de     |
| 7  | test nam  | test des    |
| 8  | test name | test desc   |
| 9  | test name | test descr  |
+----+-----------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_10 = """
+----+-----------+-------------+
| id | name      | description |
+----+-----------+-------------+
| 1  | tn        | td          |
| 2  | t n       | t d         |
| 3  | te n      | te d        |
| 4  | tes n     | tes d       |
| 5  | test n    | test d      |
| 6  | test na   | test de     |
| 7  | test nam  | test des    |
| 8  | test name | test desc   |
| 9  | test name | test descr  |
| 10 | test name | test descri |
+----+-----------+-------------+
"""
EXPECTED__RECORD__SELECT__PT_11 = """
+-----+-----------+--------------+
| id  | name      | description  |
+-----+-----------+--------------+
| 1   | tn        | td           |
| 2   | t n       | t d          |
| 3   | te n      | te d         |
| 4   | tes n     | tes d        |
| 5   | test n    | test d       |
| 6   | test na   | test de      |
| 7   | test nam  | test des     |
| 8   | test name | test desc    |
| 9   | test name | test descr   |
| 10  | test name | test descri  |
| 101 | test name | test descrip |
+-----+-----------+--------------+
"""
EXPECTED__RECORD__SELECT__PT_12 = """
+------+-----------+---------------+
| id   | name      | description   |
+------+-----------+---------------+
| 1    | tn        | td            |
| 2    | t n       | t d           |
| 3    | te n      | te d          |
| 4    | tes n     | tes d         |
| 5    | test n    | test d        |
| 6    | test na   | test de       |
| 7    | test nam  | test des      |
| 8    | test name | test desc     |
| 9    | test name | test descr    |
| 10   | test name | test descri   |
| 101  | test name | test descrip  |
| 1010 | test name | test descript |
+------+-----------+---------------+
"""
EXPECTED__RECORD__SELECT__PT_13 = """
+-------+-----------+----------------+
| id    | name      | description    |
+-------+-----------+----------------+
| 1     | tn        | td             |
| 2     | t n       | t d            |
| 3     | te n      | te d           |
| 4     | tes n     | tes d          |
| 5     | test n    | test d         |
| 6     | test na   | test de        |
| 7     | test nam  | test des       |
| 8     | test name | test desc      |
| 9     | test name | test descr     |
| 10    | test name | test descri    |
| 101   | test name | test descrip   |
| 1010  | test name | test descript  |
| 10101 | test name | test descripti |
+-------+-----------+----------------+
"""
EXPECTED__RECORD__SELECT__PT_14 = """
+--------+-----------+-----------------+
| id     | name      | description     |
+--------+-----------+-----------------+
| 1      | tn        | td              |
| 2      | t n       | t d             |
| 3      | te n      | te d            |
| 4      | tes n     | tes d           |
| 5      | test n    | test d          |
| 6      | test na   | test de         |
| 7      | test nam  | test des        |
| 8      | test name | test desc       |
| 9      | test name | test descr      |
| 10     | test name | test descri     |
| 101    | test name | test descrip    |
| 1010   | test name | test descript   |
| 10101  | test name | test descripti  |
| 101010 | test name | test descriptio |
+--------+-----------+-----------------+
"""
EXPECTED__RECORD__SELECT__PT_15 = """
+---------+-----------+------------------+
| id      | name      | description      |
+---------+-----------+------------------+
| 1       | tn        | td               |
| 2       | t n       | t d              |
| 3       | te n      | te d             |
| 4       | tes n     | tes d            |
| 5       | test n    | test d           |
| 6       | test na   | test de          |
| 7       | test nam  | test des         |
| 8       | test name | test desc        |
| 9       | test name | test descr       |
| 10      | test name | test descri      |
| 101     | test name | test descrip     |
| 1010    | test name | test descript    |
| 10101   | test name | test descripti   |
| 101010  | test name | test descriptio  |
| 1010101 | test name | test description |
+---------+-----------+------------------+
"""


class TestMysqlDisplayAbstract(TestMysqlDatabaseParent):
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


class TestMysqlDisplayCore(TestMysqlDisplayAbstract):
    """
    Tests "MySQL" DB Connector class display logic.

    Specifically tests logic defined in base display class.
    """

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


class TestMysqlDisplayTables(TestMysqlDisplayAbstract):
    """
    Tests "MySQL" DB Connector class display logic.

    Specifically tests logic defined in "tables" display subclass.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize database for tests.
        cls.db_name = 'python__db_connector__test_display__tables'
        cls.connector.database.create(cls.db_name)
        cls.connector.database.use(cls.db_name)

    def test__display__show_tables(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            description VARCHAR(100),
            PRIMARY KEY ( id )
        )"""

        # Since this directly tests display of tables, ensure we use a fresh database.
        db_name = '{0}d__tables__show'.format(self.db_name[0:-15])
        self.connector.database.create(db_name)
        self.connector.database.use(db_name)

        with self.subTest('With no tables present'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), 'Empty Set')

        with self.subTest('Db name longer - Pt 1'):
            # Create table.
            self.connector.tables.create('category', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__DB_LONGER__PT_1)

        with self.subTest('Db name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('priority', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__DB_LONGER__PT_2)

        with self.subTest('Db name longer - Pt 3'):
            # Create table.
            self.connector.tables.create('a', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__DB_LONGER__PT_3)

        with self.subTest('Db name and table name equal length'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is__really_long_table_name__test',
                columns,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__EQUAL_LENGTH)

        with self.subTest('Table name longer - Pt 1'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__test',
                columns,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_1)

        with self.subTest('Table name longer - Pt 2'):
            # Create table.
            self.connector.tables.create('zzz', columns)

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_2)

        with self.subTest('Table name longer - Pt 3'):
            # Create table.
            self.connector.tables.create(
                'test__testing__this_is_a_really_long_table_name__testing',
                columns,
            )

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.show()
            self.assertText(self.get_output(ilog, 0), 'SHOW TABLES;')
            self.assertText(self.get_output(ilog, 1), EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_3)

    def test__display__describe_tables(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            PRIMARY KEY ( id )
        )"""

        # Since this directly tests display of tables, ensure we use a fresh database.
        db_name = '{0}d__tables__desc'.format(self.db_name[0:-15])
        self.connector.database.create(db_name)
        self.connector.database.use(db_name)

        # Create initial table to describe.
        self.connector.tables.create('category', columns)

        with self.subTest('With only id'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_output(ilog, 1), 'DESCRIBE category;')
            self.assertText(self.get_output(ilog, 2), EXPECTED__TABLE__DESCRIBE__COLS_ID)

        with self.subTest('With id, name'):
            # Add new table column.
            self.connector.tables.add_column('category', 'name VARCHAR(100)')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_output(ilog, 1), 'DESCRIBE category;')
            self.assertText(self.get_output(ilog, 2), EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME)

        with self.subTest('With id, name, desc'):
            # Add new table column.
            self.connector.tables.add_column('category', 'description VARCHAR(100)')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.tables.describe('category')
            self.assertText(self.get_output(ilog, 1), 'DESCRIBE category;')
            self.assertText(self.get_output(ilog, 2), EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME_DESC)


class TestMysqlDisplayRecords(TestMysqlDisplayAbstract):
    """
    Tests "MySQL" DB Connector class display logic.

    Specifically tests logic defined in "records" display subclass.
    """
    @classmethod
    def setUpClass(cls):
        # Run parent setup logic.
        super().setUpClass()

        # Initialize database for tests.
        cls.db_name = 'python__db_connector__test_display__records'
        cls.connector.database.create(cls.db_name)
        cls.connector.database.use(cls.db_name)

    def test__display__select_records__basic(self):
        """"""
        columns = """(
            id INT NOT NULL AUTO_INCREMENT,
            name VARCHAR(100),
            description VARCHAR(100),
            PRIMARY KEY ( id )
        )"""

        self.connector.tables.create('category', columns)

        with self.subTest('With no records present'):
            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 2), 'Empty Set')

        with self.subTest('With 1 record present'):
            # Create record.
            self.connector.records.insert('category', '(1, "tn", "td")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_1)

        with self.subTest('With 2 records present'):
            # Create record.
            self.connector.records.insert('category', '(2, "t n", "t d")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_2)

        with self.subTest('With 3 records present'):
            # Create record.
            self.connector.records.insert('category', '(3, "te n", "te d")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_3)

        with self.subTest('With 4 records present'):
            # Create record.
            self.connector.records.insert('category', '(4, "tes n", "tes d")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_4)

        with self.subTest('With 5 records present'):
            # Create record.
            self.connector.records.insert('category', '(5, "test n", "test d")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_5)

        with self.subTest('With 6 records present'):
            # Create record.
            self.connector.records.insert('category', '(6, "test na", "test de")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_6)

        with self.subTest('With 7 records present'):
            # Create record.
            self.connector.records.insert('category', '(7, "test nam", "test des")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_7)

        with self.subTest('With 8 records present'):
            # Create record.
            self.connector.records.insert('category', '(8, "test name", "test desc")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_8)

        with self.subTest('With 9 records present'):
            # Create record.
            self.connector.records.insert('category', '(9, "test name", "test descr")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_9)

        with self.subTest('With 10 records present'):
            # Create record.
            self.connector.records.insert('category', '(10, "test name", "test descri")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_10)

        with self.subTest('With 11 records present'):
            # Create record.
            self.connector.records.insert('category', '(101, "test name", "test descrip")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_11)

        with self.subTest('With 12 records present'):
            # Create record.
            self.connector.records.insert('category', '(1010, "test name", "test descript")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_12)

        with self.subTest('With 13 records present'):
            # Create record.
            self.connector.records.insert('category', '(10101, "test name", "test descripti")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_13)

        with self.subTest('With 14 records present'):
            # Create record.
            self.connector.records.insert('category', '(101010, "test name", "test descriptio")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_14)

        with self.subTest('With 15 records present'):
            # Create record.
            self.connector.records.insert('category', '(1010101, "test name", "test description")')

            # Capture logging output.
            with self.assertLogs(None, 'INFO') as ilog:
                self.connector.records.select('category')
            self.assertText(self.get_output(ilog, 0), 'SELECT * FROM category;')
            self.assertText(self.get_output(ilog, 8), EXPECTED__RECORD__SELECT__PT_15)

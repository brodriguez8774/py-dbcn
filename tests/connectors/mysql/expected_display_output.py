"""
Expected display output for various functions.
"""


# region Table Display Output

EXPECTED__TABLE__SHOW__DB_LONGER__PT_1 = """
+--------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show |
+--------------------------------------------------------+
| category                                               |
+--------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__DB_LONGER__PT_2 = """
+--------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show |
+--------------------------------------------------------+
| category                                               |
| priority                                               |
+--------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__DB_LONGER__PT_3 = """
+--------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show |
+--------------------------------------------------------+
| a                                                      |
| category                                               |
| priority                                               |
+--------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__EQUAL_LENGTH = """
+--------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show |
+--------------------------------------------------------+
| a                                                      |
| category                                               |
| priority                                               |
| test___mysql___this_is_a_really_long_table_name__test_ |
+--------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_1 = """
+---------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show  |
+---------------------------------------------------------+
| a                                                       |
| category                                                |
| priority                                                |
| test___mysql___this_is_a_really_long_table_name__test_  |
| test___mysql___this_is_a_really_long_table_name__test__ |
+---------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_2 = """
+---------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show  |
+---------------------------------------------------------+
| a                                                       |
| category                                                |
| priority                                                |
| test___mysql___this_is_a_really_long_table_name__test_  |
| test___mysql___this_is_a_really_long_table_name__test__ |
| zzz                                                     |
+---------------------------------------------------------+
""".strip()


EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_3 = """
+------------------------------------------------------------+
| Tables in pydbcn__MySQL_unittest__test_d__tables__show     |
+------------------------------------------------------------+
| a                                                          |
| category                                                   |
| priority                                                   |
| test___mysql___this_is_a_really_long_table_name__test_     |
| test___mysql___this_is_a_really_long_table_name__test__    |
| test___mysql___this_is_a_really_long_table_name__testing__ |
| zzz                                                        |
+------------------------------------------------------------+
""".strip()


EXPECTED__TABLE__DESCRIBE__COLS_ID = """
+-------+------+------+-----+---------+----------------+
| Field | Type | Null | Key | Default | Extra          |
+-------+------+------+-----+---------+----------------+
| id    | int  | NO   | PRI | NULL    | auto_increment |
+-------+------+------+-----+---------+----------------+
""".strip()


EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME = """
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| id    | int          | NO   | PRI | NULL    | auto_increment |
| name  | varchar(100) | YES  |     | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
""".strip()


EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME_DESC = """
+-------------+--------------+------+-----+---------+----------------+
| Field       | Type         | Null | Key | Default | Extra          |
+-------------+--------------+------+-----+---------+----------------+
| id          | int          | NO   | PRI | NULL    | auto_increment |
| name        | varchar(100) | YES  |     | NULL    |                |
| description | varchar(100) | YES  |     | NULL    |                |
+-------------+--------------+------+-----+---------+----------------+
""".strip()

# endregion Table Display Output


# region Record Display Output

EXPECTED__RECORD__SELECT__PT_1 = """
+----+------+-------------+
| id | name | description |
+----+------+-------------+
| 1  | tn   | td          |
+----+------+-------------+
""".strip()


EXPECTED__RECORD__SELECT__PT_2 = """
+----+------+-------------+
| id | name | description |
+----+------+-------------+
| 1  | tn   | td          |
| 2  | t n  | t d         |
+----+------+-------------+
""".strip()


EXPECTED__RECORD__SELECT__PT_3 = """
+----+------+-------------+
| id | name | description |
+----+------+-------------+
| 1  | tn   | td          |
| 2  | t n  | t d         |
| 3  | te n | te d        |
+----+------+-------------+
""".strip()


EXPECTED__RECORD__SELECT__PT_4 = """
+----+-------+-------------+
| id | name  | description |
+----+-------+-------------+
| 1  | tn    | td          |
| 2  | t n   | t d         |
| 3  | te n  | te d        |
| 4  | tes n | tes d       |
+----+-------+-------------+
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


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
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__ALL = """
+----+-------------------+-------------+
| id | name              | description |
+----+-------------------+-------------+
| 1  | longer name value | short desc  |
+----+-------------------+-------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__OMIT_ID = """
+-------------------+-------------+
| name              | description |
+-------------------+-------------+
| longer name value | short desc  |
+-------------------+-------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__OMIT_NAME = """
+----+-------------+
| id | description |
+----+-------------+
| 1  | short desc  |
+----+-------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__OMIT_DESC = """
+----+-------------------+
| id | name              |
+----+-------------------+
| 1  | longer name value |
+----+-------------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_ALL = """
+-------------+-------------------+----+
| description | name              | id |
+-------------+-------------------+----+
| short desc  | longer name value | 1  |
+-------------+-------------------+----+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_OMIT_ID = """
+-------------+-------------------+
| description | name              |
+-------------+-------------------+
| short desc  | longer name value |
+-------------+-------------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_OMIT_NAME = """
+-------------+----+
| description | id |
+-------------+----+
| short desc  | 1  |
+-------------+----+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_OMIT_DESC = """
+-------------------+----+
| name              | id |
+-------------------+----+
| longer name value | 1  |
+-------------------+----+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__ALL = """
+----+---------------------+------------+
| id | test_datetime       | test_date  |
+----+---------------------+------------+
| 1  | {0} | {1} |
+----+---------------------+------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__OMIT_ID = """
+---------------------+------------+
| test_datetime       | test_date  |
+---------------------+------------+
| {0} | {1} |
+---------------------+------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__OMIT_DATETIME = """
+----+------------+
| id | test_date  |
+----+------------+
| 1  | {0} |
+----+------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__OMIT_DATE = """
+----+---------------------+
| id | test_datetime       |
+----+---------------------+
| 1  | {0} |
+----+---------------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_ALL = """
+------------+---------------------+----+
| test_date  | test_datetime       | id |
+------------+---------------------+----+
| {0} | {1} | 1  |
+------------+---------------------+----+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_OMIT_ID = """
+------------+---------------------+
| test_date  | test_datetime       |
+------------+---------------------+
| {0} | {1} |
+------------+---------------------+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATETIME = """
+------------+----+
| test_date  | id |
+------------+----+
| {0} | 1  |
+------------+----+
""".strip()


EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATE = """
+---------------------+----+
| test_datetime       | id |
+---------------------+----+
| {0} | 1  |
+---------------------+----+
""".strip()

# endregion Record Display Output


class ExpectedOutput:
    """Class of expected output values, for easy importing into test files."""

    class Tables:
        SHOW__DB_LONGER__PT_1 = EXPECTED__TABLE__SHOW__DB_LONGER__PT_1
        SHOW__DB_LONGER__PT_2 = EXPECTED__TABLE__SHOW__DB_LONGER__PT_2
        SHOW__DB_LONGER__PT_3 = EXPECTED__TABLE__SHOW__DB_LONGER__PT_3
        SHOW__EQUAL_LENGTH = EXPECTED__TABLE__SHOW__EQUAL_LENGTH
        SHOW__TABLE_LONGER__PT_1 = EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_1
        SHOW__TABLE_LONGER__PT_2 = EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_2
        SHOW__TABLE_LONGER__PT_3 = EXPECTED__TABLE__SHOW__TABLE_LONGER__PT_3
        DESCRIBE__COLS_ID = EXPECTED__TABLE__DESCRIBE__COLS_ID
        DESCRIBE__COLS_ID_NAME = EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME
        DESCRIBE__COLS_ID_NAME_DESC = EXPECTED__TABLE__DESCRIBE__COLS_ID_NAME_DESC

    class Records:
        SELECT__PT_1 = EXPECTED__RECORD__SELECT__PT_1
        SELECT__PT_2 = EXPECTED__RECORD__SELECT__PT_2
        SELECT__PT_3 = EXPECTED__RECORD__SELECT__PT_3
        SELECT__PT_4 = EXPECTED__RECORD__SELECT__PT_4
        SELECT__PT_5 = EXPECTED__RECORD__SELECT__PT_5
        SELECT__PT_6 = EXPECTED__RECORD__SELECT__PT_6
        SELECT__PT_7 = EXPECTED__RECORD__SELECT__PT_7
        SELECT__PT_8 = EXPECTED__RECORD__SELECT__PT_8
        SELECT__PT_9 = EXPECTED__RECORD__SELECT__PT_9
        SELECT__PT_10 = EXPECTED__RECORD__SELECT__PT_10
        SELECT__PT_11 = EXPECTED__RECORD__SELECT__PT_11
        SELECT__PT_12 = EXPECTED__RECORD__SELECT__PT_12
        SELECT__PT_13 = EXPECTED__RECORD__SELECT__PT_13
        SELECT__PT_14 = EXPECTED__RECORD__SELECT__PT_14
        SELECT__PT_15 = EXPECTED__RECORD__SELECT__PT_15

        LIMITED_SELECT__BASIC__ALL = EXPECTED__RECORD__LIMITED_SELECT__BASIC__ALL
        LIMITED_SELECT__BASIC__OMIT_ID = EXPECTED__RECORD__LIMITED_SELECT__BASIC__OMIT_ID
        LIMITED_SELECT__BASIC__OMIT_NAME = EXPECTED__RECORD__LIMITED_SELECT__BASIC__OMIT_NAME
        LIMITED_SELECT__BASIC__OMIT_DESC = EXPECTED__RECORD__LIMITED_SELECT__BASIC__OMIT_DESC
        LIMITED_SELECT__BASIC__REVERSED_ALL = EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_ALL
        LIMITED_SELECT__BASIC__REVERSED_OMIT_ID = EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_OMIT_ID
        LIMITED_SELECT__BASIC__REVERSED_OMIT_NAME = EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_OMIT_NAME
        LIMITED_SELECT__BASIC__REVERSED_OMIT_DESC = EXPECTED__RECORD__LIMITED_SELECT__BASIC__REVERSED_OMIT_DESC

        LIMITED_SELECT__DATETIME__ALL = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__ALL
        LIMITED_SELECT__DATETIME__OMIT_ID = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__OMIT_ID
        LIMITED_SELECT__DATETIME__OMIT_DATETIME = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__OMIT_DATETIME
        LIMITED_SELECT__DATETIME__OMIT_DATE = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__OMIT_DATE
        LIMITED_SELECT__DATETIME__REVERSED_ALL = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_ALL
        LIMITED_SELECT__DATETIME__REVERSED_OMIT_ID = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_OMIT_ID
        LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATETIME = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATETIME
        LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATE = EXPECTED__RECORD__LIMITED_SELECT__DATETIME__REVERSED_OMIT_DATE

    tables = Tables()
    records = Records()

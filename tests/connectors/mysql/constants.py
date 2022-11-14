"""
Various testing constants for MySQL.
"""


SHOW_TABLES_QUERY = """
SHOW TABLES;
""".strip()


DESCRIBE_TABLE_QUERY = """
DESCRIBE category;
""".strip()


COLUMNS_CLAUSE__MINIMAL = """
(
    id INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY ( id )
)
""".strip()


COLUMNS_CLAUSE__BASIC = """
(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100),
    description VARCHAR(100),
    PRIMARY KEY ( id )
)
""".strip()


COLUMNS_CLAUSE__DATETIME = """
(
    id INT NOT NULL AUTO_INCREMENT,
    test_datetime DATETIME,
    test_date DATE,
    PRIMARY KEY ( id )
)
""".strip()


COLUMNS_CLAUSE__AGGREGATES = """
(
    id INT NOT NULL AUTO_INCREMENT,
    test_str VARCHAR(100),
    test_int INT,
    test_bool TINYINT,
    PRIMARY KEY ( id )
)
""".strip()

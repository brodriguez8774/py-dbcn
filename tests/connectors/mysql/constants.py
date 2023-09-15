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


COLUMNS_CLAUSE__INSERT_BUG__NUMBER_OF_VALUES = """
(
    id INT NOT NULL AUTO_INCREMENT,
    test_blank_1 VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    test_blank_2 VARCHAR(255),
    address1 VARCHAR(255),
    address2 VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zipcode VARCHAR(255),
    test_blank_3 VARCHAR(255),
    phone VARCHAR(255),
    fax VARCHAR(255),
    email VARCHAR(255),
    test_blank_4 VARCHAR(255),
    date_created DATETIME,
    date_modified DATETIME,
    is_active TINYINT,
    last_activity TIMESTAMP,
    test_blank_5 VARCHAR(255),
    PRIMARY KEY ( id )
)
"""

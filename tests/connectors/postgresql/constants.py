"""
Various testing constants for PostgreSQL.
"""


SHOW_TABLES_QUERY = """
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public';
""".strip()


DESCRIBE_TABLE_QUERY = """
SELECT * FROM information_schema.columns
WHERE (table_schema = 'public' AND table_name = 'category');
""".strip()


COLUMNS_CLAUSE__MINIMAL = """
(
    id serial PRIMARY KEY
)
""".strip()


COLUMNS_CLAUSE__BASIC = """
(
    id serial PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(100)
)
""".strip()


COLUMNS_CLAUSE__DATETIME = """
(
    id serial PRIMARY KEY,
    test_datetime TIMESTAMP,
    test_date DATE
)
""".strip()


COLUMNS_CLAUSE__AGGREGATES = """
(
    id serial PRIMARY KEY,
    test_str VARCHAR(100),
    test_int INTEGER,
    test_bool BOOLEAN
)
""".strip()


COLUMNS_CLAUSE__INSERT_BUG__NUMBER_OF_VALUES = """
(
    id serial PRIMARY KEY,
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
    date_created TIMESTAMP,
    date_modified TIMESTAMP,
    is_active BOOLEAN,
    last_activity TIMESTAMP,
    test_blank_5 VARCHAR(255)
)
""".strip()

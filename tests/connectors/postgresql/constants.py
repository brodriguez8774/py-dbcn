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

import sqlite3

from agentic_ai.functions.sqldb_fn import get_conn, get_db_schema


def test_get_db_schema_contains_table():
    # create an in-memory database and a test table
    conn = get_conn(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);")
    conn.commit()

    schema = get_db_schema(conn)

    assert 'test_table' in schema
    assert 'CREATE TABLE' in schema.upper()

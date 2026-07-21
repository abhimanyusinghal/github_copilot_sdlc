"""User-lookup helpers for the Copilot lab - SECURITY exercise.

WARNING: `find_user_by_name` is intentionally vulnerable to SQL injection -
it builds the query by string concatenation. You will spot and fix this
during the lab (code review / agent mode / Autofix). The secure version uses
a parameterized query; see the acceptance criteria in the lab handout.

The database is a throwaway in-memory SQLite instance, so this runs with no
external setup.
"""

import sqlite3


def demo_connection():
    """Create an in-memory SQLite DB seeded with a couple of demo users."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)"
    )
    conn.executemany(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        [("ada", "ada@example.com"), ("linus", "linus@example.com")],
    )
    conn.commit()
    return conn


def find_user_by_name(conn, name):
    # VULNERABLE: user input is concatenated straight into the SQL string.
    # A name like:  ' OR '1'='1  returns every row. Fix with a parameterized query.
    query = "SELECT id, name, email FROM users WHERE name = '" + name + "'"
    return conn.execute(query).fetchall()

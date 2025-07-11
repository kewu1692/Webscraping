#!/usr/bin/env python3
"""
Quick-load users.csv into MySQL.

Prerequisites
-------------
pip install mysql-connector-python pandas

Environment variables (override defaults as needed)
---------------------------------------------------
MYSQL_HOST     default: 'localhost'
MYSQL_PORT     default: 3306
MYSQL_USER     default: 'root'
MYSQL_PASSWORD default: ''
MYSQL_DB       default: 'global_database'

Usage
-----
python load_users.py /path/to/users.csv
"""
import os
import sys
import pandas as pd
import mysql.connector
from pathlib import Path

# --------- Helpers ---------
def connect():
    """Return an open MySQL connection using env-var credentials."""
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "my-secret-pw"),
        database=os.getenv("MYSQL_DB", "global_database"),
        autocommit=False,
    )

def validate_columns(df):
    """Verify required columns exist before loading."""
    required = {
        "user_id",
        "name",
        "level",
        "points",
        "review_count",
        "photo_count",
        "created_at",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing required column(s): {', '.join(sorted(missing))}")

# ------------- Main -------------
def main(csv_file: Path):
    df = pd.read_csv(csv_file)
    validate_columns(df)

    insert_sql = """
        INSERT INTO users
            (user_id, name, level, points, review_count, photo_count, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name          = VALUES(name),
            level         = VALUES(level),
            points        = VALUES(points),
            review_count  = VALUES(review_count),
            photo_count   = VALUES(photo_count),
            created_at    = VALUES(created_at)
    """

    conn = connect()
    cur = conn.cursor()
    try:
        cur.executemany(insert_sql, [tuple(row) for row in df.to_numpy()])
        conn.commit()
        print(f"✓ Loaded {cur.rowcount} rows into users.")
    except Exception as exc:
        conn.rollback()
        print(f"[ERROR] {exc}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_users.py /path/to/users.csv")
        sys.exit(1)
    main(Path(sys.argv[1]).expanduser().resolve())
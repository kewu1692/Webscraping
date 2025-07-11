
#!/usr/bin/env python3
"""Load res_queue.csv into an existing global_database.res_queue table.

Prerequisites:
    pip install mysql-connector-python pandas

Environment variables (override defaults):
    MYSQL_HOST     default: 'localhost'
    MYSQL_PORT     default: 3306
    MYSQL_USER     default: 'root'
    MYSQL_PASSWORD default: ''
    MYSQL_DB       default: 'global_database'

Usage:
    python load_res_queue.py /path/to/res_queue.csv
"""
import os
import sys
import pandas as pd
import mysql.connector
from pathlib import Path

def connect():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "my-secret-pw"),
        database=os.getenv("MYSQL_DB", "global_database"),
        autocommit=False,
    )

def validate_cols(df):
    expected = {
        "work_id",
        "res_name",
        "status",
        "res_url",
        "created_at",
        "updated_at",
    }
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {', '.join(sorted(missing))}")

INSERT_SQL = """
    INSERT INTO res_queue
        (work_id, res_name, status, res_url, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        res_name   = VALUES(res_name),
        status     = VALUES(status),
        res_url    = VALUES(res_url),
        created_at = VALUES(created_at),
        updated_at = VALUES(updated_at)
"""

def main(csv_file: Path):
    df = pd.read_csv(csv_file)
    validate_cols(df)

    conn = connect()
    cur = conn.cursor()
    try:
        cur.executemany(INSERT_SQL, [tuple(row) for row in df.to_numpy()])
        conn.commit()
        print(f"✓ Loaded {cur.rowcount} rows into res_queue.")
    except Exception as exc:
        conn.rollback()
        print(f"[ERROR] {exc}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python load_res_queue.py /path/to/res_queue.csv")
        sys.exit(1)
    main(Path(sys.argv[1]).expanduser().resolve())

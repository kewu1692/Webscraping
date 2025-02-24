import mysql.connector
from mysql.connector import Error as e
import os

# create connection
def create_conn(host, password, database):
    conn = mysql.connector.connect(
        host = "54.145.65.145",
        user = "root",
        password = "your_secure_password"
        )
    return conn

# create cursor
def create_cur(conn):
    return conn.cursor()

# execution
def execute(cursor, query):
    cursor.execute(query)

# read query
def read_sql(file_path, mode):
   file = open(file_path, mode)
   return file.read()

# roll back
def roll_back(conn):
    print(f"Error: {e}")
    if conn:
        conn.rollback()  # Rollback changes on error
        print("Transaction rolled back.")
    
# closing connection
def close(cursor, conn):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
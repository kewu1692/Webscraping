import mysql.connector
from mysql.connector import Error
import os
import time

# create connection
def create_conn(host, user, password):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )
    return conn

# create cursor
def create_cur(conn):
    return conn.cursor()

# read query
def read_sql(file_path, mode):
   file = open(file_path, mode)
   return file.read()

# find new res users
def find_new_res_users(cursor):
    # select only new status
    cursor.execute("SELECT res_name FROM global_database.res_queue")
    rests = cursor.fetchall()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()
    for res in rests:
        return res if res not in databases else None
    
# create db and review table for new res users
def set_up_new_res(cursor):
    print(f"Starting monitoring...")
    print(f"New restaurant detected! Restaurant Name: {rests}")
    # change status after processing
    try:
        while True:
            time.sleep(5)
            rests = find_new_res_users(cursor)
            for res in rests:
                with open('./sql/res_db/res_db.sql', 'r') as file1:
                    db_query = file1.read()
                    db_query = db_query.replace("<RES_NAME>", res)
                    cursor.execute(db_query)
                with open('./sql/res_db/reviews.sql', 'r') as file2:
                    rev_query = file2.read()
                    db_query = rev_query.replace("<RES_NAME>", res)
                    cursor.execute(f"USE {rests[0]}")
                    cursor.execute(db_query)
    except KeyboardInterrupt:
        print("Monitoring stopped.")
    # deal with more general errors
    # race condition

# roll back
def roll_back(conn, error):
    print(f"Error: {error}")
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
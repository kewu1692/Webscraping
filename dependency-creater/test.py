import mysql.connector
from mysql.connector import Error

# create connection
try:
    # create connection
    conn = mysql.connector.connect(
        host = "54.145.65.145",
        user = "root",
        password = "your_secure_password",
        database = "global_schema"
    )
    # create cursor
    cursor = conn.cursor()

    # create variables
    user_id = 3
    res_name = "test"
    status = "new"
    res_url = "https://www.789.com"

    # execute query
    cursor.execute(f"""
        INSERT INTO global_schema.queue1(user_id, res_name, status, res_url)
        VALUES ({user_id}, "{res_name}", "{status}", "{res_url}")
    """)

    # commit changes
    conn.commit()

    # print result
    print(cursor.fetchall())

except Error as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()  # Rollback changes on error
        print("Transaction rolled back.")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
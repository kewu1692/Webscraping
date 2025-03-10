import mysql.connector
from mysql.connector import Error

# create connection
try:
    # create connection
    conn = mysql.connector.connect(
        host = "54.145.65.145",
        user = "root",
        password = "your_secure_password",
        database = "global_database"
    )
    # create cursor
    cursor = conn.cursor()

    # create variables
    res_name1 = "test1"
    status1 = "new"
    res_url1 = "https://www.123.com"
    res_name2 = "test2"
    status2 = "new"
    res_url2 = "https://www.456.com"

    # execute query
    cursor.execute(f"INSERT INTO global_database.res_queue(res_name, status, res_url) VALUES ('{res_name1}', '{status1}', '{res_url1}')")
    cursor.execute(f"INSERT INTO global_database.res_queue(res_name, status, res_url) VALUES ('{res_name2}', '{status2}', '{res_url2}')")

    # commit changes
    conn.commit()

    # # print result
    # cursor.execute("SELECT * FROM global_database.res_queue")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)

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
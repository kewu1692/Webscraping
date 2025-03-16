from mysql.connector import Error
import config
import mysql_toolbox as tool

# create connection
def insert_testing_data():
    try:
        # create connection
        mysql_connection = tool.create_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        cursor = mysql_connection.cursor()

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
        mysql_connection.commit()
        print("Testing data inserted.")

    except Error as e:
        print(f"Error: {e}")
        if mysql_connection:
            mysql_connection.rollback()  # Rollback changes on error
            print("Transaction rolled back.")

    finally:
        if cursor:
            cursor.close()
        if mysql_connection:
            mysql_connection.close()
        print("Database connection closed.")
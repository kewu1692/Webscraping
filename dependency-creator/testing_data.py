from mysql.connector import Error
import config
import mysql_toolbox as tool

# create connection
def insert_testing_data(number_of_testing_data):
    try:
        # create connection
        mysql_connection = tool.create_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        if mysql_connection:
            cursor = mysql_connection.cursor()
        else:
            raise Error("No connection to MySQL")

        # create variables

        for i in range(number_of_testing_data):
            res_name = f"test{i}"
            status = "new"
            res_url = f"https://www.test{i}.com"

            # execute query
            cursor.execute(f"INSERT INTO global_database.res_queue(res_name, status, res_url) VALUES ('{res_name}', '{status}', '{res_url}')")
    
        # commit changes
        mysql_connection.commit()
        print("Testing data inserted.")

    except Exception as e:
        print(f"Error: {e}")
        if mysql_connection:
            mysql_connection.rollback()  # Rollback changes on error
            print("Transaction rolled back.")
        raise e

    finally:
        if cursor:
            cursor.close()
        if mysql_connection:
            mysql_connection.close()
        print("Database connection closed.")
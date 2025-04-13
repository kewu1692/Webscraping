from mysql.connector import Error
import config
import mysql_toolbox as tool



# create connection
def drop_all_test_databases():

    cursor, mysql_connection = None, None
    try:
        # create connection
        mysql_connection = tool.create_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        cursor = mysql_connection.cursor()

        # clear up before testing
        cursor.execute("SHOW DATABASES;")
        databases = cursor.fetchall()
        num_databases = len(databases)

        for i in range(num_databases):
            cursor.execute(f"DROP DATABASE IF EXISTS test{i};") 
        
        cursor.execute("DROP DATABASE IF EXISTS global_database;")
            
        # commit changes
        mysql_connection.commit()
        
        print("Database Cleared.")

    except Error as e:
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


from mysql.connector import Error
import config
import functions as fun
import os


try:
    # create connection
    conn = fun.create_conn(config.host, config.user, config.password)

    # create cursor
    cursor = fun.create_cur(conn)

    # initialization
    directory = "/Users/jessie/Desktop/project/Webscraping/dependency-creater/sql/initialization"
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):  # Check if it's a file (not a subdirectory)
            with open(file_path, 'r') as file:
                query = file.read()
                cursor.execute(query)

    # commit changes
    conn.commit()

except Error:
    fun.roll_back()

finally:
    fun.close(cursor, conn)
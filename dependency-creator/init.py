from mysql.connector import Error
import config
import functions as fun
import os


try:
    # create connection
    conn = fun.create_conn(config.host, config.user, config.password)

    # create cursor
    cursor = fun.create_cur(conn)

    # initialize global db
    with open("./sql/initialization/global_db.sql", 'r') as file:
        query = file.read()
        cursor.execute(query)

    # initialize tables -> function
    directory = "./sql/initialization"
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                query = file.read()
                cursor.execute(query)

    # commit changes
    conn.commit()

except Error as error:
    fun.roll_back(conn, error)

finally:
    fun.close(cursor, conn)
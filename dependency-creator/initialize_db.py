from mysql.connector import Error
import config
import mysql_toolbox as tool


try:
    # create connection
    mysql_connection = tool.create_connection(config.HOST, config.USER, config.PASSWORD)

    # create cursor
    cursor = mysql_connection.cursor()

    # initialize global db
    db_replace_map = {"DB_NAME": config.GLOBAL}
    tool.execute_query_from_path(cursor,config.CREATE_DB_PATH,db_replace_map)

    # initialize tables
    tool.execute_queries_in_directory(cursor,config.INIT_TABLES_DIR,db_replace_map)

    # commit changes
    mysql_connection.commit()
    print("Initialization complete.")

except Error as error:
    tool.roll_back(mysql_connection, error)

finally:
    tool.close(cursor, mysql_connection)

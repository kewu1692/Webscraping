from mysql.connector import Error
import config
import mysql_toolbox as tool


try:
    # create connection
    mysql_connection = tool.create_conn(config.host, config.user, config.password)

    # create cursor
    cursor = tool.create_cur(mysql_connection)

    # initialize global db
    db_replace_map = {"DB_NAME": "global_database"}
    tool.execute_query_from_path(cursor,config.create_db_path,db_replace_map)

    # initialize tables
    tool.execute_queries_in_dir(cursor,config.init_tables_dir,db_replace_map)

    # commit changes
    mysql_connection.commit()

except Error as error:
    tool.roll_back(mysql_connection, error)

finally:
    tool.close(cursor, mysql_connection)

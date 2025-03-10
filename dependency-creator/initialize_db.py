from mysql.connector import Error
import config
import mysql_toolbox as tool


try:
    # create connection
    conn = tool.create_conn(config.host, config.user, config.password)

    # create cursor
    cursor = tool.create_cur(conn)

    # initialize global db
    db_replace = {"DB_NAME": "global_database"}
    tool.execute_query_from_path(cursor,config.create_db_path,db_replace)

    # initialize tables
    tool.execute_queries_in_dir(cursor,config.init_tables_dir,db_replace)

    # commit changes
    conn.commit()

except Error as error:
    tool.roll_back(conn, error)

finally:
    tool.close(cursor, conn)

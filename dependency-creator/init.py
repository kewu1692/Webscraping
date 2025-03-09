from mysql.connector import Error
import config
import functions as fun


try:
    # create connection
    conn = fun.create_conn(config.host, config.user, config.password)

    # create cursor
    cursor = fun.create_cur(conn)

    # initialize global db
    db_replace = {"DB_NAME": "global_database"}
    fun.execute_query_from_path(cursor,config.create_db_path,db_replace)

    # initialize tables
    fun.execute_queries_in_dir(cursor,config.init_tables_dir,db_replace)

    # commit changes
    conn.commit()

except Error as error:
    fun.roll_back(conn, error)

finally:
    fun.close(cursor, conn)

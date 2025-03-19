from mysql.connector import Error
import config
import mysql_toolbox as tool

def initialize_database():
    try:
        # create connection
        mysql_connection = tool.create_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        cursor = mysql_connection.cursor()

        # initialize global db
        # TODO: replace GLOBAL with a more descriptive name like "GLOBAL_DATABASE_NAME"
        # TODO: replace DB_NAME with a more descriptive name like "GLOBAL_DATABASE_NAME"
        # TODO: replace create_db.sql to a more descriptive name like "create_global_db.sql"
        db_replace_map = {"DB_NAME": config.GLOBAL}
        # TODO: think about future scaling of the project, is this the only database we will need?
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

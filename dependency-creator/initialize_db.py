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
        db_replace_map = {"GLOBAL_DB_NAME": config.GLOBAL_DB_NAME}
        # TODO: think about future scaling of the project, is this the only database we will need?
        tool.execute_queries_in_directory(cursor,config.INIT_DB_DIR,db_replace_map)

        # initialize tables
        tool.execute_queries_in_directory(cursor,config.INIT_TABLES_DIR,db_replace_map)

        # commit changes
        mysql_connection.commit()
        print("Initialization complete.")

    except Exception as e:
        tool.roll_back(mysql_connection, e)
        raise e

    finally:
        tool.close(cursor, mysql_connection)

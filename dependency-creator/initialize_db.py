from mysql.connector import Error
import config
import mysql_toolbox as tool

async def initialize_database():
    async_mysql_connection = cursor = None
    try:
        # create connection
        async_mysql_connection = await tool.create_async_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        cursor = await async_mysql_connection.cursor()

        # initialize global db
        db_replace_map = {"GLOBAL_DB_NAME": config.GLOBAL_DB_NAME}
        # TODO: think about future scaling of the project, is this the only database we will need?
        await tool.execute_queries_in_directory(cursor,config.INIT_DB_DIR,db_replace_map)

        # initialize tables
        await tool.execute_queries_in_directory(cursor,config.INIT_TABLES_DIR,db_replace_map)

        # commit changes
        await async_mysql_connection.commit()
        print("Initialization complete.")

    except Exception as e:
        if async_mysql_connection:
            await tool.roll_back(async_mysql_connection, e)
        raise e

    finally:        
        if cursor and async_mysql_connection:
            await tool.close(cursor, async_mysql_connection)
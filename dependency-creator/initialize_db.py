from mysql.connector import Error
import config
import mysql_toolbox as tool


async def initialize_database(pool):
    conn = cursor = None
    try:
        # create connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                # initialize global db
                db_replace_map = {"GLOBAL_DB_NAME": config.GLOBAL_DB_NAME}
                # TODO: think about future scaling of the project, is this the only database we will need?
                await tool.execute_queries_in_directory(cursor,config.INIT_DB_DIR,db_replace_map)

                # initialize tables
                await tool.execute_queries_in_directory(cursor,config.INIT_TABLES_DIR,db_replace_map)
        # commit changes
        await conn.commit()
        print("Initialization complete.")

    except Exception as e:
        if conn:
            await tool.roll_back(conn, e)
        raise e

    finally:        
        if cursor and conn:
            await tool.release(pool, conn)


from mysql.connector import Error
import config
import mysql_toolbox as tool


async def initialize_database(pool):
    try:
        # create connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # initialize global db
                db_replace_map = {"GLOBAL_DB_NAME": config.GLOBAL_DB_NAME}
                await tool.execute_queries_in_directory(cursor, config.INIT_DB_DIR, db_replace_map)

                # initialize tables
                await tool.execute_queries_in_directory(cursor, config.INIT_TABLES_DIR, db_replace_map)
                
                # commit changes - MOVED INSIDE the async with block
                await conn.commit()
                
        print("Initialization complete.")

    except Exception as e:
        print(f"Database initialization error: {e}")
        # Connection is automatically returned to pool even on exception
        raise e

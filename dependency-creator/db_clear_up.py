from mysql.connector import Error
import config
import mysql_toolbox as tool
import asyncio


# create connection
async def drop_all_test_databases():

    cursor, async_mysql_connection = None, None
    try:
        # create connection
        async_mysql_connection = await tool.create_async_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        cursor = await async_mysql_connection.cursor()

        # clear up before testing
        await cursor.execute("SHOW DATABASES;")
        databases = await cursor.fetchall()
        filtered_databases = [db[0] for db in databases if db[0] not in ('information_schema', 'mysql', 'performance_schema')]
        print(f"Databases: {filtered_databases}")
        num_databases = len(filtered_databases)


        if num_databases == 0:
            print("No databases found.")
            return False
        else:
            for i in range(num_databases):
                await cursor.execute(f"DROP DATABASE IF EXISTS test{i};") 
        
        await cursor.execute("DROP DATABASE IF EXISTS global_database;")
            
        # commit changes
        await async_mysql_connection.commit()
        
        print("Database Cleared.")

    except Error as e:
        print(f"Error: {e}")
        if async_mysql_connection:
            await async_mysql_connection.rollback()  # Rollback changes on error
            print("Transaction rolled back.")
        raise e

    finally:
        if cursor and async_mysql_connection:
            await tool.close(cursor, async_mysql_connection)

asyncio.run(drop_all_test_databases())
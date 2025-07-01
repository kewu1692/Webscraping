from mysql.connector import Error
import mysql_toolbox as tool
import asyncio


# create connection
async def drop_all_test_databases(pool):

    try:
        # create connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # clear up before testing
                await cursor.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'mysql', 'performance_schema', 'sys');")
                databases = await cursor.fetchall()
                # filtered_databases = [db[0] for db in databases if db[0] not in ('information_schema', 'mysql', 'performance_schema')]
                print(f"Databases: {databases}")
                num_databases = len(databases)
                if num_databases == 0:
                    print("No databases found.")
                    return                                                                     
                else:
                    for i in range(num_databases-1):
                        await cursor.execute(f"DROP DATABASE IF EXISTS test{i};") 
                await cursor.execute("DROP DATABASE IF EXISTS global_database;")
        # commit changes
                await conn.commit()
                print("Committed changes...")
        
        print("Database Cleared.")

    except Error as e:
        print(f"Error: {e}")
        # if conn:
            # await conn.rollback()  # Rollback changes on error
            # print("Transaction rolled back.")
        # Note: conn is not accessible here since it's scoped to the async with block
        # The connection will be automatically returned to pool even on exception
        raise e
    # we don't need the finally block here since the async with block handles closing the connection
    # and cursor automatically
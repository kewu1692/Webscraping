from mysql.connector import Error
import config
import mysql_toolbox as tool

# create connection
async def insert_testing_data(number_of_testing_data):
    cursor, async_mysql_connection = None, None
    try:
        # create connection
        async_mysql_connection = await tool.create_async_connection(config.HOST, config.USER, config.PASSWORD)

        # create cursor
        cursor = await async_mysql_connection.cursor()
        
        # create variables

        for i in range(number_of_testing_data):
            res_name = f"test{i}"
            status = "new"
            res_url = f"https://www.test{i}.com"

            # execute query
            await cursor.execute(f"INSERT INTO global_database.res_queue(res_name, status, res_url) VALUES ('{res_name}', '{status}', '{res_url}')")
    
        # commit changes
        await async_mysql_connection.commit()
        print("Testing data inserted.")

    except Exception as e:
        print(f"Error: {e}")
        if async_mysql_connection:
            await async_mysql_connection.rollback()  # Rollback changes on error
            print("Transaction rolled back.")
        raise e

    finally:
        if cursor and async_mysql_connection:
            await tool.close(cursor, async_mysql_connection)
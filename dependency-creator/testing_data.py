from mysql.connector import Error
import config
import mysql_toolbox as tool

# create connection
async def insert_testing_data(pool,number_of_testing_data):
    cursor, conn = None, None
    try:
        # create connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
        
                # create variables
                for i in range(number_of_testing_data):
                    res_name = f"test{i}"
                    status = "new"
                    res_url = f"https://www.test{i}.com"

                    # execute query
                    await cursor.execute(f"INSERT INTO {config.GLOBAL_DB_NAME}.res_queue(res_name, status, res_url) VALUES ('{res_name}', '{status}', '{res_url}')")
        # commit changes
        await conn.commit()
        print("Testing data inserted.")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            await conn.rollback()  # Rollback changes on error
            print("Transaction rolled back.")
        raise e

    finally:
        if cursor and conn:
            await tool.release(pool, conn)
from mysql.connector import Error
import config
import mysql_toolbox as tool

# create connection
async def insert_testing_data(pool, number_of_testing_data):
    try:
        # create connection and cursor
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # create variables and execute queries
                for i in range(number_of_testing_data):
                    res_name = f"test{i}"
                    status = "new"
                    res_url = f"https://www.test{i}.com"

                    # Use parameterized query to prevent SQL injection
                    query = f"INSERT INTO {config.GLOBAL_DB_NAME}.res_queue(res_name, status, res_url) VALUES (%s, %s, %s)"
                    await cursor.execute(query, (res_name, status, res_url))
                
                # commit changes - MOVED INSIDE the async with block
                await conn.commit()
                
        print("Testing data inserted.")

    except Exception as e:
        print(f"Error inserting testing data: {e}")
        # Connection is automatically returned to pool even on exception
        raise e
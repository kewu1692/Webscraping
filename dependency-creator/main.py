from mysql_toolbox import create_async_connection_pool
from db_clear_up import drop_all_test_databases
from initialize_db import initialize_database
from testing_data import insert_testing_data
from user_db_worker import dependency_creation_worker
import config

# use logging library to log, info, error, debug
import asyncio

async def main():
    pool = None
    try:    
        pool = await create_async_connection_pool(config.HOST, config.USER, config.PASSWORD)

        await drop_all_test_databases(pool)
        print("#"*50)
        
        await initialize_database(pool)
        print("#"*50)

        await insert_testing_data(pool,number_of_testing_data=1)
        print("#"*50)
        
        num_workers = 3
        tasks = []
        for i in range(num_workers):
            task = asyncio.create_task(dependency_creation_worker(pool,i))  # Pass worker id to distinguish workers
            tasks.append(task)
            
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error in main: {e}")

    finally:
        pool.close()
        await pool.wait_closed()

asyncio.run(main())
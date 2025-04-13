from db_clear_up import drop_all_test_databases
from initialize_db import initialize_database
from testing_data import insert_testing_data
from user_db_worker import user_database_worker

# use logging library to log, info, error, debug
import asyncio

async def main():
    try:
        drop_all_test_databases()
        print("#"*50)
        initialize_database()
        print("#"*50)
        insert_testing_data(number_of_testing_data=10)
        print("#"*50)
        num_workers = 2
        tasks = []
        for i in range(num_workers):
            task = asyncio.create_task(user_database_worker(i))  # Pass worker id to distinguish workers
            tasks.append(task)
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error in main: {e}")

asyncio.run(main())
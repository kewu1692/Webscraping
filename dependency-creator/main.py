from db_clear_up import drop_all_databases
from initialize_db import initialize_database
from testing_data import insert_testing_data
from user_db_worker import user_database_worker
import asyncio

async def main():
    try:
        drop_all_databases()
        initialize_database()
        insert_testing_data()
        num_workers = 5
        tasks = []
        for i in range(num_workers):
            task = asyncio.create_task(user_database_worker(i))  # Pass worker id to distinguish workers
            tasks.append(task)
        await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error in main: {e}")

asyncio.run(main())
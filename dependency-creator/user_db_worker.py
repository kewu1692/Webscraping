import mysql_toolbox as tool
import config
from mysql.connector import Error
import asyncio

# find new job
def find_new_res_job(cursor):
    try:
        print("Finding new job...")
        cursor.execute(f"""SELECT res_id, res_name FROM {config.GLOBAL_DB_NAME}.res_queue WHERE status = 'new' ORDER BY created_at LIMIT 1 FOR UPDATE""")
        rest = cursor.fetchall()
        if not rest:
            print("No new job found.")
            return None
        print(f"New job found: {rest}")
        cursor.execute(f"""UPDATE {config.GLOBAL_DB_NAME}.res_queue SET status = "in progress" WHERE res_id = {rest[0][0]}""")
        return rest
    except Error as e:
        print("Error Finding New Res:", e)
    
# create db and review table for new res users
def set_up_new_res_artifacts(cursor):
    try:
        rest = find_new_res_job(cursor)
        if not rest:
            print("No new job found.")
            return None
        print(f"Setting up the artifacts for {rest[0][1]}")
        for id, res in rest:
            res_db_replace_map = {"GLOBAL_DB_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.CREATE_DB_PATH,res_db_replace_map)
            print(f"Database created for {res}")
            res_name_replace_map = {"RES_DB_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.REVIEWS_PATH,res_name_replace_map)
            print(f"Review table created for {res}")
            cursor.execute(f"""UPDATE {config.GLOBAL_DB_NAME}.res_queue SET status = "done" WHERE res_id = {id}""")

    except Error as e:
        print("Error Setting Up New Res:", e)
        cursor.execute(f"""UPDATE {config.GLOBAL_DB_NAME}.res_queue SET status = "error" WHERE res_id = {id}""")

    #### race condition


async def user_database_worker(worker_id):
    try:
        mysql_connection, cursor = None, None
        while True:
            print(f"Worker {worker_id} polling...")
            # create connection
            mysql_connection = tool.create_connection(config.HOST, config.USER, config.PASSWORD)
            # create cursor
            cursor = mysql_connection.cursor()
            # working
            set_up_new_res_artifacts(cursor)
            mysql_connection.commit()

            # START TRANSACTION
            # TODO: create function called that finds 1 new job, this should lock the row it found
            # TODO: create function that updates the job status to processing
            # END TRANSACTION

            # TODO: create function that processes the job, create the artifacts
            # START TRANSACTION
            # TODO: create function that updates the job status to done/error, test the error case
            # END TRANSACTION

            print(f"Worker {worker_id} done, going back to sleep...")
            await asyncio.sleep(5)

    except Error as e:
        print(f"Error in worker {worker_id}: {e}")
        tool.roll_back(mysql_connection, e)

    finally:
        tool.close(cursor, mysql_connection)
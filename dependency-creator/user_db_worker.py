import mysql_toolbox as tool
import config
from mysql.connector import Error
import time
import asyncio

# find new res users
def find_new_res_users(cursor,replace_map):
    try:
        print("Finding new restaurants...")
        tool.execute_query_from_path(cursor, config.NEW_RES_PATH, replace_map)
        rests_list = cursor.fetchall()
        print(f"New restaurants found: {rests_list}")
        return rests_list
    except Error as e:
        print("Error Finding New Res:", e)
    
# create db and review table for new res users
def set_up_new_res(cursor,replace_map):
    try:
        rests = find_new_res_users(cursor,replace_map)
        for id, res in rests:
            res_db_replace_map = {"DB_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.CREATE_DB_PATH,res_db_replace_map)
            print(f"Database created for {res}")
            res_name_replace_map = {"RES_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.REVIEWS_PATH,res_name_replace_map)
            print(f"Review table created for {res}")
            id_replace_map = {"RES_ID": id }  
            update_replace_map = replace_map | id_replace_map
            tool.execute_query_from_path(cursor,config.UPDATE_STATUS_PATH,update_replace_map)
            print(f"Status changed for {id}")

    except Error as e:
        print("Error Setting Up New Res:", e)
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
            db_replace_map = {"DB_NAME": config.GLOBAL}
            set_up_new_res(cursor,db_replace_map)
            mysql_connection.commit()
            print(f"Worker {worker_id} done, going back to sleep...")
            await asyncio.sleep(5)

    except Error as e:
        print(f"Error in worker {worker_id}: {e}")
        tool.roll_back(mysql_connection, e)

    finally:
        tool.close(cursor, mysql_connection)
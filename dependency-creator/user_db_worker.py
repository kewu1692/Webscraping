import mysql_toolbox as tool
import config
from mysql.connector import Error
import time

# find new res users
def find_new_res_users(cursor,db_replace):
    tool.execute_query_from_path(cursor, config.new_res_path, db_replace)
    rests = cursor.fetchall()
    return rests
    
# create db and review table for new res users
def set_up_new_res(cursor,db_replace):
    try:
        rests = find_new_res_users(cursor,db_replace)
        print(f"New restaurants found: {rests}")
        for id, res in rests:
            res_db_replace = {"DB_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.create_db_path,res_db_replace)
            print(f"Database created for {res}")
            res_name_replace = {"RES_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.reviews_path,res_name_replace)
            print(f"Review table created for {res}")
            id_replace = {"RES_ID": id }  
            update_replace = db_replace | id_replace
            tool.execute_query_from_path(cursor,config.update_status_path,update_replace)
            print(f"Status changed for {id}")

    except Error as e:
        print("Error Setting Up New Res:", e)
    #### race condition

try:
    conn, cursor = None, None
    while True:

        print("Worker polling...")
        # create connection
        conn = tool.create_conn(config.host, config.user, config.password)

        # create cursor
        cursor = tool.create_cur(conn)

        # working
        db_replace = {"DB_NAME": "global_database"}
        tool.set_up_new_res(cursor,db_replace)

        conn.commit()

        print("Worker done, going back to sleep...")

        time.sleep(5)

except Error as e:
    tool.roll_back(conn, e)

finally:
    tool.close(cursor, conn)
import mysql_toolbox as tool
import config
from mysql.connector import Error
import time

# find new res users
def find_new_res_users(cursor,replace_map):
    print("Finding new restaurants...")
    tool.execute_query_from_path(cursor, config.new_res_path, replace_map)
    rests_list = cursor.fetchall()
    print(f"New restaurants found: {rests_list}")
    return rests_list
    
# create db and review table for new res users
def set_up_new_res(cursor,replace_map):
    try:
        rests = find_new_res_users(cursor,replace_map)
        for id, res in rests:
            res_db_replace_map = {"DB_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.create_db_path,res_db_replace_map)
            print(f"Database created for {res}")
            res_name_replace_map = {"RES_NAME": f"{res}"}
            tool.execute_query_from_path(cursor,config.reviews_path,res_name_replace_map)
            print(f"Review table created for {res}")
            id_replace_map = {"RES_ID": id }  
            update_replace_map = replace_map | id_replace_map
            tool.execute_query_from_path(cursor,config.update_status_path,update_replace_map)
            print(f"Status changed for {id}")

    except Error as e:
        print("Error Setting Up New Res:", e)
    #### race condition

try:
    conn, cursor = None, None
    while True:

        print("Worker polling...")
        # create connection
        mysql_connection = tool.create_connection(config.host, config.user, config.password)

        # create cursor
        cursor = mysql_connection.cursor()

        # working
        db_replace_map = {"DB_NAME": config.Global}
        set_up_new_res(cursor,db_replace_map)

        mysql_connection.commit()

        print("Worker done, going back to sleep...")

        time.sleep(5)

except Error as e:
    tool.roll_back(mysql_connection, e)

finally:
    tool.close(cursor, mysql_connection)
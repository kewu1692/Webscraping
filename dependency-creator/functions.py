import mysql.connector
import config
import os
from mysql.connector import Error

# create connection
def create_conn(host, user, password):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )
    return conn

# create cursor
def create_cur(conn):
    return conn.cursor()


# read_query_from_path reads sql query from a given path
def read_query_from_path(path):
    try:
        
        with open(path, 'r') as file:
            return file.read()
            
    except Error as e:
        print("Error reading sql:", e)

# execute_query_with_replace takes and executes query with assumed valid replacement dict
def execute_query_with_replace(cursor, query, replace_dict):
    try:

        for parameter, value in replace_dict.items():
            query = query.replace(f"< {parameter} >", f"{value}")
        cursor.execute(query)

    except Error as e:
        print("Error executing sql:", e)

# validate_replace_by_query takes query and dict and validates if the dict is good
def validate_replace_by_query(query, replace_dict):
    if not isinstance(query, str):
        raise TypeError(f"Expected string, got {type(query).__name__}")
    if not isinstance(replace_dict, dict):
        raise TypeError(f"Expected dict, got {type(replace_dict).__name__}")

    placeholder_count = query.count("<")
    if placeholder_count != len(replace_dict):
        print("Invalid Replace")
    else:
        print("Valid Replace") 
    ### valid value inside <>

# execute_queries_in_dir takes path of dir,loop through files and get file path, read each query, check replacement, execute query
def execute_queries_in_dir(cursor, directory, replace_dict):

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            query = read_query_from_path(file_path)
            validate_replace_by_query(query, replace_dict)
            execute_query_with_replace(cursor, query, replace_dict)
        else:
            print("Directory contains non-file objects")
            

# execute_query_from_path takes path of a file, read query, check replacement, execute query
def execute_query_from_path(cursor, path, replace_dict):
    query = read_query_from_path(path)
    validate_replace_by_query(query, replace_dict)
    execute_query_with_replace(cursor, query, replace_dict)


# find new res users
def find_new_res_users(cursor,db_replace):
    execute_query_from_path(cursor, config.new_res_path, db_replace)
    rests = cursor.fetchall()
    return rests
    
# create db and review table for new res users
def set_up_new_res(cursor,db_replace):
    try:
        rests = find_new_res_users(cursor,db_replace)
        print(f"New restaurants found: {rests}")
        for id, res in rests:
            res_db_replace = {"DB_NAME": f"{res}"}
            execute_query_from_path(cursor,config.create_db_path,res_db_replace)
            print(f"Database created for {res}")
            res_name_replace = {"RES_NAME": f"{res}"}
            execute_query_from_path(cursor,config.reviews_path,res_name_replace)
            print(f"Review table created for {res}")
            id_replace = {"RES_ID": id }  
            update_replace = db_replace | id_replace
            execute_query_from_path(cursor,config.update_status_path,update_replace)
            print(f"Status changed for {id}")

    except Error as e:
        print("Error Setting Up New Res:", e)
    #### race condition

# roll back
def roll_back(conn, error):
    print(f"Error: {error}")
    if conn:
        conn.rollback()  # Rollback changes on error
        print("Transaction rolled back.")
    
# closing connection
def close(cursor, conn):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
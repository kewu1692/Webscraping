import mysql.connector
import os
from mysql.connector import Error

# create connection
def create_conn(host, user, password):
    mysql_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )
    return mysql_connection

# create cursor
def create_cur(mysql_connection):
    return mysql_connection.cursor()


# read_query_from_path reads sql query from a given path
def read_query_from_path(file_path):
    try:
        
        with open(file_path, 'r') as file:
            return file.read()
            
    except Error as e:
        print("Error reading sql:", e)

# execute_query_with_replace takes and executes query with assumed valid replacement dict
def execute_query_with_replace(cursor, query, replace_map):
    try:

        for k, v in replace_map.items():
            query = query.replace(f"< {k} >", f"{v}")
        cursor.execute(query)

    except Error as e:
        print("Error executing sql:", e)

# validate_replace_by_query takes query and dict and validates if the dict is good
def validate_replace_by_query(query, replace_map):
    if not isinstance(query, str):
        raise TypeError(f"Expected string, got {type(query).__name__}")
    if not isinstance(replace_map, dict):
        raise TypeError(f"Expected dict, got {type(replace_map).__name__}")

    placeholder_count = query.count("<")
    if placeholder_count != len(replace_map):
        print("Invalid Replace")
    else:
        print("Valid Replace") 
    ### valid value inside <>

# execute_queries_in_dir takes path of dir,loop through files and get file path, read each query, check replacement, execute query
def execute_queries_in_dir(cursor, directory, replace_map):

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            query = read_query_from_path(file_path)
            validate_replace_by_query(query, replace_map)
            execute_query_with_replace(cursor, query, replace_map)
        else:
            print("Directory contains non-file objects")
            

# execute_query_from_path takes path of a file, read query, check replacement, execute query
def execute_query_from_path(cursor, file_path, replace_map):
    query = read_query_from_path(file_path)
    validate_replace_by_query(query, replace_map)
    execute_query_with_replace(cursor, query, replace_map)
    

# roll back
def roll_back(mysql_connection, error):
    print(f"Error: {error}")
    if mysql_connection:
        mysql_connection.rollback()  # Rollback changes on error
        print("Transaction rolled back.")
    
# closing connection
def close(cursor, mysql_connection):
    if cursor:
        cursor.close()
    if mysql_connection:
        mysql_connection.close()
    print("Database connection closed.")
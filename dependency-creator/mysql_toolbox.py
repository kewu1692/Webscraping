import mysql.connector
import os
from mysql.connector import Error
import re

# create connection
def create_connection(host, user, password):
    mysql_connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
        )
    print("Connected to MySQL")
    return mysql_connection


# read_query_from_path reads sql query from a given path
def read_query_from_path(file_path):
    try:
        with open(file_path, 'r') as file:
            print(f"Reading from {os.path.basename(file_path)}")
            return file.read()
            
    except Error as e:
        print("Error reading sql:", e)

# execute_query_with_replace takes and executes query with assumed valid replacement dict
def execute_query_with_replace(cursor, query, replace_map):
    try:
        for k, v in replace_map.items():
            query = query.replace(f"< {k} >", f"{v}")
            print(f"Replaced {k} with {v}")
        cursor.execute(query)
        print("Query executed.")

    except Error as e:
        print("Error executing sql:", e)

# validate_replace_by_query takes query and dict and validates if the dict is good
def validate_replace_by_query(query, replace_map):
    # check input type
    print("Validating input type...")
    if not isinstance(query, str):
        raise TypeError(f"Expected string, got {type(query).__name__}")
    if not isinstance(replace_map, dict):
        raise TypeError(f"Expected dict, got {type(replace_map).__name__}")
    print("Valid input type.")
    placeholders = set(re.findall(r'< (.*?) >', query))
    placeholder_count = query.count("<")
    if placeholder_count != len(replace_map):
        print("Invalid replace count.")
        return False
    elif any(key not in placeholders for key in replace_map):
        print("Invalid replace key.")
        return False
    else:
        print("Valid replace.")
        return True

# execute_queries_in_dir takes path of dir,loop through files and get file path, read each query, check replacement, execute query
def execute_queries_in_directory(cursor, directory, replace_map):
    print("Reading from directory...")
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            print(f"Reading from {filename}...")
            query = read_query_from_path(file_path)
            validation_result = validate_replace_by_query(query, replace_map)
            if validation_result:
                execute_query_with_replace(cursor, query, replace_map)
        else:
            print("Directory contains non-file objects. Fail to execute due to invalid directory.")
    print("All queries executed.")
            

# execute_query_from_path takes path of a file, read query, check replacement, execute query
def execute_query_from_path(cursor, file_path, replace_map):
    query = read_query_from_path(file_path)
    validation_result = validate_replace_by_query(query, replace_map)
    if validation_result:
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
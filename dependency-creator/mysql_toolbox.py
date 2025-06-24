# import mysql.connector
import aiomysql
import os
import re

# create MySQL connection
# def create_connection(host, user, password):
#     try:
#         mysql_connection = mysql.connector.connect(
#             host=host,
#             user=user,
#             password=password
#             )
#         print("Connected to MySQL")
#         return mysql_connection
#     except Exception as e:
#         if e.errno == 1045:  # MySQL access denied error
#             print("Login Error: Incorrect username or password.")
#         elif e.errno == 2003:  # Can't connect to MySQL server
#             print("Login Error: Unable to connect to MySQL server. Check host and port.")
#         else:
#             print("Error connecting to MySQL:", e)
#         raise e
        
# create async MySQL connection
async def create_async_connection_pool(host, user, password):
    try:
        # async_mysql_connection = await aiomysql.connect(
        #     host=host,
        #     user=user,
        #     password=password
        # )
        pool = await aiomysql.create_pool(
            host=host,
            user=user,
            password=password
        )
        print("Connected to MySQL")
        return pool
    except Exception as e:
        err_no = getattr(e, 'errno', None)
        if err_no == 1045:  # MySQL access denied error
            print("Login Error: Incorrect username or password.")
        elif err_no == 2003:  # Can't connect to MySQL server
            print("Login Error: Unable to connect to MySQL server. Check host and port.")
        else:
            print("Error connecting to MySQL:", e)
        raise e


# read_query_from_path reads sql query from a given path
# open() and file reading are synchronous operations (regular disk I/O, not network)
# no need await here unless want to go fully async for file I/O too
def read_query_from_path(file_path):
    try:
        with open(file_path, 'r') as file:
            print(f"Reading from {os.path.basename(file_path)}")
            return file.read()
            
    except Exception as e:
        print("Error reading sql:", e)
        raise e

# execute_query_with_replace takes and executes query with assumed valid replacement dict
async def execute_query_with_replace(cursor, query, replace_map):
    try:
        for k, v in replace_map.items():
            query = query.replace(f"< {k} >", f"{v}")
            print(f"Replaced {k} with {v}")
        await cursor.execute(query)
        print("Query executed.")

    except Exception as e:
        print("Error executing sql:", e)
        raise e

# validate_replace_by_query takes query and dict and validates if the dict is good
# no database calls, no network I/O, no file I/O.
def validate_replace_by_query(query, replace_map):
    try:
        if not isinstance(query, str):
            raise TypeError(f"Expected string, got {type(query).__name__}")
        if not isinstance(replace_map, dict):
            raise TypeError(f"Expected dict, got {type(replace_map).__name__}")
        
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
    except Exception as e:
        print(f"Validation Error: {e}")
        raise e
    
# execute_queries_in_dir takes path of dir,loop through files and get file path, read each query, check replacement, execute query
async def execute_queries_in_directory(cursor, directory, replace_map):
    try:
        print("Reading from directory...")
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                query = read_query_from_path(file_path)
                validation_result = validate_replace_by_query(query, replace_map)
                if validation_result:
                    await execute_query_with_replace(cursor, query, replace_map)
                else:
                    raise ValueError("Invalid query.")
            else:
                print("Directory contains non-file objects. Fail to execute due to invalid directory.")
        print("All queries executed.")
    except Exception as e:
        print("Error executing sql:", e)
        raise e
            

# execute_query_from_path takes path of a file, read query, check replacement, execute query
async def execute_query_from_path(cursor, file_path, replace_map):
    try:
        query = read_query_from_path(file_path)
        validation_result = validate_replace_by_query(query, replace_map)
        if validation_result:
            await execute_query_with_replace(cursor, query, replace_map)
        else:
            raise ValueError("Invalid query.")
    except Exception as e:
        print("Error executing sql:", e)
        raise e

# roll back
async def roll_back(conn, error):
    try:
        print(f"Error: {error}")
        if conn:
            await conn.rollback()  # Rollback changes on error
            print("Transaction rolled back.")
    except Exception as e:
        print("Error rolling back:", e)
        raise e
    
# release connection
async def release(pool, conn):
    try:
        if conn:
            await pool.release(conn)
            print("Connection released.")
    except Exception as e:
        print("Error releasing connection:", e)
        raise e

# closing connection
async def close(cursor, conn):
    try:
        if cursor:
            await cursor.close()
        if conn:
            conn.close()
        print("Database connection closed.")
    except Exception as e:
        print("Error closing connection:", e)
        raise e
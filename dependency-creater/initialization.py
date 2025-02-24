import mysql.connector
from mysql.connector import Error


try:
    # create connection
    conn = mysql.connector.connect(
        host = "54.145.65.145",
        user = "root",
        password = "your_secure_password",
    )

    # create cursor
    cursor = conn.cursor()

    # create global dbs
    cursor.execute("USE global_database")
    queries = [
        "CREATE TABLE IF NOT EXISTS global_database.res_queue (res_id INT PRIMARY KEY AUTO_INCREMENT, res_name VARCHAR(50) NOT NULL, status VARCHAR(50) NOT NULL, res_url VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS global_database.file_queue (file_id INT PRIMARY KEY AUTO_INCREMENT, status VARCHAR(50) NOT NULL, res_name VARCHAR(50) NOT NULL, folder_name VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS global_database.users (user_id INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(50), level INTEGER, points INTEGER, review_count INTEGER, photo_count INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    ]
    for query in queries:
        cursor.execute(query)

    # retrieve res_user and dbs 
    cursor.execute("SELECT res_name FROM global_database.res_queue")
    rests = cursor.fetchall()
    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()

    # create individual db and review table for new user
    for res in rests:
        if res not in databases:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {res[0]}") # each result is a tuple, res[0] to access name
            cursor.execute(f"USE {res[0]}")
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {res[0]}.reviews (review_id INT PRIMARY KEY AUTO_INCREMENT, user_id INT, rev_date DATE, rev_desc VARCHAR(225) NOT NULL, star_rating DECIMAL(5, 2) NOT NULL, service_type VARCHAR(50), meal_type VARCHAR(50), food_rating DECIMAL(5, 2), service_rating DECIMAL(5, 2), atmo_rating DECIMAL(5, 2), RECOMM_DISH VARCHAR(225), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES global_database.users(user_id))")

    # confirm dbs
    cursor.execute("SHOW DATABASES")
    databases2 = cursor.fetchall()
    print(databases2)

    # commit changes
    # conn.commit()


except Error as e:
    print(f"Error: {e}")
    if conn:
        conn.rollback()  # Rollback changes on error
        print("Transaction rolled back.")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Database connection closed.")
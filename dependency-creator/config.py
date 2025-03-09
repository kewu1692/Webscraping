import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("user")
host = os.getenv("host")
password = os.getenv("password")

sql_path = "/Users/jessie/Desktop/project/Webscraping/dependency-creator/sql"

init_dir = os.path.join(sql_path, "initialization/global")

init_db_dir = os.path.join(init_dir, "db")

create_db_path = os.path.join(init_db_dir, "create_db.sql")

init_tables_dir = os.path.join(init_dir, "tables")

ops_dir = os.path.join(sql_path, "operations")

new_res_path = os.path.join(ops_dir, "new_res.sql")

update_status_path = os.path.join(ops_dir, "update_status_res.sql")

res_dir = os.path.join(sql_path, "res")

reviews_path = os.path.join(res_dir, "reviews.sql")
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
user = os.getenv("USER")
host = os.getenv("HOST")
password = os.getenv("PASSWORD")

# Path to the sql directory
sql_path = "/Users/jessie/Desktop/project/Webscraping/dependency-creator/sql"

# Path to the initialization directory
init_dir = os.path.join(sql_path, "initialization/global")

# Path to the initialization database directory
init_db_dir = os.path.join(init_dir, "db")

# Path to the create_db.sql file
create_db_path = os.path.join(init_db_dir, "create_db.sql")

# Path to the initialization tables directory
init_tables_dir = os.path.join(init_dir, "tables")

# Path to the operations directory
ops_dir = os.path.join(sql_path, "operations")

# Path to the new_res.sql file
new_res_path = os.path.join(ops_dir, "new_res.sql")

# Path to the update_status.sql file
update_status_path = os.path.join(ops_dir, "update_status_res.sql")

# Path to restaurant directory
res_dir = os.path.join(sql_path, "res")

# Path to reviews.sql file
reviews_path = os.path.join(res_dir, "reviews.sql")

# Global database name
Global = "global_database"
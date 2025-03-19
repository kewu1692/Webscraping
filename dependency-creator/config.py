import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
USER = os.getenv("user")
HOST = os.getenv("host")
PASSWORD = os.getenv("password")

# Path to the sql directory
SQL_PATH = "/Users/jessie/Desktop/project/Webscraping/dependency-creator/sql"

# Path to the initialization directory
INIT_DIR = os.path.join(SQL_PATH, "initialization/global")

# Path to the initialization database directory
INIT_DB_DIR = os.path.join(INIT_DIR, "db")

# Path to the create_db.sql file
CREATE_DB_PATH = os.path.join(INIT_DB_DIR, "create_global_db.sql")

# Path to the initialization tables directory
INIT_TABLES_DIR = os.path.join(INIT_DIR, "tables")

# Path to the operations directory
OPS_DIR = os.path.join(SQL_PATH, "operations")

# Path to the new_res.sql file
NEW_RES_PATH = os.path.join(OPS_DIR, "new_res.sql")

# Path to the update_status.sql file
UPDATE_STATUS_PATH = os.path.join(OPS_DIR, "update_status_res.sql")

# Path to the restaurant directory
RES_DIR = os.path.join(SQL_PATH, "res")

# Path to the res database directory
RES_DB_DIR = os.path.join(RES_DIR, "db")

# Path to the create_res_db.sql file
RES_DB_PATH = os.path.join(RES_DB_DIR, "create_res_db.sql")

# Path to the res tables directory
RES_TABLES_DIR = os.path.join(RES_DIR, "tables")

# Path to reviews.sql file
REVIEWS_PATH = os.path.join(RES_TABLES_DIR, "reviews.sql")

# Global database name
GLOBAL_DB_NAME = "global_database"
from db_clear_up import drop_all_databases
from initialize_db import initialize_database
from testing_data import insert_testing_data
from user_db_worker import user_database_worker

def main():
    drop_all_databases()
    initialize_database()
    insert_testing_data()
    user_database_worker()

if __name__ == "__main__":
    main()
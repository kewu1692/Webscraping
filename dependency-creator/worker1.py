import functions as fun
import config
from mysql.connector import Error
import time

try:
    conn, cursor = None, None
    while True:

        print("Worker polling...")
        # create connection
        conn = fun.create_conn(config.host, config.user, config.password)

        # create cursor
        cursor = fun.create_cur(conn)

        # working
        db_replace = {"DB_NAME": "global_database"}
        fun.set_up_new_res(cursor,db_replace)

        conn.commit()

        print("Worker done, going back to sleep...")

        time.sleep(5)

except Error as e:
    fun.roll_back(conn, e)

finally:
    fun.close(cursor, conn)
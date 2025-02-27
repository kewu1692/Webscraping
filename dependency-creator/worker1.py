import functions as fun
import config


try:
    # create connection
    conn = fun.create_conn(config.host, config.user, config.password)

    # create cursor
    cursor = fun.create_cur(conn)

    # working
    fun.set_up_new_res(cursor)


except KeyboardInterrupt:
    print("Monitoring stopped.")

finally:
    fun.close(cursor, conn)
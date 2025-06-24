import mysql_toolbox as tool
import config
import asyncio

# find new job
async def find_new_res_job(conn,cursor):
    try:
        print("Finding new job...")
        await cursor.execute(f"""SELECT res_id, res_name FROM {config.GLOBAL_DB_NAME}.res_queue WHERE status = 'new' ORDER BY created_at LIMIT 1 FOR UPDATE""")
        rest = await cursor.fetchall()
        if not rest:
            print("No new job found.")
            return
        print(f"New job found: {rest}")

        await cursor.execute(f"""UPDATE {config.GLOBAL_DB_NAME}.res_queue SET status = "in_progress" WHERE res_id = {rest[0][0]}""")
        await conn.commit()
        return rest
    except Exception as e:
        print("Error Finding New Res:", e)
        raise e
    
# create db and review table for new res users
async def set_up_new_res_artifacts(conn, cursor):
    try:
        rest = await find_new_res_job(conn,cursor)
        if not rest:
            return
        await asyncio.sleep(5)
        print(f"Setting up artifacts for {rest[0][1]}")

        for id, res in rest:
            res_db_replace_map = {"RES_DB_NAME": f"{res}"}
            await tool.execute_queries_in_directory(cursor,config.RES_DB_DIR,res_db_replace_map)
            print(f"Database created for {res}")

            res_name_replace_map = {"RES_DB_NAME": f"{res}"}
            await tool.execute_queries_in_directory(cursor,config.RES_TABLES_DIR,res_name_replace_map)
            print(f"Review table created for {res}")
            
            # raise Exception("Simulating an error for testing purposes")  # Simulating an error to test rollback

            await cursor.execute(f"""UPDATE {config.GLOBAL_DB_NAME}.res_queue SET status = "done" WHERE res_id = {id}""")
            await conn.commit()
            print(f"Updated status to done for {res}")

    except Exception as e:
        print(f"Error setting up artifacts...", e)
        if rest:
            for id, res in rest:
                await cursor.execute(f"""UPDATE {config.GLOBAL_DB_NAME}.res_queue SET status = "error" WHERE res_id = {id}""")
                await conn.commit()
                print(f"Updated status to error for {res}")
        raise e
    


async def dependency_creation_worker(pool,worker_id):
    conn, cursor = None, None
    try:
        while True:
            print(f"Worker {worker_id} polling...")
            await asyncio.sleep(5)
            # create connection and cursor
            async with pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    # working
                    await set_up_new_res_artifacts(conn, cursor)
            await conn.commit()

            print(f"Worker {worker_id} done, going back to sleep...")
            print("#"*50)
            await asyncio.sleep(30)

    except Exception as e:
        print(f"Error in worker {worker_id}: {e}")
        if conn:
            await tool.roll_back(conn, e)
        raise e

    finally:
        print(f"Worker {worker_id} closing connection...")
        if cursor and conn:
            await tool.release(pool, conn)
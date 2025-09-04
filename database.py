import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
from log_config import logger

from config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_ENDPOINT,
    DB_NAME
)


class Database:
    def __init__(self, pool_name="mypool", pool_size=5):
        try:
            self.pool = pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_session=True,
                host=DB_ENDPOINT,
                database=DB_NAME,
                user=DB_USERNAME,
                password=DB_PASSWORD
            )
            logger.info(f"✅ Connection pool '{pool_name}' created with size {pool_size}")
        except Error as e:
            logger.error(f"❌ Error creating connection pool: {e}")
            self.pool = None

    def insert_call(self, data):
        if self.pool is None:
            logger.error("❌ No connection pool available.")
            return

        query = f"""INSERT INTO calls (db_call_id, manager_id, manager_login, manager_name, client_number, client_name, duration, answered, direction, start_time, answer_time, end_time, recording, waiting_sec)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        conn = None
        cursor = None
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (
                data["db_call_id"],
                data["manager_id"],
                data["manager_login"],
                data["manager_name"],
                data["client_number"],
                data["client_name"],
                data["duration"],
                data["answered"],
                data["direction"],
                data["start_time"],
                data["answer_time"],
                data["end_time"],
                data["recording"],
                data["waiting_sec"]
            ))
            conn.commit()
        except Error as e:
            logger.error(f"❌ Error inserting data: {e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
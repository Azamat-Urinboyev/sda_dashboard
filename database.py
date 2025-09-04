import mysql.connector
from mysql.connector import Error
from log_config import logger

from config import (
    DB_USERNAME,
    DB_PASSWORD,
    DB_ENDPOINT,
    DB_NAME
)


class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host=DB_ENDPOINT,
                user=DB_USERNAME,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL database")
        except Error as e:
            print(f"❌ Error while connecting to MySQL: {e}")
            self.connection = None

    def insert_data(self, table, data):
        """
        Insert data into a table.
        Args:
            table (str): Table name
            data (dict): Dictionary where keys = column names, values = column values
        Example:
            db.insert_data("employees", {"name": "Alice", "age": 30})
        """
        if self.connection is None:
            print("❌ No database connection")
            return

        placeholders = ", ".join(["%s"] * len(data))
        columns = ", ".join(data.keys())
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print(f"✅ Inserted into {table}: {data}")
        except Error as e:
            print(f"❌ Error inserting data: {e}")

    def close(self):
        """
        Close the database connection
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔒 MySQL connection closed")

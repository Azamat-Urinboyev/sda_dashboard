from dotenv import load_dotenv
import os

load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_ENDPOINT = os.getenv("DB_ENDPOINT")
DB_NAME = os.getenv("DB_NAME")

CLOCKSTER_TOKEN = os.getenv("CLOCKSTER_TOKEN")


CLOCKSTER_SALES_DEPARTMENT_ID = 14921


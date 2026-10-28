import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

# main project folder (one level up from src)
PROJECT_FOLDER = Path(__file__).resolve().parent.parent

load_dotenv(PROJECT_FOLDER / ".env")


def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as e:
        print("Couldn't connect to MySQL. Is Docker running? (docker start sales-db)")
        print(e)
        exit(1)
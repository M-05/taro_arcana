import MySQLdb
import os
from dotenv import load_dotenv
load_dotenv()

SQL = os.getenv("SQL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

# Database connection string
DB_URL = f'{SQL}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

DATABASE_NAME = "subscribe"

# Connect to MySQL server
conn = MySQLdb.connect(
                        host=HOST, user=USERNAME, password=PASSWORD, port=3306
                        # , db=DBNAME
)
engine = conn.cursor()

def create_database():
    # Execute SQL command to create database
    engine.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME};")

def drop_database():
    # Execute SQL command to drop database
    engine.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME};")


def main():
# Check if database exists
    engine.execute("SHOW DATABASES")
    databases = engine.fetchall()
    database_exists = any(DATABASE_NAME in db for db in databases)

    if not database_exists:
        print(f"{DATABASE_NAME} 데이터베이스가 존재하지 않습니다.\n{DATABASE_NAME} 데이터베이스를 생성하겠습니다.")
        create_database()
    else:
        print(f"{DATABASE_NAME} 데이터베이스가 존재합니다.\n{DATABASE_NAME} 데이터베이스를 삭제 후 다시 생성하겠습니다.")
        drop_database()
        create_database()

if __name__ == "__main__":
    # main()

    create_database()

    # drop_database()
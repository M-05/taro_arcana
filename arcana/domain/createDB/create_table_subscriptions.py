from sqlalchemy import (create_engine, MetaData, Table,
                        Column, Integer, String, DateTime)
from sqlalchemy.sql import func

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
TABLE_NAME = "subscriptions"


def create_table():
    engine = create_engine(DB_URL)
    metadata = MetaData()

    # Define the table structure
    table = Table(
        TABLE_NAME,
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(50), nullable=False),
        Column("email", String(100), unique=True, nullable=False),
        Column("age", String(10), nullable=False),
        Column("gender", String(1), nullable=False),
        Column("favorite_celebrity", String(100), nullable=True),
        Column("subscribed_date_and_time", DateTime, default=func.now())
    )

    # Create the table
    metadata.create_all(engine)


def drop_table():
    engine = create_engine(DB_URL)
    metadata = MetaData()
    # Reflect the existing table
    table = Table(TABLE_NAME, metadata, autoload_with=engine)
    # Drop the table
    table.drop(engine)


def main():
    try:
        drop_table()
        print(
            f"{TABLE_NAME} 테이블이 존재합니다.\n"
            f"{TABLE_NAME} 테이블을 삭제 후 생성하겠습니다."
            )

    except Exception as e:
        print(
            f"{TABLE_NAME} 테이블이 존재하지 않습니다.\n"
            f"{TABLE_NAME} 테이블을 생성하겠습니다."
            )
    create_table()


if __name__ == "__main__":
    main()
    # create_table()
    # drop_table()

import asyncio

import databases
import sqlalchemy


DATABASE_URL = "sqlite+aiosqlite:///async_students.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

students = sqlalchemy.Table(
    "students",
    metadata,
    sqlalchemy.Column(
        "id",
        sqlalchemy.Integer,
        primary_key=True,
    ),
    sqlalchemy.Column(
        "full_name",
        sqlalchemy.String(100),
        nullable=False,
    ),
    sqlalchemy.Column(
        "group_name",
        sqlalchemy.String(20),
        nullable=False,
    ),
    sqlalchemy.Column(
        "variant",
        sqlalchemy.Integer,
        nullable=False,
    ),
)


async def main():
    """Демонстрирует асинхронную работу с базой данных."""
    engine = sqlalchemy.create_engine(
        "sqlite:///async_students.db"
    )

    metadata.drop_all(engine)
    metadata.create_all(engine)

    await database.connect()

    try:
        insert_query = students.insert()

        await database.execute_many(
            query=insert_query,
            values=[
                {
                    "full_name": "Ковалевич Александра Андреевна",
                    "group_name": "221141р",
                    "variant": 4,
                },
                {
                    "full_name": "Иванов Иван Иванович",
                    "group_name": "221141р",
                    "variant": 2,
                },
                {
                    "full_name": "Петров Пётр Петрович",
                    "group_name": "221141р",
                    "variant": 7,
                },
            ],
        )

        select_query = students.select()

        rows = await database.fetch_all(
            query=select_query
        )

        print("Асинхронно полученные записи:")

        for row in rows:
            print(
                row["id"],
                row["full_name"],
                row["group_name"],
                row["variant"],
            )

    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

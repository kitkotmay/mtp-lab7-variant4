import sqlite3


DATABASE_NAME = "task6.db"


def main():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            group_name TEXT NOT NULL,
            variant INTEGER NOT NULL
        )
    """)

    cursor.execute("DELETE FROM students")

    students = [
        (
            "Ковалевич Александра Андреевна",
            "221141р",
            4,
        ),
        (
            "Иванов Иван Иванович",
            "221141р",
            2,
        ),
        (
            "Петров Пётр Петрович",
            "221141р",
            4,
        ),
    ]

    cursor.executemany(
        """
        INSERT INTO students (full_name, group_name, variant)
        VALUES (?, ?, ?)
        """,
        students,
    )

    connection.commit()

    variant = int(input("Введите вариант для поиска: "))

    cursor.execute(
        """
        SELECT id, full_name, group_name, variant
        FROM students
        WHERE variant = ?
        """,
        (variant,),
    )

    result = cursor.fetchall()

    print(f"\nСтуденты с вариантом {variant}:")

    if result:
        for student in result:
            print(student)
    else:
        print("Записи не найдены.")

    connection.close()


if __name__ == "__main__":
    main()

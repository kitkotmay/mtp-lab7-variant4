import sqlite3


DATABASE_NAME = "task4.db"


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

    cursor.execute(
        """
        INSERT INTO students (full_name, group_name, variant)
        VALUES (?, ?, ?)
        """,
        (
            "Ковалевич Александра Андреевна",
            "221141р",
            4,
        ),
    )

    connection.commit()

    print("До обновления:")

    cursor.execute("SELECT * FROM students")

    for student in cursor.fetchall():
        print(student)

    cursor.execute(
        """
        UPDATE students
        SET variant = ?
        WHERE full_name = ?
        """,
        (
            7,
            "Ковалевич Александра Андреевна",
        ),
    )

    connection.commit()

    print("\nПосле обновления:")

    cursor.execute("SELECT * FROM students")

    for student in cursor.fetchall():
        print(student)

    connection.close()


if __name__ == "__main__":
    main()

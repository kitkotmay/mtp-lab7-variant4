import sqlite3


DATABASE_NAME = "transactions.db"


def show_accounts(cursor):
    """Выводит все счета."""
    cursor.execute(
        "SELECT id, owner, balance FROM accounts ORDER BY id"
    )

    for account in cursor.fetchall():
        print(account)


def transfer_money(
    connection,
    sender_id,
    receiver_id,
    amount,
):
    """Переводит деньги в рамках одной транзакции."""
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT balance FROM accounts WHERE id = ?",
            (sender_id,),
        )

        sender = cursor.fetchone()

        if sender is None:
            raise ValueError("Счёт отправителя не найден.")

        if sender[0] < amount:
            raise ValueError("Недостаточно средств.")

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - ?
            WHERE id = ?
            """,
            (amount, sender_id),
        )

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + ?
            WHERE id = ?
            """,
            (amount, receiver_id),
        )

        if cursor.rowcount == 0:
            raise ValueError("Счёт получателя не найден.")

        connection.commit()
        print("\nТранзакция успешно выполнена.")

    except (sqlite3.Error, ValueError) as error:
        connection.rollback()
        print(f"\nТранзакция отменена: {error}")


def main():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            owner TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)

    cursor.execute("DELETE FROM accounts")

    cursor.executemany(
        """
        INSERT INTO accounts (id, owner, balance)
        VALUES (?, ?, ?)
        """,
        [
            (1, "Александра", 1000.0),
            (2, "Иван", 500.0),
        ],
    )

    connection.commit()

    print("До транзакции:")
    show_accounts(cursor)

    transfer_money(
        connection,
        sender_id=1,
        receiver_id=2,
        amount=300.0,
    )

    print("\nПосле транзакции:")
    show_accounts(cursor)

    connection.close()


if __name__ == "__main__":
    main()

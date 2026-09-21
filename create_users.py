import mysql.connector
import bcrypt
from db import get_db_config


def create_user(username, password, role):

    config = get_db_config()

    conn = None
    cursor = None

    try:

        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password_hash,
                role
            )
            VALUES
            (
                %s,
                %s,
                %s
            )
            """,
            (
                username,
                password_hash,
                role
            )
        )

        conn.commit()

        print(
            f"✅ {role} user '{username}' created."
        )

    except mysql.connector.Error as error:

        print("❌ Database error:")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


def main():

    print()
    print("========================================")
    print("       CREATE PATIENT CONNECT USER")
    print("========================================")

    username = input("Username: ").strip()

    password = input("Password: ").strip()

    print()
    print("Select role:")
    print("1. ADMIN")
    print("2. DOCTOR")
    print("3. STAFF")

    choice = input("Role: ").strip()

    roles = {
        "1": "ADMIN",
        "2": "DOCTOR",
        "3": "STAFF"
    }

    role = roles.get(choice)

    if role is None:

        print("❌ Invalid role.")
        return

    create_user(
        username,
        password,
        role
    )


if __name__ == "__main__":
    main()
import mysql.connector
import bcrypt
from db import get_db_config


def login():

    print()
    print("========================================")
    print("          PATIENT CONNECT")
    print("             SECURE LOGIN")
    print("========================================")

    username = input("Username: ").strip()
    password = input("Password: ")

    conn = None
    cursor = None

    try:

        conn = mysql.connector.connect(
            **get_db_config()
        )

        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                user_id,
                username,
                password_hash,
                role,
                active
            FROM users
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        user = cursor.fetchone()

        if user is None:

            print()
            print("❌ Invalid username or password.")
            return None

        if not user["active"]:

            print()
            print("❌ This account is inactive.")
            return None

        stored_hash = user["password_hash"]

        if isinstance(stored_hash, str):

            stored_hash = stored_hash.encode(
                "utf-8"
            )

        if not bcrypt.checkpw(
            password.encode("utf-8"),
            stored_hash
        ):

            print()
            print("❌ Invalid username or password.")
            return None

        print()
        print("========================================")
        print("           LOGIN SUCCESSFUL")
        print("========================================")
        print(
            "Welcome:",
            user["username"]
        )
        print(
            "Role:",
            user["role"]
        )
        print("========================================")

        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"]
        }

    except mysql.connector.Error as error:

        print()
        print("❌ Database connection failed:")
        print(error)

        return None

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


if __name__ == "__main__":

    user = login()

    if user:

        print()
        print("Login test completed successfully.")
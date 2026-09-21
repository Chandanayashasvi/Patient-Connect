import mysql.connector
from db import get_db_config


conn = None
cursor = None

try:

    conn = mysql.connector.connect(**get_db_config())

    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, role, active
        FROM users
        ORDER BY user_id
    """)

    users = cursor.fetchall()

    print()
    print("========================================")
    print("          PATIENT CONNECT USERS")
    print("========================================")

    for user in users:

        print(
            "ID:", user[0],
            "| Username:", user[1],
            "| Role:", user[2],
            "| Active:", user[3]
        )

    print("========================================")

except mysql.connector.Error as error:

    print("❌ Database error:")
    print(error)

finally:

    if cursor is not None:
        cursor.close()

    if conn is not None:
        conn.close()
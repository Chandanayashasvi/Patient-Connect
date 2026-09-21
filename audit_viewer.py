
import mysql.connector
from db import get_db_config


# ============================================================
# VIEW AUDIT LOGS
# ============================================================

def view_audit_logs():

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**get_db_config())
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                a.audit_id,
                u.username,
                u.role,
                a.action,
                a.table_name,
                a.record_id,
                a.details,
                a.created_at
            FROM audit_logs a
            LEFT JOIN users u
                ON a.user_id = u.user_id
            ORDER BY a.created_at DESC
            LIMIT 100
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        print()
        print("============================================================")
        print("                     AUDIT LOGS")
        print("============================================================")

        if not rows:
            print("No audit logs found.")
            return

        for row in rows:

            print()
            print("------------------------------------------------------------")
            print("Audit ID :", row["audit_id"])
            print("User     :", row["username"] or "SYSTEM")
            print("Role     :", row["role"] or "SYSTEM")
            print("Action   :", row["action"])
            print("Table    :", row["table_name"] or "-")
            print("Record ID:", row["record_id"] or "-")
            print("Details  :", row["details"] or "-")
            print("Time     :", row["created_at"])

        print()
        print("============================================================")
        print("Showing latest 100 audit records.")
        print("============================================================")

        input("\nPress Enter to continue...")

    except mysql.connector.Error as e:
        print()
        print("❌ Database error:", e)
        input("Press Enter to continue...")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":
    view_audit_logs()


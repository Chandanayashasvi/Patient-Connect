
import mysql.connector
from db import get_db_config


# ============================================================
# AUDIT LOG
# ============================================================

def log_action(
    user_id=None,
    action="UNKNOWN",
    table_name=None,
    record_id=None,
    details=None
):
    """
    Add an activity to the audit_logs table.

    Parameters:
        user_id    : ID of logged-in user
        action     : Action performed
        table_name : Database table affected
        record_id  : ID of affected record
        details    : Additional information
    """

    connection = None
    cursor = None

    try:
        connection = mysql.connector.connect(**get_db_config())
        cursor = connection.cursor()

        query = """
            INSERT INTO audit_logs
            (
                user_id,
                action,
                table_name,
                record_id,
                details
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            action,
            table_name,
            record_id,
            details
        )

        cursor.execute(query, values)
        connection.commit()

    except mysql.connector.Error as e:
        print("⚠️ Audit log error:", e)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()


# ============================================================
# TEST AUDIT LOG
# ============================================================

if __name__ == "__main__":

    print("========================================")
    print("          AUDIT LOGGER TEST")
    print("========================================")

    log_action(
        user_id=1,
        action="SYSTEM_TEST",
        table_name="audit_logs",
        record_id=None,
        details="Audit logging system test"
    )

    print("✅ Audit log test completed.")


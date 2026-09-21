import mysql.connector
from db import get_db_config


# ============================================================
# CHECK INSURANCE ELIGIBILITY
# ============================================================

def check_eligibility(user):

    print()
    print("========================================")
    print("       INSURANCE ELIGIBILITY")
    print("========================================")

    try:
        insurance_id = int(input("Insurance ID: ").strip())
    except ValueError:
        print("❌ Insurance ID must be a number.")
        return

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(
            **get_db_config()
        )

        cursor = conn.cursor(dictionary=True)

        # Get insurance information
        cursor.execute(
            """
            SELECT
                insurance_id,
                patient_id,
                insurance_provider,
                member_id,
                insurance_status,
                effective_date,
                expiration_date
            FROM patient_insurance
            WHERE insurance_id = %s
            """,
            (insurance_id,)
        )

        insurance = cursor.fetchone()

        if insurance is None:
            print("❌ Insurance record not found.")
            return

        # Display basic information
        print()
        print("----------------------------------------")
        print("Insurance ID :", insurance["insurance_id"])
        print("Patient ID   :", insurance["patient_id"])
        print("Provider     :", insurance["insurance_provider"])
        print("Status       :", insurance["insurance_status"])
        print("Effective    :", insurance["effective_date"])
        print("Expiration   :", insurance["expiration_date"])
        print("----------------------------------------")

        # Determine eligibility
        cursor.execute(
            """
            SELECT
                CASE
                    WHEN insurance_status = 'ACTIVE'
                         AND (
                             effective_date IS NULL
                             OR effective_date <= CURDATE()
                         )
                         AND (
                             expiration_date IS NULL
                             OR expiration_date >= CURDATE()
                         )
                    THEN 'ELIGIBLE'

                    WHEN insurance_status = 'PENDING'
                    THEN 'PENDING'

                    ELSE 'NOT_ELIGIBLE'
                END AS eligibility_status
            FROM patient_insurance
            WHERE insurance_id = %s
            """,
            (insurance_id,)
        )

        result = cursor.fetchone()

        eligibility_status = result["eligibility_status"]

        if eligibility_status == "ELIGIBLE":
            response_message = (
                "Insurance is active and currently eligible."
            )

        elif eligibility_status == "PENDING":
            response_message = (
                "Insurance eligibility is pending verification."
            )

        else:
            response_message = (
                "Insurance is not currently eligible."
            )

        # Save eligibility check
        cursor.execute(
            """
            INSERT INTO insurance_eligibility
            (
                insurance_id,
                checked_by,
                eligibility_status,
                response_message
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                insurance_id,
                user["user_id"],
                eligibility_status,
                response_message
            )
        )

        conn.commit()

        print()
        print("========================================")
        print("       ELIGIBILITY RESULT")
        print("========================================")
        print("Status :", eligibility_status)
        print("Message:", response_message)
        print("========================================")

    except mysql.connector.Error as error:

        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass

        print("❌ Database error:")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# ============================================================
# VIEW ELIGIBILITY HISTORY
# ============================================================

def view_eligibility_history():

    print()
    print("========================================")
    print("       ELIGIBILITY HISTORY")
    print("========================================")

    try:
        insurance_id = int(input("Insurance ID: ").strip())
    except ValueError:
        print("❌ Insurance ID must be a number.")
        return

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
                eligibility_id,
                insurance_id,
                checked_by,
                eligibility_status,
                checked_at,
                response_message
            FROM insurance_eligibility
            WHERE insurance_id = %s
            ORDER BY checked_at DESC
            """,
            (insurance_id,)
        )

        rows = cursor.fetchall()

        if not rows:
            print("No eligibility history found.")
            return

        for row in rows:

            print()
            print("----------------------------------------")
            print("Eligibility ID :", row["eligibility_id"])
            print("Insurance ID   :", row["insurance_id"])
            print("Checked By     :", row["checked_by"])
            print("Status         :", row["eligibility_status"])
            print("Checked At     :", row["checked_at"])
            print("Message        :", row["response_message"])
            print("----------------------------------------")

    except mysql.connector.Error as error:

        print("❌ Database error:")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# ============================================================
# ELIGIBILITY MENU
# ============================================================

def eligibility_menu(user):

    while True:

        print()
        print("========================================")
        print("       INSURANCE ELIGIBILITY")
        print("========================================")
        print("1. Check Eligibility")
        print("2. View Eligibility History")
        print("3. Back")
        print("========================================")

        choice = input("Select option: ").strip()

        if choice == "1":
            check_eligibility(user)

        elif choice == "2":
            view_eligibility_history()

        elif choice == "3":
            break

        else:
            print("❌ Invalid option.")
            
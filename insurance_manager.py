import mysql.connector
from db import get_db_config


def add_insurance(user):

    print()
    print("========================================")
    print("          ADD PATIENT INSURANCE")
    print("========================================")

    try:
        patient_id = int(input("Patient ID: ").strip())
    except ValueError:
        print("❌ Patient ID must be a number.")
        return

    provider = input("Insurance provider: ").strip()
    member_id = input("Member ID: ").strip()
    group_number = input("Group number: ").strip()
    plan_name = input("Plan name: ").strip()
    holder_name = input("Policy holder name: ").strip()
    relationship = input(
        "Relationship to policy holder: "
    ).strip()

    status = input(
        "Status (ACTIVE/INACTIVE/EXPIRED/PENDING): "
    ).strip().upper()

    if status not in (
        "ACTIVE",
        "INACTIVE",
        "EXPIRED",
        "PENDING"
    ):
        print("❌ Invalid insurance status.")
        return

    effective_date = input(
        "Effective date (YYYY-MM-DD): "
    ).strip()

    expiration_date = input(
        "Expiration date (YYYY-MM-DD): "
    ).strip()

    conn = None
    cursor = None

    try:

        conn = mysql.connector.connect(
            **get_db_config()
        )

        cursor = conn.cursor()

        # Check patient
        cursor.execute(
            """
            SELECT patient_id
            FROM patients
            WHERE patient_id = %s
            """,
            (patient_id,)
        )

        if cursor.fetchone() is None:
            print("❌ Patient not found.")
            return

        # Add insurance
        cursor.execute(
            """
            INSERT INTO patient_insurance
            (
                patient_id,
                insurance_provider,
                member_id,
                group_number,
                plan_name,
                policy_holder_name,
                relationship_to_policy_holder,
                insurance_status,
                effective_date,
                expiration_date
            )
            VALUES
            (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            """,
            (
                patient_id,
                provider,
                member_id,
                group_number,
                plan_name,
                holder_name,
                relationship,
                status,
                effective_date,
                expiration_date
            )
        )

        insurance_id = cursor.lastrowid

        # Audit log
        cursor.execute(
            """
            INSERT INTO audit_logs
            (
                user_id,
                action,
                table_name,
                record_id,
                details
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                %s
            )
            """,
            (
                user["user_id"],
                "ADD_INSURANCE",
                "patient_insurance",
                insurance_id,
                "Insurance record added"
            )
        )

        conn.commit()

        print()
        print("✅ Insurance added successfully.")
        print("Insurance ID:", insurance_id)

    except mysql.connector.Error as error:

        if conn is not None:
            conn.rollback()

        print("❌ Database error:")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


def view_insurance():

    print()
    print("========================================")
    print("        VIEW PATIENT INSURANCE")
    print("========================================")

    try:
        patient_id = int(input("Patient ID: ").strip())
    except ValueError:
        print("❌ Patient ID must be a number.")
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
                insurance_id,
                patient_id,
                insurance_provider,
                member_id,
                group_number,
                plan_name,
                policy_holder_name,
                relationship_to_policy_holder,
                insurance_status,
                effective_date,
                expiration_date
            FROM patient_insurance
            WHERE patient_id = %s
            ORDER BY insurance_id
            """,
            (patient_id,)
        )

        records = cursor.fetchall()

        if not records:
            print("No insurance records found.")
            return

        for row in records:

            member_id = str(row["member_id"])

            if len(member_id) > 4:
                masked_member = (
                    "*" * (len(member_id) - 4)
                    + member_id[-4:]
                )
            else:
                masked_member = "****"

            print()
            print("----------------------------------------")
            print("Insurance ID :", row["insurance_id"])
            print("Provider     :", row["insurance_provider"])
            print("Member ID    :", masked_member)
            print("Group Number :", row["group_number"])
            print("Plan         :", row["plan_name"])
            print("Policy Holder:", row["policy_holder_name"])
            print("Relationship  :", row[
                "relationship_to_policy_holder"
            ])
            print("Status       :", row["insurance_status"])
            print("Effective    :", row["effective_date"])
            print("Expiration   :", row["expiration_date"])
            print("----------------------------------------")

    except mysql.connector.Error as error:

        print("❌ Database error:")
        print(error)

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


def insurance_menu(user):

    while True:

        print()
        print("========================================")
        print("        INSURANCE MANAGEMENT")
        print("========================================")
        print("1. Add Insurance")
        print("2. View Patient Insurance")
        print("3. Back")
        print("========================================")

        choice = input("Select option: ").strip()

        if choice == "1":
            add_insurance(user)

        elif choice == "2":
            view_insurance()

        elif choice == "3":
            break

        else:
            print("❌ Invalid option.")
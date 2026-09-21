# ============================================================
# PATIENT CONNECT - CLI
# ============================================================
# USA Healthcare Insurance + Eligibility
# MySQL Backend
# Stored Procedures
# Email Notifications
# CSV Export
# Excel Sync
# ============================================================

from excel_sync import sync_patients_to_excel
import csv

from db import get_connection
from mailer import send_email


# ============================================================
# HELPER
# ============================================================

def pause():
    input("\nPress Enter to continue...")


# ============================================================
# 1. CREATE PATIENT
# ============================================================

def create_patient():

    try:

        clinic_id = int(
            input("Clinic ID: ").strip()
        )

        first_name = input(
            "First name: "
        ).strip()

        last_name = input(
            "Last name: "
        ).strip()

        email = input(
            "Email: "
        ).strip()

        phone = input(
            "Phone: "
        ).strip()

        date_of_birth = input(
            "Date of birth (YYYY-MM-DD): "
        ).strip()

        gender = input(
            "Gender (M/F/Other/Unknown): "
        ).strip()

        if gender not in [
            "M",
            "F",
            "Other",
            "Unknown"
        ]:

            print("❌ Invalid gender.")
            return

        # ====================================================
        # CREATE PATIENT
        # ====================================================

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO patients
                    (
                        clinic_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        date_of_birth,
                        gender
                    )
                    VALUES
                    (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        clinic_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        date_of_birth,
                        gender
                    )
                )

                patient_id = cursor.lastrowid

                conn.commit()

                print()
                print("✅ Patient created successfully.")
                print(
                    f"Patient ID: {patient_id}"
                )

            finally:

                cursor.close()

        # ====================================================
        # OPTIONAL INSURANCE
        # ====================================================

        add_insurance = input(
            "\nDo you want to add insurance? (Y/N): "
        ).strip().upper()

        if add_insurance != "Y":

            print(
                "Patient created without insurance."
            )

            return

        # ====================================================
        # USA INSURANCE TYPE
        # ====================================================

        print()
        print("=" * 50)
        print("          USA PATIENT INSURANCE")
        print("=" * 50)

        print("1. Medicare")
        print("2. Medicaid")
        print("3. Private Insurance")

        print("=" * 50)

        insurance_choice = input(
            "Select insurance type: "
        ).strip()

        insurance_types = {
            "1": "MEDICARE",
            "2": "MEDICAID",
            "3": "PRIVATE"
        }

        if insurance_choice not in insurance_types:

            print(
                "❌ Invalid insurance type."
            )

            print(
                "Patient was created, "
                "but insurance was not added."
            )

            return

        insurance_type = insurance_types[
            insurance_choice
        ]

        # ====================================================
        # PROVIDER
        # ====================================================

        if insurance_type == "MEDICARE":

            provider = "Medicare"

        elif insurance_type == "MEDICAID":

            provider = input(
                "Medicaid provider/program: "
            ).strip()

            if not provider:

                provider = "Medicaid"

        else:

            provider = input(
                "Private insurance provider: "
            ).strip()

            if not provider:

                print(
                    "❌ Insurance provider is required."
                )

                return

        # ====================================================
        # INSURANCE DETAILS
        # ====================================================

        member_id = input(
            "Member ID: "
        ).strip()

        if not member_id:

            print(
                "❌ Member ID is required."
            )

            return

        group_number = input(
            "Group number (optional): "
        ).strip()

        plan_name = input(
            "Plan name: "
        ).strip()

        holder_name = input(
            "Policy holder name: "
        ).strip()

        relationship = input(
            "Relationship to policy holder: "
        ).strip()

        status = input(
            "Status "
            "(ACTIVE/INACTIVE/EXPIRED/PENDING): "
        ).strip().upper()

        valid_statuses = [
            "ACTIVE",
            "INACTIVE",
            "EXPIRED",
            "PENDING"
        ]

        if status not in valid_statuses:

            print(
                "❌ Invalid insurance status."
            )

            print(
                "Patient was created, "
                "but insurance was not added."
            )

            return

        effective_date = input(
            "Effective date (YYYY-MM-DD): "
        ).strip()

        expiration_date = input(
            "Expiration date (YYYY-MM-DD): "
        ).strip()

        # ====================================================
        # INSERT INSURANCE
        # ====================================================

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    INSERT INTO patient_insurance
                    (
                        patient_id,
                        insurance_type,
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
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        patient_id,
                        insurance_type,
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

                conn.commit()

                print()
                print("=" * 50)
                print("       INSURANCE ADDED SUCCESSFULLY")
                print("=" * 50)

                print(
                    f"Insurance ID   : {insurance_id}"
                )

                print(
                    f"Patient ID     : {patient_id}"
                )

                print(
                    f"Insurance Type : {insurance_type}"
                )

                print(
                    f"Provider       : {provider}"
                )

                print(
                    f"Status         : {status}"
                )

                print("=" * 50)

            finally:

                cursor.close()

    except ValueError:

        print(
            "❌ Please enter a valid numeric Clinic ID."
        )

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 2. VIEW PATIENTS
# ============================================================

def view_patients():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        p.patient_id,
                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS patient_name,
                        c.clinic_name,
                        p.email,
                        p.phone,
                        p.date_of_birth,
                        p.gender
                    FROM patients p
                    JOIN clinics c
                        ON p.clinic_id = c.clinic_id
                    ORDER BY p.patient_id
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No patients found."
                    )

                    return

                print(
                    "\n================ PATIENTS ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Name: {row[1]} | "
                        f"Clinic: {row[2]} | "
                        f"Email: {row[3]} | "
                        f"Phone: {row[4]} | "
                        f"DOB: {row[5]} | "
                        f"Gender: {row[6]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 3. SEARCH PATIENT
# ============================================================

def search_patient():

    try:

        keyword = input(
            "Enter patient name or email: "
        ).strip()

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        patient_id,
                        first_name,
                        last_name,
                        email,
                        phone
                    FROM patients
                    WHERE first_name LIKE %s
                       OR last_name LIKE %s
                       OR email LIKE %s
                    ORDER BY patient_id
                    """,
                    (
                        f"%{keyword}%",
                        f"%{keyword}%",
                        f"%{keyword}%"
                    )
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No matching patients found."
                    )

                    return

                print(
                    "\n================ SEARCH RESULTS ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Name: {row[1]} {row[2]} | "
                        f"Email: {row[3]} | "
                        f"Phone: {row[4]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 4. VIEW CLINICS
# ============================================================

def view_clinics():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        clinic_id,
                        clinic_name,
                        address,
                        phone,
                        email
                    FROM clinics
                    ORDER BY clinic_id
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No clinics found."
                    )

                    return

                print(
                    "\n================ CLINICS ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Clinic: {row[1]} | "
                        f"Address: {row[2]} | "
                        f"Phone: {row[3]} | "
                        f"Email: {row[4]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 5. VIEW PROVIDERS
# ============================================================

def view_providers():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        p.provider_id,
                        p.provider_name,
                        c.clinic_name,
                        p.specialty,
                        p.email,
                        p.phone
                    FROM providers p
                    JOIN clinics c
                        ON p.clinic_id = c.clinic_id
                    ORDER BY p.provider_id
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No providers found."
                    )

                    return

                print(
                    "\n================ PROVIDERS ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Provider: {row[1]} | "
                        f"Clinic: {row[2]} | "
                        f"Specialty: {row[3]} | "
                        f"Email: {row[4]} | "
                        f"Phone: {row[5]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 6. VIEW APPOINTMENTS
# ============================================================

def view_appointments():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        a.appointment_id,
                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS patient_name,
                        pr.provider_name,
                        c.clinic_name,
                        a.scheduled_at,
                        a.status,
                        a.reason
                    FROM appointments a
                    JOIN patients p
                        ON a.patient_id = p.patient_id
                    JOIN providers pr
                        ON a.provider_id = pr.provider_id
                    JOIN clinics c
                        ON a.clinic_id = c.clinic_id
                    ORDER BY a.scheduled_at
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No appointments found."
                    )

                    return

                print(
                    "\n================ APPOINTMENTS ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Patient: {row[1]} | "
                        f"Provider: {row[2]} | "
                        f"Clinic: {row[3]} | "
                        f"Date: {row[4]} | "
                        f"Status: {row[5]} | "
                        f"Reason: {row[6]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 7. BOOK APPOINTMENT + EMAIL
# ============================================================

def book_appointment():

    try:

        patient_id = int(
            input("Patient ID: ").strip()
        )

        provider_id = int(
            input("Provider ID: ").strip()
        )

        scheduled_at = input(
            "Date and time (YYYY-MM-DD HH:MM:SS): "
        ).strip()

        reason = input(
            "Reason: "
        ).strip()

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.callproc(
                    "sp_book_appointment",
                    (
                        patient_id,
                        provider_id,
                        scheduled_at,
                        reason
                    )
                )

                appointment_id = None

                for result in cursor.stored_results():

                    rows = result.fetchall()

                    for row in rows:

                        appointment_id = row[0]

                        print(
                            f"\n✅ Appointment booked. "
                            f"Appointment ID: "
                            f"{appointment_id}"
                        )

                conn.commit()

                # ------------------------------------------------
                # GET PATIENT DETAILS
                # ------------------------------------------------

                cursor.execute(
                    """
                    SELECT
                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS patient_name,
                        p.email,
                        pr.provider_name,
                        c.clinic_name
                    FROM patients p
                    JOIN providers pr
                        ON pr.provider_id = %s
                    JOIN clinics c
                        ON c.clinic_id = p.clinic_id
                    WHERE p.patient_id = %s
                    """,
                    (
                        provider_id,
                        patient_id
                    )
                )

                patient = cursor.fetchone()

                if not patient:

                    print(
                        "⚠️ Patient details not found."
                    )

                    return

                patient_name = patient[0]
                patient_email = patient[1]
                provider_name = patient[2]
                clinic_name = patient[3]

                # ------------------------------------------------
                # SEND EMAIL
                # ------------------------------------------------

                if patient_email:

                    subject = (
                        "PatientConnect - "
                        "Appointment Confirmation"
                    )

                    text = f"""
Hello {patient_name},

Your appointment has been successfully booked.

Appointment ID: {appointment_id}
Provider: {provider_name}
Clinic: {clinic_name}
Date and Time: {scheduled_at}
Reason: {reason}

Thank you,
PatientConnect
"""

                    email_sent = send_email(
                        to_email=patient_email,
                        subject=subject,
                        text=text,
                        to_name=patient_name
                    )

                    if email_sent:

                        print(
                            f"📧 Confirmation email sent to "
                            f"{patient_email}"
                        )

                    else:

                        print(
                            "⚠️ Appointment booked, "
                            "but confirmation email failed."
                        )

                else:

                    print(
                        "⚠️ Appointment booked, "
                        "but patient has no email address."
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 8. UPDATE APPOINTMENT STATUS
# ============================================================

def update_appointment_status():

    try:

        appointment_id = int(
            input("Appointment ID: ").strip()
        )

        new_status = input(
            "New status "
            "(scheduled/confirmed/completed/"
            "cancelled/no_show/rescheduled): "
        ).strip()

        note = input(
            "Note: "
        ).strip()

        valid_statuses = [
            "scheduled",
            "confirmed",
            "completed",
            "cancelled",
            "no_show",
            "rescheduled"
        ]

        if new_status not in valid_statuses:

            print(
                "❌ Invalid status."
            )

            return

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.callproc(
                    "sp_update_appointment_status",
                    (
                        appointment_id,
                        new_status,
                        note
                    )
                )

                for result in cursor.stored_results():

                    rows = result.fetchall()

                    for row in rows:

                        print(
                            f"\n✅ Appointment "
                            f"{row[0]} changed from "
                            f"{row[1]} to {row[2]}."
                        )

                conn.commit()

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 9. VIEW MESSAGES
# ============================================================

def view_messages():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        m.message_id,
                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS patient_name,
                        m.appointment_id,
                        m.message_type,
                        m.channel,
                        m.status,
                        m.sent_at
                    FROM messages m
                    JOIN patients p
                        ON m.patient_id = p.patient_id
                    ORDER BY m.message_id
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No messages found."
                    )

                    return

                print(
                    "\n================ MESSAGES ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Patient: {row[1]} | "
                        f"Appointment: {row[2]} | "
                        f"Type: {row[3]} | "
                        f"Channel: {row[4]} | "
                        f"Status: {row[5]} | "
                        f"Sent: {row[6]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 10. CLINIC APPOINTMENT COUNT
# ============================================================

def clinic_appointment_count():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.callproc(
                    "sp_clinic_appointment_count"
                )

                print(
                    "\n========= CLINIC APPOINTMENT COUNT ========="
                )

                for result in cursor.stored_results():

                    rows = result.fetchall()

                    for row in rows:

                        print(
                            f"Clinic ID: {row[0]} | "
                            f"Clinic: {row[1]} | "
                            f"Appointments: {row[2]}"
                        )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 11. RECALL CANDIDATES
# ============================================================

def recall_candidates():

    try:

        condition_id = int(
            input("Condition ID: ").strip()
        )

        months = int(
            input("Months overdue: ").strip()
        )

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.callproc(
                    "sp_recall_candidates",
                    (
                        condition_id,
                        months
                    )
                )

                found = False

                print(
                    "\n========= RECALL CANDIDATES ========="
                )

                for result in cursor.stored_results():

                    rows = result.fetchall()

                    for row in rows:

                        found = True

                        print(
                            f"Patient ID: {row[0]} | "
                            f"Patient: {row[1]} | "
                            f"Condition: {row[2]} | "
                            f"Last visit: {row[3]} | "
                            f"Days overdue: {row[4]}"
                        )

                if not found:

                    print(
                        "No recall candidates found."
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 12. DUE REMINDERS
# ============================================================

def due_reminders():

    try:

        hours = int(
            input("Hours ahead: ").strip()
        )

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.callproc(
                    "sp_due_reminders",
                    (hours,)
                )

                found = False

                print(
                    "\n========= DUE REMINDERS ========="
                )

                for result in cursor.stored_results():

                    rows = result.fetchall()

                    for row in rows:

                        found = True

                        print(
                            f"Appointment ID: {row[0]} | "
                            f"Patient ID: {row[1]} | "
                            f"Patient: {row[2]} | "
                            f"Provider ID: {row[3]} | "
                            f"Date: {row[4]} | "
                            f"Reason: {row[5]}"
                        )

                if not found:

                    print(
                        "No reminders are due."
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 13. EXPORT PATIENTS TO CSV
# ============================================================

def export_patients_csv():

    try:

        filename = input(
            "CSV filename "
            "(default patients.csv): "
        ).strip()

        if not filename:

            filename = "patients.csv"

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        p.patient_id,
                        p.first_name,
                        p.last_name,
                        c.clinic_name,
                        p.email,
                        p.phone,
                        p.date_of_birth,
                        p.gender
                    FROM patients p
                    JOIN clinics c
                        ON p.clinic_id = c.clinic_id
                    ORDER BY p.patient_id
                    """
                )

                rows = cursor.fetchall()

                with open(
                    filename,
                    "w",
                    newline="",
                    encoding="utf-8"
                ) as file:

                    writer = csv.writer(file)

                    writer.writerow(
                        [
                            "Patient ID",
                            "First Name",
                            "Last Name",
                            "Clinic",
                            "Email",
                            "Phone",
                            "Date of Birth",
                            "Gender"
                        ]
                    )

                    writer.writerows(rows)

                print(
                    f"✅ Patients exported to "
                    f"{filename}"
                )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ CSV export error:",
            e
        )


# ============================================================
# 14. VIEW CONDITIONS
# ============================================================

def view_conditions():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        condition_id,
                        condition_name
                    FROM conditions
                    ORDER BY condition_id
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No conditions found."
                    )

                    return

                print(
                    "\n================ CONDITIONS ================"
                )

                for row in rows:

                    print(
                        f"ID: {row[0]} | "
                        f"Condition: {row[1]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 15. VIEW PATIENT CONDITIONS
# ============================================================

def view_patient_conditions():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        p.patient_id,
                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS patient_name,
                        c.condition_id,
                        c.condition_name
                    FROM patient_conditions pc
                    JOIN patients p
                        ON pc.patient_id = p.patient_id
                    JOIN conditions c
                        ON pc.condition_id = c.condition_id
                    ORDER BY p.patient_id
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No patient conditions found."
                    )

                    return

                print(
                    "\n========== PATIENT CONDITIONS =========="
                )

                for row in rows:

                    print(
                        f"Patient ID: {row[0]} | "
                        f"Patient: {row[1]} | "
                        f"Condition ID: {row[2]} | "
                        f"Condition: {row[3]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 16. VIEW APPOINTMENT STATUS HISTORY
# ============================================================

def view_appointment_history():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        h.history_id,
                        h.appointment_id,
                        h.old_status,
                        h.new_status,
                        h.changed_at,
                        h.note
                    FROM appointment_status_history h
                    ORDER BY h.history_id DESC
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No appointment history found."
                    )

                    return

                print(
                    "\n======= APPOINTMENT STATUS HISTORY ======="
                )

                for row in rows:

                    print(
                        f"History ID: {row[0]} | "
                        f"Appointment ID: {row[1]} | "
                        f"Old: {row[2]} | "
                        f"New: {row[3]} | "
                        f"Changed: {row[4]} | "
                        f"Note: {row[5]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 17. PATIENT APPOINTMENT HISTORY
# ============================================================

def patient_appointment_history():

    try:

        patient_id = int(
            input("Patient ID: ").strip()
        )

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        a.appointment_id,
                        a.scheduled_at,
                        a.status,
                        a.reason,
                        pr.provider_name,
                        c.clinic_name
                    FROM appointments a
                    JOIN providers pr
                        ON a.provider_id =
                           pr.provider_id
                    JOIN clinics c
                        ON a.clinic_id =
                           c.clinic_id
                    WHERE a.patient_id = %s
                    ORDER BY a.scheduled_at DESC
                    """,
                    (patient_id,)
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No appointments found "
                        "for this patient."
                    )

                    return

                print(
                    "\n======= PATIENT APPOINTMENT HISTORY ======="
                )

                for row in rows:

                    print(
                        f"Appointment ID: {row[0]} | "
                        f"Date: {row[1]} | "
                        f"Status: {row[2]} | "
                        f"Reason: {row[3]} | "
                        f"Provider: {row[4]} | "
                        f"Clinic: {row[5]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 18. PROVIDER APPOINTMENT COUNT
# ============================================================

def provider_appointment_count():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        pr.provider_id,
                        pr.provider_name,
                        pr.specialty,
                        COUNT(a.appointment_id)
                            AS appointment_count
                    FROM providers pr
                    LEFT JOIN appointments a
                        ON pr.provider_id =
                           a.provider_id
                    GROUP BY
                        pr.provider_id,
                        pr.provider_name,
                        pr.specialty
                    ORDER BY appointment_count DESC
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No providers found."
                    )

                    return

                print(
                    "\n======= PROVIDER APPOINTMENT COUNT ======="
                )

                for row in rows:

                    print(
                        f"Provider ID: {row[0]} | "
                        f"Provider: {row[1]} | "
                        f"Specialty: {row[2]} | "
                        f"Appointments: {row[3]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 19. APPOINTMENT STATUS SUMMARY
# ============================================================

def appointment_status_summary():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        status,
                        COUNT(*) AS total
                    FROM appointments
                    GROUP BY status
                    ORDER BY total DESC
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No appointments found."
                    )

                    return

                print(
                    "\n======= APPOINTMENT STATUS SUMMARY ======="
                )

                for row in rows:

                    print(
                        f"Status: {row[0]} | "
                        f"Count: {row[1]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 20. MESSAGE DELIVERY SUMMARY
# ============================================================

def message_delivery_summary():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        channel,
                        status,
                        COUNT(*) AS total
                    FROM messages
                    GROUP BY
                        channel,
                        status
                    ORDER BY
                        channel,
                        total DESC
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No messages found."
                    )

                    return

                print(
                    "\n======= MESSAGE DELIVERY SUMMARY ======="
                )

                for row in rows:

                    print(
                        f"Channel: {row[0]} | "
                        f"Status: {row[1]} | "
                        f"Count: {row[2]}"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 21. NO-SHOW REPORT
# ============================================================

def no_show_report():

    try:

        with get_connection() as conn:

            cursor = conn.cursor()

            try:

                cursor.execute(
                    """
                    SELECT
                        pr.provider_id,
                        pr.provider_name,

                        COUNT(a.appointment_id)
                            AS total_appointments,

                        SUM(
                            CASE
                                WHEN a.status = 'no_show'
                                THEN 1
                                ELSE 0
                            END
                        ) AS no_shows,

                        ROUND(
                            (
                                SUM(
                                    CASE
                                        WHEN a.status = 'no_show'
                                        THEN 1
                                        ELSE 0
                                    END
                                )
                                /
                                NULLIF(
                                    COUNT(
                                        a.appointment_id
                                    ),
                                    0
                                )
                            ) * 100,
                            2
                        ) AS no_show_rate

                    FROM providers pr

                    LEFT JOIN appointments a
                        ON pr.provider_id =
                           a.provider_id

                    GROUP BY
                        pr.provider_id,
                        pr.provider_name

                    ORDER BY no_show_rate DESC
                    """
                )

                rows = cursor.fetchall()

                if not rows:

                    print(
                        "No data found."
                    )

                    return

                print(
                    "\n================ NO-SHOW REPORT ================"
                )

                for row in rows:

                    print(
                        f"Provider ID: {row[0]} | "
                        f"Provider: {row[1]} | "
                        f"Appointments: {row[2]} | "
                        f"No Shows: {row[3]} | "
                        f"No-show Rate: {row[4]}%"
                    )

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 22. USA INSURANCE ELIGIBILITY LIST
# ============================================================

def view_eligibility_list():

    try:

        with get_connection() as conn:

            cursor = conn.cursor(dictionary=True)

            try:

                cursor.execute(
                    """
                    SELECT
                        pi.insurance_id,
                        pi.patient_id,

                        CONCAT(
                            p.first_name,
                            ' ',
                            p.last_name
                        ) AS patient_name,

                        pi.insurance_type,
                        pi.insurance_provider,
                        pi.member_id,
                        pi.group_number,
                        pi.plan_name,
                        pi.policy_holder_name,
                        pi.relationship_to_policy_holder,
                        pi.insurance_status,
                        pi.effective_date,
                        pi.expiration_date,

                        CASE

                            WHEN pi.insurance_status = 'ACTIVE'
                                 AND (
                                     pi.effective_date IS NULL
                                     OR pi.effective_date <= CURDATE()
                                 )
                                 AND (
                                     pi.expiration_date IS NULL
                                     OR pi.expiration_date >= CURDATE()
                                 )

                            THEN 'ELIGIBLE'

                            WHEN pi.insurance_status = 'PENDING'

                            THEN 'PENDING'

                            ELSE 'NOT_ELIGIBLE'

                        END AS eligibility_status

                    FROM patient_insurance pi

                    JOIN patients p
                        ON pi.patient_id =
                           p.patient_id

                    ORDER BY
                        pi.patient_id,
                        pi.insurance_id
                    """
                )

                rows = cursor.fetchall()

                print()
                print("=" * 80)
                print(
                    "             USA INSURANCE ELIGIBILITY LIST"
                )
                print("=" * 80)

                if not rows:

                    print(
                        "No insurance records found."
                    )

                    return

                eligible_count = 0
                pending_count = 0
                not_eligible_count = 0

                for row in rows:

                    print()
                    print("-" * 80)

                    print(
                        f"Insurance ID    : "
                        f"{row['insurance_id']}"
                    )

                    print(
                        f"Patient ID      : "
                        f"{row['patient_id']}"
                    )

                    print(
                        f"Patient         : "
                        f"{row['patient_name']}"
                    )

                    print(
                        f"Insurance Type  : "
                        f"{row['insurance_type']}"
                    )

                    print(
                        f"Provider        : "
                        f"{row['insurance_provider']}"
                    )

                    # ------------------------------------------------
                    # MASK MEMBER ID
                    # ------------------------------------------------

                    member_id = str(
                        row["member_id"]
                    )

                    if len(member_id) > 4:

                        masked_member = (
                            "*" *
                            (len(member_id) - 4)
                            +
                            member_id[-4:]
                        )

                    else:

                        masked_member = "****"

                    print(
                        f"Member ID       : "
                        f"{masked_member}"
                    )

                    print(
                        f"Group Number    : "
                        f"{row['group_number'] or 'N/A'}"
                    )

                    print(
                        f"Plan            : "
                        f"{row['plan_name'] or 'N/A'}"
                    )

                    print(
                        f"Policy Holder   : "
                        f"{row['policy_holder_name'] or 'N/A'}"
                    )

                    print(
                        f"Relationship    : "
                        f"{row['relationship_to_policy_holder'] or 'N/A'}"
                    )

                    print(
                        f"Insurance Status: "
                        f"{row['insurance_status']}"
                    )

                    print(
                        f"Effective Date  : "
                        f"{row['effective_date'] or 'N/A'}"
                    )

                    print(
                        f"Expiration Date : "
                        f"{row['expiration_date'] or 'N/A'}"
                    )

                    print(
                        f"Eligibility     : "
                        f"{row['eligibility_status']}"
                    )

                    # ------------------------------------------------
                    # COUNT ELIGIBILITY
                    # ------------------------------------------------

                    if row["eligibility_status"] == "ELIGIBLE":

                        eligible_count += 1

                    elif row["eligibility_status"] == "PENDING":

                        pending_count += 1

                    else:

                        not_eligible_count += 1

                print()
                print("=" * 80)
                print("                 ELIGIBILITY SUMMARY")
                print("=" * 80)

                print(
                    f"Total Records     : {len(rows)}"
                )

                print(
                    f"Eligible           : {eligible_count}"
                )

                print(
                    f"Pending            : {pending_count}"
                )

                print(
                    f"Not Eligible       : "
                    f"{not_eligible_count}"
                )

                print("=" * 80)

            finally:

                cursor.close()

    except Exception as e:

        print(
            "❌ Database error:",
            e
        )


# ============================================================
# 23. MAIN MENU
# ============================================================

def main():

    while True:

        print("\n")

        print("=" * 65)

        print(
            "                    PATIENT CONNECT"
        )

        print(
            "             USA HEALTHCARE MANAGEMENT"
        )

        print("=" * 65)

        print("1.  Create Patient")
        print("2.  View Patients")
        print("3.  Search Patient")
        print("4.  View Clinics")
        print("5.  View Providers")
        print("6.  View Appointments")
        print("7.  Book Appointment")
        print("8.  Update Appointment Status")
        print("9.  View Messages")
        print("10. Clinic Appointment Count")
        print("11. Recall Candidates")
        print("12. Due Reminders")
        print("13. Export Patients to CSV")
        print("14. View Conditions")
        print("15. View Patient Conditions")
        print("16. View Appointment Status History")
        print("17. Patient Appointment History")
        print("18. Provider Appointment Count")
        print("19. Appointment Status Summary")
        print("20. Message Delivery Summary")
        print("21. No-show Report")
        print("22. USA Insurance Eligibility List")
        print("23. Exit")

        print("=" * 65)

        choice = input(
            "Select an option: "
        ).strip()

        # ====================================================
        # MENU HANDLING
        # ====================================================

        if choice == "1":

            create_patient()

        elif choice == "2":

            view_patients()

        elif choice == "3":

            search_patient()

        elif choice == "4":

            view_clinics()

        elif choice == "5":

            view_providers()

        elif choice == "6":

            view_appointments()

        elif choice == "7":

            book_appointment()

        elif choice == "8":

            update_appointment_status()

        elif choice == "9":

            view_messages()

        elif choice == "10":

            clinic_appointment_count()

        elif choice == "11":

            recall_candidates()

        elif choice == "12":

            due_reminders()

        elif choice == "13":

            export_patients_csv()

        elif choice == "14":

            view_conditions()

        elif choice == "15":

            view_patient_conditions()

        elif choice == "16":

            view_appointment_history()

        elif choice == "17":

            patient_appointment_history()

        elif choice == "18":

            provider_appointment_count()

        elif choice == "19":

            appointment_status_summary()

        elif choice == "20":

            message_delivery_summary()

        elif choice == "21":

            no_show_report()

        elif choice == "22":

            view_eligibility_list()

        elif choice == "23":

            print()
            print(
                "Thank you for using Patient Connect."
            )

            break

        else:

            print(
                "\n❌ Invalid option. "
                "Please select 1-23."
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    main()
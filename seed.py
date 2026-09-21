import random
from datetime import datetime, timedelta

from faker import Faker

from db import get_connection


fake = Faker()


def clear_data():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

            cursor.execute("TRUNCATE TABLE messages")
            cursor.execute("TRUNCATE TABLE appointment_status_history")
            cursor.execute("TRUNCATE TABLE appointments")
            cursor.execute("TRUNCATE TABLE patient_conditions")
            cursor.execute("TRUNCATE TABLE conditions")
            cursor.execute("TRUNCATE TABLE patients")
            cursor.execute("TRUNCATE TABLE providers")
            cursor.execute("TRUNCATE TABLE clinics")

            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

            conn.commit()

            print("Old sample data cleared.")

        finally:
            cursor.close()


def seed_clinics():
    rows = [
        (
            "CityCare Clinic",
            "100 Main St, Austin, TX",
            "(555) 100-1111",
            "hello@citycare.com"
        ),
        (
            "Northside Family Health",
            "250 Oak Ave, Chicago, IL",
            "(555) 200-2222",
            "care@northsidehealth.com"
        ),
        (
            "Sunrise Medical Group",
            "88 Harbor Blvd, Miami, FL",
            "(555) 300-3333",
            "info@sunrisemed.com"
        )
    ]

    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.executemany(
                """
                INSERT INTO clinics
                (clinic_name, address, phone, email)
                VALUES (%s, %s, %s, %s)
                """,
                rows
            )

            conn.commit()

            print("Clinics seeded.")

        finally:
            cursor.close()


def seed_providers():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT clinic_id FROM clinics"
            )

            clinics = [row[0] for row in cursor.fetchall()]

            rows = []

            specialties = [
                "Cardiology",
                "Dermatology",
                "Family Medicine",
                "Orthopedics",
                "Pediatrics"
            ]

            for clinic_id in clinics:

                for _ in range(3):

                    rows.append(
                        (
                            clinic_id,
                            fake.name(),
                            random.choice(specialties),
                            fake.email(),
                            fake.phone_number()
                        )
                    )

            cursor.executemany(
                """
                INSERT INTO providers
                (
                    clinic_id,
                    provider_name,
                    specialty,
                    email,
                    phone
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                rows
            )

            conn.commit()

            print("Providers seeded.")

        finally:
            cursor.close()


def seed_patients():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT clinic_id FROM clinics"
            )

            clinics = [row[0] for row in cursor.fetchall()]

            rows = []

            for clinic_id in clinics:

                for _ in range(12):

                    rows.append(
                        (
                            clinic_id,
                            fake.first_name(),
                            fake.last_name(),
                            fake.email(),
                            fake.phone_number(),
                            fake.date_of_birth(
                                minimum_age=18,
                                maximum_age=80
                            ).strftime("%Y-%m-%d"),
                            random.choice(
                                ["M", "F", "Other"]
                            )
                        )
                    )

            cursor.executemany(
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
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                rows
            )

            conn.commit()

            print("Patients seeded.")

        finally:
            cursor.close()


def seed_conditions():
    rows = [
        ("Diabetes",),
        ("Hypertension",),
        ("Asthma",),
        ("Arthritis",),
        ("COPD",)
    ]

    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.executemany(
                """
                INSERT INTO conditions
                (condition_name)
                VALUES (%s)
                """,
                rows
            )

            conn.commit()

            print("Conditions seeded.")

        finally:
            cursor.close()


def seed_patient_conditions():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT patient_id FROM patients"
            )

            patients = [
                row[0]
                for row in cursor.fetchall()
            ]

            cursor.execute(
                "SELECT condition_id FROM conditions"
            )

            conditions = [
                row[0]
                for row in cursor.fetchall()
            ]

            rows = []

            for patient_id in patients:

                selected = random.sample(
                    conditions,
                    random.randint(1, 2)
                )

                for condition_id in selected:
                    rows.append(
                        (
                            patient_id,
                            condition_id
                        )
                    )

            cursor.executemany(
                """
                INSERT INTO patient_conditions
                (patient_id, condition_id)
                VALUES (%s, %s)
                """,
                rows
            )

            conn.commit()

            print("Patient conditions seeded.")

        finally:
            cursor.close()


def seed_appointments():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT patient_id FROM patients"
            )

            patients = [
                row[0]
                for row in cursor.fetchall()
            ]

            cursor.execute(
                """
                SELECT provider_id, clinic_id
                FROM providers
                """
            )

            providers = cursor.fetchall()

            rows = []

            statuses = [
                "scheduled",
                "confirmed",
                "completed",
                "cancelled",
                "no_show"
            ]

            reasons = [
                "Follow-up",
                "Consultation",
                "Checkup",
                "Medication review"
            ]

            for _ in range(80):

                patient_id = random.choice(patients)

                provider_id, clinic_id = random.choice(
                    providers
                )

                scheduled_at = (
                    datetime.now()
                    + timedelta(
                        days=random.randint(-120, 60),
                        hours=random.randint(0, 23)
                    )
                )

                rows.append(
                    (
                        patient_id,
                        provider_id,
                        clinic_id,
                        scheduled_at.strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        random.choice(statuses),
                        random.choice(reasons)
                    )
                )

            cursor.executemany(
                """
                INSERT INTO appointments
                (
                    patient_id,
                    provider_id,
                    clinic_id,
                    scheduled_at,
                    status,
                    reason
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                rows
            )

            conn.commit()

            print("Appointments seeded.")

        finally:
            cursor.close()


def seed_history():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT appointment_id, status
                FROM appointments
                """
            )

            appointments = cursor.fetchall()

            rows = []

            for appointment_id, status in appointments:

                rows.append(
                    (
                        appointment_id,
                        None,
                        status,
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                        "Initial status"
                    )
                )

            cursor.executemany(
                """
                INSERT INTO appointment_status_history
                (
                    appointment_id,
                    old_status,
                    new_status,
                    changed_at,
                    note
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                rows
            )

            conn.commit()

            print("Appointment history seeded.")

        finally:
            cursor.close()


def seed_messages():
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT appointment_id, patient_id
                FROM appointments
                """
            )

            appointments = cursor.fetchall()

            rows = []

            for appointment_id, patient_id in appointments:

                channel = random.choice(
                    ["sms", "email", "voice"]
                )

                message_type = random.choice(
                    [
                        "reminder",
                        "confirmation",
                        "follow_up"
                    ]
                )

                status = random.choice(
                    [
                        "sent",
                        "delivered",
                        "failed",
                        "opened"
                    ]
                )

                sent_at = (
                    datetime.now()
                    - timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(1, 24)
                    )
                ).strftime("%Y-%m-%d %H:%M:%S")

                delivered_at = None

                if status in ("delivered", "opened"):
                    delivered_at = sent_at

                rows.append(
                    (
                        patient_id,
                        appointment_id,
                        message_type,
                        channel,
                        status,
                        "Sample message content",
                        sent_at,
                        delivered_at,
                        None
                    )
                )

            cursor.executemany(
                """
                INSERT INTO messages
                (
                    patient_id,
                    appointment_id,
                    message_type,
                    channel,
                    status,
                    content,
                    sent_at,
                    delivered_at,
                    response_at
                )
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                rows
            )

            conn.commit()

            print("Messages seeded.")

        finally:
            cursor.close()


def main():
    print("\n========================================")
    print("       PATIENT CONNECT SEEDING")
    print("========================================\n")

    clear_data()

    seed_clinics()
    seed_providers()
    seed_patients()
    seed_conditions()
    seed_patient_conditions()
    seed_appointments()
    seed_history()
    seed_messages()

    print("\n========================================")
    print("Sample data loaded successfully.")
    print("========================================")


if __name__ == "__main__":
    main()
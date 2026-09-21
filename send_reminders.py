import random
from datetime import datetime
from db import get_connection

DELIVERY_RATES = {
    "sms": 0.93,
    "email": 0.90,
    "voice": 0.95
}


def get_due_reminders(hours_ahead):
    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.callproc("sp_due_reminders", (hours_ahead,))

            reminders = []

            for result in cursor.stored_results():
                reminders.extend(result.fetchall())

            return reminders

        finally:
            cursor.close()


def send_reminder(patient_id, appointment_id, channel, content):
    success_rate = DELIVERY_RATES.get(channel, 0.90)

    sent_at = datetime.now()

    if random.random() <= success_rate:
        status = "delivered"
        delivered_at = datetime.now()
    else:
        status = "failed"
        delivered_at = None

    with get_connection() as conn:
        cursor = conn.cursor()

        try:
            cursor.execute(
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
                    delivered_at
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
                    %s
                )
                """,
                (
                    patient_id,
                    appointment_id,
                    "reminder",
                    channel,
                    status,
                    content,
                    sent_at,
                    delivered_at
                )
            )

            conn.commit()

        finally:
            cursor.close()

    return status


def process_reminders(hours_ahead):
    print()
    print("==============================================")
    print("       PATIENT CONNECT REMINDER ENGINE")
    print("==============================================")

    print()
    print(
        "Checking appointments in next",
        hours_ahead,
        "hours..."
    )

    reminders = get_due_reminders(hours_ahead)

    if not reminders:
        print()
        print("No reminders are due.")
        return

    print()
    print("Found", len(reminders), "appointment(s).")

    for row in reminders:
        appointment_id = row[0]
        patient_id = row[1]
        patient_name = row[2]
        provider_id = row[3]
        scheduled_at = row[4]
        reason = row[5]

        channel = random.choice(
            ["sms", "email", "voice"]
        )

        content = (
            "Reminder: "
            + str(patient_name)
            + ", your appointment is scheduled for "
            + str(scheduled_at)
            + ". Reason: "
            + str(reason)
        )

        status = send_reminder(
            patient_id,
            appointment_id,
            channel,
            content
        )

        print()
        print("----------------------------------------------")
        print("Appointment ID:", appointment_id)
        print("Patient ID:", patient_id)
        print("Patient:", patient_name)
        print("Provider ID:", provider_id)
        print("Date:", scheduled_at)
        print("Reason:", reason)
        print("Channel:", channel)
        print("Status:", status)

    print()
    print("==============================================")
    print("       REMINDER PROCESSING COMPLETED")
    print("==============================================")


def main():
    print()
    print("==============================================")
    print("          PATIENT CONNECT")
    print("          REMINDER SYSTEM")
    print("==============================================")

    try:
        value = input(
            "Enter hours ahead (default 48): "
        ).strip()

        if value == "":
            hours_ahead = 48
        else:
            hours_ahead = int(value)

        if hours_ahead <= 0:
            print("Hours must be greater than zero.")
            return

        process_reminders(hours_ahead)

    except ValueError:
        print("Please enter a valid number.")

    except Exception as error:
        print("Reminder engine error:", error)


if __name__ == "__main__":
    main()
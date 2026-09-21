from db import get_connection

def reset_database():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        print("Dropping existing tables...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in [
            "messages",
            "appointment_status_history",
            "appointments",
            "patient_conditions",
            "conditions",
            "providers",
            "patients",
            "clinics",
        ]:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
            except Exception as e:
                print(f"Could not drop {table}: {e}")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print("Reset complete.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    reset_database()
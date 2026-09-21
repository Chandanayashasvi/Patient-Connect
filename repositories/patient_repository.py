import csv
from db import get_connection

class PatientRepository:
    def create_patient(self, data):
        sql = """
            INSERT INTO patients (clinic_id, first_name, last_name, email, phone, date_of_birth, gender)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (
                    data.get("clinic_id"),
                    data.get("first_name"),
                    data.get("last_name"),
                    data.get("email"),
                    data.get("phone"),
                    data.get("date_of_birth"),
                    data.get("gender"),
                ))
                conn.commit()
                return cursor.lastrowid
            finally:
                cursor.close()

    def get_all_patients(self):
        sql = "SELECT * FROM patients ORDER BY patient_id"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql)
                return cursor.fetchall()
            finally:
                cursor.close()

    def get_patient_by_id(self, patient_id):
        sql = "SELECT * FROM patients WHERE patient_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql, (patient_id,))
                rows = cursor.fetchall()
                return rows[0] if rows else None
            finally:
                cursor.close()

    def update_patient(self, patient_id, data):
        fields = []
        params = []
        for key, value in data.items():
            if value is not None:
                fields.append(f"{key} = %s")
                params.append(value)
        if not fields:
            return False

        params.append(patient_id)
        sql = f"UPDATE patients SET {', '.join(fields)} WHERE patient_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, tuple(params))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()

    def delete_patient(self, patient_id):
        sql = "DELETE FROM patients WHERE patient_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (patient_id,))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
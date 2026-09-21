from db import get_connection

class ClinicRepository:
    def create_clinic(self, data):
        sql = """
            INSERT INTO clinics (clinic_name, address, phone, email)
            VALUES (%s, %s, %s, %s)
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (
                    data.get("clinic_name"),
                    data.get("address"),
                    data.get("phone"),
                    data.get("email"),
                ))
                conn.commit()
                return cursor.lastrowid
            finally:
                cursor.close()

    def get_all_clinics(self):
        sql = "SELECT * FROM clinics ORDER BY clinic_id"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql)
                return cursor.fetchall()
            finally:
                cursor.close()

    def get_clinic_by_id(self, clinic_id):
        sql = "SELECT * FROM clinics WHERE clinic_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql, (clinic_id,))
                rows = cursor.fetchall()
                return rows[0] if rows else None
            finally:
                cursor.close()

    def update_clinic(self, clinic_id, data):
        fields = []
        params = []

        for key, value in data.items():
            if value is not None:
                fields.append(f"{key} = %s")
                params.append(value)

        if not fields:
            return False

        params.append(clinic_id)
        sql = f"UPDATE clinics SET {', '.join(fields)} WHERE clinic_id = %s"

        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, tuple(params))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()

    def delete_clinic(self, clinic_id):
        sql = "DELETE FROM clinics WHERE clinic_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (clinic_id,))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
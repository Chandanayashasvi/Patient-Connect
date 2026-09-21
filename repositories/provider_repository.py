from db import get_connection

class ProviderRepository:
    def create_provider(self, data):
        sql = """
            INSERT INTO providers (clinic_id, provider_name, specialty, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (
                    data.get("clinic_id"),
                    data.get("provider_name"),
                    data.get("specialty"),
                    data.get("email"),
                    data.get("phone"),
                ))
                conn.commit()
                return cursor.lastrowid
            finally:
                cursor.close()

    def get_all_providers(self):
        sql = "SELECT * FROM providers ORDER BY provider_id"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql)
                return cursor.fetchall()
            finally:
                cursor.close()

    def get_provider_by_id(self, provider_id):
        sql = "SELECT * FROM providers WHERE provider_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(sql, (provider_id,))
                rows = cursor.fetchall()
                return rows[0] if rows else None
            finally:
                cursor.close()

    def update_provider(self, provider_id, data):
        fields = []
        params = []
        for key, value in data.items():
            if value is not None:
                fields.append(f"{key} = %s")
                params.append(value)
        if not fields:
            return False

        params.append(provider_id)
        sql = f"UPDATE providers SET {', '.join(fields)} WHERE provider_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, tuple(params))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()

    def delete_provider(self, provider_id):
        sql = "DELETE FROM providers WHERE provider_id = %s"
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (provider_id,))
                conn.commit()
                return cursor.rowcount > 0
            finally:
                cursor.close()
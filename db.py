import os
from contextlib import contextmanager
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_db_config():
    return {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", "patientconnect"),
        "port": int(os.getenv("MYSQL_PORT", "3306"))
    }


@contextmanager
def get_connection():
    conn = None

    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        yield conn

    except mysql.connector.Error as e:
        print("❌ Database connection failed:", e)
        raise

    finally:
        if conn is not None and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    try:
        with get_connection() as conn:
            print("Database connection OK:", conn.database)
    except Exception:
        pass
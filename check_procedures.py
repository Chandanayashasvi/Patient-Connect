import mysql.connector
from db import get_db_config

config = get_db_config()

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

cursor.execute(
    "SHOW PROCEDURE STATUS WHERE Db = 'patientconnect'"
)

procedures = cursor.fetchall()

print("\n========== STORED PROCEDURES ==========\n")

if not procedures:
    print("❌ NO STORED PROCEDURES FOUND")

else:
    for row in procedures:
        print("✅", row[1])

print("\n========================================")

cursor.close()
conn.close()
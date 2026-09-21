import mysql.connector
from db import get_db_config


def execute_sql_file(cursor, filename):
    print(f"\nRunning {filename}...")

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()

    # Remove DELIMITER commands.
    sql = sql.replace("DELIMITER $$", "")
    sql = sql.replace("DELIMITER ;", "")

    # Procedures end with $$.
    if "CREATE PROCEDURE" in sql.upper():

        statements = sql.split("$$")

    else:

        statements = sql.split(";")

    for statement in statements:

        statement = statement.strip()

        if not statement:
            continue

        try:

            cursor.execute(statement)

        except mysql.connector.Error as e:

            print(f"\n❌ Error in {filename}:")
            print(e)

            print("\nSQL:")
            print(statement)

            raise


def main():

    config = get_db_config()

    # Connect WITHOUT selecting patientconnect
    config_without_database = config.copy()
    config_without_database.pop("database", None)

    print("Connecting to MySQL...")

    conn = mysql.connector.connect(
        **config_without_database
    )

    cursor = conn.cursor()

    try:

        # ------------------------------------------------
        # Schema
        # ------------------------------------------------

        execute_sql_file(
            cursor,
            "schema.sql"
        )

        conn.commit()

        print("✅ Schema created successfully.")


        # ------------------------------------------------
        # Reconnect to new database
        # ------------------------------------------------

        cursor.close()
        conn.close()

        conn = mysql.connector.connect(
            **config
        )

        cursor = conn.cursor()


        # ------------------------------------------------
        # Stored Procedures
        # ------------------------------------------------

        execute_sql_file(
            cursor,
            "procedures.sql"
        )

        conn.commit()

        print("✅ Stored procedures created successfully.")

        print("\n====================================")
        print("DATABASE SETUP COMPLETED")
        print("====================================")


    finally:

        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
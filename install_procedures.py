import mysql.connector
from db import get_db_config

def clear_results(cursor):
    try:
        while cursor.nextset():
            pass
    except Exception:
        pass

def main():
    config = get_db_config()

    print("========================================")
    print("   INSTALLING STORED PROCEDURES")
    print("========================================")

    try:
        with open("procedures.sql", "r", encoding="utf-8") as file:
            sql = file.read()
    except FileNotFoundError:
        print("ERROR: procedures.sql not found")
        return

    # Remove DELIMITER commands
    sql = sql.replace("DELIMITER $$", "")
    sql = sql.replace("DELIMITER ;", "")

    # Remove SQL comment lines
    lines = []
    for line in sql.splitlines():
        if not line.strip().startswith("--"):
            lines.append(line)
    sql = "\n".join(lines)

    # Split procedures using $$
    procedures = sql.split("$$")
    count = 0

    for procedure in procedures:
        procedure = procedure.strip()
        if not procedure:
            continue
        if "CREATE PROCEDURE" not in procedure.upper():
            continue

        count += 1
        print()
        print("----------------------------------------")
        print("Creating procedure", count)
        print("----------------------------------------")

        conn = None
        cursor = None

        try:
            # New connection for every procedure
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Remove final semicolon if present
            procedure = procedure.rstrip(";").strip()

            cursor.execute(procedure)

            # Clear pending MySQL results
            clear_results(cursor)

            # CREATE PROCEDURE is DDL — no commit needed
            print("SUCCESS: Procedure created")

        except mysql.connector.Error as error:
            print("ERROR creating procedure:")
            print(error)

        finally:
            if cursor is not None:
                try:
                    clear_results(cursor)
                except Exception:
                    pass
                try:
                    cursor.close()
                except Exception:
                    pass

            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    print()
    print("========================================")
    print("INSTALLATION FINISHED")
    print("Procedures found:", count)
    print("========================================")


if __name__ == "__main__":
    main()

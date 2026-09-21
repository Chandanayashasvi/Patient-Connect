import csv
from db import get_connection

def call_procedure(proc_name, args):
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.callproc(proc_name, args)
            for result in cursor.stored_results():
                rows = result.fetchall()
                columns = [column[0] for column in result.description]
                return rows, columns
            return [], []
        finally:
            cursor.close()

def export_csv(filename, rows, columns):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

def main():
    rows, columns = call_procedure("sp_recall_candidates", (1, 6))
    if rows:
        export_csv("recall_candidates.csv", rows, columns)
        print("Recall candidates exported to recall_candidates.csv")
        for row in rows[:5]:
            print(row)

    rows, columns = call_procedure("sp_due_reminders", (48,))
    if rows:
        export_csv("due_reminders.csv", rows, columns)
        print("Due reminders exported to due_reminders.csv")
        for row in rows[:5]:
            print(row)

if __name__ == "__main__":
    main()
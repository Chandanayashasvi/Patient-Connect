import mysql.connector
from openpyxl import Workbook
from db import get_db_config

EXCEL_FILE = "PatientConnect_Patients.xlsx"

def sync_patients_to_excel():
    conn = None
    cursor = None
    try:
        config = get_db_config()
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                patient_id,
                clinic_id,
                first_name,
                last_name,
                email,
                phone,
                date_of_birth,
                gender
            FROM patients
            ORDER BY patient_id
        """)

        patients = cursor.fetchall()
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Patients"

        headers = [
            "Patient ID",
            "Clinic ID",
            "First Name",
            "Last Name",
            "Email",
            "Phone",
            "Date of Birth",
            "Gender"
        ]
        sheet.append(headers)

        for patient in patients:
            sheet.append([
                patient["patient_id"],
                patient["clinic_id"],
                patient["first_name"],
                patient["last_name"],
                patient["email"],
                patient["phone"],
                patient["date_of_birth"],
                patient["gender"]
            ])

        # Freeze header row
        sheet.freeze_panes = "A2"

        # Adjust column widths
        for column in sheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                if cell.value is not None:
                    max_length = max(max_length, len(str(cell.value)))
            sheet.column_dimensions[column_letter].width = min(max_length + 2, 30)

        # Information sheet
        info = workbook.create_sheet("Export Info")
        info["A1"] = "PatientConnect"
        info["A2"] = "Confidential Patient Information"
        info["A3"] = "Source"
        info["B3"] = "PatientConnect MySQL Database"
        info["A4"] = "Patient Count"
        info["B4"] = len(patients)

        workbook.save(EXCEL_FILE)

        print("\n========================================")
        print("          EXCEL SYNC")
        print("========================================")
        print("Patients exported:", len(patients))
        print("Excel file:", EXCEL_FILE)
        print("Status: SUCCESS")
        print("========================================")

    except mysql.connector.Error as error:
        print("❌ Database error:", error)
    except Exception as error:
        print("❌ Excel sync error:", error)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    sync_patients_to_excel()

import re
from datetime import datetime
from repositories.patient_repository import PatientRepository

class PatientService:
    def __init__(self):
        self.repo = PatientRepository()

    def validate_email(self, email):
        if email is None or str(email).strip() == "":
            return
        if not re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", str(email)):
            raise ValueError("Invalid email format.")

    def validate_phone(self, phone):
        if phone is None or str(phone).strip() == "":
            return
        digits = re.sub(r"[^0-9]", "", str(phone))
        if len(digits) < 7:
            raise ValueError("Invalid phone number.")

    def validate_date(self, value):
        if value is None or str(value).strip() == "":
            return
        try:
            datetime.strptime(str(value), "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Date must be in YYYY-MM-DD format.") from exc

    def create_patient(self, data):
        if not data.get("first_name") or str(data.get("first_name")).strip() == "":
            raise ValueError("First name is required.")
        if not data.get("last_name") or str(data.get("last_name")).strip() == "":
            raise ValueError("Last name is required.")
        if "email" in data and data["email"]:
            self.validate_email(data["email"])
        if "phone" in data and data["phone"]:
            self.validate_phone(data["phone"])
        if "date_of_birth" in data and data["date_of_birth"]:
            self.validate_date(data["date_of_birth"])

        return self.repo.create_patient(data)

    def get_all_patients(self):
        return self.repo.get_all_patients()

    def update_patient(self, patient_id, data):
        if patient_id <= 0:
            raise ValueError("Patient ID must be positive.")
        if "email" in data and data["email"]:
            self.validate_email(data["email"])
        if "phone" in data and data["phone"]:
            self.validate_phone(data["phone"])
        if "date_of_birth" in data and data["date_of_birth"]:
            self.validate_date(data["date_of_birth"])
        return self.repo.update_patient(patient_id, data)

    def delete_patient(self, patient_id):
        if patient_id <= 0:
            raise ValueError("Patient ID must be positive.")
        return self.repo.delete_patient(patient_id)
import re
from repositories.clinic_repository import ClinicRepository

class ClinicService:
    def __init__(self):
        self.repo = ClinicRepository()

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

    def create_clinic(self, data):
        if not data.get("clinic_name") or str(data.get("clinic_name")).strip() == "":
            raise ValueError("Clinic name is required.")

        if "email" in data and data["email"]:
            self.validate_email(data["email"])
        if "phone" in data and data["phone"]:
            self.validate_phone(data["phone"])

        return self.repo.create_clinic(data)

    def get_all_clinics(self):
        return self.repo.get_all_clinics()

    def update_clinic(self, clinic_id, data):
        if clinic_id <= 0:
            raise ValueError("Clinic ID must be positive.")

        if "email" in data and data["email"]:
            self.validate_email(data["email"])
        if "phone" in data and data["phone"]:
            self.validate_phone(data["phone"])

        return self.repo.update_clinic(clinic_id, data)

    def delete_clinic(self, clinic_id):
        if clinic_id <= 0:
            raise ValueError("Clinic ID must be positive.")
        return self.repo.delete_clinic(clinic_id)
import re
from repositories.provider_repository import ProviderRepository

class ProviderService:
    def __init__(self):
        self.repo = ProviderRepository()

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

    def create_provider(self, data):
        if not data.get("provider_name") or str(data.get("provider_name")).strip() == "":
            raise ValueError("Provider name is required.")
        if "email" in data and data["email"]:
            self.validate_email(data["email"])
        if "phone" in data and data["phone"]:
            self.validate_phone(data["phone"])
        return self.repo.create_provider(data)

    def get_all_providers(self):
        return self.repo.get_all_providers()

    def update_provider(self, provider_id, data):
        if provider_id <= 0:
            raise ValueError("Provider ID must be positive.")
        if "email" in data and data["email"]:
            self.validate_email(data["email"])
        if "phone" in data and data["phone"]:
            self.validate_phone(data["phone"])
        return self.repo.update_provider(provider_id, data)

    def delete_provider(self, provider_id):
        if provider_id <= 0:
            raise ValueError("Provider ID must be positive.")
        return self.repo.delete_provider(provider_id)
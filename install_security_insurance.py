import mysql.connector
from db import get_db_config


def main():

    config = get_db_config()

    conn = None
    cursor = None

    try:

        print("========================================")
        print("   PATIENT CONNECT SECURITY + INSURANCE")
        print("========================================")

        conn = mysql.connector.connect(**config)

        cursor = conn.cursor()

        # ====================================================
        # 1. USERS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,

                username VARCHAR(50) NOT NULL UNIQUE,

                password_hash VARCHAR(255) NOT NULL,

                role ENUM(
                    'ADMIN',
                    'DOCTOR',
                    'STAFF'
                ) NOT NULL,

                active BOOLEAN DEFAULT TRUE,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        print("✅ Users table ready.")

        # ====================================================
        # 2. PATIENT INSURANCE
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patient_insurance (
                insurance_id INT AUTO_INCREMENT PRIMARY KEY,

                patient_id INT NOT NULL,

                insurance_provider VARCHAR(150) NOT NULL,

                member_id VARCHAR(100) NOT NULL,

                group_number VARCHAR(100),

                plan_name VARCHAR(100),

                policy_holder_name VARCHAR(150),

                relationship_to_policy_holder VARCHAR(50),

                insurance_status ENUM(
                    'ACTIVE',
                    'INACTIVE',
                    'EXPIRED',
                    'PENDING'
                ) DEFAULT 'PENDING',

                effective_date DATE,

                expiration_date DATE,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,

                CONSTRAINT fk_patient_insurance_patient
                    FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id)
                    ON DELETE CASCADE
            )
        """)

        print("✅ Patient insurance table ready.")

        # ====================================================
        # 3. INSURANCE ELIGIBILITY
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insurance_eligibility (
                eligibility_id INT AUTO_INCREMENT PRIMARY KEY,

                insurance_id INT NOT NULL,

                checked_by INT NULL,

                eligibility_status ENUM(
                    'ELIGIBLE',
                    'NOT_ELIGIBLE',
                    'PENDING'
                ) NOT NULL,

                checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                response_message VARCHAR(255),

                CONSTRAINT fk_eligibility_insurance
                    FOREIGN KEY (insurance_id)
                    REFERENCES patient_insurance(insurance_id)
                    ON DELETE CASCADE
            )
        """)

        print("✅ Insurance eligibility table ready.")

        # ====================================================
        # 4. INSURANCE CLAIMS
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS insurance_claims (
                claim_id INT AUTO_INCREMENT PRIMARY KEY,

                patient_id INT NOT NULL,

                insurance_id INT NOT NULL,

                appointment_id INT NULL,

                claim_number VARCHAR(100) UNIQUE,

                claim_status ENUM(
                    'DRAFT',
                    'SUBMITTED',
                    'PROCESSING',
                    'APPROVED',
                    'DENIED'
                ) DEFAULT 'DRAFT',

                claim_amount DECIMAL(10,2) DEFAULT 0.00,

                submitted_at DATETIME NULL,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,

                CONSTRAINT fk_claim_patient
                    FOREIGN KEY (patient_id)
                    REFERENCES patients(patient_id)
                    ON DELETE CASCADE,

                CONSTRAINT fk_claim_insurance
                    FOREIGN KEY (insurance_id)
                    REFERENCES patient_insurance(insurance_id)
                    ON DELETE CASCADE,

                CONSTRAINT fk_claim_appointment
                    FOREIGN KEY (appointment_id)
                    REFERENCES appointments(appointment_id)
                    ON DELETE SET NULL
            )
        """)

        print("✅ Insurance claims table ready.")

        # ====================================================
        # 5. AUDIT LOG
        # ====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                audit_id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NULL,

                action VARCHAR(100) NOT NULL,

                table_name VARCHAR(100),

                record_id INT NULL,

                details VARCHAR(500),

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                CONSTRAINT fk_audit_user
                    FOREIGN KEY (user_id)
                    REFERENCES users(user_id)
                    ON DELETE SET NULL
            )
        """)

        print("✅ Audit logs table ready.")

        conn.commit()

        print()
        print("========================================")
        print("          INSTALLATION COMPLETE")
        print("========================================")
        print()
        print("Roles:")
        print("  ADMIN")
        print("  DOCTOR")
        print("  STAFF")
        print()
        print("Healthcare features:")
        print("  Insurance")
        print("  Eligibility")
        print("  Claims")
        print("  Audit Logs")
        print()
        print("========================================")

    except mysql.connector.Error as error:

        print()
        print("❌ DATABASE ERROR:")
        print(error)

        if conn is not None:
            try:
                conn.rollback()
            except Exception:
                pass

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()
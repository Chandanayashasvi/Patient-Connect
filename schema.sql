```sql
-- ============================================================
-- PATIENT CONNECT
-- COMPLETE DATABASE SCHEMA
-- USA HEALTHCARE VERSION
-- ============================================================

-- ============================================================
-- RESET DATABASE
-- ============================================================

DROP DATABASE IF EXISTS patientconnect;

CREATE DATABASE patientconnect;

USE patientconnect;


-- ============================================================
-- 1. CLINICS
-- ============================================================

CREATE TABLE clinics (

    clinic_id INT PRIMARY KEY AUTO_INCREMENT,

    clinic_name VARCHAR(150) NOT NULL,

    address VARCHAR(255),

    phone VARCHAR(50),

    email VARCHAR(150)
);


-- ============================================================
-- 2. PROVIDERS
-- ============================================================

CREATE TABLE providers (

    provider_id INT PRIMARY KEY AUTO_INCREMENT,

    clinic_id INT NOT NULL,

    provider_name VARCHAR(150) NOT NULL,

    specialty VARCHAR(150),

    email VARCHAR(150),

    phone VARCHAR(50),

    CONSTRAINT fk_providers_clinic
        FOREIGN KEY (clinic_id)
        REFERENCES clinics(clinic_id)
);


-- ============================================================
-- 3. PATIENTS
-- ============================================================

CREATE TABLE patients (

    patient_id INT PRIMARY KEY AUTO_INCREMENT,

    clinic_id INT NOT NULL,

    first_name VARCHAR(100) NOT NULL,

    last_name VARCHAR(100) NOT NULL,

    email VARCHAR(150),

    phone VARCHAR(50),

    date_of_birth DATE,

    gender ENUM(
        'M',
        'F',
        'Other',
        'Unknown'
    ),

    CONSTRAINT fk_patients_clinic
        FOREIGN KEY (clinic_id)
        REFERENCES clinics(clinic_id)
);


-- ============================================================
-- 4. PATIENT INSURANCE
-- USA HEALTHCARE INSURANCE
-- ============================================================

CREATE TABLE patient_insurance (

    insurance_id INT PRIMARY KEY AUTO_INCREMENT,

    patient_id INT NOT NULL,

    -- USA insurance category
    insurance_type ENUM(
        'MEDICARE',
        'MEDICAID',
        'PRIVATE'
    ) NOT NULL DEFAULT 'PRIVATE',

    -- Insurance company/program
    insurance_provider VARCHAR(150) NOT NULL,

    -- Member identification number
    member_id VARCHAR(100) NOT NULL,

    -- Employer/group plan number
    group_number VARCHAR(100),

    -- Insurance plan
    plan_name VARCHAR(150),

    -- Person responsible for policy
    policy_holder_name VARCHAR(150),

    -- SELF / SPOUSE / CHILD / OTHER
    relationship_to_policy_holder VARCHAR(50),

    -- Current insurance state
    insurance_status ENUM(
        'ACTIVE',
        'INACTIVE',
        'EXPIRED',
        'PENDING'
    ) NOT NULL DEFAULT 'PENDING',

    -- Coverage dates
    effective_date DATE,

    expiration_date DATE,

    CONSTRAINT fk_insurance_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 5. CONDITIONS
-- ============================================================

CREATE TABLE conditions (

    condition_id INT PRIMARY KEY AUTO_INCREMENT,

    condition_name VARCHAR(150) NOT NULL
);


-- ============================================================
-- 6. PATIENT CONDITIONS
-- ============================================================

CREATE TABLE patient_conditions (

    patient_id INT NOT NULL,

    condition_id INT NOT NULL,

    PRIMARY KEY (
        patient_id,
        condition_id
    ),

    CONSTRAINT fk_pc_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_pc_condition
        FOREIGN KEY (condition_id)
        REFERENCES conditions(condition_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 7. APPOINTMENTS
-- ============================================================

CREATE TABLE appointments (

    appointment_id INT PRIMARY KEY AUTO_INCREMENT,

    patient_id INT NOT NULL,

    provider_id INT NOT NULL,

    clinic_id INT NOT NULL,

    scheduled_at DATETIME NOT NULL,

    status ENUM(
        'scheduled',
        'confirmed',
        'completed',
        'cancelled',
        'no_show',
        'rescheduled'
    ) NOT NULL DEFAULT 'scheduled',

    reason VARCHAR(255),

    CONSTRAINT fk_appointments_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_appointments_provider
        FOREIGN KEY (provider_id)
        REFERENCES providers(provider_id),

    CONSTRAINT fk_appointments_clinic
        FOREIGN KEY (clinic_id)
        REFERENCES clinics(clinic_id)
);


-- ============================================================
-- 8. APPOINTMENT STATUS HISTORY
-- ============================================================

CREATE TABLE appointment_status_history (

    history_id INT PRIMARY KEY AUTO_INCREMENT,

    appointment_id INT NOT NULL,

    old_status VARCHAR(50),

    new_status VARCHAR(50) NOT NULL,

    changed_at DATETIME
        NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    note VARCHAR(255),

    CONSTRAINT fk_history_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointments(appointment_id)
        ON DELETE CASCADE
);


-- ============================================================
-- 9. MESSAGES
-- ============================================================

CREATE TABLE messages (

    message_id INT PRIMARY KEY AUTO_INCREMENT,

    patient_id INT NOT NULL,

    appointment_id INT,

    message_type ENUM(
        'reminder',
        'confirmation',
        'recall',
        'follow_up',
        'birthday'
    ) NOT NULL,

    channel ENUM(
        'sms',
        'email',
        'voice'
    ) NOT NULL,

    status ENUM(
        'queued',
        'sent',
        'delivered',
        'failed',
        'opened',
        'replied'
    ) NOT NULL DEFAULT 'queued',

    content TEXT,

    sent_at DATETIME,

    delivered_at DATETIME,

    response_at DATETIME,

    CONSTRAINT fk_messages_patient
        FOREIGN KEY (patient_id)
        REFERENCES patients(patient_id),

    CONSTRAINT fk_messages_appointment
        FOREIGN KEY (appointment_id)
        REFERENCES appointments(appointment_id)
);


-- ============================================================
-- 10. CLINIC INDEXES
-- ============================================================

CREATE INDEX idx_clinics_name
ON clinics(clinic_name);


-- ============================================================
-- 11. PROVIDER INDEXES
-- ============================================================

CREATE INDEX idx_providers_clinic
ON providers(clinic_id);

CREATE INDEX idx_providers_name
ON providers(provider_name);


-- ============================================================
-- 12. PATIENT INDEXES
-- ============================================================

CREATE INDEX idx_patients_clinic
ON patients(clinic_id);

CREATE INDEX idx_patients_name
ON patients(first_name, last_name);

CREATE INDEX idx_patients_email
ON patients(email);


-- ============================================================
-- 13. INSURANCE INDEXES
-- ============================================================

CREATE INDEX idx_patient_insurance_patient
ON patient_insurance(patient_id);

CREATE INDEX idx_patient_insurance_type
ON patient_insurance(insurance_type);

CREATE INDEX idx_patient_insurance_status
ON patient_insurance(insurance_status);

CREATE INDEX idx_patient_insurance_dates
ON patient_insurance(
    effective_date,
    expiration_date
);

CREATE INDEX idx_patient_insurance_member
ON patient_insurance(member_id);


-- ============================================================
-- 14. APPOINTMENT INDEXES
-- ============================================================

CREATE INDEX idx_appointments_patient
ON appointments(patient_id);

CREATE INDEX idx_appointments_provider_time
ON appointments(
    provider_id,
    scheduled_at
);

CREATE INDEX idx_appointments_clinic
ON appointments(clinic_id);

CREATE INDEX idx_appointments_status_time
ON appointments(
    status,
    scheduled_at
);


-- ============================================================
-- 15. MESSAGE INDEXES
-- ============================================================

CREATE INDEX idx_messages_patient_status
ON messages(
    patient_id,
    status
);

CREATE INDEX idx_messages_appointment_type
ON messages(
    appointment_id,
    message_type,
    status
);


-- ============================================================
-- 16. PATIENT CONDITION INDEX
-- ============================================================

CREATE INDEX idx_patient_conditions_condition
ON patient_conditions(condition_id);


-- ============================================================
-- SCHEMA COMPLETE
-- ============================================================

SELECT
    'PatientConnect database schema created successfully.'
    AS message;
```

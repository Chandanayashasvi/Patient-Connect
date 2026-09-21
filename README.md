Patient Connect

Backend healthcare communication system for appointment scheduling, automated reminders, recall management, and analytics. Built with Python and MySQL.

Overview

Patient Connect manages the core workflow of a clinic's patient communication pipeline: booking appointments without double-booking, tracking status changes through a full audit trail, sending reminders on a schedule, and generating operational reports (no-show rates, reminder effectiveness, message delivery, status durations).

Tech Stack

Language: Python 3

Database: MySQL 8.0+ (transactions, row locking, stored procedures, window functions)

Python packages:

Package	Purpose
mysql-connector-python	MySQL connectivity
Faker	Synthetic data generation for seeding
python-dotenv	Environment-based configuration
Project Structure
PatientConnect/
├── schema.sql            # Database schema
├── procedures.sql        # Stored procedures
├── queries.sql            # Analytics queries
├── seed.py                # Sample data generator
├── db.py                  # Database connection layer
├── reports.py             # Reporting CLI (with CSV export)
├── send_reminders.py      # Reminder automation engine
├── requirements.txt
├── .env.example
└── README.md
Database Schema

8 relational tables:

Table	Purpose
clinics	Facility information
providers	Doctors / specialists
patients	Patient demographics
conditions	Medical condition reference data
patient_conditions	Patient ↔ condition mapping
appointments	Appointment scheduling
appointment_status_history	Full status audit trail
messages	Communication log

Appointment status flow: Scheduled → Confirmed → Completed / No Show / Cancelled

Stored Procedures
Procedure	Purpose
sp_clinic_appointment_count	Appointment stats per provider
sp_book_appointment	Transaction-safe booking (row locking, prevents double-booking, auto history)
sp_update_appointment_status	Updates status and writes history
sp_recall_candidates	Identifies patients due for follow-up
sp_due_reminders	Returns appointments needing reminders (idempotent)
Reporting
No-show rate: No Shows / (Completed + No Shows), per provider
Reminder effectiveness: outcomes for patients who received reminders vs. those who didn't
Message delivery analytics: total sent, delivered, failed, delivery %
Status duration: average time spent per appointment status, using LEAD() and TIMESTAMPDIFF() window functions
Setup

1. Install dependencies

bash
pip install -r requirements.txt

2. Create the database

bash
mysql -u root -p -e "CREATE DATABASE patientconnect;"

3. Load schema

bash
mysql -u root -p patientconnect < schema.sql

4. Load stored procedures

bash
mysql -u root -p patientconnect < procedures.sql

5. Configure environment

Create a .env file:

env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=patientconnect
DB_USER=root
DB_PASSWORD=your_password
Usage

Generate sample data

bash
python seed.py
clinics: 3
providers: 16
patients: 187
appointments: 810
messages: 1181

Run reports

bash
python reports.py
python reports.py --csv out/

Run reminder engine

bash
python send_reminders.py --dry-run
python send_reminders.py --hours 48
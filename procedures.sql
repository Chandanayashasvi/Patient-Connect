USE patientconnect;

DROP PROCEDURE IF EXISTS sp_clinic_appointment_count;
DROP PROCEDURE IF EXISTS sp_book_appointment;
DROP PROCEDURE IF EXISTS sp_update_appointment_status;
DROP PROCEDURE IF EXISTS sp_recall_candidates;
DROP PROCEDURE IF EXISTS sp_due_reminders;

DELIMITER $$

CREATE PROCEDURE sp_clinic_appointment_count()
BEGIN
    SELECT
        c.clinic_id,
        c.clinic_name,
        COUNT(a.appointment_id) AS appointment_count
    FROM clinics c
    LEFT JOIN appointments a
        ON a.clinic_id = c.clinic_id
    GROUP BY
        c.clinic_id,
        c.clinic_name
    ORDER BY appointment_count DESC;
END$$


CREATE PROCEDURE sp_book_appointment(
    IN p_patient_id INT,
    IN p_provider_id INT,
    IN p_scheduled_at DATETIME,
    IN p_reason VARCHAR(255)
)
BEGIN
    DECLARE v_clinic_id INT DEFAULT NULL;
    DECLARE v_exists INT DEFAULT 0;
    DECLARE v_appointment_id INT;

    SELECT clinic_id
    INTO v_clinic_id
    FROM providers
    WHERE provider_id = p_provider_id
    LIMIT 1;

    IF v_clinic_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Invalid provider_id';
    END IF;

    SELECT COUNT(*)
    INTO v_exists
    FROM appointments
    WHERE provider_id = p_provider_id
      AND scheduled_at = p_scheduled_at
      AND status NOT IN ('cancelled', 'rescheduled');

    IF v_exists > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
        'Double booking: provider already has an appointment at this time.';
    END IF;

    INSERT INTO appointments
    (
        patient_id,
        provider_id,
        clinic_id,
        scheduled_at,
        status,
        reason
    )
    VALUES
    (
        p_patient_id,
        p_provider_id,
        v_clinic_id,
        p_scheduled_at,
        'scheduled',
        p_reason
    );

    SET v_appointment_id = LAST_INSERT_ID();

    INSERT INTO appointment_status_history
    (
        appointment_id,
        old_status,
        new_status,
        changed_at,
        note
    )
    VALUES
    (
        v_appointment_id,
        NULL,
        'scheduled',
        NOW(),
        'Appointment booked.'
    );

    SELECT
        v_appointment_id AS appointment_id,
        'booked' AS status;
END$$


CREATE PROCEDURE sp_update_appointment_status(
    IN p_appointment_id INT,
    IN p_new_status VARCHAR(50),
    IN p_note VARCHAR(255)
)
BEGIN
    DECLARE v_old_status VARCHAR(50);

    SELECT status
    INTO v_old_status
    FROM appointments
    WHERE appointment_id = p_appointment_id
    LIMIT 1;

    IF v_old_status IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Appointment not found';
    END IF;

    UPDATE appointments
    SET status = p_new_status
    WHERE appointment_id = p_appointment_id;

    INSERT INTO appointment_status_history
    (
        appointment_id,
        old_status,
        new_status,
        changed_at,
        note
    )
    VALUES
    (
        p_appointment_id,
        v_old_status,
        p_new_status,
        NOW(),
        p_note
    );

    SELECT
        p_appointment_id AS appointment_id,
        v_old_status AS old_status,
        p_new_status AS new_status;
END$$


CREATE PROCEDURE sp_recall_candidates(
    IN p_condition_id INT,
    IN p_months INT
)
BEGIN
    SELECT
        p.patient_id,
        CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
        c.condition_name,

        MAX(
            CASE
                WHEN a.status = 'completed'
                THEN a.scheduled_at
            END
        ) AS last_completed_visit,

        DATEDIFF(
            NOW(),
            MAX(
                CASE
                    WHEN a.status = 'completed'
                    THEN a.scheduled_at
                END
            )
        ) AS days_overdue

    FROM patient_conditions pc

    JOIN patients p
        ON p.patient_id = pc.patient_id

    JOIN conditions c
        ON c.condition_id = pc.condition_id

    LEFT JOIN appointments a
        ON a.patient_id = p.patient_id
       AND a.status = 'completed'

    WHERE pc.condition_id = p_condition_id

    GROUP BY
        p.patient_id,
        p.first_name,
        p.last_name,
        c.condition_name

    HAVING
        MAX(
            CASE
                WHEN a.status = 'completed'
                THEN a.scheduled_at
            END
        ) IS NULL

        OR

        DATEDIFF(
            NOW(),
            MAX(
                CASE
                    WHEN a.status = 'completed'
                    THEN a.scheduled_at
                END
            )
        ) > (p_months * 30)

    ORDER BY days_overdue DESC;
END$$


CREATE PROCEDURE sp_due_reminders(
    IN p_hours_ahead INT
)
BEGIN
    SELECT
        a.appointment_id,
        a.patient_id,

        CONCAT(
            p.first_name,
            ' ',
            p.last_name
        ) AS patient_name,

        a.provider_id,
        a.scheduled_at,
        a.reason

    FROM appointments a

    JOIN patients p
        ON p.patient_id = a.patient_id

    WHERE a.status IN ('scheduled', 'confirmed')

      AND a.scheduled_at >= NOW()

      AND a.scheduled_at <=
          DATE_ADD(
              NOW(),
              INTERVAL p_hours_ahead HOUR
          )

      AND NOT EXISTS
      (
          SELECT 1
          FROM messages m
          WHERE m.appointment_id = a.appointment_id
            AND m.message_type = 'reminder'
            AND m.status IN ('sent', 'delivered')
      )

    ORDER BY a.scheduled_at ASC;
END$$

DELIMITER ;
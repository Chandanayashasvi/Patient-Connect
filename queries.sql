SELECT
    p.provider_id,
    p.provider_name,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'completed' THEN 1 ELSE 0 END) AS completed_count,
    SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count,
    ROUND(
        100.0 * SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.appointment_id), 0),
        2
    ) AS no_show_pct
FROM providers p
LEFT JOIN appointments a
    ON a.provider_id = p.provider_id
GROUP BY p.provider_id, p.provider_name
ORDER BY no_show_pct DESC, total_appointments DESC;

SELECT
    CASE WHEN m.message_id IS NOT NULL THEN 'reminded' ELSE 'not_reminded' END AS reminder_group,
    COUNT(a.appointment_id) AS total_appointments,
    SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) AS no_show_count,
    ROUND(
        100.0 * SUM(CASE WHEN a.status = 'no_show' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.appointment_id), 0),
        2
    ) AS no_show_pct
FROM appointments a
LEFT JOIN (
    SELECT DISTINCT appointment_id
    FROM messages
    WHERE message_type = 'reminder'
      AND status IN ('sent', 'delivered', 'opened')
) m
    ON m.appointment_id = a.appointment_id
WHERE a.scheduled_at < NOW()
GROUP BY CASE WHEN m.message_id IS NOT NULL THEN 'reminded' ELSE 'not_reminded' END;

SELECT
    m.channel,
    COUNT(*) AS total_messages,
    SUM(CASE WHEN m.status = 'delivered' THEN 1 ELSE 0 END) AS delivered_count,
    SUM(CASE WHEN m.status = 'failed' THEN 1 ELSE 0 END) AS failed_count,
    ROUND(
        100.0 * SUM(CASE WHEN m.status = 'delivered' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0),
        2
    ) AS delivery_pct
FROM messages m
GROUP BY m.channel
ORDER BY delivery_pct DESC;

SELECT
    p.patient_id,
    CONCAT(p.first_name, ' ', p.last_name) AS patient_name,
    c.condition_name,
    MAX(CASE WHEN a.status = 'completed' THEN a.scheduled_at END) AS last_completed_visit,
    DATEDIFF(NOW(), MAX(CASE WHEN a.status = 'completed' THEN a.scheduled_at END)) AS days_since_last_completed
FROM patient_conditions pc
JOIN conditions c
    ON c.condition_id = pc.condition_id
JOIN patients p
    ON p.patient_id = pc.patient_id
LEFT JOIN appointments a
    ON a.patient_id = p.patient_id
   AND a.status = 'completed'
WHERE pc.condition_id = %s
GROUP BY p.patient_id, p.first_name, p.last_name, c.condition_name
HAVING
    MAX(CASE WHEN a.status = 'completed' THEN a.scheduled_at END) IS NULL
    OR DATEDIFF(NOW(), MAX(CASE WHEN a.status = 'completed' THEN a.scheduled_at END)) > (%s * 30)
ORDER BY days_since_last_completed DESC;

SELECT
    h.new_status,
    AVG(TIMESTAMPDIFF(MINUTE, h.changed_at, next_change.changed_at)) AS avg_minutes_in_status
FROM appointment_status_history h
LEFT JOIN appointment_status_history next_change
    ON next_change.appointment_id = h.appointment_id
   AND next_change.changed_at > h.changed_at
GROUP BY h.new_status
ORDER BY avg_minutes_in_status DESC;

DROP VIEW IF EXISTS v_school_safety_ranking;
DROP VIEW IF EXISTS v_infrastructure_gaps;
DROP VIEW IF EXISTS v_cost_benefit_optimization;

CREATE VIEW v_school_safety_ranking AS
SELECT
    s.school_id, s.school_name, s.zone, s.student_population,
    s.latitude, s.longitude, a.star_rating, a.sync_status,
    sky.estimated_avg_daily_traffic,
    ROUND((5.0 - a.star_rating) * (s.student_population / 100.0)
          * (sky.estimated_avg_daily_traffic / 1000.0), 2) AS risk_index,
    RANK() OVER (ORDER BY (5.0 - a.star_rating) * (s.student_population / 100.0)
          * (sky.estimated_avg_daily_traffic / 1000.0) DESC) AS ahmedabad_safety_rank
FROM schools_dim s
JOIN irap_audit_logs a ON a.school_id = s.school_id
JOIN sky_satellite_metrics sky ON sky.school_id = s.school_id;

CREATE VIEW v_infrastructure_gaps AS
SELECT 'Sidewalks' AS infrastructure_type,
       SUM(CASE WHEN sidewalk_score < 50 THEN 1 ELSE 0 END) AS schools_needing_improvement,
       ROUND(AVG(sidewalk_score), 1) AS avg_city_score
FROM irap_audit_logs
UNION ALL
SELECT 'Pedestrian Crossings',
       SUM(CASE WHEN crossing_score < 50 THEN 1 ELSE 0 END),
       ROUND(AVG(crossing_score), 1)
FROM irap_audit_logs
UNION ALL
SELECT 'Speed Management',
       SUM(CASE WHEN speed_management_score < 50 THEN 1 ELSE 0 END),
       ROUND(AVG(speed_management_score), 1)
FROM irap_audit_logs
UNION ALL
SELECT 'Student Visibility',
       SUM(CASE WHEN student_visibility_score < 50 THEN 1 ELSE 0 END),
       ROUND(AVG(student_visibility_score), 1)
FROM irap_audit_logs;

CREATE VIEW v_cost_benefit_optimization AS
SELECT
    s.school_id, s.school_name, s.zone,
    a.star_rating AS current_rating, c.measure_name, c.estimated_cost_inr,
    c.projected_star_rating_increase,
    ROUND((c.projected_star_rating_increase * s.student_population)
          / (c.estimated_cost_inr / 1000.0), 2) AS students_protected_per_1k_inr
FROM schools_dim s
JOIN irap_audit_logs a ON a.school_id = s.school_id
CROSS JOIN countermeasure_costs c
WHERE a.star_rating <= 3;

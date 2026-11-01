DROP VIEW IF EXISTS v_prescribed_interventions;
CREATE VIEW v_prescribed_interventions AS
WITH def AS (
  SELECT s.school_id, s.school_name, s.zone, s.student_population,
         a.star_rating AS current_rating,
         a.sidewalk_score, a.crossing_score, a.speed_management_score, a.student_visibility_score
  FROM schools_dim s
  JOIN irap_audit_logs a ON a.school_id = s.school_id
  WHERE a.star_rating <= 3
)
SELECT school_id, school_name, zone, current_rating, student_population,
       'Sidewalk Construction (100m)' AS measure_name, 85000 AS estimated_cost_inr, 1.5 AS projected_star_rating_increase,
       sidewalk_score AS component_score, 'Sidewalks' AS diagnosed_component
FROM def WHERE sidewalk_score < 55
UNION ALL
SELECT school_id, school_name, zone, current_rating, student_population,
       'Raised Zebra Crossing', 45000, 1.0, crossing_score, 'Pedestrian Crossings'
FROM def WHERE crossing_score < 55
UNION ALL
SELECT school_id, school_name, zone, current_rating, student_population,
       'School Speed Limit Signage', 15000, 0.5, speed_management_score, 'Speed Management'
FROM def WHERE speed_management_score < 55
UNION ALL
SELECT school_id, school_name, zone, current_rating, student_population,
       'High-Visibility School Paint', 25000, 0.5, student_visibility_score, 'Student Visibility'
FROM def WHERE student_visibility_score < 55;

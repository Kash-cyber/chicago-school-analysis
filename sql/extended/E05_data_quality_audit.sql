-- E05: Completeness of the columns used in this project
SELECT COUNT(*)                                       AS total_schools,
       SUM(Safety_Score IS NULL)                      AS missing_safety_score,
       SUM(Average_Student_Attendance IS NULL)        AS missing_attendance,
       SUM(College_Enrollment IS NULL)                AS missing_college_enrollment,
       SUM(COMMUNITY_AREA_NUMBER IS NULL)             AS missing_community_area,
       SUM(Rate_of_Misconducts__per_100_students_ IS NULL) AS missing_misconduct_rate
FROM CHICAGO_PUBLIC_SCHOOLS_DATA;

-- E01: Profile of each school type (ES / MS / HS): size, safety, attendance, college enrollment
SELECT "Elementary, Middle, or High School"                                   AS school_type,
       COUNT(*)                                                               AS schools,
       ROUND(AVG(Safety_Score), 1)                                            AS avg_safety_score,
       ROUND(AVG(CAST(REPLACE(Average_Student_Attendance, '%', '') AS REAL)), 1) AS avg_attendance_pct,
       ROUND(AVG(College_Enrollment), 0)                                      AS avg_college_enrollment
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
GROUP BY "Elementary, Middle, or High School"
ORDER BY schools DESC;

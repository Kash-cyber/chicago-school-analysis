-- E03: School-level safety, attendance and misconduct values for correlation analysis
SELECT Name_of_School                                                         AS school,
       "Elementary, Middle, or High School"                                  AS school_type,
       Safety_Score                                                          AS safety_score,
       CAST(REPLACE(Average_Student_Attendance, '%', '') AS REAL)            AS attendance_pct,
       Rate_of_Misconducts__per_100_students_                                AS misconducts_per_100
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE Safety_Score IS NOT NULL;

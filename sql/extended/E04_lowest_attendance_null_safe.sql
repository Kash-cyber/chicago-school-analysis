-- E04: NULL-safe version of Problem 5: numeric sort, missing values excluded
SELECT Name_of_School,
       CAST(REPLACE(Average_Student_Attendance, '%', '') AS REAL) AS attendance_pct
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE Average_Student_Attendance IS NOT NULL
ORDER BY attendance_pct ASC
LIMIT 5;

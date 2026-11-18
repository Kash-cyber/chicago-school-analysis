-- Problem 6: Same result set with the '%' sign removed
SELECT Name_of_School, REPLACE(Average_Student_Attendance, '%', '') AS attendance_pct
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
ORDER BY Average_Student_Attendance
LIMIT 5;

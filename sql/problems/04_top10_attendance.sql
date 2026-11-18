-- Problem 4: Top 10 schools by average student attendance
SELECT Name_of_School, Average_Student_Attendance
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
ORDER BY Average_Student_Attendance DESC NULLS LAST
LIMIT 10;

-- Problem 7: Schools with average student attendance below 70%
SELECT Name_of_School, Average_Student_Attendance
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE CAST(REPLACE(Average_Student_Attendance, '%', '') AS DOUBLE) < 70
ORDER BY Average_Student_Attendance;

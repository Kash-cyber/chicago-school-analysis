-- Problem 5: 5 schools with the lowest average student attendance (ascending)
SELECT Name_of_School, Average_Student_Attendance
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
ORDER BY Average_Student_Attendance
LIMIT 5;

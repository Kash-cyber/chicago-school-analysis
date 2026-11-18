-- Problem 8: Total college enrollment for each community area
SELECT Community_Area_Name, SUM(College_Enrollment) AS total_enrollment
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
GROUP BY Community_Area_Name;

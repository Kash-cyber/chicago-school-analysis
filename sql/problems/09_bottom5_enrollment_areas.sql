-- Problem 9: 5 community areas with the least total college enrollment
SELECT Community_Area_Name, SUM(College_Enrollment) AS total_enrollment
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
GROUP BY Community_Area_Name
ORDER BY total_enrollment ASC
LIMIT 5;

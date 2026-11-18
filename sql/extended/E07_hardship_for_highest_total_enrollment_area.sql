-- E07: Problem 12 asks for "the community area with the highest College Enrollment".
-- The lab solution picks the area of the single LARGEST SCHOOL. This query answers the other reading:
-- the area with the highest TOTAL enrollment across all its schools.
SELECT cd.community_area_number,
       cd.community_area_name,
       cd.hardship_index,
       t.total_enrollment
FROM CENSUS_DATA cd
JOIN (
    SELECT COMMUNITY_AREA_NUMBER, SUM(College_Enrollment) AS total_enrollment
    FROM CHICAGO_PUBLIC_SCHOOLS_DATA
    GROUP BY COMMUNITY_AREA_NUMBER
    ORDER BY total_enrollment DESC
    LIMIT 1
) t ON t.community_area_number = cd.community_area_number;

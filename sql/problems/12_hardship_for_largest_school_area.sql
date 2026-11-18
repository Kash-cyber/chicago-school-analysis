-- Problem 12: Hardship index of the community area of the school with the highest College Enrollment
SELECT community_area_number, community_area_name, hardship_index
FROM CENSUS_DATA
WHERE community_area_number IN (
    SELECT community_area_number FROM CHICAGO_PUBLIC_SCHOOLS_DATA
    ORDER BY college_enrollment DESC LIMIT 1
);

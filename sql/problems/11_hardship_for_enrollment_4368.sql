-- Problem 11: Hardship index of the community area of the school with college enrollment 4368
SELECT hardship_index
FROM CENSUS_DATA CD, CHICAGO_PUBLIC_SCHOOLS_DATA CPS
WHERE CD.community_area_number = CPS.community_area_number
  AND college_enrollment = 4368;

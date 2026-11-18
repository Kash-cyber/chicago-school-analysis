-- E02: Average school safety score per community area next to the area's hardship index
SELECT cps.COMMUNITY_AREA_NAME            AS community_area,
       COUNT(*)                            AS schools,
       ROUND(AVG(cps.Safety_Score), 1)     AS avg_safety_score,
       cd.hardship_index                   AS hardship_index
FROM CHICAGO_PUBLIC_SCHOOLS_DATA cps
JOIN CENSUS_DATA cd ON cd.community_area_number = cps.COMMUNITY_AREA_NUMBER
GROUP BY cps.COMMUNITY_AREA_NUMBER, cps.COMMUNITY_AREA_NAME, cd.hardship_index
ORDER BY cd.hardship_index;

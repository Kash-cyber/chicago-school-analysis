-- E06: Community areas ranked by average school safety score (areas with 3+ schools)
SELECT COMMUNITY_AREA_NAME        AS community_area,
       COUNT(*)                   AS schools,
       ROUND(AVG(Safety_Score),1) AS avg_safety_score
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE Safety_Score IS NOT NULL
GROUP BY COMMUNITY_AREA_NAME
HAVING COUNT(*) >= 3
ORDER BY avg_safety_score DESC;

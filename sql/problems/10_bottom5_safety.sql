-- Problem 10: 5 schools with the lowest safety score
SELECT name_of_school, safety_score
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE safety_score != 'None'
ORDER BY safety_score
LIMIT 5;

-- Problem 3: Which schools have the highest Safety Score?
SELECT Name_of_School, Safety_Score
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE Safety_Score = (SELECT MAX(Safety_Score) FROM CHICAGO_PUBLIC_SCHOOLS_DATA);

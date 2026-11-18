-- Problem 1: How many elementary schools are in the dataset?
SELECT COUNT(*) AS elementary_schools
FROM CHICAGO_PUBLIC_SCHOOLS_DATA
WHERE "Elementary, Middle, or High School" = 'ES';

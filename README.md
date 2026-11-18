# 🏫 Chicago Public Schools — SQL Data Analysis

A SQL-based analysis of Chicago Public Schools data from 2011–12, using **SQLite**, **Python**, **pandas**, and **Jupyter Notebook**.

The project explores school safety, attendance, enrollment, and community-area census data to show how SQL can turn a real-world dataset into useful insights. It began as the IBM _Working with a Real World Data-set using SQL and Python_ lab and was extended into a documented, reproducible project.

📊 **566 schools** · **78 columns** · **77 community areas** · **12 SQL problems**

![Attendance extremes](figures/03_attendance_extremes.png)

---

## 🎯 Why This Project?

I built this project to practice SQL with a real-world dataset rather than working only with simple practice tables. The project helped me understand how data analysts:

- 🔎 Explore and filter large datasets
- 🧹 Handle missing and incorrectly formatted data
- 🧮 Use SQL for calculations and aggregation
- 🔗 Combine information from different tables
- 📊 Turn query results into visualizations
- 💡 Convert raw data into meaningful findings

It also taught me an important lesson: real-world data is rarely perfectly clean. Some values were stored as text, some were missing, and some column names were not as straightforward as they first appeared.

---

## ⚙️ Project Workflow

```
CSV Data
   ↓
Python + pandas
   ↓
SQLite Database
   ↓
Schema Inspection
   ↓
SQL Queries
   ↓
Data Cleaning
   ↓
Analysis
   ↓
Graphs & Findings
```

### 🛠️ Technologies

Python · pandas · SQLite · SQL · matplotlib · Jupyter Notebook

---

## 📌 Key Findings

| Metric / Question                            | Result                                                                                        |
| -------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Schools in the dataset**                   | **566**, across **78 columns**                                                                |
| **Elementary schools**                       | **462** (81.6% of total)                                                                      |
| **Highest safety score**                     | **99**, shared by **19 schools** (17 elementary-level, 2 high schools)                        |
| **Lowest safety score**                      | **1** (Edmond Burke Elementary)                                                               |
| **Highest average attendance**               | **98.4%** (John Charles Haines Elementary)                                                    |
| **Schools below 70% attendance**             | **8**, of which **7 are high schools** (lowest: Richard T. Crane Technical Prep at **57.9%**) |
| **Community areas**                          | **77**, with a total enrollment of **354,346** students                                       |
| **Largest / smallest area by enrollment**    | South Lawndale (**14,793**) / Oakland (**140**) — a **106×** difference                       |
| **Enrollment concentration**                 | Top 10 areas hold **28.7%** of all students; the 38 smallest hold **24.4%**                   |
| **Hardship index for largest school's area** | **6** (North Center, home of Lane Technical High School)                                      |

### What the Data Says

- 🎓 **Attendance follows school type:** All ten highest attendance rates (97.2%–98.4%) belong to elementary-level schools, at least six of them selective programs (Classical, Gifted, Magnet, Language Academy). Of the 8 schools below 70%, 7 are high schools and 1 is an early-childhood center—creating a **40-point spread** between the extremes.

- 🛡️ **Safety spans the entire scale:** Safety scores range from 1 to 99. Both elementary schools and high schools appear among the highest and lowest safety scores, showing that school type alone does not explain safety.

- 👥 **Enrollment is right-skewed:** With a mean of 4,602 vs. a median of 4,206 students per area, enrollment varies wildly. South Lawndale has roughly 106× more students than Oakland, and several of the smallest areas (like O'Hare and the Loop) are not primarily residential.

- 📈 **Enrollment is heavily concentrated:** Students are not evenly distributed across the city—the top 10 community areas contain **28.7%** of all enrolled students, while the 38 smallest areas combined contain **24.4%**.

- 🏘️ **Low hardship at the largest school:** Lane Technical High School (4,368 students) is located in North Center, which has a hardship index of just 6 (on a 1–100 scale where higher means more hardship).

### 📊 Visual Insights

<p align="center">
  <img src="figures/01_enrollment_top_bottom_areas.png" width="95%" alt="Top and Bottom Community Areas by Enrollment">
</p>

<p align="center">
  <img src="figures/02_enrollment_concentration.png" width="48%" alt="Enrollment Concentration">
  <img src="figures/04_safety_extremes.png" width="48%" alt="Safety Score Extremes">
</p>

---

## 🔍 What I Did

| Step                  | Action              | Description                                                                                                                                                     |
| --------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 📥 Load**        | Read & Store        | Loaded the school (`566 rows`) and census (`78 rows`) CSV files using `pandas` and stored them in SQLite via `DataFrame.to_sql()`.                              |
| **2. 🔬 Inspect**     | Schema Check        | Inspected the database schema using `sqlite_master` and `PRAGMA_TABLE_INFO` to list tables, count columns, and check types (`59 TEXT`, `12 REAL`, `7 INTEGER`). |
| **3. 🏷️ Clean Names** | Quote Identifiers   | Handled mixed-case column names and the 6 columns containing spaces, commas, or parentheses (e.g., `"Elementary, Middle, or High School"`).                     |
| **4. 💻 Query**       | Answer 12 Problems  | Wrote 12 SQL queries using counting, `MAX`, subqueries, `ORDER BY ... LIMIT`, `GROUP BY`, and joins across both tables.                                         |
| **5. 🧹 Fix Data**    | Handle Messy Values | Cleaned percentages stored as text and filtered out `NULL` values so sorting and calculations worked properly.                                                  |
| **6. 📊 Visualize**   | Plot & Verify       | Created graphs from the query results, organized queries into `.sql` files, and built a pipeline with smoke tests to verify live results.                       |

### 💻 SQL Skills Demonstrated

`SELECT` · `WHERE` · `COUNT()` · `MAX()` · `SUM()` · `GROUP BY` · `ORDER BY` · `LIMIT` · `JOIN` · `Subqueries` · `CAST()` · `REPLACE()` · `NULLS LAST` · `PRAGMA_TABLE_INFO`

**Example of cleaning an attendance value stored as text:**

```sql
CAST(REPLACE(attendance, '%', '') AS REAL)
```

---

## 🚧 Data-Quality Findings (The "Real World" Part)

Working with uncleaned civic data revealed several common SQL traps:

| Pitfall                           | What Happened                                                                                                                                                               | Safe Habit                                                                              |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| **Numbers stored as text**        | 59 of 78 columns are `TEXT`; attendance is stored as `'96.00%'`.                                                                                                            | Use `CAST(REPLACE(col, '%', '') AS REAL)` before comparing or averaging.                |
| **NULLs sort first (ascending)**  | Problem 5's "lowest attendance" initially returned _Velma F Thomas Early Childhood Center_, which simply had **no value**.                                                  | Filter with `IS NOT NULL`, or explicitly state `NULLS FIRST/LAST`.                      |
| **Text sorting is lexicographic** | Sorting text worked only because values had two digits before the decimal; `'100.00%'` would sort before `'57.90%'`.                                                        | Always cast strings to numeric types before sorting.                                    |
| **Comparing to `'None'`**         | The lab's safety filter `!= 'None'` works only because `NULL != x` evaluates to `NULL` in SQLite.                                                                           | Explicitly use `IS NOT NULL`.                                                           |
| **Ties hidden by `MAX()`**        | 19 schools share the top safety score of 99.                                                                                                                                | Use `= (SELECT MAX(...))` to return all tied rows.                                      |
| **Ambiguous questions**           | "Community area with the highest College Enrollment" can mean the area of the single largest _school_ (North Center) or the area with the highest _total_ (South Lawndale). | Clarify which interpretation a query uses (extended query `E07` covers the area total). |
| **Misleading column names**       | `COLLEGE_ENROLLMENT` holds 500–1,300 for elementary schools, meaning it actually represents each school's total student headcount.                                          | Sanity-check values against sample rows before interpreting results.                    |

---

## 🗄️ Data Sources

| Table / File                  | Contents                                                         | Source                                                                                                                       |
| ----------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `CHICAGO_PUBLIC_SCHOOLS_DATA` | School-level progress-report metrics, 2011–12 (`566 × 78`)       | [Chicago Data Portal](https://data.cityofchicago.org/Education/Chicago-Public-Schools-Progress-Report-Cards-2011-/9xs2-f89t) |
| `CENSUS_DATA`                 | Community-area socioeconomic indicators including hardship index | Course-hosted `ChicagoCensusData.csv`                                                                                        |

_(Note: Because raw CSVs are downloaded at runtime, the repository stores the column schema, 8 sample rows, per-area enrollment totals, and the verified outputs of all 12 problems.)_

---

## 📂 Project Structure

```
├── README.md
├── requirements.txt
├── run_pipeline.py                          # CSV -> SQLite -> run all SQL -> checks, metrics, charts
├── src/
│   └── chicago_sql.py                       # Load, query, and chart helpers
├── sql/
│   ├── problems/                            # The 12 lab problems, one .sql file each
│   └── extended/                            # 7 additional analysis queries (E01–E07)
├── notebooks/
│   └── Chicago_Schools_SQL_Analysis.ipynb   # Narrative walkthrough with results and insights
├── data/                                    # Schema (78 cols), sample rows, per-area totals
├── results/                                 # Verified outputs & reproduction checks
├── figures/
│   ├── 01_enrollment_top_bottom_areas.png
│   ├── 02_enrollment_concentration.png
│   ├── 03_attendance_extremes.png
│   └── 04_safety_extremes.png
├── tests/
│   └── test_queries.py                      # Smoke tests for every .sql file against the schema
└── original/
    └── RealDataPractice_original.ipynb      # Starting lab notebook, untouched
```

---

## 🚀 How to Run

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Rebuild the database and run the full pipeline:**

   ```bash
   # Downloads source CSVs (requires internet), runs all queries, checks results, and builds charts
   python run_pipeline.py

   # Or run using local copies of the CSVs:
   python run_pipeline.py --schools-csv ChicagoPublicSchools.csv --census-csv ChicagoCensusData.csv
   ```

3. **Explore the Jupyter Notebook:**

   ```bash
   jupyter notebook notebooks/Chicago_Schools_SQL_Analysis.ipynb
   ```

4. **Run the query tests:**
   ```bash
   python tests/test_queries.py
   ```

---

## ⚠️ Limitations & Next Steps

### Limitations

- **Scope:** Reported numbers cover the 12 core lab problems. Extended queries in `sql/extended/` are implemented and tested against the schema, and running `python run_pipeline.py` generates their full-dataset outputs.
- **Timeframe:** Covers a single school year (2011–12) using descriptive statistics only (no causal claims).
- **Inferred School Types:** School types in charts were inferred from school names (e.g., `"High School"`) where the type column wasn't part of the captured output.
- **Enrollment Counts:** Totals count students attending schools _located_ in each community area rather than residents, ignoring schools with missing values.

### Next Steps

- 📉 Generate and embed correlation charts from the extended queries (safety vs. attendance, area safety vs. hardship).
- 🏫 Compare attendance and safety across school types using the full table.
- 🪟 Implement SQL window functions (e.g., ranking schools within each community area) and reusable views.

---

## 💡 Main Takeaway

This project demonstrates how **SQL + Python + visualization** can transform a large, messy dataset into clear and understandable findings. More importantly, it gave me practical experience working with real-world data problems—like text-formatted numbers, `NULL` sorting quirks, and ambiguous column names—rather than just writing SQL queries against perfectly clean tables.

---

## 👋 Connect With Me

[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/kashaf-malik-738689304)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Kash-cyber)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:kashafqaiser1707@gmail.com)

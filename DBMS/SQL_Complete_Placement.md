# ⭐⭐⭐⭐⭐ Chapter 3: The Complete SQL Handbook

Every SQL topic needed for TCS, Infosys, Wipro, Amazon, Microsoft, and Oracle placements — with examples, outputs, MCQs, and interview answers.

---

## 1. Sample Database Setup

> [!NOTE]
> All queries in this chapter use these two tables. Run this first.

```sql
CREATE TABLE Departments (
    Dept_ID   INT PRIMARY KEY,
    Dept_Name VARCHAR(50),
    Location  VARCHAR(50)
);

INSERT INTO Departments VALUES (1, 'HR',      'Mumbai');
INSERT INTO Departments VALUES (2, 'IT',      'Bangalore');
INSERT INTO Departments VALUES (3, 'Finance', 'Delhi');
INSERT INTO Departments VALUES (4, 'Sales',   'Chennai');

CREATE TABLE Employees (
    Emp_ID     INT PRIMARY KEY,
    Emp_Name   VARCHAR(50),
    Salary     DECIMAL(10,2),
    Dept_ID    INT,
    Manager_ID INT
);

INSERT INTO Employees VALUES (101, 'Alice',   90000, 1, NULL);
INSERT INTO Employees VALUES (102, 'Bob',     80000, 2, 101);
INSERT INTO Employees VALUES (103, 'Charlie', 75000, 2, 101);
INSERT INTO Employees VALUES (104, 'David',   50000, 3, 102);
INSERT INTO Employees VALUES (105, 'Eve',     80000, 2, 101);
INSERT INTO Employees VALUES (106, 'Frank',   60000, 4, 102);
INSERT INTO Employees VALUES (107, 'Grace',   60000, 4, 102);
INSERT INTO Employees VALUES (108, 'Henry',   NULL,  3, 101);
```

**Employees Table:**
| Emp_ID | Emp_Name | Salary | Dept_ID | Manager_ID |
|:---|:---|:---|:---|:---|
| 101 | Alice | 90000 | 1 | NULL |
| 102 | Bob | 80000 | 2 | 101 |
| 103 | Charlie | 75000 | 2 | 101 |
| 104 | David | 50000 | 3 | 102 |
| 105 | Eve | 80000 | 2 | 101 |
| 106 | Frank | 60000 | 4 | 102 |
| 107 | Grace | 60000 | 4 | 102 |
| 108 | Henry | NULL | 3 | 101 |

---

## 2. Basic SELECT Queries

### SELECT
```sql
SELECT Emp_Name, Salary FROM Employees;
```
Fetches only `Emp_Name` and `Salary` columns. `SELECT *` fetches all columns (avoid in production).

### WHERE
```sql
SELECT * FROM Employees WHERE Salary > 70000;
```
**Output:** Alice (90000), Bob (80000), Charlie (75000), Eve (80000).

### DISTINCT
Removes duplicate values from results.
```sql
SELECT DISTINCT Dept_ID FROM Employees;
```
**Output:** 1, 2, 3, 4 (each department ID appears only once, even though IT has 3 employees).

### ORDER BY
```sql
SELECT Emp_Name, Salary FROM Employees ORDER BY Salary DESC;
```
`DESC` = highest first. `ASC` = lowest first (default).

**Output:** Alice (90000) → Bob (80000) → Eve (80000) → Charlie (75000) → Frank (60000) → Grace (60000) → David (50000) → Henry (NULL).

> [!TIP]
> **Interview Note:** NULL values appear LAST in ascending ORDER BY and FIRST in descending ORDER BY (standard SQL behavior).

### LIMIT / TOP / FETCH
```sql
-- MySQL / PostgreSQL
SELECT * FROM Employees ORDER BY Salary DESC LIMIT 3;

-- SQL Server
SELECT TOP 3 * FROM Employees ORDER BY Salary DESC;

-- Oracle (12c+)
SELECT * FROM Employees ORDER BY Salary DESC FETCH FIRST 3 ROWS ONLY;
```
**Output:** Top 3 — Alice (90000), Bob (80000), Eve (80000).

---

## 3. Logical & Filter Operators

### AND, OR, NOT
```sql
-- AND: Both conditions must be true
SELECT * FROM Employees WHERE Dept_ID = 2 AND Salary > 75000;
-- Output: Bob (80000), Eve (80000)

-- OR: Either condition must be true
SELECT * FROM Employees WHERE Dept_ID = 1 OR Dept_ID = 4;
-- Output: Alice, Frank, Grace

-- NOT: Inverts the condition
SELECT * FROM Employees WHERE NOT Dept_ID = 2;
-- Output: Alice, David, Frank, Grace, Henry
```

### IN
Tests if a value matches any value in a list.
```sql
SELECT * FROM Employees WHERE Dept_ID IN (1, 4);
```
**Output:** Alice (Dept 1), Frank (Dept 4), Grace (Dept 4).
> Equivalent to: `WHERE Dept_ID = 1 OR Dept_ID = 4` — but cleaner.

### BETWEEN
Tests if a value lies within a range (inclusive on both ends).
```sql
SELECT * FROM Employees WHERE Salary BETWEEN 60000 AND 80000;
```
**Output:** Bob (80000), Charlie (75000), Eve (80000), Frank (60000), Grace (60000).

### LIKE
Pattern matching for strings.

| Pattern | Meaning |
|:---|:---|
| `'A%'` | Starts with A |
| `'%e'` | Ends with e |
| `'%li%'` | Contains "li" anywhere |
| `'_li_e'` | Any char, then "li", then any char, then "e" |

```sql
SELECT * FROM Employees WHERE Emp_Name LIKE 'A%';
-- Output: Alice

SELECT * FROM Employees WHERE Emp_Name LIKE '%e';
-- Output: Alice, Charlie, Grace
```

### IS NULL / IS NOT NULL
> [!IMPORTANT]
> You CANNOT use `= NULL`. NULL is not a value; it is the absence of a value. You must use `IS NULL`.

```sql
-- Find employees with no salary recorded
SELECT * FROM Employees WHERE Salary IS NULL;
-- Output: Henry

-- Find employees who have a salary
SELECT * FROM Employees WHERE Salary IS NOT NULL;
-- Output: All except Henry
```

---

## 4. NULL Handling: COALESCE

`COALESCE(value1, value2, ...)` returns the **first non-NULL** value in the list.

```sql
SELECT Emp_Name, COALESCE(Salary, 0) AS Salary
FROM Employees;
```
**Output:** Henry's salary shows as 0 instead of NULL. All others unchanged.

> [!TIP]
> **Memory Trick:** COALESCE = "Use this, or if null, use that."

---

## 5. Aggregate Functions

Aggregate functions operate on a **set of rows** and return a **single value**.

| Function | What it does |
|:---|:---|
| `COUNT(*)` | Counts all rows including NULLs |
| `COUNT(col)` | Counts non-NULL values in that column |
| `SUM(col)` | Sum of all non-NULL values |
| `AVG(col)` | Average of all non-NULL values |
| `MIN(col)` | Minimum value |
| `MAX(col)` | Maximum value |

```sql
SELECT
    COUNT(*)         AS Total_Rows,      -- 8
    COUNT(Salary)    AS Salaried_Emps,   -- 7 (Henry excluded)
    SUM(Salary)      AS Total_Payroll,   -- 495000
    AVG(Salary)      AS Avg_Salary,      -- 70714.28
    MIN(Salary)      AS Min_Salary,      -- 50000
    MAX(Salary)      AS Max_Salary       -- 90000
FROM Employees;
```

> [!WARNING]
> `AVG()` ignores NULLs. Alice's NULL salary is NOT counted in the denominator, so AVG(Salary) = 495000 / 7, not 495000 / 8.

---

## 6. GROUP BY & HAVING

### GROUP BY
Groups rows that have the same values and allows aggregate functions per group.

```sql
SELECT Dept_ID, COUNT(*) AS Headcount, AVG(Salary) AS Avg_Salary
FROM Employees
GROUP BY Dept_ID;
```

**Output:**
| Dept_ID | Headcount | Avg_Salary |
|:---|:---|:---|
| 1 | 1 | 90000 |
| 2 | 3 | 78333.33 |
| 3 | 2 | 50000 |
| 4 | 2 | 60000 |

### HAVING
Filters **groups** after aggregation. `WHERE` cannot be used with aggregate functions.

```sql
-- Departments with more than 1 employee
SELECT Dept_ID, COUNT(*) AS Headcount
FROM Employees
GROUP BY Dept_ID
HAVING COUNT(*) > 1;
```

**Output:** Dept 2 (3 employees), Dept 3 (2), Dept 4 (2).

> [!TIP]
> **Memory Trick:**
> `WHERE` = Filter **rows** (before GROUP BY)
> `HAVING` = Filter **groups** (after GROUP BY)

---

## 7. Constraints

Constraints enforce rules on data in a table.

| Constraint | Purpose |
|:---|:---|
| `PRIMARY KEY` | Unique + NOT NULL. Uniquely identifies each row. |
| `FOREIGN KEY` | Links to Primary Key of another table. Enforces referential integrity. |
| `UNIQUE` | No duplicate values allowed. Unlike PK, can have one NULL. |
| `NOT NULL` | Column cannot have NULL values. |
| `CHECK` | Validates a condition before inserting/updating. |
| `DEFAULT` | Assigns a default value if none is provided. |

```sql
CREATE TABLE Orders (
    Order_ID   INT PRIMARY KEY,
    Order_Date DATE DEFAULT GETDATE(),
    Amount     DECIMAL(10,2) CHECK (Amount > 0),
    Status     VARCHAR(20) NOT NULL,
    Emp_ID     INT,
    FOREIGN KEY (Emp_ID) REFERENCES Employees(Emp_ID)
);
```

---

## 8. DDL: ALTER, DROP, TRUNCATE

### ALTER
Modifies the structure of an existing table.
```sql
-- Add a new column
ALTER TABLE Employees ADD Email VARCHAR(100);

-- Modify column data type
ALTER TABLE Employees MODIFY Emp_Name VARCHAR(100);  -- MySQL
ALTER TABLE Employees ALTER COLUMN Emp_Name VARCHAR(100);  -- SQL Server

-- Drop a column
ALTER TABLE Employees DROP COLUMN Email;
```

### DROP vs TRUNCATE
```sql
-- Remove ALL rows, keep structure (DDL, fast, no rollback in MySQL)
TRUNCATE TABLE Employees;

-- Permanently destroy the entire table (structure + data)
DROP TABLE Employees;
```

See the full comparison table in Chapter 1.

---

## 9. DML: UPDATE & DELETE

### UPDATE
```sql
-- Give IT department a 10% salary raise
UPDATE Employees
SET Salary = Salary * 1.10
WHERE Dept_ID = 2;
```
> [!WARNING]
> Always use a `WHERE` clause with UPDATE. Without it, **every row** in the table gets updated.

### DELETE
```sql
-- Remove a specific employee
DELETE FROM Employees WHERE Emp_ID = 108;

-- Remove all employees from Finance dept
DELETE FROM Employees WHERE Dept_ID = 3;
```
> [!WARNING]
> Always use a `WHERE` clause with DELETE. Without it, **every row** is deleted (same as TRUNCATE but slower).

---

## 10. JOINS (Complete Guide)

```text
         [ SQL JOINS ]
        /      |      \
   [Inner]  [Outer]  [Cross] [Self]
           /   |   \
      [Left][Right][Full]
```

### INNER JOIN
Returns only rows with a match in **both** tables.
```sql
SELECT E.Emp_Name, D.Dept_Name
FROM Employees E
INNER JOIN Departments D ON E.Dept_ID = D.Dept_ID;
```
**Output:** 8 rows. All employees matched to their department name.
*(Henry in Dept 3=Finance also appears. Sales dept has Frank and Grace.)*

### LEFT JOIN
All rows from left table; NULLs for unmatched right-side columns.
```sql
SELECT E.Emp_Name, D.Dept_Name
FROM Employees E
LEFT JOIN Departments D ON E.Dept_ID = D.Dept_ID;
```
**Output:** All 8 employees. If any employee had a non-existent Dept_ID, their Dept_Name would be NULL.

### RIGHT JOIN
All rows from right table; NULLs for unmatched left-side columns.
```sql
SELECT E.Emp_Name, D.Dept_Name
FROM Employees E
RIGHT JOIN Departments D ON E.Dept_ID = D.Dept_ID;
```
**Output:** All 4 departments. If a department had no employees, Emp_Name would be NULL.

### FULL OUTER JOIN
All rows from both tables. NULLs where no match exists on either side.
```sql
-- SQL Server / PostgreSQL
SELECT E.Emp_Name, D.Dept_Name
FROM Employees E
FULL OUTER JOIN Departments D ON E.Dept_ID = D.Dept_ID;

-- MySQL workaround (MySQL lacks FULL OUTER JOIN)
SELECT E.Emp_Name, D.Dept_Name FROM Employees E LEFT JOIN Departments D ON E.Dept_ID = D.Dept_ID
UNION
SELECT E.Emp_Name, D.Dept_Name FROM Employees E RIGHT JOIN Departments D ON E.Dept_ID = D.Dept_ID;
```

### CROSS JOIN
Returns the **Cartesian product** — every row of Table A paired with every row of Table B.
```sql
SELECT E.Emp_Name, D.Dept_Name
FROM Employees E
CROSS JOIN Departments D;
```
**Output:** 8 employees × 4 departments = **32 rows**.
> Used rarely. Practical use: generating all combinations (e.g., all products × all stores).

### SELF JOIN ⭐⭐⭐⭐⭐
A table joined with **itself**. Classic use: finding an employee's manager (who is also an employee).
```sql
SELECT E.Emp_Name AS Employee, M.Emp_Name AS Manager
FROM Employees E
LEFT JOIN Employees M ON E.Manager_ID = M.Emp_ID;
```
**Output:**
| Employee | Manager |
|:---|:---|
| Alice | NULL |
| Bob | Alice |
| Charlie | Alice |
| David | Bob |
| Eve | Alice |
| Frank | Bob |
| Grace | Bob |
| Henry | Alice |

---

## 11. Set Operations

Set operations combine results of two or more SELECT queries. Both queries must have the same number of columns and compatible data types.

### UNION
Combines results and **removes duplicates**.
```sql
SELECT Dept_ID FROM Employees
UNION
SELECT Dept_ID FROM Departments;
-- Output: 1, 2, 3, 4 (unique values only)
```

### UNION ALL
Combines results and **keeps duplicates**. Faster than UNION.
```sql
SELECT Dept_ID FROM Employees
UNION ALL
SELECT Dept_ID FROM Departments;
-- Output: 1,2,2,2,3,3,4,4 from Employees + 1,2,3,4 from Departments = 12 rows
```

### INTERSECT
Returns rows that appear in **both** result sets.
```sql
SELECT Dept_ID FROM Employees
INTERSECT
SELECT Dept_ID FROM Departments;
-- Output: 1, 2, 3, 4 (all Dept_IDs in Employees also exist in Departments)
```
> [!NOTE]
> MySQL supports INTERSECT only from version 8.0.31+. SQL Server and PostgreSQL support it natively.

### EXCEPT / MINUS
Returns rows from the **first** query that do **not** appear in the second.
```sql
-- SQL Server / PostgreSQL
SELECT Dept_ID FROM Departments
EXCEPT
SELECT Dept_ID FROM Employees;
-- Output: Empty (all departments have at least one employee in our data)

-- Oracle uses MINUS instead of EXCEPT
SELECT Dept_ID FROM Departments
MINUS
SELECT Dept_ID FROM Employees;
```

---

## 12. Subqueries: EXISTS, ANY, ALL

### EXISTS
Returns TRUE if the subquery returns at least one row.
```sql
-- Find departments that have at least one employee
SELECT Dept_Name FROM Departments D
WHERE EXISTS (
    SELECT 1 FROM Employees E WHERE E.Dept_ID = D.Dept_ID
);
-- Output: HR, IT, Finance, Sales (all departments have employees in our data)
```

### ANY
Returns TRUE if the comparison is true for **at least one** value in the subquery result.
```sql
-- Employees earning more than at least one Finance dept employee
SELECT Emp_Name FROM Employees
WHERE Salary > ANY (SELECT Salary FROM Employees WHERE Dept_ID = 3);
-- (Finance salaries: 50000, NULL) — any employee earning > 50000 qualifies
-- Output: Alice, Bob, Charlie, Eve, Frank, Grace
```

### ALL
Returns TRUE if the comparison is true for **all** values in the subquery result.
```sql
-- Employees earning more than ALL Finance dept employees (ignores NULLs)
SELECT Emp_Name FROM Employees
WHERE Salary > ALL (SELECT Salary FROM Employees WHERE Dept_ID = 3 AND Salary IS NOT NULL);
-- Finance non-null salaries: 50000 only. Employees earning > 50000:
-- Output: Alice, Bob, Charlie, Eve, Frank, Grace
```

---

## 13. CASE Expression

`CASE` is SQL's IF-THEN-ELSE. Returns a value based on conditions.

```sql
SELECT Emp_Name, Salary,
    CASE
        WHEN Salary >= 80000 THEN 'High'
        WHEN Salary >= 60000 THEN 'Medium'
        WHEN Salary IS NULL  THEN 'Not Set'
        ELSE 'Low'
    END AS Salary_Grade
FROM Employees;
```

**Output:**
| Emp_Name | Salary | Salary_Grade |
|:---|:---|:---|
| Alice | 90000 | High |
| Bob | 80000 | High |
| Charlie | 75000 | Medium |
| David | 50000 | Low |
| Eve | 80000 | High |
| Frank | 60000 | Medium |
| Grace | 60000 | Medium |
| Henry | NULL | Not Set |

---

## 14. Views

A **View** is a virtual table based on a stored SELECT query. It does not store data physically.

```sql
-- Create a view
CREATE VIEW IT_Employees AS
SELECT Emp_Name, Salary
FROM Employees
WHERE Dept_ID = 2;

-- Use it like a table
SELECT * FROM IT_Employees;
-- Output: Bob, Charlie, Eve

-- Drop a view
DROP VIEW IT_Employees;
```

**Why use Views?**
* **Security:** Expose only specific columns/rows to certain users.
* **Simplicity:** Hide complex JOIN logic behind a simple view name.
* **Consistency:** Ensure all queries use the same logic.

> [!IMPORTANT]
> A view is NOT a physical copy of data. Every time you query a view, the underlying SELECT runs again.

---

## 15. Indexes

An **Index** is a database object that speeds up data retrieval at the cost of extra storage and slower writes.

```sql
-- Create an index on Salary for fast salary-based lookups
CREATE INDEX idx_salary ON Employees(Salary);

-- Create a unique index (no duplicate values allowed)
CREATE UNIQUE INDEX idx_emp_name ON Employees(Emp_Name);

-- Drop an index
DROP INDEX idx_salary ON Employees;  -- MySQL
DROP INDEX idx_salary;               -- Oracle / PostgreSQL
```

| Type | Description |
|:---|:---|
| **Clustered Index** | Determines physical sort order of data. ONE per table. Usually the Primary Key. |
| **Non-Clustered Index** | Separate structure with pointers to actual rows. Many per table allowed. |

---

## 16. Window Functions ⭐⭐⭐⭐⭐

Window functions perform calculations across a **window** (set of related rows) without collapsing results like `GROUP BY`.

**Syntax:**
```sql
function_name() OVER (PARTITION BY col ORDER BY col)
```

### ROW_NUMBER()
Assigns a unique sequential integer to each row. No ties — always unique.
```sql
SELECT Emp_Name, Salary,
    ROW_NUMBER() OVER (ORDER BY Salary DESC) AS Row_Num
FROM Employees WHERE Salary IS NOT NULL;
```
**Output:** Alice=1, Bob=2, Eve=3, Charlie=4, Frank=5, Grace=6, David=7

### RANK()
Assigns the same rank to tied values. **Skips** next rank numbers after a tie.
```sql
SELECT Emp_Name, Salary,
    RANK() OVER (ORDER BY Salary DESC) AS Rnk
FROM Employees WHERE Salary IS NOT NULL;
```
**Output:** Alice=1, Bob=2, Eve=2, Charlie=4 (skips 3), Frank=5, Grace=5, David=7

### DENSE_RANK()
Assigns the same rank to tied values. Does **NOT** skip next rank numbers.
```sql
SELECT Emp_Name, Salary,
    DENSE_RANK() OVER (ORDER BY Salary DESC) AS Dense_Rnk
FROM Employees WHERE Salary IS NOT NULL;
```
**Output:** Alice=1, Bob=2, Eve=2, Charlie=3, Frank=4, Grace=4, David=5

> [!TIP]
> ### 🧠 Memory Trick: ROW_NUMBER vs RANK vs DENSE_RANK
> Imagine 2 people tie for 2nd place (80000 salary — Bob and Eve):
> * `ROW_NUMBER()`: 1, **2, 3**, 4 — Always unique, no ties
> * `RANK()`: 1, **2, 2**, 4 — Ties get same rank, SKIPS 3
> * `DENSE_RANK()`: 1, **2, 2**, 3 — Ties get same rank, NO skip

### PARTITION BY
Divides the result set into groups (partitions) and applies the window function within each group independently.

```sql
-- Rank employees BY SALARY within each department
SELECT Emp_Name, Dept_ID, Salary,
    DENSE_RANK() OVER (PARTITION BY Dept_ID ORDER BY Salary DESC) AS Dept_Rank
FROM Employees WHERE Salary IS NOT NULL;
```
**Output (key rows):**
| Emp_Name | Dept_ID | Salary | Dept_Rank |
|:---|:---|:---|:---|
| Alice | 1 | 90000 | 1 |
| Bob | 2 | 80000 | 1 |
| Eve | 2 | 80000 | 1 |
| Charlie | 2 | 75000 | 2 |
| David | 3 | 50000 | 1 |
| Frank | 4 | 60000 | 1 |
| Grace | 4 | 60000 | 1 |

---

## 17. ⭐⭐⭐⭐⭐ Classic Placement Query Patterns

These are the most-asked SQL coding questions in every placement interview.

### 1. 2nd Highest Salary
```sql
-- Method 1: Subquery (works everywhere)
SELECT MAX(Salary) AS Second_Highest
FROM Employees
WHERE Salary < (SELECT MAX(Salary) FROM Employees);
-- Output: 80000

-- Method 2: DENSE_RANK (best for N-th highest)
WITH Ranked AS (
    SELECT Salary, DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employees WHERE Salary IS NOT NULL
)
SELECT Salary FROM Ranked WHERE rnk = 2;
-- Output: 80000
```

### 2. Nth Highest Salary (Generic)
```sql
-- Replace N with any number (e.g., 3 for 3rd highest)
WITH Ranked AS (
    SELECT Emp_Name, Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employees WHERE Salary IS NOT NULL
)
SELECT Emp_Name, Salary FROM Ranked WHERE rnk = 3;
-- For N=3: Output: Charlie (75000)
```

### 3. Find Duplicate Records
```sql
-- Find salaries that appear more than once
SELECT Salary, COUNT(*) AS Count
FROM Employees
WHERE Salary IS NOT NULL
GROUP BY Salary
HAVING COUNT(*) > 1;
-- Output: 80000 (Bob and Eve), 60000 (Frank and Grace)
```

### 4. Remove Duplicate Records (Keep one)
```sql
-- Keep the row with the lowest Emp_ID, delete the rest
WITH CTE AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY Emp_Name ORDER BY Emp_ID) AS rn
    FROM Employees
)
DELETE FROM CTE WHERE rn > 1;
```

### 5. Department-Wise Highest Salary
```sql
-- Method 1: GROUP BY + MAX
SELECT D.Dept_Name, MAX(E.Salary) AS Max_Salary
FROM Employees E
JOIN Departments D ON E.Dept_ID = D.Dept_ID
GROUP BY D.Dept_Name;

-- Method 2: PARTITION BY (shows employee name too)
WITH Ranked AS (
    SELECT Emp_Name, Dept_ID, Salary,
           RANK() OVER (PARTITION BY Dept_ID ORDER BY Salary DESC) AS rnk
    FROM Employees WHERE Salary IS NOT NULL
)
SELECT Emp_Name, Dept_ID, Salary FROM Ranked WHERE rnk = 1;
```

**Output:**
| Dept_Name | Max_Salary |
|:---|:---|
| HR | 90000 |
| IT | 80000 |
| Finance | 50000 |
| Sales | 60000 |

### 6. Employees Earning More Than Their Manager
```sql
SELECT E.Emp_Name AS Employee, E.Salary AS Emp_Salary,
       M.Emp_Name AS Manager,  M.Salary AS Mgr_Salary
FROM Employees E
JOIN Employees M ON E.Manager_ID = M.Emp_ID
WHERE E.Salary > M.Salary;
-- Output: Empty (no employee earns more than their manager in our dataset)
-- Test it: UPDATE Employees SET Salary = 95000 WHERE Emp_ID = 102;
-- Then Bob (95000) > Alice (90000) → Bob appears in result
```

### 7. Top 3 Salaries (Distinct)
```sql
WITH Ranked AS (
    SELECT DISTINCT Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employees WHERE Salary IS NOT NULL
)
SELECT Salary FROM Ranked WHERE rnk <= 3;
-- Output: 90000, 80000, 75000
```

### 8. Consecutive Records with Same Salary (Using LAG)
```sql
-- Find employees where their salary equals the previous employee's salary
SELECT Emp_Name, Salary,
       LAG(Salary) OVER (ORDER BY Emp_ID) AS Prev_Salary
FROM Employees
WHERE Salary = LAG(Salary) OVER (ORDER BY Emp_ID);
```
> [!NOTE]
> `LAG(col)` accesses the value from the **previous row**. `LEAD(col)` accesses the **next row**.

---

## 18. String Functions (MySQL)

String functions are essential for data cleaning and transformation. Highly tested in coding rounds.

| Function | Description | Example | Output |
| :--- | :--- | :--- | :--- |
| `UPPER(str)` | Converts to uppercase | `UPPER('alice')` | `ALICE` |
| `LOWER(str)` | Converts to lowercase | `LOWER('ALICE')` | `alice` |
| `LENGTH(str)` | Returns byte length | `LENGTH('Alice')` | `5` |
| `CHAR_LENGTH(str)` | Returns character count | `CHAR_LENGTH('Alice')` | `5` |
| `SUBSTRING(str, pos, len)` | Extracts substring | `SUBSTRING('Alice', 2, 3)` | `lic` |
| `LEFT(str, n)` | First N characters | `LEFT('Alice', 3)` | `Ali` |
| `RIGHT(str, n)` | Last N characters | `RIGHT('Alice', 3)` | `ice` |
| `TRIM(str)` | Removes leading/trailing spaces | `TRIM('  hi  ')` | `hi` |
| `LTRIM(str)` | Removes leading spaces | `LTRIM('  hi')` | `hi` |
| `RTRIM(str)` | Removes trailing spaces | `RTRIM('hi  ')` | `hi` |
| `REPLACE(str, from, to)` | Replaces substring | `REPLACE('Hello World', 'World', 'SQL')` | `Hello SQL` |
| `CONCAT(s1, s2, ...)` | Joins strings | `CONCAT('Alice', ' - ', 'HR')` | `Alice - HR` |
| `INSTR(str, substr)` | Position of first occurrence | `INSTR('Alice', 'li')` | `2` |
| `LPAD(str, len, pad)` | Left-pads to length | `LPAD('5', 4, '0')` | `0005` |
| `RPAD(str, len, pad)` | Right-pads to length | `RPAD('5', 4, '0')` | `5000` |
| `REVERSE(str)` | Reverses the string | `REVERSE('SQL')` | `LQS` |

```sql
-- Practical Examples
SELECT UPPER(Emp_Name), CHAR_LENGTH(Emp_Name) AS Name_Length
FROM Employees;

-- Extract first name from 'Alice Smith'
SELECT SUBSTRING_INDEX('Alice Smith', ' ', 1) AS First_Name;
-- Output: Alice

-- Pad employee ID to 5 digits: 101 → 00101
SELECT LPAD(Emp_ID, 5, '0') AS Padded_ID FROM Employees;
```

---

## 19. Date and Time Functions (MySQL)

| Function | Description | Example | Output |
| :--- | :--- | :--- | :--- |
| `NOW()` | Current date and time | `NOW()` | `2025-01-15 14:30:00` |
| `CURDATE()` | Current date only | `CURDATE()` | `2025-01-15` |
| `CURTIME()` | Current time only | `CURTIME()` | `14:30:00` |
| `DATE(datetime)` | Extracts date part | `DATE(NOW())` | `2025-01-15` |
| `YEAR(date)` | Extracts year | `YEAR('2025-01-15')` | `2025` |
| `MONTH(date)` | Extracts month | `MONTH('2025-01-15')` | `1` |
| `DAY(date)` | Extracts day | `DAY('2025-01-15')` | `15` |
| `DATEDIFF(d1, d2)` | Days between two dates | `DATEDIFF('2025-01-15', '2025-01-01')` | `14` |
| `DATE_ADD(date, INTERVAL n unit)` | Adds to a date | `DATE_ADD('2025-01-01', INTERVAL 30 DAY)` | `2025-01-31` |
| `DATE_SUB(date, INTERVAL n unit)` | Subtracts from a date | `DATE_SUB('2025-01-31', INTERVAL 1 MONTH)` | `2024-12-31` |
| `DATE_FORMAT(date, format)` | Formats a date | `DATE_FORMAT('2025-01-15', '%d-%b-%Y')` | `15-Jan-2025` |
| `TIMESTAMPDIFF(unit, d1, d2)` | Difference in specified unit | `TIMESTAMPDIFF(YEAR, '2000-01-01', '2025-01-01')` | `25` |
| `EXTRACT(unit FROM date)` | Extracts a date part | `EXTRACT(YEAR FROM '2025-01-15')` | `2025` |

```sql
-- Employees hired more than 5 years ago (assuming a Hire_Date column)
SELECT Emp_Name FROM Employees
WHERE TIMESTAMPDIFF(YEAR, Hire_Date, CURDATE()) > 5;

-- Format today's date
SELECT DATE_FORMAT(CURDATE(), '%d/%m/%Y') AS Formatted_Date;
-- Output: 15/01/2025
```

---

## 20. Mathematical Functions

| Function | Description | Example | Output |
| :--- | :--- | :--- | :--- |
| `ROUND(n, d)` | Rounds to d decimal places | `ROUND(456.567, 2)` | `456.57` |
| `CEIL(n)` / `CEILING(n)` | Rounds UP to nearest integer | `CEIL(4.1)` | `5` |
| `FLOOR(n)` | Rounds DOWN to nearest integer | `FLOOR(4.9)` | `4` |
| `ABS(n)` | Absolute value | `ABS(-50)` | `50` |
| `MOD(n, d)` | Remainder (modulo) | `MOD(10, 3)` | `1` |
| `POWER(n, p)` | n raised to power p | `POWER(2, 10)` | `1024` |
| `SQRT(n)` | Square root | `SQRT(144)` | `12` |
| `TRUNCATE(n, d)` | Truncates to d decimal places (no rounding) | `TRUNCATE(456.567, 2)` | `456.56` |

```sql
-- Round average salary to 2 decimal places
SELECT ROUND(AVG(Salary), 2) AS Avg_Salary FROM Employees;

-- Find employees with odd Emp_IDs
SELECT Emp_Name FROM Employees WHERE MOD(Emp_ID, 2) = 1;
```

---

## 21. Transactions: BEGIN, COMMIT, ROLLBACK, SAVEPOINT

A **Transaction** is a sequence of SQL statements treated as a single unit of work.

```sql
-- Basic Transaction
START TRANSACTION;  -- or BEGIN;

    UPDATE Employees SET Salary = Salary - 5000 WHERE Emp_ID = 101;
    UPDATE Employees SET Salary = Salary + 5000 WHERE Emp_ID = 102;

COMMIT;  -- Make changes permanent

-- If something goes wrong:
ROLLBACK;  -- Undo all changes since START TRANSACTION
```

### SAVEPOINT — Partial Rollback

A SAVEPOINT lets you rollback to a specific point within a transaction without undoing everything.

```sql
START TRANSACTION;

    INSERT INTO Employees VALUES (110, 'Zara', 70000, 1, 101);
    SAVEPOINT after_insert;  -- Mark this point

    UPDATE Employees SET Salary = -1 WHERE Emp_ID = 110;  -- Mistake!

ROLLBACK TO SAVEPOINT after_insert;  -- Undo only the UPDATE, keep the INSERT

COMMIT;  -- Now only the INSERT is committed
```

> [!TIP]
> **Memory Trick:**
> - `COMMIT` = Save progress in a game
> - `ROLLBACK` = Restart from last save
> - `SAVEPOINT` = Create a checkpoint mid-game

---

## 22. CTEs (Common Table Expressions) — WITH Clause

A **CTE** is a named temporary result set that exists only for the duration of a single query. It makes complex queries more readable.

### Basic CTE

```sql
-- Without CTE (hard to read nested subquery)
SELECT * FROM (
    SELECT Emp_Name, Salary, DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employees WHERE Salary IS NOT NULL
) AS ranked WHERE rnk = 2;

-- With CTE (clean and readable)
WITH RankedSalaries AS (
    SELECT Emp_Name, Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) AS rnk
    FROM Employees WHERE Salary IS NOT NULL
)
SELECT Emp_Name, Salary FROM RankedSalaries WHERE rnk = 2;
-- Output: Bob (80000), Eve (80000)
```

### Multiple CTEs

```sql
WITH
    IT_Employees AS (
        SELECT * FROM Employees WHERE Dept_ID = 2
    ),
    IT_Stats AS (
        SELECT AVG(Salary) AS Avg_IT_Salary FROM IT_Employees
    )
SELECT E.Emp_Name, E.Salary, S.Avg_IT_Salary
FROM IT_Employees E, IT_Stats S;
```

### ⭐⭐⭐⭐⭐ Recursive CTE (Very Important for Interviews!)

A **Recursive CTE** calls itself and is used for hierarchical data (org charts, category trees, folder structures).

**Use Case:** Find all employees under a manager (the entire org hierarchy).

```sql
-- Find Alice's entire reporting chain (all employees reporting to Alice, directly or indirectly)
WITH RECURSIVE OrgChart AS (
    -- Anchor member: Start with Alice (Emp_ID = 101)
    SELECT Emp_ID, Emp_Name, Manager_ID, 0 AS Level
    FROM Employees
    WHERE Emp_ID = 101

    UNION ALL

    -- Recursive member: Find employees whose manager is already in the CTE
    SELECT E.Emp_ID, E.Emp_Name, E.Manager_ID, O.Level + 1
    FROM Employees E
    INNER JOIN OrgChart O ON E.Manager_ID = O.Emp_ID
)
SELECT Emp_ID, Emp_Name, Level FROM OrgChart;
```

**Output:**
| Emp_ID | Emp_Name | Level |
|:---|:---|:---|
| 101 | Alice | 0 (top) |
| 102 | Bob | 1 |
| 103 | Charlie | 1 |
| 105 | Eve | 1 |
| 108 | Henry | 1 |
| 104 | David | 2 |
| 106 | Frank | 2 |
| 107 | Grace | 2 |

> [!IMPORTANT]
> **Recursive CTE Structure:**
> 1. **Anchor Member:** The base case (starting row).
> 2. `UNION ALL`
> 3. **Recursive Member:** References the CTE itself to get the next level.
> MySQL supports Recursive CTEs from version 8.0+.

---

## 23. Stored Procedures

A **Stored Procedure** is a precompiled, reusable block of SQL stored in the database. Call it with `CALL`.

```sql
-- Create a stored procedure to give a department a salary raise
DELIMITER $$

CREATE PROCEDURE GiveSalaryRaise(
    IN dept_id INT,        -- IN: input parameter (read-only inside proc)
    IN raise_pct DECIMAL(5,2)  -- percentage raise
)
BEGIN
    UPDATE Employees
    SET Salary = Salary * (1 + raise_pct / 100)
    WHERE Dept_ID = dept_id AND Salary IS NOT NULL;
    
    SELECT CONCAT('Salary updated for Dept_ID: ', dept_id) AS Message;
END$$

DELIMITER ;

-- Call the procedure
CALL GiveSalaryRaise(2, 10);  -- Give IT department a 10% raise
```

### IN vs OUT vs INOUT Parameters

| Parameter Type | Description |
| :--- | :--- |
| `IN` | Read-only input value. Changes inside procedure do NOT affect the caller. |
| `OUT` | Output value. Procedure sets it; caller can read it after the call. |
| `INOUT` | Both input and output. Caller passes a value in; procedure can modify it. |

```sql
-- Procedure with OUT parameter
DELIMITER $$
CREATE PROCEDURE GetDeptHeadcount(
    IN dept_id INT,
    OUT headcount INT
)
BEGIN
    SELECT COUNT(*) INTO headcount
    FROM Employees
    WHERE Dept_ID = dept_id;
END$$
DELIMITER ;

-- Calling with OUT
CALL GetDeptHeadcount(2, @count);
SELECT @count;  -- Output: 3
```

> [!TIP]
> **Interview Answer:** Stored Procedures improve performance (precompiled), reduce network traffic (only CALL sent, not full SQL), and improve security (users call procedures without direct table access).

---

## 24. User-Defined Functions (UDF)

A **Function** is similar to a Stored Procedure but MUST return a single value and can be used inside a SELECT statement.

```sql
DELIMITER $$

CREATE FUNCTION GetSalaryGrade(salary DECIMAL(10,2))
RETURNS VARCHAR(10)
DETERMINISTIC   -- Same input always produces same output
BEGIN
    DECLARE grade VARCHAR(10);
    IF salary >= 80000 THEN SET grade = 'High';
    ELSEIF salary >= 60000 THEN SET grade = 'Medium';
    ELSEIF salary IS NULL THEN SET grade = 'Not Set';
    ELSE SET grade = 'Low';
    END IF;
    RETURN grade;
END$$

DELIMITER ;

-- Use in SELECT (like a built-in function)
SELECT Emp_Name, Salary, GetSalaryGrade(Salary) AS Grade
FROM Employees;
```

| Feature | Stored Procedure | Function |
| :--- | :--- | :--- |
| Returns value | Optional (can return 0 or many values) | Must return exactly 1 value |
| Used in SELECT | ❌ Cannot be called in SELECT | ✅ Can be used in SELECT |
| Called with | `CALL proc_name()` | Used in expression: `SELECT func_name()` |
| Transaction control | Can use COMMIT/ROLLBACK | Cannot |

---

## 25. Triggers

A **Trigger** is a special stored procedure that automatically fires in response to a DML event (`INSERT`, `UPDATE`, `DELETE`) on a table.

**Timing:** `BEFORE` (fires before the DML) or `AFTER` (fires after the DML).

```sql
-- AFTER INSERT Trigger: Log every new employee into an audit table
CREATE TABLE Audit_Log (
    Log_ID     INT AUTO_INCREMENT PRIMARY KEY,
    Action     VARCHAR(50),
    Emp_ID     INT,
    Log_Time   DATETIME DEFAULT NOW()
);

DELIMITER $$

CREATE TRIGGER after_employee_insert
AFTER INSERT ON Employees
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(Action, Emp_ID)
    VALUES ('INSERT', NEW.Emp_ID);
END$$

-- BEFORE UPDATE Trigger: Prevent salary from being set below 0
CREATE TRIGGER before_salary_update
BEFORE UPDATE ON Employees
FOR EACH ROW
BEGIN
    IF NEW.Salary < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Salary cannot be negative!';
    END IF;
END$$

DELIMITER ;
```

> [!NOTE]
> **`NEW` and `OLD` in Triggers:**
> - `NEW.column` = The new value being inserted/updated.
> - `OLD.column` = The old value before the update/delete.
> - `INSERT` triggers: only `NEW` is available.
> - `DELETE` triggers: only `OLD` is available.
> - `UPDATE` triggers: both `NEW` and `OLD` are available.

---

## 26. More Window Functions: NTILE, FIRST_VALUE, LAST_VALUE

### NTILE(n)
Divides rows into `n` equal buckets and assigns a bucket number to each row.

```sql
-- Divide employees into 4 salary quartiles
SELECT Emp_Name, Salary,
    NTILE(4) OVER (ORDER BY Salary DESC) AS Quartile
FROM Employees WHERE Salary IS NOT NULL;
```

**Output:**
| Emp_Name | Salary | Quartile |
|:---|:---|:---|
| Alice | 90000 | 1 (top 25%) |
| Bob | 80000 | 1 |
| Eve | 80000 | 2 |
| Charlie | 75000 | 2 |
| Frank | 60000 | 3 |
| Grace | 60000 | 3 |
| David | 50000 | 4 (bottom 25%) |

### FIRST_VALUE() and LAST_VALUE()

```sql
-- Show each employee's salary alongside the highest salary in their department
SELECT Emp_Name, Dept_ID, Salary,
    FIRST_VALUE(Salary) OVER (PARTITION BY Dept_ID ORDER BY Salary DESC) AS Dept_Max_Salary,
    LAST_VALUE(Salary)  OVER (PARTITION BY Dept_ID ORDER BY Salary DESC
                              ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS Dept_Min_Salary
FROM Employees WHERE Salary IS NOT NULL;
```

> [!WARNING]
> `LAST_VALUE` requires `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` to see the actual last value in the window. Without this, it only looks at rows up to the current row.

---

## 27. ROLLUP and CUBE (Subtotals and Grand Totals)

### GROUP BY WITH ROLLUP
Adds subtotals and a grand total row automatically.

```sql
SELECT Dept_ID, COUNT(*) AS Headcount, SUM(Salary) AS Total_Salary
FROM Employees
WHERE Salary IS NOT NULL
GROUP BY Dept_ID WITH ROLLUP;
```

**Output:**
| Dept_ID | Headcount | Total_Salary |
|:---|:---|:---|
| 1 | 1 | 90000 |
| 2 | 3 | 235000 |
| 3 | 1 | 50000 |
| 4 | 2 | 120000 |
| **NULL** | **7** | **495000** ← Grand Total |

> [!NOTE]
> The `NULL` in the last row represents the grand total (all groups combined). Use `COALESCE(Dept_ID, 'ALL')` to show "ALL" instead of NULL.

---

## 28. EXPLAIN — Query Optimization

`EXPLAIN` shows how MySQL executes a query — essential for performance tuning interviews.

```sql
EXPLAIN SELECT * FROM Employees WHERE Dept_ID = 2;
```

**Key columns in EXPLAIN output:**
| Column | What to Look For |
| :--- | :--- |
| `type` | `ALL` = Full scan (bad for large tables). `ref`/`range`/`const` = Index used (good). |
| `rows` | Estimated number of rows examined. Lower is better. |
| `key` | The index actually used (NULL means no index used). |
| `Extra` | `Using filesort` = Sorting in memory (can be slow). `Using index` = Index covers the query (fast). |

```sql
-- Without index: type=ALL, key=NULL (full scan)
EXPLAIN SELECT * FROM Employees WHERE Dept_ID = 2;

-- After creating index:
CREATE INDEX idx_dept ON Employees(Dept_ID);

-- With index: type=ref, key=idx_dept (efficient!)
EXPLAIN SELECT * FROM Employees WHERE Dept_ID = 2;
```

---

## 29. More Classic Placement Query Patterns

### 9. Running Total (Cumulative Sum)
```sql
SELECT Emp_Name, Salary,
    SUM(Salary) OVER (ORDER BY Emp_ID) AS Running_Total
FROM Employees WHERE Salary IS NOT NULL;
```

### 10. Moving Average (3-row window)
```sql
SELECT Emp_Name, Salary,
    AVG(Salary) OVER (ORDER BY Emp_ID ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS Moving_Avg
FROM Employees WHERE Salary IS NOT NULL;
```

### 11. Employees Without a Department (Orphan Records)
```sql
-- Using LEFT JOIN — more efficient than NOT IN with NULLs
SELECT E.Emp_Name
FROM Employees E
LEFT JOIN Departments D ON E.Dept_ID = D.Dept_ID
WHERE D.Dept_ID IS NULL;
```

### 12. Departments With No Employees
```sql
SELECT D.Dept_Name
FROM Departments D
LEFT JOIN Employees E ON D.Dept_ID = E.Dept_ID
WHERE E.Emp_ID IS NULL;
```

### 13. Find All Managers (Employees Who Manage Others)
```sql
SELECT DISTINCT M.Emp_Name AS Manager
FROM Employees E
JOIN Employees M ON E.Manager_ID = M.Emp_ID;
-- Output: Alice, Bob
```

### 14. Employees Who Are NOT Managers
```sql
SELECT Emp_Name FROM Employees
WHERE Emp_ID NOT IN (
    SELECT DISTINCT Manager_ID FROM Employees WHERE Manager_ID IS NOT NULL
);
-- Output: Charlie, David, Eve, Frank, Grace, Henry
```

### 15. Salary Greater Than Department Average
```sql
SELECT E.Emp_Name, E.Salary, D.Avg_Dept_Salary
FROM Employees E
JOIN (
    SELECT Dept_ID, AVG(Salary) AS Avg_Dept_Salary
    FROM Employees GROUP BY Dept_ID
) D ON E.Dept_ID = D.Dept_ID
WHERE E.Salary > D.Avg_Dept_Salary;
```

### 16. Pivot Table: Count employees per department in columns
```sql
SELECT
    SUM(CASE WHEN Dept_ID = 1 THEN 1 ELSE 0 END) AS HR_Count,
    SUM(CASE WHEN Dept_ID = 2 THEN 1 ELSE 0 END) AS IT_Count,
    SUM(CASE WHEN Dept_ID = 3 THEN 1 ELSE 0 END) AS Finance_Count,
    SUM(CASE WHEN Dept_ID = 4 THEN 1 ELSE 0 END) AS Sales_Count
FROM Employees;
```

### 17. Delete Duplicate Emails (Classic LeetCode #196)
```sql
-- Keep the row with the smallest ID, delete the rest
DELETE E1 FROM Employees E1
INNER JOIN Employees E2
WHERE E1.Emp_ID > E2.Emp_ID AND E1.Emp_Name = E2.Emp_Name;
```

---



## ⚡ 5-Minute Quick Revision

1. **SELECT / WHERE / DISTINCT / ORDER BY / LIMIT** — basic retrieval and filtering.
2. **AND, OR, NOT / IN / BETWEEN / LIKE** — logical and pattern filters.
3. **IS NULL / IS NOT NULL / COALESCE** — NULL handling. Never use `= NULL`.
4. **Aggregate Functions** — COUNT/SUM/AVG/MIN/MAX ignore NULLs (except COUNT(*)).
5. **GROUP BY** — groups rows. **HAVING** — filters groups. Never use aggregate in WHERE.
6. **Constraints** — PK (unique+notnull), FK (referential), UNIQUE, NOT NULL, CHECK, DEFAULT.
7. **JOINS** — INNER (both match), LEFT (all left), RIGHT (all right), FULL (all both), CROSS (Cartesian), SELF (same table).
8. **UNION** (dedup) vs **UNION ALL** (keep all). INTERSECT (common). EXCEPT/MINUS (difference).
9. **EXISTS** (any row?), **ANY** (any match?), **ALL** (all match?).
10. **CASE** — SQL if-then-else. **COALESCE** — first non-NULL.
11. **VIEW** — virtual table, no physical storage.
12. **INDEX** — speeds up SELECT, slows INSERT/UPDATE/DELETE.
13. **ROW_NUMBER** (always unique) vs **RANK** (ties + gaps) vs **DENSE_RANK** (ties, no gaps).
14. **PARTITION BY** — apply window function per group independently.

## 🤔 Common Mistakes in Interviews

1. **Using `= NULL` instead of `IS NULL`** — SQL will always return empty result with `= NULL`.
2. **Using aggregate in WHERE** — Use HAVING for aggregates, WHERE for row-level filters.
3. **RANK vs DENSE_RANK confusion** — Remember RANK skips numbers, DENSE_RANK does not.
4. **Forgetting SELF JOIN needs aliases** — `FROM Employees E JOIN Employees M` — both must have different aliases.
5. **UNION removes duplicates, UNION ALL keeps them** — UNION is slower due to dedup step.
6. **FULL OUTER JOIN not supported in MySQL natively** — simulate with LEFT UNION RIGHT.

## 📝 Top 10 Placement MCQs

**Q1. Which clause is used to filter results AFTER aggregation?**
A) WHERE  B) HAVING  C) GROUP BY  D) ORDER BY
> **Answer: B) HAVING.**

**Q2. What does `SELECT COUNT(*) FROM Employees` return if Henry has NULL salary?**
A) 7  B) 8  C) 0  D) NULL
> **Answer: B) 8.** COUNT(*) counts ALL rows including NULLs.

**Q3. CROSS JOIN between 5 rows and 4 rows produces how many rows?**
A) 9  B) 20  C) 5  D) 4
> **Answer: B) 20.** Cartesian product: 5 × 4 = 20.

**Q4. Which window function does NOT produce gaps after ties?**
A) RANK()  B) ROW_NUMBER()  C) DENSE_RANK()  D) NTILE()
> **Answer: C) DENSE_RANK().**

**Q5. Which of the following is used to check if a subquery returns any row?**
A) ANY  B) ALL  C) EXISTS  D) IN
> **Answer: C) EXISTS.**

**Q6. What is the correct way to check for NULL in SQL?**
A) `= NULL`  B) `IS NULL`  C) `== NULL`  D) `EQUALS NULL`
> **Answer: B) IS NULL.**

**Q7. UNION vs UNION ALL — which is faster?**
A) UNION  B) UNION ALL  C) Both are equal  D) Depends on the table
> **Answer: B) UNION ALL.** No duplicate removal step.

**Q8. A view in SQL is:**
A) A copy of data stored on disk
B) A virtual table based on a SELECT query
C) A stored procedure
D) An index on a table
> **Answer: B) A virtual table based on a SELECT query.**

**Q9. Which function returns the value of the previous row's column?**
A) LEAD()  B) LAG()  C) FIRST_VALUE()  D) RANK()
> **Answer: B) LAG().**

**Q10. Which SQL set operator removes duplicates by default?**
A) UNION ALL  B) INTERSECT  C) UNION  D) EXCEPT
> **Answer: C) UNION.** (UNION ALL keeps duplicates; INTERSECT and EXCEPT also deduplicate, but UNION is the standard answer here.)

## 🎤 Top 10 Interview Questions

1. **What is the difference between WHERE and HAVING?**
   * WHERE filters individual rows before grouping. HAVING filters groups after GROUP BY. Aggregate functions (like MAX, COUNT) cannot be used in WHERE.

2. **Explain RANK(), DENSE_RANK(), and ROW_NUMBER() with an example.**
   * ROW_NUMBER: always unique (1,2,3). RANK: same for ties, skips next number (1,2,2,4). DENSE_RANK: same for ties, no skip (1,2,2,3).

3. **What is a SELF JOIN? When do you use it?**
   * A self join joins a table to itself using two different aliases. Classic use: finding an employee's manager, who is also an employee in the same table.

4. **What is the difference between UNION and UNION ALL?**
   * UNION combines results from two queries and removes duplicates (slower). UNION ALL combines results and keeps all duplicates (faster).

5. **How do you find the Nth highest salary?**
   * Use DENSE_RANK() OVER (ORDER BY Salary DESC) in a CTE, then filter WHERE rnk = N. DENSE_RANK handles ties correctly.

6. **What is a View? Why use it over a direct query?**
   * A view is a saved SELECT query treated as a virtual table. Use it for security (restrict column access), simplicity (hide complex JOINs), and consistency (same logic reused everywhere).

7. **What is COALESCE? How is it different from ISNULL?**
   * COALESCE(a,b,c,...) returns the first non-NULL value and accepts multiple arguments. It is ANSI SQL standard. ISNULL(a,b) is SQL Server-specific and accepts only two arguments.

8. **What is the difference between DELETE and TRUNCATE?**
   * DELETE is DML, logs each row, supports WHERE, can be rolled back. TRUNCATE is DDL, deallocates pages, no WHERE, cannot be rolled back in MySQL (can be in PostgreSQL inside a transaction).

9. **What is the difference between EXISTS and IN?**
   * EXISTS checks if a subquery returns any row (stops at first match, more efficient for large datasets). IN checks if a value matches any value in a list/subquery result (fetches all values first).

10. **Write a query to find employees who earn more than the average salary.**
    ```sql
    SELECT Emp_Name, Salary
    FROM Employees
    WHERE Salary > (SELECT AVG(Salary) FROM Employees);
    ```

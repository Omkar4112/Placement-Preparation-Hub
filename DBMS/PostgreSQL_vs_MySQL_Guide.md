# ⭐⭐⭐ PostgreSQL vs MySQL — Placement Guide

This file covers key differences between PostgreSQL and MySQL, important PostgreSQL-specific features, and placement interview questions.

---

## 1. What is PostgreSQL?

**📘 Easy Definition**
PostgreSQL (also called Postgres) is a free, open-source, advanced relational database management system.

**💼 Interview Definition**
PostgreSQL is an open-source Object-Relational Database Management System (ORDBMS) that emphasizes extensibility and SQL standards compliance. It supports advanced data types, full ACID compliance, and complex queries.

> [!NOTE]
> PostgreSQL is used by companies like Apple, Instagram, Spotify, Reddit, and Twitch. It is increasingly popular in product-based company interviews.

---

## 2. PostgreSQL vs MySQL — Complete Comparison Table

| Feature | MySQL | PostgreSQL |
|:---|:---|:---|
| **Type** | RDBMS | ORDBMS (Object-Relational) |
| **License** | Open-source (GPL) | Open-source (PostgreSQL License — more permissive) |
| **FULL OUTER JOIN** | ❌ Not supported natively | ✅ Supported |
| **INTERSECT** | ❌ Only from v8.0.31+ | ✅ Supported |
| **EXCEPT** | ❌ Only from v8.0.31+ | ✅ Supported |
| **TRUNCATE rollback** | ❌ Auto-commits, cannot rollback | ✅ Can rollback inside a transaction |
| **Window Functions** | ✅ From v8.0 only | ✅ Supported (much earlier) |
| **CTEs (WITH clause)** | ✅ From v8.0 only | ✅ Supported (much earlier) |
| **JSON Support** | JSON type (basic) | JSONB (binary, indexable, faster queries) |
| **Arrays** | ❌ Not supported | ✅ Native array data type |
| **Auto-increment** | `AUTO_INCREMENT` | `SERIAL`, `BIGSERIAL`, or `GENERATED AS IDENTITY` |
| **Case sensitivity** | Case-insensitive by default | Case-sensitive by default |
| **String Concat** | `CONCAT(a, b)` only | Both `CONCAT(a, b)` and `a \|\| b` operator |
| **ILIKE** | ❌ (LIKE is case-insensitive by default) | ✅ `ILIKE` for case-insensitive LIKE |
| **Regex** | `REGEXP` or `RLIKE` | `~` (case-sensitive), `~*` (case-insensitive) |
| **Stored Procedures** | ✅ Supported | ✅ Supported (also supports functions returning sets) |
| **Performance** | Faster for simple read/write | Faster for complex queries and analytics |
| **Partial Indexes** | ❌ Not supported | ✅ Supported |
| **Materialized Views** | ❌ Not supported | ✅ Supported |
| **Inheritance** | ❌ Not supported | ✅ Table inheritance supported |
| **Check Constraints** | Parsed but not enforced (before v8.0.16) | ✅ Strictly enforced |

---

## 3. Key PostgreSQL-Only Features

### 3.1 SERIAL / AUTO-INCREMENT
```sql
-- MySQL way
CREATE TABLE Students (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(50)
);

-- PostgreSQL way (SERIAL)
CREATE TABLE Students (
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(50)
);

-- PostgreSQL modern way (GENERATED AS IDENTITY — SQL standard)
CREATE TABLE Students (
    ID INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    Name VARCHAR(50)
);
```

### 3.2 TRUNCATE Can Be Rolled Back
```sql
BEGIN;
    TRUNCATE TABLE Employees;
    -- Realize it was a mistake!
ROLLBACK;
-- In PostgreSQL: Employees table is RESTORED
-- In MySQL: Data is GONE (auto-committed)
```

### 3.3 RETURNING Clause (Very Useful!)
Get the inserted/updated/deleted rows back immediately.
```sql
-- Insert and immediately see the generated ID
INSERT INTO Students (Name) VALUES ('Alice')
RETURNING ID, Name;
-- Output: ID=1, Name=Alice

-- Delete and see what was deleted
DELETE FROM Students WHERE ID = 1
RETURNING *;
```
> MySQL does NOT have `RETURNING`. You must use `LAST_INSERT_ID()` for inserts.

### 3.4 JSONB — Binary JSON (PostgreSQL Superpower)
```sql
CREATE TABLE Orders (
    ID   SERIAL PRIMARY KEY,
    Info JSONB
);

INSERT INTO Orders (Info) VALUES ('{"customer": "Alice", "items": ["book", "pen"], "total": 450}');

-- Query inside JSON
SELECT Info->>'customer' AS Customer FROM Orders;
-- Output: Alice

-- Filter by JSON field
SELECT * FROM Orders WHERE Info->>'customer' = 'Alice';
```
> MySQL's JSON type is slower for queries. PostgreSQL's JSONB stores data in binary format and can be indexed.

### 3.5 Array Data Type
```sql
CREATE TABLE Students (
    ID    SERIAL PRIMARY KEY,
    Name  VARCHAR(50),
    Marks INT[]  -- Array of integers
);

INSERT INTO Students (Name, Marks) VALUES ('Alice', ARRAY[85, 90, 78]);

-- Query: Find students with any mark above 88
SELECT Name FROM Students WHERE 85 = ANY(Marks);
```

### 3.6 String Concatenation with ||
```sql
-- Both work in PostgreSQL
SELECT CONCAT(Emp_Name, ' - ', Dept_ID) FROM Employees;
SELECT Emp_Name || ' - ' || Dept_ID FROM Employees;

-- MySQL only supports CONCAT()
```

### 3.7 ILIKE (Case-Insensitive LIKE)
```sql
-- PostgreSQL: Find names regardless of case
SELECT * FROM Employees WHERE Emp_Name ILIKE 'alice';
-- Output: Alice (matches even though 'alice' is lowercase)

-- MySQL: LIKE is case-insensitive by default for most collations
SELECT * FROM Employees WHERE Emp_Name LIKE 'alice';
-- Output: Alice (MySQL is case-insensitive by default)
```

### 3.8 Materialized Views
A **Materialized View** stores the result physically on disk (unlike a regular view which re-runs every time).
```sql
-- Create a materialized view (stores data physically)
CREATE MATERIALIZED VIEW high_earners AS
SELECT Emp_Name, Salary FROM Employees WHERE Salary > 70000;

-- Refresh when underlying data changes
REFRESH MATERIALIZED VIEW high_earners;

-- Query like a normal table
SELECT * FROM high_earners;
```
> **Regular View:** Re-runs the query every time. Slow for complex queries.
> **Materialized View:** Stores results. Fast to query. Must be manually refreshed.

### 3.9 Partial Indexes
Create an index only on a subset of rows.
```sql
-- Index only on active employees (WHERE condition)
CREATE INDEX idx_active_salary ON Employees(Salary)
WHERE Salary IS NOT NULL;
-- Smaller, faster index than indexing all rows
```

---

## 4. Important Syntax Differences — Side by Side

| Operation | MySQL | PostgreSQL |
|:---|:---|:---|
| **Auto-increment** | `AUTO_INCREMENT` | `SERIAL` or `GENERATED AS IDENTITY` |
| **Limit rows** | `LIMIT 10` | `LIMIT 10` (same) |
| **Top N rows** | `LIMIT 10` | `LIMIT 10` or `FETCH FIRST 10 ROWS ONLY` |
| **Modify column** | `ALTER TABLE t MODIFY col VARCHAR(100)` | `ALTER TABLE t ALTER COLUMN col TYPE VARCHAR(100)` |
| **String concat** | `CONCAT(a, b)` | `a \|\| b` or `CONCAT(a, b)` |
| **Current date** | `NOW()` or `CURDATE()` | `NOW()` or `CURRENT_DATE` |
| **If-null** | `IFNULL(a, b)` | `COALESCE(a, b)` (COALESCE works in both) |
| **Show tables** | `SHOW TABLES;` | `\dt` (psql) or `SELECT tablename FROM pg_tables;` |
| **Show databases** | `SHOW DATABASES;` | `\l` (psql) or `SELECT datname FROM pg_database;` |
| **Regex match** | `col REGEXP 'pattern'` | `col ~ 'pattern'` |
| **Case-insensitive LIKE** | `LIKE` (default) | `ILIKE` |

---

## 5. What Stays the Same in Both

> [!TIP]
> For placement MCQs, if the question does not mention a specific database, these standard SQL features work identically in both.

- All basic SELECT, WHERE, ORDER BY, LIMIT queries
- INNER JOIN, LEFT JOIN, RIGHT JOIN syntax
- GROUP BY and HAVING
- All aggregate functions (COUNT, SUM, AVG, MIN, MAX)
- Subqueries, EXISTS, IN, ANY, ALL
- CASE expressions
- COALESCE (standard SQL, works in both)
- Window functions: ROW_NUMBER(), RANK(), DENSE_RANK(), PARTITION BY (both support, MySQL from v8.0)
- CTEs with `WITH` (both support, MySQL from v8.0)
- CREATE, ALTER, DROP, INSERT, UPDATE, DELETE syntax

---

## 6. ⭐ Placement Interview Questions

### Theory Questions

**Q1. What is the difference between MySQL and PostgreSQL?**
> MySQL is an RDBMS focused on simplicity and speed for web applications. PostgreSQL is an ORDBMS that emphasizes SQL standards compliance, extensibility, and support for advanced data types like JSONB and Arrays. Key differences: PostgreSQL supports FULL OUTER JOIN, INTERSECT, EXCEPT, TRUNCATE rollback, JSONB, Arrays, and Materialized Views natively, while MySQL does not (or added them only in recent versions).

**Q2. Can TRUNCATE be rolled back?**
> In PostgreSQL: YES — if TRUNCATE is executed inside a `BEGIN...ROLLBACK` transaction block, it can be rolled back. In MySQL: NO — TRUNCATE is auto-committed and cannot be rolled back. For placement MCQs, the standard expected answer is "TRUNCATE cannot be rolled back" (MySQL behavior).

**Q3. What is JSONB in PostgreSQL?**
> JSONB is a binary JSON format in PostgreSQL that stores JSON data in a decomposed binary format. It is faster to query than the regular JSON type because it doesn't need to re-parse the JSON on every read. JSONB also supports indexing on JSON fields, making searches extremely fast.

**Q4. What is a Materialized View? How is it different from a regular View?**
> A regular View is a virtual table — it stores the SQL query, not the data. Every time you query it, the underlying SELECT runs again. A Materialized View stores the actual result set physically on disk. It is much faster to query but requires manual refresh (`REFRESH MATERIALIZED VIEW`) when underlying data changes. Materialized Views are a PostgreSQL feature; MySQL does not support them.

**Q5. What is the difference between UNION and EXCEPT in PostgreSQL?**
> UNION combines results of two queries and removes duplicates. EXCEPT returns rows from the first query that do NOT appear in the second query result. EXCEPT is the PostgreSQL/SQL Server equivalent of Oracle's MINUS. In MySQL, EXCEPT was added only from v8.0.31.

---

### MCQs

**Q1. Which of the following is NOT supported natively in MySQL (before v8.0)?**
A) INNER JOIN
B) FULL OUTER JOIN ⭐
C) LEFT JOIN
D) CROSS JOIN
> **Answer: B) FULL OUTER JOIN.** MySQL does not support FULL OUTER JOIN natively. Use `LEFT JOIN UNION RIGHT JOIN` as a workaround.

**Q2. In PostgreSQL, TRUNCATE inside a transaction:**
A) Cannot be rolled back
B) Can be rolled back ⭐
C) Causes a deadlock
D) Is not allowed inside a transaction
> **Answer: B) Can be rolled back.** Unlike MySQL, PostgreSQL treats TRUNCATE as a transactional DDL statement.

**Q3. Which PostgreSQL data type stores JSON in binary format with indexing support?**
A) JSON
B) TEXT
C) JSONB ⭐
D) BLOB
> **Answer: C) JSONB.**

**Q4. What is the PostgreSQL equivalent of MySQL's `AUTO_INCREMENT`?**
A) IDENTITY
B) SEQUENCE
C) SERIAL ⭐
D) INCREMENT
> **Answer: C) SERIAL** (or `GENERATED AS IDENTITY` in modern PostgreSQL).

**Q5. Which clause is unique to PostgreSQL that returns the affected rows after INSERT/UPDATE/DELETE?**
A) OUTPUT
B) RETURNING ⭐
C) FETCH
D) RESULT
> **Answer: B) RETURNING.** SQL Server uses `OUTPUT`. MySQL has no equivalent.

**Q6. Which of the following is a case-insensitive LIKE operator in PostgreSQL?**
A) LIKE
B) RLIKE
C) ILIKE ⭐
D) SLIKE
> **Answer: C) ILIKE.** MySQL's LIKE is case-insensitive by default, so it doesn't need ILIKE.

**Q7. What does `REFRESH MATERIALIZED VIEW` do?**
A) Creates a new materialized view
B) Deletes a materialized view
C) Updates the stored data of a materialized view with fresh query results ⭐
D) Converts a view to a materialized view
> **Answer: C.**

**Q8. Which PostgreSQL operator is used for pattern matching with regex (case-sensitive)?**
A) REGEXP
B) RLIKE
C) ~  ⭐
D) MATCH
> **Answer: C) ~** (tilde). Use `~*` for case-insensitive. MySQL uses `REGEXP`.

---

## 7. ⚡ 2-Minute Quick Revision

1. **PostgreSQL = ORDBMS** (Object-Relational). MySQL = RDBMS.
2. **FULL OUTER JOIN** — PostgreSQL ✅ | MySQL ❌ (use LEFT UNION RIGHT).
3. **INTERSECT / EXCEPT** — PostgreSQL ✅ | MySQL from v8.0.31+ only.
4. **TRUNCATE rollback** — PostgreSQL ✅ | MySQL ❌.
5. **JSONB** — PostgreSQL's binary JSON. Faster, indexable. MySQL has basic JSON only.
6. **RETURNING** — PostgreSQL's way to get back rows after INSERT/UPDATE/DELETE.
7. **SERIAL** — PostgreSQL's auto-increment. MySQL uses `AUTO_INCREMENT`.
8. **ILIKE** — PostgreSQL's case-insensitive LIKE.
9. **||** — PostgreSQL string concat operator. MySQL only has `CONCAT()`.
10. **Materialized Views** — PostgreSQL stores results physically. Must `REFRESH`. MySQL doesn't have this.
11. **Arrays** — PostgreSQL supports array columns natively. MySQL doesn't.
12. **Partial Indexes** — PostgreSQL can index a subset of rows. MySQL can't.
13. **Standard SQL (joins, aggregates, window functions, CTEs, CASE)** — Same in both.

# 🏆 Ultimate Revision and Practice Handbook ⭐⭐⭐⭐⭐

This resource consolidates all the high-level study sheets, master practice question sets, and last-minute revision notes for placement preparation.

---

## 1. The Ultimate DBMS Revision Sheet ⭐⭐⭐⭐⭐

### 🏛️ Schema & Structural Design
*   **Three Abstraction Levels:** View (External) -> Conceptual (Logical) -> Internal (Physical).
*   **Data Independence:**
    *   *Physical:* Modify physical storage (SSD vs. HDD, index files) without affecting logical schemas.
    *   *Logical:* Modify conceptual schemas (adding attributes, partitioning tables) without affecting user views.
*   **Metadata Catalog:** A set of read-only system tables containing database structure definitions.

### 🔑 Keys Cheat Sheet
*   **Super Key (SK):** Any set of columns that uniquely identifies a row.
*   **Candidate Key (CK):** A minimal super key. Removing any column destroys uniqueness.
*   **Primary Key (PK):** The candidate key selected to uniquely identify rows. Cannot contain NULLs.
*   **Alternate Key (AK):** All candidate keys not selected as the primary key ($AK = CK - PK$).
*   **Foreign Key (FK):** Points to a primary key in a parent table. Enforces referential integrity.
*   **Composite Key:** A key composed of more than one column.

### 📐 Normalization Cheat Sheet
*   **1NF:** Atomic attribute values only. No composite or multivalued attributes.
*   **2NF:** In 1NF + No **Partial Dependency** ($\text{Part of Candidate Key} \rightarrow \text{Non-Prime}$).
*   **3NF:** In 2NF + No **Transitive Dependency** ($X \rightarrow Y \Rightarrow X \text{ is Super Key or } Y \text{ is Prime}$).
*   **BCNF:** For every non-trivial $X \rightarrow Y$, $X$ must be a Super Key.
*   **Lossless-Join Test:** $R_1 \cap R_2 \rightarrow R_1 \text{ or } R_1 \cap R_2 \rightarrow R_2$.
*   **Dependency Preservation:** $(F_1 \cup F_2)^+ \equiv F^+$.

### ⚙️ Concurrency & Locks
*   **ACID:** Atomicity (Transaction Manager), Consistency (Programmer/Constraints), Isolation (Concurrency Control), Durability (Recovery Manager).
*   **2PL:** Growing phase (locks acquired, none released) -> Shrinking phase (locks released, none acquired).
*   **Strict 2PL:** Hold all Exclusive locks until commit to prevent cascading rollbacks.
*   **Deadlock Prevention:** Wait-Die (older waits, younger dies) and Wound-Wait (older aborts younger, younger waits).

---

## 2. The Ultimate SQL Revision Sheet ⭐⭐⭐⭐⭐

### 📋 Logical Query Execution Order
$$\text{FROM} \rightarrow \text{JOIN} \rightarrow \text{ON} \rightarrow \text{WHERE} \rightarrow \text{GROUP BY} \rightarrow \text{HAVING} \rightarrow \text{SELECT} \rightarrow \text{DISTINCT} \rightarrow \text{ORDER BY} \rightarrow \text{LIMIT}$$

### 💻 Core Syntax Templates

#### Joins
*   **Inner Join:** Matches keys in both tables.
*   **Left Join:** All rows from left table, with NULLs for non-matching right columns.
*   **Self Join:** Join a table to itself using distinct aliases (e.g., matching employees to managers).

#### Window Functions
*   `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC)`
*   `RANK() OVER (ORDER BY salary DESC)` (leaves gaps after ties: `1, 2, 2, 4`)
*   `DENSE_RANK() OVER (ORDER BY salary DESC)` (no gaps: `1, 2, 2, 3`)
*   `LAG(salary, 1)` (retrieves value from the previous row)
*   `LEAD(salary, 1)` (retrieves value from the next row)

#### Null Handling
*   `COALESCE(val1, val2, 0)`: Returns the first non-null value.
*   `IS NULL` / `IS NOT NULL`: Used to check for NULL values in filters.

---

## 📝 Top 100 Placement MCQs ⭐⭐⭐⭐⭐

*This set contains a mixed-bag of questions covering DBMS, ER models, normalization, SQL, and advanced concurrency.*

#### Q1. Which level of database schema abstraction describes how data is physically stored on disk?
A) Conceptual Level  
B) External Level  
C) Internal Level ⭐  
D) Logical Level  
*Explanation: The internal (physical) level defines paths, indexing, and block sizes on storage.*

#### Q2. A candidate key that is not chosen as the primary key is called:
A) Super Key  
B) Foreign Key  
C) Alternate Key ⭐  
D) Composite Key  
*Explanation: Alternate keys are candidate keys not selected as the primary key.*

#### Q3. What constraint requires foreign key values in a child table to match primary key values in the parent table?
A) Entity Integrity  
B) Referential Integrity ⭐  
C) Domain Constraint  
D) Check Constraint  
*Explanation: Referential integrity enforces valid relationships between foreign and primary keys.*

#### Q4. What occurs when deleting a row deletes unrelated but important structural data?
A) Deletion Anomaly ⭐  
B) Update Anomaly  
C) Insertion Anomaly  
D) Lost Update  
*Explanation: Deletion anomaly is the accidental loss of unrelated facts when a row is deleted.*

#### Q5. A relation is in 2NF if it is in 1NF and contains no:
A) Transitive dependencies  
B) Partial dependencies ⭐  
C) Multi-valued dependencies  
D) Join dependencies  
*Explanation: 2NF eliminates partial dependencies (non-prime attributes depending on a subset of a candidate key).*

#### Q6. For a non-trivial FD X -> Y, if X is not a super key but Y is a prime attribute, the relation is in:
A) BCNF  
B) 2NF but not 3NF  
C) 3NF ⭐  
D) 1NF only  
*Explanation: 3NF allows X -> Y if Y is prime, whereas BCNF requires X to be a super key.*

#### Q7. Which property ensures that a transaction is rolled back if any statement fails?
A) Isolation  
B) Consistency  
C) Atomicity ⭐  
D) Durability  
*Explanation: Atomicity guarantees "all-or-nothing" transaction execution.*

#### Q8. What log protocol requires writing modifications to log files on disk before updating data tables?
A) Write-Ahead Logging (WAL) ⭐  
B) Checkpoint Logging  
C) Commit Logging  
D) Rollback Buffering  
*Explanation: WAL requires log entries to be written to disk before database modifications are applied.*

#### Q9. Which isolation level prevents dirty reads but allows non-repeatable reads?
A) Read Uncommitted  
B) Read Committed ⭐  
C) Repeatable Read  
D) Serializable  
*Explanation: Read Committed restricts reads to committed data, preventing dirty reads.*

#### Q10. Which window function assigns sequential numbers starting at 1?
A) RANK()  
B) DENSE_RANK()  
C) ROW_NUMBER() ⭐  
D) NTILE()  
*Explanation: ROW_NUMBER() assigns consecutive integers to rows.*

#### Q11. Which SQL operator matches values against a wildcard pattern?
A) IN  
B) LIKE ⭐  
C) BETWEEN  
D) EXISTS  
*Explanation: LIKE performs pattern matching using `%` and `_`.*

#### Q12. In an ER diagram, a multivalued attribute is represented by:
A) Oval  
B) Dashed Oval  
C) Double Oval ⭐  
D) Rectangle  
*Explanation: Double ovals represent multivalued attributes.*

#### Q13. An entity set that does not have sufficient attributes to form a primary key is a:
A) Strong Entity Set  
B) Weak Entity Set ⭐  
C) Simple Entity Set  
D) Composite Entity Set  
*Explanation: Weak entity sets lack a primary key and depend on a strong parent entity.*

#### Q14. What occurs when a transaction reads uncommitted changes that are later rolled back?
A) Non-repeatable read  
B) Dirty read ⭐  
C) Phantom read  
D) Lost update  
*Explanation: Dirty reads occur when uncommitted data is read by another transaction.*

#### Q15. How many clustered indexes can a table have?
A) 1 ⭐  
B) 2  
C) 32  
D) Unlimited  
*Explanation: Because physical tables can be sorted in only one way, there can be at most one clustered index.*

#### Q16. Which data model organizes records in a tree structure where each child has only one parent?
A) Network Model  
B) Relational Model  
C) Hierarchical Model ⭐  
D) Object-Oriented Model  
*Explanation: Hierarchical models use tree structures; child nodes can have only one parent.*

#### Q17. The database schema represents:
A) The physical files on disk  
B) The state of database data at a given point in time  
C) The logical design or blueprint of the database ⭐  
D) The user privilege log  
*Explanation: The schema is the structural design of the database.*

#### Q18. Which command is used to add a new column to an existing table?
A) UPDATE  
B) ALTER TABLE ⭐  
C) CREATE COLUMN  
D) ADD COLUMN  
*Explanation: Modifying structural definitions is a DDL operation performed via `ALTER TABLE`.*

#### Q19. What does `SELECT COUNT(dept_id) FROM employees` return?
A) The total number of rows in the table  
B) The number of rows with non-null department IDs ⭐  
C) The count of unique departments  
D) The sum of department IDs  
*Explanation: Passing a column name to COUNT ignores NULL values.*

#### Q20. What is a minimal super key?
A) Primary Key  
B) Candidate Key ⭐  
C) Alternate Key  
D) Foreign Key  
*Explanation: Candidate keys are minimal super keys.*

#### Q21. Which join type returns all rows from the right table, plus matching rows from the left?
A) LEFT OUTER JOIN  
B) RIGHT OUTER JOIN ⭐  
C) INNER JOIN  
D) FULL OUTER JOIN  
*Explanation: RIGHT JOIN returns all rows from the right table, with NULLs for non-matching left columns.*

#### Q22. The intersection of R1 and R2 must determine either R1 or R2 for a decomposition to be:
A) Dependency-preserving  
B) Lossless-join ⭐  
C) BCNF  
D) Trivial  
*Explanation: The common attributes (intersection) must form a key for at least one of the decomposed tables.*

#### Q23. Which command is a DML command?
A) CREATE  
B) UPDATE ⭐  
C) ALTER  
D) TRUNCATE  
*Explanation: UPDATE modifies data values, making it a DML command.*

#### Q24. What shape represents a relationship in an ER diagram?
A) Rectangle  
B) Oval  
C) Diamond ⭐  
D) Double Oval  
*Explanation: Diamonds represent relationships in Peter Chen's ER notation.*

#### Q25. Which anomaly occurs when a transaction overwrites another transaction's updates without reading them?
A) Lost Update ⭐  
B) Dirty Read  
C) Non-Repeatable Read  
D) Phantom Read  
*Explanation: Lost update occurs when concurrent writes overwrite changes without isolating them.*

#### Q26. Which isolation level is the strongest and prevents all anomalies?
A) Repeatable Read  
B) Serializable ⭐  
C) Read Committed  
D) Snapshot Isolation  
*Explanation: Serializable is the highest isolation level, executing transactions as if they were run sequentially.*

#### Q27. A functional dependency X -> Y is trivial if:
A) Y is NULL  
B) Y is a subset of X ⭐  
C) X is a primary key  
D) Y determines X  
*Explanation: Trivial FDs are automatically true by definition because the RHS is a subset of the LHS.*

#### Q28. What shape represents a weak entity set in an ER diagram?
A) Rectangle  
B) Double Rectangle ⭐  
C) Diamond  
D) Oval  
*Explanation: Double rectangles represent weak entities.*

#### Q29. Which command is used to remove all rows from a table and deallocate its pages?
A) DELETE  
B) TRUNCATE ⭐  
C) DROP  
D) REMOVE  
*Explanation: TRUNCATE is a DDL command that resets a table, bypassing delete triggers.*

#### Q30. What does the COALESCE function return?
A) The number of non-null records  
B) The first non-null value in a list of arguments ⭐  
C) The string length  
D) The sum of columns  
*Explanation: `COALESCE(val1, val2, ...)` returns the first non-NULL expression.*

#### Q31. In the database query execution order, which clause is evaluated first?
A) SELECT  
B) WHERE  
C) FROM ⭐  
D) GROUP BY  
*Explanation: FROM is evaluated first to identify source tables.*

#### Q32. What occurs during the growing phase of 2PL?
A) The database is compressed  
B) Transactions can acquire locks but cannot release any ⭐  
C) Transactions abort  
D) Index files shrink  
*Explanation: In the growing phase, locks can be acquired but none can be released.*

#### Q33. B+ Tree leaf nodes are connected via a:
A) Linked List ⭐  
B) Binary Tree  
C) Stack  
D) Queue  
*Explanation: Leaf nodes are linked as a doubly linked list to optimize sequential scans.*

#### Q34. OLAP databases are typically:
A) Normalized to 3NF  
B) Denormalized ⭐  
C) Stored in RAM only  
D) Free of indexes  
*Explanation: OLAP systems use denormalized schemas (like Star or Snowflake) to speed up complex queries.*

#### Q35. Distributing database partitions across multiple physical servers is called:
A) Partitioning  
B) Sharding ⭐  
C) Replication  
D) Normalization  
*Explanation: Sharding distributes partitions across multiple database servers.*

#### Q36. MongoDB is which type of NoSQL database?
A) Key-Value  
B) Document-oriented ⭐  
C) Column Family  
D) Graph Database  
*Explanation: MongoDB stores records as documents (BSON).*

#### Q37. What is a self-join?
A) A join between two instances of the same table ⭐  
B) A join that matches primary keys with itself  
C) A join that runs without ON conditions  
D) A join that updates records  
*Explanation: A self-join joins a table to itself using distinct aliases.*

#### Q38. How is TRUNCATE different from DELETE?
A) TRUNCATE can have a WHERE clause  
B) DELETE is faster than TRUNCATE  
C) TRUNCATE is a DDL command that deallocates storage pages, bypassing delete triggers ⭐  
D) TRUNCATE can be rolled back in all engines  
*Explanation: TRUNCATE is a DDL operation that resets a table, making it faster than row-by-row DELETE operations.*

#### Q39. What does the EXISTS operator return?
A) A table of matching values  
B) A boolean value indicating if a subquery returns any rows ⭐  
C) A list of non-null IDs  
D) The count of records  
*Explanation: EXISTS returns TRUE if the subquery returns at least one row, stopping evaluation early.*

#### Q40. Which window function assigns ranks with gaps?
A) RANK() ⭐  
B) DENSE_RANK()  
C) ROW_NUMBER()  
D) LEAD()  
*Explanation: RANK() leaves gaps in ranks in case of ties (e.g., `1, 2, 2, 4`).*

#### Q41. In the relational model, relations are represented as:
A) Trees  
B) Graphs  
C) Tables ⭐  
D) Files  
*Explanation: Relational database design represents relations as two-dimensional tables.*

#### Q42. What is metadata?
A) Big data  
B) Unstructured data  
C) Data about data ⭐  
D) Encrypted data  
*Explanation: Metadata is structural information that describes schemas, tables, columns, and constraints.*

#### Q43. What rule prevents primary keys from containing NULL values?
A) Referential Integrity  
B) Entity Integrity ⭐  
C) Domain Constraint  
D) Key Constraint  
*Explanation: Entity Integrity states that no primary key attribute can be NULL to ensure unique row identification.*

#### Q44. The ability to modify the conceptual schema without rewriting application programs is called:
A) Physical data independence  
B) Logical data independence ⭐  
C) Schema evolution  
D) Structural integrity  
*Explanation: Logical data independence protects the external view (applications) from conceptual changes.*

#### Q45. Which level of DBMS architecture is closest to the physical storage?
A) External level  
B) View level  
C) Conceptual level  
D) Internal level ⭐  
*Explanation: The internal level (physical schema) describes how data blocks, files, and indices are stored on disk.*

#### Q46. In Three-Level Architecture, mappings are used to:
A) Link different user applications  
B) Translate requests between levels to achieve data independence ⭐  
C) Compress files on physical disks  
D) Log query statistics  
*Explanation: Mappings connect the external-conceptual and conceptual-internal levels to maintain data independence.*

#### Q47. A composite key is a key that consists of:
A) Text and numeric columns  
B) References to multiple parent tables  
C) Multiple attributes ⭐  
D) Encrypted values  
*Explanation: Composite keys combine two or more columns to form a unique identifier.*

#### Q48. Which database user is responsible for authorization management and backup configuration?
A) Database Designer  
B) Application Developer  
C) Database Administrator (DBA) ⭐  
D) Naive User  
*Explanation: DBAs manage access permissions, backups, performance tuning, and hardware management.*

#### Q49. What is the main disadvantage of the Hierarchical Data Model?
A) It lacks graphical tools  
B) It cannot support 1:N relations  
C) It cannot support N:M (many-to-many) relationships naturally ⭐  
D) It consumes too much CPU  
*Explanation: Trees only allow a child node to have one parent, making N:M relations hard to model.*

#### Q50. A database state that violates referential integrity contains:
A) Duplicate primary key values  
B) A foreign key value that does not exist as a primary key value in the parent table ⭐  
C) Two rows with identical values  
D) A candidate key that is NULL  
*Explanation: Referential integrity requires foreign keys to match an existing primary key or be NULL.*

#### Q51. What occurs during ON DELETE CASCADE?
A) Deleting a child row deletes the parent row  
B) Deleting a parent row automatically deletes its associated child rows ⭐  
C) Deleting a parent row sets child foreign keys to NULL  
D) The delete operation is blocked  
*Explanation: CASCADE propagates parent-row deletions downwards to child tables.*

#### Q52. Which shape represents a derived attribute in an ERD?
A) Oval  
B) Double Oval  
C) Dashed Oval ⭐  
D) Rectangle  
*Explanation: Dashed ovals represent derived attributes.*

#### Q53. If A -> B and B -> C, then A -> C. Which axiom is this?
A) Augmentation  
B) Reflexivity  
C) Transitivity ⭐  
D) Decomposition  
*Explanation: Transitivity rule: if A determines B and B determines C, then A determines C.*

#### Q54. In 3NF, for every non-trivial FD X -> Y, which condition must hold?
A) X is a super key or Y is a prime attribute ⭐  
B) Y must be a super key  
C) X must be a prime attribute  
D) X and Y must be composite  
*Explanation: 3NF allows X -> Y if X is a super key OR if Y is a prime attribute.*

#### Q55. BCNF is stricter than 3NF because:
A) It does not allow primary keys  
B) For every non-trivial FD X -> Y, X must be a super key ⭐  
C) It allows multivalued dependencies  
D) It requires foreign key indexes  
*Explanation: BCNF removes the "Y is a prime attribute" exception, requiring the LHS of all non-trivial FDs to be a super key.*

#### Q56. Prime attributes are attributes that:
A) Are numeric prime numbers  
B) Are part of some candidate key ⭐  
C) Are foreign keys  
D) Can be NULL  
*Explanation: An attribute is prime if it is a member of any candidate key.*

#### Q57. If a table contains employee skills, and an employee can have multiple skills, storing them in a single row as "C++, Java" violates:
A) 1NF ⭐  
B) 2NF  
C) 3NF  
D) BCNF  
*Explanation: Comma-separated values are non-atomic, which violates 1NF.*

#### Q58. A table with candidate key A and FD B -> C has a:
A) Partial dependency  
B) Transitive dependency ⭐  
C) No dependency  
D) Primary dependency  
*Explanation: A determines B (since A is a key) and B determines C. This yields a transitive dependency: A -> B -> C.*

#### Q59. What shape represents a relationship in an ERD?
A) Oval  
B) Rectangle  
C) Diamond ⭐  
D) Double Oval  
*Explanation: Diamonds represent relationships.*

#### Q60. Which normal form is concerned with multi-valued dependencies (MVD)?
A) 3NF  
B) BCNF  
C) 4NF ⭐  
D) 5NF  
*Explanation: 4NF is designed to eliminate multi-valued dependencies.*

#### Q61. Which clause is used to filter records after aggregation?
A) WHERE  
B) HAVING ⭐  
C) GROUP BY  
D) ORDER BY  
*Explanation: HAVING filters groups; WHERE filters records before grouping.*

#### Q62. What does the UNION operator do?
A) Combines tables side-by-side  
B) Combines the result sets of two queries and removes duplicates ⭐  
C) Combines result sets keeping all duplicates  
D) Sorts two tables  
*Explanation: UNION combines query outputs vertically and removes duplicate rows.*

#### Q63. What is the difference between UNION and UNION ALL?
A) UNION is faster than UNION ALL  
B) UNION removes duplicates, while UNION ALL keeps all records ⭐  
C) UNION works on strings, UNION ALL on numbers  
D) UNION ALL can only combine three queries  
*Explanation: UNION performs a deduplication step, making UNION ALL faster.*

#### Q64. Which join returns all records from the left table and matching records from the right?
A) INNER JOIN  
B) RIGHT JOIN  
C) LEFT JOIN ⭐  
D) CROSS JOIN  
*Explanation: LEFT JOIN includes all rows from the left table, with NULLs for non-matching right table columns.*

#### Q65. What is a Cartesian Product in SQL?
A) A join that matches keys  
B) The result of a LEFT JOIN  
C) The pairing of every row in one table with every row in another (CROSS JOIN) ⭐  
D) A query that returns zero rows  
*Explanation: A CROSS JOIN produces a Cartesian product, returning $M \times N$ rows.*

#### Q66. How do you check for NULL values in a WHERE clause?
A) `column = NULL`  
B) `column IS NULL` ⭐  
C) `column IN (NULL)`  
D) `column EQUALS NULL`  
*Explanation: Direct comparison operators with NULL fail. Use `IS NULL` instead.*

#### Q67. What is a CTE in SQL?
A) Constant Table Entity  
B) Common Table Expression ⭐  
C) Column Transaction Engine  
D) Core Table Extension  
*Explanation: A CTE is a temporary named result set defined using the `WITH` clause.*

#### Q68. Which window function assigns sequential ranks without gaps?
A) RANK()  
B) DENSE_RANK() ⭐  
C) ROW_NUMBER()  
D) LEAD()  
*Explanation: DENSE_RANK() assigns consecutive integer ranks. RANK() leaves gaps.*

#### Q69. Which constraint ensures that a column cannot have duplicate values?
A) NOT NULL  
B) CHECK  
C) UNIQUE ⭐  
D) DEFAULT  
*Explanation: The UNIQUE constraint guarantees that all values in a column are distinct.*

#### Q70. What is a correlated subquery?
A) A subquery that runs once before the outer query  
B) A subquery that references columns from the outer query, executing once for each row in the outer query ⭐  
C) A subquery that uses joins  
D) A subquery defined inside a CTE  
*Explanation: Correlated subqueries depend on the outer query's current row value.*

#### Q71. Can a PRIMARY KEY column contain NULL values?
A) Yes, if it is a composite key  
B) No ⭐  
C) Yes, at most one row  
D) Yes, if configured in the schema  
*Explanation: Primary keys enforce unique, non-null properties.*

#### Q72. What is the output of `SELECT 5 + NULL`?
A) 5  
B) 0  
C) NULL ⭐  
D) Error  
*Explanation: Any arithmetic operation involving a NULL value yields NULL.*

#### Q73. What is the purpose of the FOREIGN KEY constraint?
A) Enforces entity uniqueness  
B) Speed up query execution  
C) Enforces referential integrity between tables ⭐  
D) Compresses data  
*Explanation: Foreign keys link tables, ensuring that child table values point to valid parent records.*

#### Q74. Which command is used to remove a table structure and all its data?
A) DELETE TABLE  
B) TRUNCATE TABLE  
C) DROP TABLE ⭐  
D) REMOVE TABLE  
*Explanation: DROP deletes the table structure, data, indexes, and constraints.*

#### Q75. What does the window partition clause `PARTITION BY` do?
A) Physically partitions the table on disk  
B) Groups rows into partitions to calculate window function values independently within each group ⭐  
C) Sorts the final output  
D) Deletes duplicate groups  
*Explanation: `PARTITION BY` divides rows into groups for window function computation.*

#### Q76. Which function finds the difference between consecutive records?
A) FIRST_VALUE()  
B) LEAD() / LAG() ⭐  
C) ROW_NUMBER()  
D) NTILE()  
*Explanation: LEAD() and LAG() access values in rows relative to the current row.*

#### Q77. What is a VIEW in SQL?
A) A physical table copy stored on disk  
B) A virtual table defined by a saved SQL query ⭐  
C) A performance-tuning index  
D) A database trigger  
*Explanation: Views are virtual tables that run their defined SELECT query when queried.*

#### Q78. Which set operator returns records from the first query that are not present in the second?
A) UNION  
B) INTERSECT  
C) EXCEPT / MINUS ⭐  
D) UNION ALL  
*Explanation: EXCEPT (or MINUS) returns the set difference.*

#### Q79. Can a table have more than one UNIQUE constraint?
A) Yes ⭐  
B) No  
C) Only if there is no primary key  
D) Only on numeric columns  
*Explanation: Yes, a table can have multiple unique columns, but at most one primary key.*

#### Q80. What does the wildcard `_` represent?
A) Zero or more characters  
B) Exactly one character ⭐  
C) A number  
D) A space  
*Explanation: The underscore matches exactly one character in LIKE patterns.*

#### Q81. What does the wildcard `%` represent?
A) Exactly one character  
B) Zero or more characters ⭐  
C) A percentage number  
D) A null character  
*Explanation: The percent symbol matches any string of zero or more characters.*

#### Q82. Which JOIN returns all rows from the right table?
A) LEFT JOIN  
B) RIGHT JOIN ⭐  
C) INNER JOIN  
D) FULL JOIN  
*Explanation: RIGHT JOIN returns all rows from the right table.*

#### Q83. Which constraint prevents null values in a column?
A) UNIQUE  
B) NOT NULL ⭐  
C) CHECK  
D) DEFAULT  
*Explanation: `NOT NULL` prevents NULL values.*

#### Q84. Which function returns the row count?
A) SUM()  
B) COUNT() ⭐  
C) ROW_NUMBER()  
D) SIZE()  
*Explanation: `COUNT()` counts rows.*

#### Q85. Which CAP guarantee ensures that every read returns the most recent write?
A) Consistency ⭐  
B) Availability  
C) Partition Tolerance  
D) Speed  
*Explanation: Consistency guarantees that reads return the latest data or fail.*

#### Q86. Key-Value stores are best suited for:
A) Complex reports  
B) Simple caching and session management ⭐  
C) Social network graphs  
D) Document indexing  
*Explanation: Key-Value stores are optimized for simple lookups, making them ideal for caching.*

#### Q87. A transaction that is rolled back enters the:
A) Failed State  
B) Aborted State ⭐  
C) Terminated State  
D) Suspended State  
*Explanation: Aborted is the state entered after rollback is complete.*

#### Q88. Which anomaly does Read Committed isolation allow?
A) Dirty Read  
B) Non-Repeatable Read ⭐  
C) Lost Update  
D) Transaction deadlock  
*Explanation: Read Committed allows non-repeatable reads and phantom reads.*

#### Q89. What does a Wait-For Graph (WFG) show?
A) CPU wait times  
B) Transaction lock dependencies ⭐  
C) Log buffer write delays  
D) Query queues  
*Explanation: WFGs map transactions and the locks they are waiting for.*

#### Q90. What occurs during vertical partitioning?
A) Rows are split  
B) Columns are split into separate tables ⭐  
C) Tables are distributed across servers  
D) Indexes are deleted  
*Explanation: Vertical partitioning splits columns into separate tables.*

#### Q91. In MongoDB, a row equivalent is called a:
A) Collection  
B) Document ⭐  
C) Field  
D) Object  
*Explanation: Documents represent individual records in MongoDB.*

#### Q92. Strict 2-Phase Locking prevents:
A) Deadlocks  
B) Cascading Rollbacks ⭐  
C) Thread leaks  
D) Query syntax errors  
*Explanation: Strict 2PL prevents cascading rollbacks by holding exclusive locks until transactions commit.*

#### Q93. The Wait-Die scheme is based on:
A) Lock types  
B) Transaction ages (timestamps) ⭐  
C) Query complexity  
D) Table row counts  
*Explanation: Wait-Die is a deadlock prevention protocol based on transaction age.*

#### Q94. In timestamp-based concurrency control, transactions are ordered by:
A) Priority numbers  
B) Start times (timestamps) ⭐  
C) Execution costs  
D) The DBA  
*Explanation: Timestamp protocols order transactions by their start times.*

#### Q95. Which database system is optimized for high volumes of simple transaction writes and reads?
A) OLAP  
B) NoSQL Graph DB  
C) OLTP ⭐  
D) Data Warehouse  
*Explanation: Online Transaction Processing (OLTP) is optimized for real-time transaction processing.*

#### Q96. How does a DBMS detect deadlocks?
A) By parsing queries  
B) By using a Wait-For Graph (WFG) ⭐  
C) By measuring CPU load  
D) By tracking transaction row counts  
*Explanation: The DBMS checks for cycles in the WFG to detect deadlocks.*

#### Q97. Which normal form is concerned with join dependencies?
A) 3NF  
B) BCNF  
C) 4NF  
D) 5NF ⭐  
*Explanation: 5NF (Project-Join Normal Form) deals with join dependencies.*

#### Q98. What does `SELECT COUNT(*)` do?
A) Counts columns  
B) Counts all rows, including those with NULL values ⭐  
C) Counts unique values  
D) Sums numeric fields  
*Explanation: `COUNT(*)` counts the total number of rows.*

#### Q99. What does the UNION operator do to duplicate rows?
A) Keeps them  
B) Removes them ⭐  
C) Sorts them  
D) Throws an error  
*Explanation: UNION removes duplicates.*

#### Q100. Which clause is evaluated last in a SELECT query?
A) SELECT  
B) ORDER BY  
C) LIMIT ⭐  
D) HAVING  
*Explanation: LIMIT is evaluated last to restrict the returned row count.*

---

## ❓ Top 100 Interview Questions ⭐⭐⭐⭐⭐

#### Q1. Explain the difference between DBMS and File System.
**Answer:** File systems store raw files on disk without transactional safety, query optimization, or fine-grained concurrency control. A DBMS provides structured tables, ACID compliance, lock-based concurrency control, indexing, and declarative query languages (SQL).

#### Q2. What is Data Abstraction? Explain the three levels of database abstraction.
**Answer:** Data abstraction hides physical storage details. The three levels are:
1.  *Internal (Physical):* Describes physical storage structures (files, block layouts, B+ Trees).
2.  *Conceptual (Logical):* Describes tables, columns, relations, and constraints.
3.  *External (View):* Describes subsets of data visible to specific users.

#### Q3. What is the difference between Physical and Logical Data Independence?
**Answer:**
*   *Physical:* Modify physical storage (SSD vs. HDD, index files) without affecting logical schemas.
*   *Logical:* Modify conceptual schemas (adding columns, splitting tables) without affecting user views or application code.

#### Q4. What is a Data Dictionary/System Catalog?
**Answer:** A read-only set of system tables where the DBMS stores metadata (schema definitions, table properties, constraints, indexing directories, and user privileges).

#### Q5. Define Super Key, Candidate Key, and Primary Key. Give an example.
**Answer:**
*   *Super Key:* Any set of columns that uniquely identifies a row.
*   *Candidate Key:* A minimal super key (no redundant columns).
*   *Primary Key:* The selected candidate key used to identify rows. Cannot contain NULLs.
*   *Example:* In `Employee(EmpID, PassportNo, Name)`, `EmpID` and `PassportNo` are candidate keys. If `EmpID` is chosen as the primary key, `PassportNo` is the alternate key.

#### Q6. What is a Foreign Key? Why is it used?
**Answer:** A column in a table that references the primary key of another table. It is used to link tables and enforce referential integrity.

#### Q7. Explain Entity Integrity and Referential Integrity constraints.
**Answer:**
*   *Entity Integrity:* Primary key columns cannot contain NULL values.
*   *Referential Integrity:* Foreign key values must either match a valid primary key value in the parent table or be NULL.

#### Q8. What are the different referential actions available during delete/update operations?
**Answer:** `ON DELETE/UPDATE CASCADE` (propagate changes), `SET NULL` (set foreign keys to NULL), `SET DEFAULT` (set foreign keys to default values), and `RESTRICT` / `NO ACTION` (block the operation).

#### Q9. Difference between DDL, DML, and TCL.
**Answer:**
*   *DDL (Data Definition):* Defines structure (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`). Auto-committed.
*   *DML (Data Manipulation):* Writes data (`INSERT`, `UPDATE`, `DELETE`). Can be rolled back.
*   *TCL (Transaction Control):* Manages transactions (`COMMIT`, `ROLLBACK`, `SAVEPOINT`).

#### Q10. What is a composite key? When would you use it?
**Answer:** A key consisting of two or more columns to guarantee uniqueness. Used in junction tables for many-to-many relationships (e.g., `StudentCourses(StudentID, CourseID)`).

#### Q11. Compare DELETE, TRUNCATE, and DROP commands.
**Answer:**
*   *DELETE:* DML. Deletes specific rows using a WHERE clause. Writes to logs (slow) and can be rolled back.
*   *TRUNCATE:* DDL. Empties the table by deallocating pages. Fast, auto-committed, and bypasses delete triggers.
*   *DROP:* DDL. Permanently deletes the table structure and data.

#### Q12. What are the advantages of the Relational Model over Hierarchical and Network models?
**Answer:** Relational models represent data in simple 2D tables, which is easier to understand than trees or graph pointers. Relationships are defined by data values (Keys), not memory pointers, providing physical data independence.

#### Q13. Explain the difference between a Strong Entity Set and a Weak Entity Set.
**Answer:** Strong entities have their own primary key. Weak entities lack a primary key and depend on a strong parent entity (owner) for identification using a discriminator (partial key).

#### Q14. What are the different types of attributes in an ER model?
**Answer:** Simple (atomic), Composite (divisible), Multivalued (multiple values, double oval), and Derived (computed, dashed oval).

#### Q15. What are Cardinality Ratios and Participation Constraints in ER Diagrams?
**Answer:** Cardinality defines maximum relationship links (1:1, 1:N, M:N). Participation defines minimum relationship links: Total (every entity participates, double line) or Partial (only some participate, single line).

#### Q16. What is Functional Dependency?
**Answer:** A constraint $X \rightarrow Y$ stating that if two rows match on value $X$, they must match on value $Y$ (X functionally determines Y).

#### Q17. Explain Armstrong's Axioms.
**Answer:** Primary rules for deriving FDs: Reflexivity (if $Y \subseteq X$, then $X \rightarrow Y$), Augmentation (if $X \rightarrow Y$, then $XZ \rightarrow YZ$), and Transitivity (if $X \rightarrow Y$ and $Y \rightarrow Z$, then $X \rightarrow Z$).

#### Q18. What is the closure of an attribute set?
**Answer:** The set of all attributes functionally determined by that set under a given set of functional dependencies $F$ (denoted $X^+$).

#### Q19. How do you find the Candidate Keys of a relation using attribute closure?
**Answer:** Identify attributes that never appear on the RHS of any FD. Find their closure. If it contains all attributes of the relation, they form the candidate key. Otherwise, systematically add other columns to find minimal combinations that determine all attributes.

#### Q20. What is a Minimal Cover (or Canonical Cover)?
**Answer:** A simplified, equivalent set of dependencies containing no redundant FDs or redundant attributes (decomposed RHS, removed extraneous LHS attributes, and removed redundant FDs).

#### Q21. Define Database Normalization. Why is it performed?
**Answer:** The process of organizing database tables to minimize redundancy and eliminate insertion, update, and deletion anomalies.

#### Q22. Explain the difference between 3NF and BCNF.
**Answer:** For a non-trivial FD $X \rightarrow Y$, 3NF allows $X$ to be a super key OR $Y$ to be a prime attribute. BCNF requires $X$ to be a super key (no prime attribute exception).

#### Q23. Can we always decompose a relation into BCNF? What is the trade-off?
**Answer:** We can always decompose any relation into BCNF in a lossless manner. However, BCNF decomposition is not always dependency-preserving.

#### Q24. What is Lossless-Join Decomposition? How do you test for it?
**Answer:** A decomposition of relation $R$ into $R_1$ and $R_2$ is lossless-join if joining the sub-relations reconstructs the original table without creating fake rows. Test: $R_1 \cap R_2 \rightarrow R_1$ or $R_1 \cap R_2 \rightarrow R_2$.

#### Q25. What is Dependency Preservation?
**Answer:** A decomposition is dependency-preserving if the union of the functional dependencies of the sub-relations is equivalent to the original set of dependencies $F$, allowing constraints to be verified within individual tables.

#### Q26. Explain SQL logical query execution order.
**Answer:** `FROM` -> `JOIN` -> `ON` -> `WHERE` -> `GROUP BY` -> `HAVING` -> `SELECT` -> `DISTINCT` -> `ORDER BY` -> `LIMIT`.

#### Q27. What is the difference between WHERE and HAVING?
**Answer:** `WHERE` filters rows before grouping and cannot contain aggregate functions. `HAVING` filters groups after grouping and can contain aggregate functions.

#### Q28. Compare JOIN types.
**Answer:** `INNER` (matching keys), `LEFT` (all left, matching right), `RIGHT` (all right, matching left), `FULL` (all rows from both), and `CROSS` (Cartesian product).

#### Q29. What is a Self Join? Give a use case.
**Answer:** A table joined to itself using distinct aliases (e.g., finding managers of employees when both are stored in the same table).

#### Q30. What is the difference between a Subquery and a Correlated Subquery?
**Answer:** Subqueries run independently of the outer query. Correlated subqueries reference columns from the outer query and run once for each row in the outer query.

#### Q31. Explain the difference between NULL, zero, and an empty string.
**Answer:** NULL represents a missing or unknown value. Zero is a defined numeric value. An empty string is a defined text string with length 0.

#### Q32. What does the UNION operator do? How does it differ from UNION ALL?
**Answer:** Both combine result sets vertically. UNION removes duplicates (slow), while UNION ALL keeps all duplicate rows (fast).

#### Q33. How do you find the Nth highest salary?
**Answer:** Using a correlated subquery or using `DENSE_RANK() OVER (ORDER BY salary DESC)` inside a CTE, then filtering where rank = N.

#### Q34. What is a CTE (Common Table Expression)? Why is it used over subqueries?
**Answer:** A temporary named result set defined using the `WITH` clause. It improves query readability, is reusable within the query scope, and supports recursion.

#### Q35. Explain window functions. How are they different from GROUP BY?
**Answer:** GROUP BY collapses rows into a single summary row per group. Window functions calculate values over a partition of rows without collapsing them; every row remains distinct in the output.

#### Q36. Compare RANK(), DENSE_RANK(), and ROW_NUMBER().
**Answer:** `ROW_NUMBER` assigns sequential numbers. `RANK` assigns ranks, skipping numbers after ties. `DENSE_RANK` assigns consecutive ranks, without skipping numbers.

#### Q37. How do you delete duplicate records keeping the one with the smallest ID?
**Answer:** `DELETE FROM employees WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY name, dept_id);`

#### Q38. What are ACID properties?
**Answer:** Atomicity (all-or-nothing), Consistency (rules preserved), Isolation (independent transactions), and Durability (committed changes survive crashes).

#### Q39. What is a View? What are the benefits?
**Answer:** A virtual table defined by a saved SQL query. It simplifies queries, provides security by restricting column access, and ensures logical data independence.

#### Q40. What is an Index? Explain Clustered vs Non-Clustered.
**Answer:** A B+ Tree data structure that speeds up data retrieval. Clustered indexes determine the physical storage order of rows (limit of 1). Non-clustered indexes store search keys and pointers to rows (multiple allowed).

#### Q41. Explain the Write-Ahead Logging (WAL) protocol.
**Answer:** Modifying a database page requires first writing the log entry describing the change to disk, guaranteeing crash recovery and durability.

#### Q42. Why are B+ Trees preferred over B Trees for indexing?
**Answer:** B+ Trees store data pointers only in leaf nodes (allowing internal nodes to hold more search keys, increasing fan-out and reducing height) and leaf nodes are linked, optimizing sequential scans and range queries.

#### Q43. What is the CAP Theorem?
**Answer:** A distributed system can simultaneously guarantee at most two of the following: Consistency, Availability, and Partition Tolerance. Under network partition, a system must trade off consistency or availability.

#### Q44. What is a Deadlock? How does the DBMS handle it?
**Answer:** A circular wait condition where transactions wait for locks held by each other. Handled using detection (Wait-For Graph cycles) or prevention (Wait-Die or Wound-Wait timestamp schemes).

#### Q45. Explain the isolation levels defined in SQL.
**Answer:** Read Uncommitted (allows dirty reads), Read Committed (prevents dirty reads), Repeatable Read (prevents non-repeatable reads), and Serializable (prevents all anomalies).

#### Q46. What is the difference between a Stored Procedure and a Function?
**Answer:** Stored procedures can perform write transactions and return multiple values/tables. Functions must return a single value and cannot perform write transactions (no COMMIT/ROLLBACK).

#### Q47. Explain the difference between horizontal partitioning, vertical partitioning, and sharding.
**Answer:** Horizontal partitioning splits rows on the same server. Vertical partitioning splits columns into separate tables on the same server. Sharding distributes partitions across multiple database servers.

#### Q48. What is a Trigger?
**Answer:** A database object that automatically executes in response to DML events (INSERT, UPDATE, DELETE).

#### Q49. Compare OLTP and OLAP systems.
**Answer:** OLTP is normalized (3NF), optimized for fast transaction writes/reads, and stores current data. OLAP is denormalized, optimized for complex analytics on large datasets, and stores historical data.

#### Q50. Explain MongoDB collections and documents.
**Answer:** Collections group documents (equivalent to tables in SQL). Documents store records as BSON objects (equivalent to rows in SQL).

#### Q51. What is the difference between NVL, IFNULL, and COALESCE?
**Answer:** `NVL` is Oracle-specific. `IFNULL` is MySQL-specific. `COALESCE` is the ANSI-SQL standard function that returns the first non-null argument.

#### Q52. Explain the Wait-For Graph (WFG).
**Answer:** A directed graph used to detect deadlocks. Nodes represent transactions, and edges represent lock wait dependencies. Cycles in the graph indicate deadlocks.

#### Q53. What is a self-referencing foreign key?
**Answer:** A foreign key column that points to the primary key of the same table (e.g., manager ID in an employee table).

#### Q54. What are domain constraints?
**Answer:** Constraints defining the set of valid values for a column (data types, lengths, and CHECK conditions).

#### Q55. What is a checkpoint?
**Answer:** An operation that writes all dirty memory buffers and logs to disk, limiting how far back the recovery manager must scan during crash recovery.

#### Q56. What is a trivial functional dependency?
**Answer:** $X \rightarrow Y$ where $Y$ is a subset of $X$ (e.g., `(EmpID, Name) -> EmpID`).

#### Q57. What is an update anomaly?
**Answer:** An inconsistency that occurs when duplicate data in one table is updated in one place but not another.

#### Q58. What is a partial dependency?
**Answer:** When a non-prime attribute functionally depends on a proper subset of a composite candidate key, violating 2NF.

#### Q59. What is a transitive dependency?
**Answer:** When a non-prime attribute functionally determines another non-prime attribute, violating 3NF.

#### Q60. Why is BCNF stricter than 3NF?
**Answer:** BCNF removes the "Y is a prime attribute" exception, requiring the LHS of all non-trivial FDs to be a super key.

#### Q61. What is a Cartesian Product?
**Answer:** The pairing of every row in one table with every row in another, produced by a CROSS JOIN.

#### Q62. What does `LIMIT 1 OFFSET 2` do?
**Answer:** Skips the first two rows and returns the third row.

#### Q63. What is the result of `SELECT 10 / NULL`?
**Answer:** NULL. Any arithmetic operation involving a NULL value yields NULL.

#### Q64. Can you use aggregate functions in a WHERE clause?
**Answer:** No. WHERE filters rows before aggregation occurs. Use HAVING to filter aggregate values.

#### Q65. What is a recursive CTE?
**Answer:** A CTE that references itself, used to query hierarchical data (e.g., organizational charts).

#### Q66. What is the difference between CHAR and VARCHAR?
**Answer:** CHAR is fixed-length, padding values with spaces. VARCHAR is variable-length, using only the bytes needed plus a length prefix.

#### Q67. What does the `NTILE(n)` function do?
**Answer:** Divides a sorted partition of rows into `n` roughly equal groups or buckets.

#### Q68. What is a natural join?
**Answer:** Joins tables automatically based on columns with identical names and data types, which can cause errors if columns share unrelated names.

#### Q69. What is the default port for MySQL?
**Answer:** 3306.

#### Q70. What is the default port for PostgreSQL?
**Answer:** 5432.

#### Q71. What does the `%` wildcard match in a LIKE query?
**Answer:** Zero or more characters.

#### Q72. What does the `_` wildcard match in a LIKE query?
**Answer:** Exactly one character.

#### Q73. What does `SELECT 1` do in an EXISTS subquery?
**Answer:** Evaluates the presence of matching rows, ignoring projected columns.

#### Q74. What is denormalization?
**Answer:** The process of introducing redundancy by combining tables to improve read performance in read-heavy applications (OLAP).

#### Q75. What is a sharding key?
**Answer:** The column used to distribute rows across physical servers in a sharded database.

#### Q76. What is BSON?
**Answer:** Binary JSON, the binary serialization format used to store documents in MongoDB.

#### Q77. What is a cursor?
**Answer:** A database object used to retrieve and process rows of a query result set one row at a time.

#### Q78. What is the compatibility of two Shared (S) locks?
**Answer:** Compatible. Multiple transactions can hold shared locks on the same row simultaneously.

#### Q79. What is the compatibility of a Shared (S) lock and an Exclusive (X) lock?
**Answer:** Conflicting. An exclusive lock blocks all other locks.

#### Q80. What is a savepoint?
**Answer:** A checkpoint within a transaction that allows rolling back specific statements without undoing the entire transaction.

#### Q81. What is an active transaction state?
**Answer:** The initial state where a transaction begins execution and read/write statements are processed.

#### Q82. What is an aborted transaction state?
**Answer:** The state entered after the database is rolled back to its pre-transaction state following a failure.

#### Q83. Explain the Wait-Die scheme.
**Answer:** Older transactions wait for younger ones. Younger transactions die (abort) when requesting locks held by older ones.

#### Q84. Explain the Wound-Wait scheme.
**Answer:** Older transactions wound (abort) younger ones to acquire locks. Younger transactions wait for older ones.

#### Q85. What is strict 2PL?
**Answer:** Requires all exclusive locks to be held until the transaction commits or aborts, preventing cascading rollbacks.

#### Q86. What is rigorous 2PL?
**Answer:** Requires all locks (both shared and exclusive) to be held until the transaction commits or aborts.

#### Q87. What is a clustered index leaf node?
**Answer:** Contains the actual physical data rows of the table.

#### Q88. What is a non-clustered index leaf node?
**Answer:** Contains search keys and row pointers to physical row locations.

#### Q89. What is a cascading rollback?
**Answer:** When a transaction failure requires rolling back multiple dependent transactions that read its uncommitted data.

#### Q90. What is the intersection of two tables?
**Answer:** The set of rows present in both tables, returned by the `INTERSECT` operator.

#### Q91. What is the difference between UNION and UNION ALL?
**Answer:** UNION removes duplicate rows (slow), while UNION ALL keeps all duplicate rows (fast).

#### Q92. What does `SELECT NULL = NULL` evaluate to?
**Answer:** NULL.

#### Q93. What does the HAVING clause do?
**Answer:** Filters aggregated groups after they are grouped by a `GROUP BY` clause.

#### Q94. What is a derived table?
**Answer:** A subquery defined in a FROM clause.

#### Q95. What does `COALESCE(NULL, 10, NULL)` return?
**Answer:** 10.

#### Q96. Can a view be updated if it contains a GROUP BY clause?
**Answer:** No. Views containing aggregations, groupings, or distinct filters are read-only.

#### Q97. What is a primary key?
**Answer:** The selected candidate key used to identify rows. Cannot contain NULLs.

#### Q98. What is a candidate key?
**Answer:** A minimal super key.

#### Q99. What is a super key?
**Answer:** Any set of columns that uniquely identifies a row.

#### Q100. What is a transaction?
**Answer:** A logical unit of database execution that must run as a single atomic unit.

---

## ⚡ Last-Minute 1-Hour Revision Notes ⭐⭐⭐⭐⭐

*Read this section in the final hour before your interview.*

*   **ACID Guarantees:** Atomicity (all or nothing), Consistency (schema rules preserved), Isolation (concurrency boundaries), Durability (persistent writes).
*   **Logical Execution Order:** FROM -> JOIN -> ON -> WHERE -> GROUP BY -> HAVING -> SELECT -> DISTINCT -> ORDER BY -> LIMIT.
*   **Keys:**
    *   *Super Key:* Uniquely identifies rows.
    *   *Candidate Key:* Minimal super key.
    *   *Primary Key:* Selected candidate key (cannot contain NULLs).
    *   *Foreign Key:* Points to primary key in parent table (enforces referential integrity).
*   **Normalization Rules:**
    *   *1NF:* Atomic attributes.
    *   *2NF:* 1NF + No Partial Dependency ($\text{Part of Key} \rightarrow \text{Non-Prime}$).
    *   *3NF:* 2NF + No Transitive Dependency ($Key \rightarrow A \rightarrow B$).
    *   *BCNF:* LHS of all non-trivial FDs must be a Super Key.
*   **Decomposition Tests:**
    *   *Lossless:* Intersection must be a key for $R_1$ or $R_2$ ($R_1 \cap R_2 \rightarrow R_1$ or $R_1 \cap R_2 \rightarrow R_2$).
    *   *Dependency Preserving:* All original FDs can be checked within individual sub-relations.
*   **Locks:**
    *   *Shared (S):* Read lock. Multiple transactions can hold shared locks concurrently.
    *   *Exclusive (X):* Write lock. Blocks all other locks.
    *   *2PL:* Growing phase (acquire locks), Shrinking phase (release locks). Holds all exclusive locks until commit in Strict 2PL.
*   **Crash Recovery:** Write-Ahead Logging (WAL) requires writing logs to disk before modifying data pages. Checkpoints write dirty buffers and logs to disk, limiting recovery scan times.
*   **Indexes:**
    *   *Clustered:* Physical table rows are sorted in index order. Limit of one per table.
    *   *Non-Clustered:* Search keys and pointers to row locations. Multiple allowed.
    *   *B+ Tree:* Internal nodes store keys; leaf nodes store data pointers and are linked to optimize range scans.
*   **SQL Window Functions:**
    *   `ROW_NUMBER()`: Consecutive integers.
    *   `RANK()`: Ranks with gaps.
    *   `DENSE_RANK()`: Ranks without gaps.
    *   `LAG()` / `LEAD()`: Access previous/next rows.
*   **NoSQL & Scaling:**
    *   *OLTP:* High write concurrency, normalized.
    *   *OLAP:* Aggregations and analytics, denormalized.
    *   *Partitioning:* Table split on a single server.
    *   *Sharding:* Partitioning split across multiple servers.
    *   *CAP Theorem:* Network partitions require trading off consistency or availability.
    *   *MongoDB:* Document-oriented NoSQL database. Stores documents (BSON) in collections.

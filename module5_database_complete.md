# MODULE 5: Database Complete Guide
## PostgreSQL + VigilAI Schema — From Basics to Expert

---

> [!NOTE]
> VigilAI uses **PostgreSQL 16** as its database. This module teaches database fundamentals from scratch, explains every table in the schema, and shows you how to query real VigilAI data.

---

## 📚 What is a Database?

A database is an organized collection of structured data that can be efficiently stored, retrieved, updated, and deleted.

**Why not just use files?**

| Approach | Problem |
|----------|---------|
| Text files | No searching, no relationships, data corruption risk |
| Excel/CSV | No concurrent access, no transactions, not scalable |
| Database | Concurrent access, ACID transactions, relationships, indexing, backups |

---

## 🔤 SQL vs NoSQL

| Feature | SQL (PostgreSQL) | NoSQL (MongoDB) |
|---------|-----------------|-----------------|
| Structure | Tables with fixed columns | Documents (flexible JSON) |
| Relationships | Foreign keys, JOINs | Embedded documents or manual |
| ACID | Full ACID compliance | Varies |
| Use case | Structured, relational data | Flexible, hierarchical data |
| VigilAI choice | ✅ Used | ❌ Not used |

**Why VigilAI uses PostgreSQL:**
- Medical data is highly structured (defined vital sign fields)
- ACID transactions needed (don't lose patient data)
- Complex queries needed (aggregate statistics, joins)
- PostgreSQL-specific features used (UUID, arrays, generated columns)

---

## 🏗️ Database Fundamentals

### Tables
A table is like a spreadsheet — rows (records) and columns (fields).

```
patients table:
┌─────────────┬────────────┬──────────────┬─────┬────────┐
│ patient_id  │ clinic_id  │ phone_number │ age │ gender │
├─────────────┼────────────┼──────────────┼─────┼────────┤
│ 1           │ clinic-001 │ +9198765... │ 45  │ M      │
│ 2           │ clinic-001 │ +9198765... │ 28  │ F      │
│ 3           │ clinic-002 │ +9198765... │ 3   │ F      │
└─────────────┴────────────┴──────────────┴─────┴────────┘
```

### Primary Keys
A primary key uniquely identifies each row. No two rows can have the same primary key.

```sql
-- SERIAL = auto-incrementing integer (1, 2, 3, ...)
patient_id SERIAL PRIMARY KEY

-- UUID = universally unique identifier (random)
id UUID PRIMARY KEY DEFAULT uuid_generate_v4()
-- Example: "550e8400-e29b-41d4-a716-446655440000"
```

### Foreign Keys
A foreign key links one table to another, enforcing referential integrity.

```sql
-- In vitals table:
patient_id INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE
-- "patient_id in vitals must exist in patients.patient_id"
-- "ON DELETE CASCADE" = if a patient is deleted, delete their vitals too
```

### Constraints
Rules that must be satisfied for data to be stored:

```sql
-- CHECK constraint — validates the value:
age INT NOT NULL CHECK (age >= 0 AND age <= 150)
-- Can't store age = -5 or age = 200

-- UNIQUE constraint — no duplicates:
email VARCHAR(255) UNIQUE NOT NULL
-- Can't have two users with the same email

-- NOT NULL — must have a value:
clinic_id VARCHAR(100) NOT NULL
-- Can't be empty/null
```

---

## 🗄️ VigilAI Database Schema — Complete Table Guide

The schema is defined in:
- `database/schema/01_users.sql` — Users/Auth tables
- `database/schema/02_core.sql` — All application tables

---

### Table 1: `users` — System Authentication

```sql
CREATE TABLE IF NOT EXISTS users (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- UUID = random unique ID (not sequential — harder to guess)
    -- uuid_generate_v4() = auto-generates a UUID
    
    email         VARCHAR(255) UNIQUE NOT NULL,
    -- VARCHAR(255) = text up to 255 characters
    -- UNIQUE = no two users with same email
    
    password_hash VARCHAR(255) NOT NULL,
    -- Stores BCrypt hash, NEVER the plain password
    -- BCrypt example: "$2a$12$XrHo..."
    
    role          VARCHAR(20) NOT NULL CHECK (role IN ('CLINIC', 'HOSPITAL', 'ADMIN')),
    -- CHECK constraint limits valid values to only these three roles
    
    entity_id     VARCHAR(100),
    -- For CLINIC role: stores clinic ID (e.g., "clinic-demo-001")
    -- For HOSPITAL role: stores hospital_id (e.g., "1")
    -- For ADMIN: NULL (admins manage everything)
    
    full_name     VARCHAR(200),
    phone         VARCHAR(20),
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    last_login    TIMESTAMP,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for fast lookups:
CREATE INDEX idx_users_email ON users(email);
-- "Find user by email" is the most common operation (login) → needs an index
CREATE INDEX idx_users_role ON users(role);
```

**Seed Data:**
```sql
-- Pre-seeded users (passwords are BCrypt hashes):
-- Admin@123  → $2a$12$XrHoZRJVJvXbIZ1/kKg.Zug8S...
-- Clinic@123 → $2a$12$Q3ZO/62p8o966iGmwE6e8...
-- Hospital@123 → $2a$12$b2iyPEQRapbuADGCzgdOIe...
```

**Entity Relationship:**
```
users (1) ──── (M) documents (uploads)
users (1) ──── (M) audit_log_worm (audit trail)
```

---

### Table 2: `patients` — Patient Registry

```sql
CREATE TABLE IF NOT EXISTS patients (
    patient_id    SERIAL PRIMARY KEY,
    -- SERIAL = auto-increment: 1, 2, 3, ...
    
    clinic_id     VARCHAR(100) NOT NULL,
    -- Which clinic this patient belongs to
    
    phone_number  VARCHAR(20) NOT NULL,
    -- Primary identifier for patients in rural settings (no national health ID)
    
    full_name     VARCHAR(200),
    age           INT NOT NULL CHECK (age >= 0 AND age <= 150),
    gender        VARCHAR(1) CHECK (gender IN ('M', 'F', 'O')),
    medical_history TEXT,
    
    -- GENERATED COLUMN — computed by the database automatically:
    age_group     VARCHAR(20) GENERATED ALWAYS AS (
                      CASE
                          WHEN age <= 0  THEN 'NEONATAL'
                          WHEN age <= 18 THEN 'PEDIATRIC'
                          ELSE 'ADULT'
                      END
                  ) STORED,
    -- age_group is NEVER manually set — DB calculates it from age
    -- Used by the AI model to apply age-appropriate thresholds
    
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    
    UNIQUE(clinic_id, phone_number)
    -- A patient is identified by their clinic + phone number
    -- Same phone number at different clinics = different patients
);
```

**Key Design Decision:** Using `clinic_id + phone_number` as the composite unique key enables the `PatientService.findOrCreate()` logic:
```java
// If clinic-001 + +919876543210 exists, return existing patient
// If not, create new patient with those details
public Patient findOrCreate(String clinicId, String phone, ...) {
    return patientRepo
        .findByClinicIdAndPhoneNumber(clinicId, phone)
        .orElseGet(() -> {
            Patient p = Patient.builder()...build();
            return patientRepo.save(p);
        });
}
```

---

### Table 3: `vitals` — Patient Measurements

```sql
CREATE TABLE IF NOT EXISTS vitals (
    vital_id                 SERIAL PRIMARY KEY,
    patient_id               INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    clinic_id                VARCHAR(100) NOT NULL,
    
    -- The five vital signs measured:
    heart_rate               INT CHECK (heart_rate >= 0 AND heart_rate <= 300),
    temperature              DECIMAL(5,2) CHECK (temperature >= 25.0 AND temperature <= 45.0),
    -- DECIMAL(5,2) = 5 total digits, 2 after decimal: 38.75
    respiratory_rate         INT CHECK (respiratory_rate >= 0 AND respiratory_rate <= 100),
    blood_pressure_systolic  INT CHECK (blood_pressure_systolic >= 0 AND blood_pressure_systolic <= 300),
    blood_pressure_diastolic INT CHECK (blood_pressure_diastolic >= 0 AND blood_pressure_diastolic <= 200),
    spo2                     INT CHECK (spo2 >= 0 AND spo2 <= 100),
    -- SpO2 = blood oxygen saturation (%)
    
    clinical_notes           TEXT,
    emergency_type           VARCHAR(30) CHECK (emergency_type IN (
                                 'CARDIAC','STROKE','RESPIRATORY','TRAUMA',
                                 'SEPSIS','POISONING','OBSTETRIC','DIABETIC',
                                 'SEIZURE','HEAT_STROKE','UNKNOWN')),
    
    vital_timestamp          TIMESTAMP NOT NULL,
    -- When vitals were measured (may differ from created_at)
    
    sync_status              VARCHAR(20) NOT NULL DEFAULT 'PENDING'
                             CHECK (sync_status IN ('PENDING', 'SYNCED', 'FAILED')),
    -- Supports offline-first: clinic can record vitals offline, sync later
    
    is_encrypted             BOOLEAN NOT NULL DEFAULT TRUE,
    created_at               TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Normal Vital Sign Ranges:**
| Vital | Normal Range | Flag Threshold (Adult) |
|-------|-------------|----------------------|
| Heart Rate | 60-100 bpm | > 100 (tachycardia) or < 60 (bradycardia) |
| Temperature | 36.5-37.5°C | > 38.5°C (fever) |
| Respiratory Rate | 12-20 /min | > 24 /min (tachypnea) |
| Blood Pressure | 90/60 - 120/80 mmHg | Systolic < 100 (hypotension) |
| SpO2 | 95-100% | < 92% (critical) |

---

### Table 4: `triage_flags` — Abnormal Vital Flags

```sql
CREATE TABLE IF NOT EXISTS triage_flags (
    triage_id      SERIAL PRIMARY KEY,
    patient_id     INT NOT NULL REFERENCES patients(patient_id) ON DELETE CASCADE,
    vital_id       INT NOT NULL REFERENCES vitals(vital_id) ON DELETE CASCADE,
    
    rule_severity  VARCHAR(20) NOT NULL CHECK (rule_severity IN ('PRIORITY', 'NORMAL')),
    -- 'PRIORITY' if 2+ vitals are flagged
    
    -- Individual flags (which vitals are abnormal?):
    hr_flag        BOOLEAN NOT NULL DEFAULT FALSE,   -- heart rate abnormal
    temp_flag      BOOLEAN NOT NULL DEFAULT FALSE,   -- temperature abnormal
    rr_flag        BOOLEAN NOT NULL DEFAULT FALSE,   -- respiratory rate abnormal
    bp_flag        BOOLEAN NOT NULL DEFAULT FALSE,   -- blood pressure abnormal
    spo2_flag      BOOLEAN NOT NULL DEFAULT FALSE,   -- oxygen saturation abnormal
    
    flag_count     INT NOT NULL DEFAULT 0,
    -- Count of TRUE flags (max 5)
    -- PRIORITY if flag_count >= 2
    
    flagged_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Triage Logic (from VitalController.java):**
```java
boolean hrFlag   = vital.getHeartRate() > 100;
boolean tempFlag = vital.getTemperature() > 38.5;
boolean rrFlag   = vital.getRespiratoryRate() > 24;
boolean bpFlag   = vital.getBloodPressureSystolic() < 100;
boolean spo2Flag = vital.getSpo2() < 92;

// Age-adaptive thresholds:
if ("NEONATAL".equals(ageGroup)) {
    hrFlag = (vital.getHeartRate() > 180 || vital.getHeartRate() < 100);
    rrFlag = vital.getRespiratoryRate() > 60;  // neonates breathe faster
} else if ("PEDIATRIC".equals(ageGroup)) {
    hrFlag = vital.getHeartRate() > 140;       // children have faster HR
}

int flagCount = (hrFlag?1:0)+(tempFlag?1:0)+(rrFlag?1:0)+(bpFlag?1:0)+(spo2Flag?1:0);
String severity = flagCount >= 2 ? "PRIORITY" : "NORMAL";
```

---

### Table 5: `hospitals` — Hospital Registry

```sql
CREATE TABLE IF NOT EXISTS hospitals (
    hospital_id           SERIAL PRIMARY KEY,
    name                  VARCHAR(200) NOT NULL,
    code                  VARCHAR(20) UNIQUE NOT NULL,  -- e.g., "BMCRI", "SJMC"
    
    latitude              DECIMAL(10,7) NOT NULL,
    longitude             DECIMAL(10,7) NOT NULL,
    -- GPS coordinates for distance calculation (Haversine formula)
    
    total_icu_beds        INT NOT NULL DEFAULT 0,
    occupied_beds         INT NOT NULL DEFAULT 0,
    -- available = total - occupied (used in hospital scoring)
    
    specializations       TEXT[] DEFAULT '{}',
    -- PostgreSQL ARRAY! Can store multiple values: {'SEPSIS','CARDIAC','TRAUMA'}
    -- Used to match emergency type to hospital specialty
    
    sepsis_mortality_rate DECIMAL(5,2) NOT NULL DEFAULT 0,
    -- Lower mortality rate = better hospital = higher score
    
    is_level1_trauma      BOOLEAN NOT NULL DEFAULT FALSE,
    -- Level 1 trauma centers have full 24/7 surgical capability
    
    dispatcher_phone      VARCHAR(20),
    contact_email         VARCHAR(100),
    api_endpoint          VARCHAR(500),
    has_api_integration   BOOLEAN NOT NULL DEFAULT FALSE,
    is_active             BOOLEAN NOT NULL DEFAULT TRUE,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at            TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Seeded Hospitals:**
| Hospital | Code | ICU Beds | Occupied | Mortality | Level 1 |
|----------|------|----------|---------|-----------|---------|
| Bangalore Medical College | BMCRI | 40 | 28 | 12.5% | Yes |
| St. John's Medical | SJMC | 25 | 18 | 15.2% | No |
| Mysore Medical | MMC | 20 | 12 | 18.0% | No |
| Manipal Whitefield | MHW | 50 | 35 | 9.8% | Yes |

---

### Table 6: `doctors` — Hospital Staff

```sql
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id    SERIAL PRIMARY KEY,
    hospital_id  INT NOT NULL REFERENCES hospitals(hospital_id),
    full_name    VARCHAR(200) NOT NULL,
    specialty    VARCHAR(100),
    is_available BOOLEAN NOT NULL DEFAULT TRUE,
    shift_start  TIME,
    shift_end    TIME,
    created_at   TIMESTAMP NOT NULL DEFAULT NOW()
);
```

---

### Table 7: `alerts` — The Heart of VigilAI

This is the most important table — it records every AI-generated emergency alert.

```sql
CREATE TABLE IF NOT EXISTS alerts (
    alert_id             BIGSERIAL PRIMARY KEY,
    -- BIGSERIAL = big auto-increment (can store up to 9 quadrillion alerts!)
    
    patient_id           INT REFERENCES patients(patient_id) ON DELETE CASCADE,
    clinic_id            VARCHAR(100) NOT NULL,
    
    -- AI Model Output:
    risk_score           DECIMAL(5,4) NOT NULL CHECK (risk_score >= 0 AND risk_score <= 1),
    -- e.g., 0.8732 (87.32% risk)
    severity             VARCHAR(30) NOT NULL,  -- "CRITICAL", "HIGH ALERT", "MEDIUM"
    risk_level           VARCHAR(20),
    emergency_type       VARCHAR(30),
    top_features         TEXT[] DEFAULT '{}',   -- which vitals drove the AI decision
    confidence           DECIMAL(5,4),
    model_version        VARCHAR(50),           -- "VigilAI_v2.0"
    
    -- LLM Explanation Output:
    llm_explanation      TEXT,    -- "The AI assessed 87% CRITICAL sepsis risk..."
    treatment_recs       TEXT,    -- "Immediate Actions: O₂ supplementation..."
    paramedic_guidance   TEXT,    -- "EN-ROUTE PROTOCOL: ..."
    
    -- Vital snapshot at time of alert (denormalized for speed):
    heart_rate           INT,
    temperature          DECIMAL(5,2),
    respiratory_rate     INT,
    bp_systolic          INT,
    bp_diastolic         INT,
    spo2                 INT,
    patient_age          INT,
    
    -- Clinician Decision Workflow:
    status               VARCHAR(20) DEFAULT 'NEW',
    clinician_decision   VARCHAR(20) DEFAULT 'PENDING'
                         CHECK (clinician_decision IN ('APPROVED','HOLD','PENDING','DISMISSED')),
    clinician_id         VARCHAR(100),   -- who made the decision
    hold_reason          TEXT,
    notes                TEXT,
    decision_at          TIMESTAMP,
    
    -- Dispatch Information:
    dispatch_status      VARCHAR(30) DEFAULT 'PENDING',
    hospital_id          INT REFERENCES hospitals(hospital_id),
    dispatched_at        TIMESTAMP,
    
    -- Clinic Location (for distance calculation):
    clinic_latitude      DECIMAL(10,7),
    clinic_longitude     DECIMAL(10,7),
    
    alert_timestamp      TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at           TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at           TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Alert Lifecycle State Machine:**
```
NEW (alert created)
    ↓ doctor reviews
PENDING → APPROVED → DISPATCHED
        → HOLD (need more info)
        → DISMISSED (false alarm)
```

---

### Table 8: `audit_log_worm` — Immutable Audit Trail

WORM = Write Once, Read Many. Every action is permanently recorded.

```sql
CREATE TABLE IF NOT EXISTS audit_log_worm (
    log_id        BIGSERIAL PRIMARY KEY,
    action        VARCHAR(100) NOT NULL,  -- "USER_LOGIN", "ALERT_CREATED", "DISPATCH_SENT"
    entity_type   VARCHAR(50) NOT NULL,   -- "USER", "ALERT", "DISPATCH"
    entity_id     VARCHAR(100) NOT NULL,  -- ID of the affected entity
    user_id       VARCHAR(100),           -- who performed the action
    old_value     TEXT,                   -- what it was before
    new_value     TEXT,                   -- what it changed to
    timestamp     TIMESTAMP NOT NULL DEFAULT NOW(),
    hash_previous VARCHAR(256),           -- hash of previous log entry (chain!)
    hash_current  VARCHAR(256) NOT NULL,  -- hash of this entry
    signature     VARCHAR(512),           -- cryptographic signature
    immutable     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Why WORM?** In healthcare, audit trails must be tamper-evident. The hash chain means if someone modifies an old entry, all subsequent hashes become invalid — proving tampering occurred.

---

### Table 9: `outcomes` — Model Feedback Loop

```sql
CREATE TABLE IF NOT EXISTS outcomes (
    outcome_id      SERIAL PRIMARY KEY,
    alert_id        BIGINT REFERENCES alerts(alert_id) ON DELETE CASCADE,
    was_sepsis      BOOLEAN,          -- Was the AI right? Was it actually sepsis?
    final_diagnosis VARCHAR(200),     -- Doctor's confirmed diagnosis
    patient_survived BOOLEAN,
    data_source     VARCHAR(100),
    confirmed_at    TIMESTAMP NOT NULL DEFAULT NOW()
);
```

**Purpose:** This table feeds the model retraining pipeline. By recording whether the AI's predictions were correct, the model can be improved over time (active learning).

---

## 🔗 Entity Relationship Diagram

```
users ──────────────────────────────── documents
  |                                        |
  └─ uploaded_by (UUID FK)                 |
                                           |
patients ──────────────────────── vitals  |
  |           |                      |    |
  |           └── triage_flags       |    |
  |                                  |    |
  └──────────────── alerts ──────────┘    |
                      |        \          |
                      |         └─────────┘
                      |           (patient FK)
                   hospitals
                      |
                    doctors
                      |
                   outcomes ← alerts
                   
audit_log_worm (tracks all entities)
```

---

## 📊 SQL Queries — Practical Examples

### 1. Get all pending alerts for a hospital:
```sql
SELECT 
    a.alert_id,
    p.full_name AS patient_name,
    p.age,
    a.severity,
    a.risk_score,
    a.emergency_type,
    a.heart_rate,
    a.temperature,
    a.spo2,
    a.llm_explanation,
    a.alert_timestamp
FROM alerts a
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.clinician_decision = 'PENDING'
  AND a.status = 'NEW'
ORDER BY a.alert_timestamp DESC;
```

### 2. Get vitals history for a patient:
```sql
SELECT 
    v.vital_id,
    v.heart_rate,
    v.temperature,
    v.respiratory_rate,
    v.blood_pressure_systolic,
    v.blood_pressure_diastolic,
    v.spo2,
    v.vital_timestamp,
    tf.rule_severity,
    tf.flag_count
FROM vitals v
LEFT JOIN triage_flags tf ON v.vital_id = tf.vital_id
WHERE v.patient_id = 3
ORDER BY v.vital_timestamp DESC;
```

### 3. Hospital statistics:
```sql
SELECT 
    h.name,
    h.total_icu_beds,
    h.occupied_beds,
    (h.total_icu_beds - h.occupied_beds) AS available_beds,
    h.sepsis_mortality_rate,
    COUNT(DISTINCT a.alert_id) AS alerts_today,
    COUNT(DISTINCT d.doctor_id) AS doctors_on_duty
FROM hospitals h
LEFT JOIN alerts a ON h.hospital_id = a.hospital_id 
    AND a.alert_timestamp >= CURRENT_DATE
LEFT JOIN doctors d ON h.hospital_id = d.hospital_id 
    AND d.is_available = TRUE
GROUP BY h.hospital_id, h.name, h.total_icu_beds, h.occupied_beds, h.sepsis_mortality_rate
ORDER BY available_beds DESC;
```

### 4. Find high-risk patients by age group:
```sql
SELECT 
    p.age_group,
    COUNT(*) AS high_risk_count,
    AVG(a.risk_score) AS avg_risk_score,
    MAX(a.risk_score) AS max_risk_score
FROM alerts a
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.severity IN ('CRITICAL', 'HIGH ALERT')
  AND a.alert_timestamp >= NOW() - INTERVAL '7 days'
GROUP BY p.age_group
ORDER BY avg_risk_score DESC;
```

### 5. Audit trail for a specific alert:
```sql
SELECT 
    action,
    entity_type,
    entity_id,
    user_id,
    old_value,
    new_value,
    timestamp
FROM audit_log_worm
WHERE entity_id = '47'
  AND entity_type = 'ALERT'
ORDER BY timestamp;
```

---

## 📈 Indexes — Why They Matter for Performance

An index is like a book's index — instead of reading every page to find "sepsis," you look it up in the index and go directly to the right page.

```sql
-- Without index: scan all 1 million alert rows to find pending ones
SELECT * FROM alerts WHERE clinician_decision = 'PENDING';
-- With index: jump directly to relevant rows
CREATE INDEX idx_alerts_dispatch ON alerts(dispatch_status);

-- Partial index (only index active hospitals — more efficient):
CREATE INDEX idx_hospitals_active ON hospitals(is_active) WHERE is_active = TRUE;
-- This index only includes active hospitals, so it's smaller and faster

-- Composite index (for queries with multiple WHERE conditions):
CREATE INDEX idx_vitals_clinic ON vitals(clinic_id);
CREATE INDEX idx_vitals_timestamp ON vitals(vital_timestamp DESC);
```

---

## 🔄 Transactions — All or Nothing

A transaction groups multiple operations so they either ALL succeed or ALL fail.

```
Scenario: Nurse submits vitals, alert is created
    Step 1: INSERT INTO vitals (...)
    Step 2: INSERT INTO triage_flags (...)
    Step 3: INSERT INTO alerts (...)
    
    If Step 3 fails (database error):
        Without transaction: vitals saved but no alert → data inconsistency!
        With transaction: ALL three are rolled back → consistent state
```

Spring Boot handles transactions automatically for `@Transactional` methods:
```java
@Transactional
public void submitVitalsComplete(VitalRequest req) {
    Vital vital = vitalRepo.save(buildVital(req));      // step 1
    TriageFlag triage = triageRepo.save(buildTriage(vital)); // step 2
    Alert alert = alertRepo.save(buildAlert(vital));    // step 3
    // If step 3 throws, steps 1 and 2 are automatically rolled back
}
```

---

## 🔢 Normalization — Organizing Data Efficiently

**1NF:** Each column has one value per row
- ✅ `emergency_type` = 'SEPSIS' (not 'SEPSIS, CARDIAC')
- PostgreSQL arrays (`specializations TEXT[]`) are an exception for convenience

**2NF:** No partial dependencies
- ✅ `vitals` stores `clinic_id` separately (even though it can be derived from patient)
- This is intentional denormalization for query performance

**3NF:** No transitive dependencies
- ✅ `alerts` stores vital snapshot (denormalized)
- Design decision: If vitals are deleted, alert still shows what triggered it

**Why VigilAI denormalizes alerts?**
```sql
-- alerts table stores: heart_rate, temperature, spo2, bp_systolic, etc.
-- These are ALSO in the vitals table.
-- Why duplicate? Because vitals can be archived/deleted, but alerts must be permanent.
-- Medical-legal requirement: The alert must show EXACTLY what data triggered it.
```

---

## 💡 PostgreSQL-Specific Features Used

### 1. UUID Extension:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- Enables uuid_generate_v4() function for user IDs
SELECT uuid_generate_v4();
-- → 'f47ac10b-58cc-4372-a567-0e02b2c3d479'
```

### 2. Arrays:
```sql
-- Store multiple specializations in one column:
specializations TEXT[] DEFAULT '{}',

-- Query: find hospitals that specialize in CARDIAC:
SELECT name FROM hospitals WHERE 'CARDIAC' = ANY(specializations);

-- Seed data uses ARRAY syntax:
ARRAY['SEPSIS','CARDIAC','TRAUMA','STROKE']
```

### 3. Generated Column:
```sql
-- Database computes age_group from age automatically:
age_group VARCHAR(20) GENERATED ALWAYS AS (
    CASE
        WHEN age <= 0  THEN 'NEONATAL'
        WHEN age <= 18 THEN 'PEDIATRIC'
        ELSE 'ADULT'
    END
) STORED
-- STORED = computed and stored on disk (fast reads)
-- Cannot manually INSERT/UPDATE this column
```

### 4. Partial Index:
```sql
-- Only index the rows where is_active = TRUE:
CREATE INDEX idx_hospitals_active ON hospitals(is_active) WHERE is_active = TRUE;
-- Much smaller and faster than indexing all rows
```

---

## 💼 Interview Questions & Answers

### Q1: What is the difference between SQL and NoSQL?
**A:** SQL databases use structured tables with fixed schemas and support ACID transactions and complex JOINs. NoSQL databases store flexible documents (JSON) without a fixed schema. VigilAI uses PostgreSQL (SQL) because medical data is highly structured, relationships between tables are critical (patients → vitals → alerts), and ACID compliance is non-negotiable for medical records.

### Q2: What is the purpose of a Primary Key?
**A:** A primary key uniquely identifies each row in a table. It must be unique and not null. VigilAI uses `SERIAL PRIMARY KEY` (auto-increment integers) for most tables, but `UUID PRIMARY KEY` for users (harder to guess/enumerate).

### Q3: What is a Foreign Key?
**A:** A foreign key enforces referential integrity between tables. `vitals.patient_id REFERENCES patients(patient_id)` means every vital must belong to a real patient. `ON DELETE CASCADE` means if a patient is deleted, all their vitals are also deleted automatically.

### Q4: What is an Index and when should you use one?
**A:** An index is a data structure that speeds up queries by allowing the database to find rows without scanning the entire table. Use indexes on columns frequently used in WHERE clauses, JOIN conditions, and ORDER BY. VigilAI indexes `email` (for login), `clinic_id` (for filtering), and `alert_timestamp DESC` (for sorting alerts).

### Q5: What is a Transaction?
**A:** A transaction groups multiple SQL operations into an atomic unit — either ALL succeed or ALL fail (rollback). This prevents data inconsistency. In VigilAI, saving vitals + triage flags + creating an alert should be one transaction so partial failures don't leave inconsistent data.

### Q6: What is denormalization and when is it acceptable?
**A:** Denormalization is storing redundant data to improve query performance (trading storage for speed). VigilAI denormalizes vitals into the alerts table so alert history is self-contained and can be displayed without JOINs, even if vitals are archived. In healthcare, the legal requirement that an alert must show exactly what triggered it justifies this denormalization.

### Q7: What is a generated column?
**A:** A generated column's value is automatically computed by the database from other columns. In VigilAI, `age_group` is generated from `age` using a CASE expression. You can read it but never write to it manually. It's stored on disk for fast reads.

### Q8: What is the WORM pattern in audit logs?
**A:** WORM (Write Once, Read Many) means records can never be deleted or modified after creation. VigilAI's `audit_log_worm` table uses a hash chain — each entry contains the hash of the previous entry. If someone modifies any entry, subsequent hashes become invalid, proving tampering. This is a medical-legal requirement.

---

## 🎯 Mini Assignment

### SQL Practice Queries:
1. Write a query that finds the top 3 most common emergency types in the last 30 days.
2. Write a query that calculates the average risk score by clinic.
3. Write a query to find patients over 60 with more than 2 alerts.
4. Write a query to find hospitals with available ICU beds > 10 that specialize in CARDIAC emergencies.

### Schema Design Challenge:
Add a new table `ambulances` to the VigilAI schema with fields for: ambulance ID, hospital it belongs to, current latitude/longitude, driver name, is_available, and last updated timestamp. Write the CREATE TABLE statement with appropriate constraints and indexes.

---

> **Next Module:** Module 6 dives deep into every file in the project — complete code walkthrough with explanations of every function, dependency, and architecture decision.

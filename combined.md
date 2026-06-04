# MODULE 1: Technology Foundations
## VigilAI MedLink — Complete Beginner to Expert Learning Roadmap

---

> [!NOTE]
> This module assumes you know **absolutely nothing** about software development. Every concept is explained from scratch, using VigilAI MedLink as the teaching example throughout.

---

## 📌 What Is This Project?

**VigilAI MedLink** is a real-world healthcare emergency response platform. Here's what it does in plain English:

1. A **clinic nurse** measures a patient's vitals (heart rate, blood pressure, temperature, etc.)
2. She enters these vitals into a **web app** on her phone/computer
3. The data is sent to an **AI model** that predicts if the patient has sepsis (a life-threatening infection)
4. If the risk is HIGH, an **alert** is created and sent to a **hospital**
5. The hospital doctor reviews the alert and **approves ambulance dispatch**
6. The system selects the **best hospital** (based on distance, ICU beds, specialization) and dispatches an ambulance

This is a **full-stack** project — it has a frontend, backend, AI service, and database all working together.

---

## 🏗️ What Is Software Development?

Software development is the process of creating programs (applications) that solve real-world problems.

Think of it like building a hospital:
- The **building's exterior** = Frontend (what users see)
- The **hospital's internal systems** (electricity, plumbing, records) = Backend (the logic)
- The **medical records room** = Database (where data is stored)

```
USER CLICKS BUTTON
       ↓
  Frontend (HTML/CSS/JS)
       ↓  sends request
  Backend (Java/Spring Boot)
       ↓  queries
  Database (PostgreSQL)
       ↓  returns data
  Backend formats response
       ↓
  Frontend displays result
```

---

## 🖥️ Frontend vs Backend vs Database

### Frontend — "What the User Sees"

The frontend is everything visible on the screen. In VigilAI MedLink:

| File | Purpose |
|------|---------|
| `frontend/login.html` | The login page with email/password form |
| `frontend/clinic.html` | The clinic nurse's dashboard |
| `frontend/hospital.html` | The hospital doctor's alert view |
| `frontend/admin.html` | The admin's system management panel |

**Real Example from Project:**
In `login.html`, you see a beautiful dark-themed login form with glassmorphism effects and animated glowing orbs. This is all frontend — HTML structure + CSS styling + JavaScript behavior.

```html
<!-- This is FRONTEND code from login.html -->
<input type="email" id="email" placeholder="doctor@hospital.org">
<button onclick="login()">Sign In →</button>
```

### Backend — "The Brain"

The backend processes requests, contains business logic, and talks to the database.

In VigilAI MedLink, the backend is built with **Java + Spring Boot**:

| File | Purpose |
|------|---------|
| `AuthController.java` | Handles login/logout |
| `VitalController.java` | Accepts patient vitals, runs AI prediction |
| `AlertController.java` | Manages emergency alerts |
| `VigilService.java` | Selects best hospital using scoring algorithm |

**Real Example:**
When a nurse submits vitals, `VitalController.java` does 7 things:
1. Finds/creates the patient record
2. Detects the emergency type
3. Saves the vitals to database
4. Runs the triage rules
5. Calls the AI model
6. Calls the LLM for explanation
7. Creates an alert if risk is HIGH/MEDIUM

### Database — "The Memory"

The database stores all persistent data. VigilAI uses **PostgreSQL**.

| Table | What It Stores |
|-------|---------------|
| `users` | Clinic staff, hospital doctors, admins |
| `patients` | Patient records |
| `vitals` | Each set of measurements taken |
| `alerts` | AI-generated emergency alerts |
| `hospitals` | Hospital details, ICU beds, location |
| `triage_flags` | Which vital signs are abnormal |
| `audit_log_worm` | Immutable record of every action |

---

## 🌐 Client-Server Architecture

This is the fundamental pattern of how the internet works.

```
┌──────────────────┐         HTTP Request          ┌──────────────────┐
│                  │ ─────────────────────────────► │                  │
│    CLIENT        │                                │     SERVER       │
│  (Browser/App)   │ ◄───────────────────────────── │  (Backend API)   │
│                  │         HTTP Response          │                  │
└──────────────────┘                                └──────────────────┘
```

**In VigilAI:**
- **Client** = The browser showing `clinic.html`
- **Server** = The Spring Boot backend running on port 8080

### Analogy:
Think of a restaurant:
- **Client** = You (the customer) who orders food
- **Server** = The waiter who takes your order to the kitchen
- **Kitchen** = The backend that processes the order
- **Database** = The pantry where ingredients are stored

---

## 📡 HTTP/HTTPS — How Computers Talk

HTTP (HyperText Transfer Protocol) is the language computers use to communicate over the internet.

**HTTPS** = HTTP + Security (the 'S' means encrypted)

### HTTP Methods (Verbs):

| Method | Meaning | Example in VigilAI |
|--------|---------|-------------------|
| `GET` | Retrieve data | Get list of alerts |
| `POST` | Create/send data | Submit patient vitals |
| `PUT` | Update existing data | Update alert status |
| `DELETE` | Remove data | Delete a patient record |
| `PATCH` | Partially update | Update just the dispatch status |

**Real Example from VigilAI login.html:**
```javascript
// This is the LOGIN request from frontend
const res = await fetch(`${API}/auth/login`, {
  method: 'POST',                              // ← HTTP method
  headers: { 'Content-Type': 'application/json' }, // ← tells server it's JSON
  body: JSON.stringify({ email, password })    // ← the data being sent
});
```

### HTTP Status Codes:

| Code | Meaning | Where in VigilAI |
|------|---------|-----------------|
| 200 | OK — Success | Successful login |
| 201 | Created | New patient created |
| 400 | Bad Request — invalid data | Missing required field |
| 401 | Unauthorized — not logged in | Wrong password |
| 403 | Forbidden — no permission | Clinic trying to access admin panel |
| 404 | Not Found | Patient ID doesn't exist |
| 500 | Server Error | Database connection failed |

**From AuthController.java:**
```java
// When login fails with wrong password:
return ResponseEntity.status(401).body(Map.of("error", "Invalid email or password"));

// When login succeeds:
return ResponseEntity.ok(new AuthResponse(token, user.getRole().name(), ...));
// ResponseEntity.ok() = status 200
```

---

## 🔄 Request-Response Cycle

Let's trace EXACTLY what happens when a nurse logs into VigilAI:

```
STEP 1: Nurse opens browser → types https://vigilai.app/login.html
        Browser loads login.html, CSS, and JavaScript

STEP 2: Nurse types email + password → clicks "Sign In"
        JavaScript function login() is called

STEP 3: Browser sends HTTP POST request to backend
        POST /auth/login
        Body: { "email": "clinic@vigilai.health", "password": "Clinic@123" }

STEP 4: Spring Boot server receives request
        AuthController.login() method executes

STEP 5: Backend queries database
        SELECT * FROM users WHERE email = 'clinic@vigilai.health'

STEP 6: Database returns user row
        {id: "...", email: "clinic@vigilai.health", password_hash: "$2a$12$...", role: "CLINIC"}

STEP 7: Backend checks password
        BCrypt compares "Clinic@123" with the stored hash → MATCH!

STEP 8: Backend creates JWT token (a digital badge)
        Token contains: {email, role: "CLINIC", entityId: "clinic-demo-001", expiry: 24hrs}

STEP 9: Backend sends response to browser
        HTTP 200 OK
        Body: { "token": "eyJhbGc...", "role": "CLINIC", "entityId": "clinic-demo-001" }

STEP 10: Browser stores token in localStorage
         localStorage.setItem('vigilai_token', data.token)

STEP 11: Browser redirects to clinic.html
         window.location.href = 'clinic.html'
```

---

## 🔌 APIs — Application Programming Interfaces

An API is a set of rules that allows different software programs to communicate.

**Analogy:** An API is like a restaurant menu. You don't need to know how the kitchen works — you just know what you can order (the API endpoints) and what you'll get back.

### VigilAI's API Endpoints:

```
Authentication:
  POST /auth/login          → Login (returns JWT token)
  POST /auth/register       → Create new user
  GET  /auth/me             → Get current user info

Clinic Operations:
  POST /api/clinic/vitals             → Submit patient vitals (triggers AI!)
  GET  /api/clinic/vitals/patient/123 → Get vitals history for patient 123
  GET  /api/clinic/patients           → List clinic's patients

Hospital Operations:
  GET  /api/hospital/alerts           → Get all pending alerts
  POST /api/hospital/alerts/123/decision → Approve/reject alert 123
  GET  /api/hospital/dashboard        → Hospital statistics

Admin Operations:
  GET  /api/admin/users               → All system users
  GET  /api/admin/stats               → System-wide statistics

AI Service (Python):
  POST /predict             → Get risk prediction for vitals
  POST /explain             → Get clinical explanation
  GET  /health              → Check if AI service is alive
```

---

## 📦 JSON — The Language of APIs

JSON (JavaScript Object Notation) is the format used to send data between frontend and backend.

**Real example from VigilAI — submitting patient vitals:**

```json
// REQUEST (Frontend → Backend):
{
  "phoneNumber": "+919876543210",
  "fullName": "Ramesh Patil",
  "age": 45,
  "gender": "M",
  "clinicId": "clinic-demo-001",
  "heart_rate": 112,
  "temperature": 38.8,
  "respiratory_rate": 24,
  "systolic_bp": 95,
  "diastolic_bp": 60,
  "spo2": 91,
  "clinicalNotes": "Patient complaining of high fever and difficulty breathing",
  "emergencyType": "AUTO-DETECT"
}

// RESPONSE (Backend → Frontend):
{
  "vitalId": 47,
  "patientId": 3,
  "ageGroup": "ADULT",
  "riskLevel": "CRITICAL",
  "riskScore": 0.8732,
  "triageSeverity": "PRIORITY",
  "flagCount": 4,
  "alertCreated": true,
  "explanation": "The AI model assessed a 87% CRITICAL sepsis risk...",
  "treatmentRecs": "IMMEDIATE ACTIONS:\n• O₂ supplementation...",
  "paramedicGuidance": "EN-ROUTE PROTOCOL (ADULT):..."
}
```

### JSON Data Types:

| Type | Example | Used in VigilAI for |
|------|---------|---------------------|
| String | `"CRITICAL"` | Risk level, names |
| Number | `112`, `38.8` | Heart rate, temperature |
| Boolean | `true`, `false` | Alert created or not |
| Array | `["CARDIAC","SEPSIS"]` | Specializations |
| Object | `{"key": "value"}` | Nested data |
| Null | `null` | Missing optional fields |

---

## 🔐 Authentication Basics

Authentication = "Proving who you are"
Authorization = "What you're allowed to do"

**Analogy:**
- Authentication = Showing your ID card at the hospital gate
- Authorization = The ID says "DOCTOR" so you can enter the ICU (but a VISITOR cannot)

### VigilAI's Three Roles:

| Role | Who Uses It | What They Can Do |
|------|------------|-----------------|
| `CLINIC` | Nurses/paramedics at rural clinics | Submit vitals, view their patients |
| `HOSPITAL` | Doctors at receiving hospitals | View alerts, approve/reject dispatch |
| `ADMIN` | System administrators | Manage all users, view all data |

### JWT (JSON Web Token) — The Digital Badge:

When you log in, you get a JWT token. It's like a digitally-signed badge that proves your identity.

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGluaWNAdmlnaWxhaS5oZWFsdGgi.xxxxx
       ↑                          ↑                                    ↑
   Header                      Payload                           Signature
(encryption type)          (your data inside)              (tamper-proof seal)
```

The payload contains:
```json
{
  "sub": "clinic@vigilai.health",
  "role": "CLINIC",
  "entityId": "clinic-demo-001",
  "iat": 1717401600,   ← issued at (timestamp)
  "exp": 1717488000    ← expiry (24 hours later)
}
```

---

## 🏗️ How VigilAI Fits Into This Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         VIGILAI MEDLINK SYSTEM                       │
│                                                                       │
│  ┌─────────────┐    HTTP/WebSocket    ┌─────────────────────────┐   │
│  │  FRONTEND   │ ◄──────────────────► │  BACKEND (Spring Boot)  │   │
│  │             │                      │  Port 8080               │   │
│  │ login.html  │                      │                         │   │
│  │ clinic.html │                      │  Controllers            │   │
│  │hospital.html│                      │  Services               │   │
│  │  admin.html │                      │  Repositories           │   │
│  └─────────────┘                      └───────────┬─────────────┘   │
│        ↑                                          │                  │
│        │ Port 3000                          HTTP  │  JDBC            │
│     Nginx                                        │                  │
│                                    ┌─────────────▼──┐  ┌─────────┐ │
│                                    │  AI SERVICE    │  │DATABASE │ │
│                                    │  (FastAPI/     │  │(Postgres│ │
│                                    │   Python)      │  │Port 5432│ │
│                                    │  Port 8000     │  └─────────┘ │
│                                    │                │              │
│                                    │  XGBoost Model │              │
│                                    │  Rule Engine   │              │
│                                    └────────────────┘              │
└─────────────────────────────────────────────────────────────────────┘
```

### Port Numbers — What Are They?

Ports are like apartment numbers in a building. The building is the server (computer), and different services listen on different apartment numbers:

| Port | Service | Why That Port? |
|------|---------|---------------|
| 3000 | Frontend (Nginx) | Common for web servers |
| 8080 | Backend (Spring Boot) | Common for Java applications |
| 8000 | AI Service (FastAPI) | FastAPI default |
| 5432 | PostgreSQL database | PostgreSQL's standard port |

---

## 🌍 Real-World Industry Context

### The Healthcare Tech Stack Problem

Healthcare applications face unique challenges:
1. **HIPAA Compliance** — Patient data must be encrypted
2. **Auditability** — Every action must be logged (VigilAI uses WORM audit logs)
3. **High Availability** — The system cannot go down during emergencies
4. **Low Latency** — In a sepsis emergency, every second counts

### Why These Technology Choices Were Made:

| Technology | Why It Was Chosen |
|-----------|------------------|
| Java + Spring Boot | Enterprise-grade, type-safe, large ecosystem, HIPAA-compliant libraries |
| PostgreSQL | ACID compliant (safe for medical records), powerful query engine |
| Python + FastAPI | Best ML/AI ecosystem, fast to prototype, async-ready |
| XGBoost | Industry standard for tabular medical data, interpretable |
| JWT | Stateless authentication — scales well, no server-side session storage needed |
| Docker | Reproducible deployments, easy to scale each service independently |
| WebSocket | Real-time alert push to hospital without polling |

---

## 🎯 Mini Assignment

Before moving to Module 2, test your understanding:

1. **Draw the architecture**: Without looking at the diagram, draw how clinic.html communicates with the database when a nurse submits vitals.

2. **Identify the layers**: Open `frontend/clinic.html`. Can you find:
   - Where the HTTP request is made?
   - What the API endpoint is?
   - What JSON data is sent?

3. **Trace a login**: Write down (in plain English) every step that happens when hospital@vigilai.health logs in with password Hospital@123.

---

## 💼 Interview Questions & Answers

### Q1: What is the difference between frontend and backend?
**A:** Frontend is everything the user sees in the browser — HTML structure, CSS styling, JavaScript behavior. Backend is the server-side logic that processes requests, validates data, and interacts with the database. In VigilAI, the frontend is plain HTML/CSS/JS files, and the backend is a Java Spring Boot application.

### Q2: What is an API?
**A:** An API (Application Programming Interface) is a set of defined rules/endpoints through which different software systems communicate. In VigilAI, the frontend calls `POST /auth/login` to authenticate and `POST /api/clinic/vitals` to submit patient data. The AI service also exposes APIs that the backend calls.

### Q3: What is the purpose of HTTP status codes?
**A:** HTTP status codes communicate the result of a request. 2xx means success, 4xx means client error (bad request, unauthorized), 5xx means server error. In VigilAI, we return 401 for wrong credentials, 403 for insufficient permissions, and 200 for successful operations.

### Q4: What is JWT and why is it used?
**A:** JWT (JSON Web Token) is a compact, self-contained token for transmitting information securely. It's used for authentication because it's stateless — the server doesn't need to store sessions. Each token contains the user's email, role, and entity ID, signed with a secret key. VigilAI uses JWT to authenticate API calls after login.

### Q5: What is the difference between authentication and authorization?
**A:** Authentication verifies WHO you are (login with email/password). Authorization determines WHAT you can do (CLINIC role can submit vitals but not manage users; ADMIN role can do everything). VigilAI enforces both — JWT for authentication, Spring Security's `@PreAuthorize` annotations for authorization.

### Q6: What is a database and why do we need one?
**A:** A database persistently stores structured data. Without it, all data would be lost when the server restarts. VigilAI uses PostgreSQL to store patients, vitals, alerts, hospitals, and audit logs. The database ensures data survives server restarts, power failures, and deployments.

### Q7: What does HTTPS add over HTTP?
**A:** HTTPS adds TLS encryption, which means data is encrypted in transit and cannot be read by a man-in-the-middle attacker. This is critical for VigilAI since it transmits patient medical data. HTTPS also adds server authentication (the browser verifies it's talking to the real server, not an impostor).

---

## 🔍 Common Beginner Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Storing JWT in localStorage | Vulnerable to XSS attacks | Use httpOnly cookies in production |
| Sending passwords in plain text | Anyone can intercept them | Always use HTTPS + bcrypt hashing |
| Putting secrets in code | Anyone who reads the code can exploit them | Use environment variables |
| No error handling | App crashes with cryptic errors | Always handle errors gracefully |
| No input validation | SQL injection, crashes | Validate every input on both frontend and backend |

---

> **Next Module:** Module 2 covers the programming languages used in this project — Java and JavaScript — from absolute basics to advanced concepts used in VigilAI.
# MODULE 2: Language Fundamentals
## Java + JavaScript — From Zero to VigilAI Expert

---

> [!NOTE]
> VigilAI MedLink uses **Java** for the backend and **JavaScript** for the frontend. This module teaches both languages starting from absolute basics, always referencing real code from the project.

---

## 🗂️ Language Overview

| Language | Where Used | Why This Language |
|----------|-----------|------------------|
| **Java 17** | Backend (Spring Boot) | Strongly-typed, enterprise-grade, excellent for large systems |
| **JavaScript** | Frontend (login.html, clinic.html) | Runs in browsers, no install needed, async-first |
| **Python** | AI Service (FastAPI) | Best ML libraries (XGBoost, scikit-learn), concise syntax |
| **SQL** | Database queries | Standard language for relational databases |

---

# PART A: JAVA (Backend Language)

---

## 🔤 Variables in Java

A variable is a named container that holds a value.

```java
// Java is STATICALLY TYPED — you must declare the type
int heartRate = 112;           // integer (whole number)
double temperature = 38.8;     // decimal number
String clinicId = "clinic-001"; // text
boolean isHighRisk = true;     // true/false
```

**From the VigilAI project (`VitalController.java`):**
```java
boolean isHighRisk = "HIGH".equalsIgnoreCase(aiResp.getRisk_level())
        || "CRITICAL".equalsIgnoreCase(aiResp.getRisk_level());

boolean isMediumRisk = "MEDIUM".equalsIgnoreCase(aiResp.getRisk_level());
```
Here, `isHighRisk` and `isMediumRisk` are boolean variables that store whether the patient's AI-assessed risk level is high or medium.

---

## 📊 Data Types in Java

### Primitive Types (built-in, simple values):

| Type | Example | Range | Used in VigilAI for |
|------|---------|-------|---------------------|
| `int` | `112` | -2B to 2B | Heart rate, age, bed count |
| `long` | `1717401600L` | Very large numbers | Alert IDs, timestamps |
| `double` | `38.8` | Decimal | Temperature, distance, score |
| `boolean` | `true/false` | Only 2 values | isHighRisk, isActive |
| `char` | `'M'` | Single character | Gender (rarely used) |

### Object Types (complex, reference types):

| Type | Example | Used in VigilAI for |
|------|---------|---------------------|
| `String` | `"clinic-001"` | IDs, names, messages |
| `BigDecimal` | `BigDecimal.valueOf(38.8)` | Precise decimal (temperature in DB) |
| `LocalDateTime` | `LocalDateTime.now()` | Timestamps |
| `UUID` | `UUID.randomUUID()` | User IDs |
| `List<T>` | `List<Hospital>` | Collections of objects |
| `Map<K,V>` | `Map<String, Object>` | Key-value pairs (API responses) |

**From `VitalController.java`:**
```java
// BigDecimal used for temperature to avoid floating-point errors
Vital vital = Vital.builder()
    .temperature(BigDecimal.valueOf(req.getTemperature()))  // precise decimal
    .heartRate(req.getHeart_rate())                         // int
    .spo2((int) req.getSpo2())                              // cast to int
    .build();
```

---

## ➕ Operators in Java

### Arithmetic Operators:
```java
// From VigilService.java — Hospital scoring formula:
double score = 0;
score += (100 - mortality) * 0.35;      // lower mortality → better score
score += Math.min(availableBeds * 10.0, 100) * 0.30;  // ICU beds
score += Math.max(0, 100 - distance) * 0.20;           // closer is better
```

### Comparison Operators:
```java
// From VitalController.java — Triage rules:
boolean hrFlag   = vital.getHeartRate() > 100;          // greater than
boolean tempFlag = vital.getTemperature() > 38.5;       // greater than
boolean bpFlag   = vital.getBloodPressureSystolic() < 100; // less than
boolean spo2Flag = vital.getSpo2() < 92;                // less than
```

### Logical Operators:
```java
// AND (&&) — both must be true
if (req.getMedicalHistory() != null && !req.getMedicalHistory().isBlank()) {
    patient.setMedicalHistory(req.getMedicalHistory());
}

// OR (||) — either can be true  
if (isHighRisk || isMediumRisk) {
    // create alert
}

// NOT (!)
if (!passwordEncoder.matches(req.getPassword(), user.getPassword())) {
    return ResponseEntity.status(401)...;
}
```

---

## 🔀 Conditions (if/else) in Java

```java
// From AuthController.java — Login flow:
if (user == null || !passwordEncoder.matches(req.getPassword(), user.getPassword())) {
    return ResponseEntity.status(401).body(Map.of("error", "Invalid email or password"));
}

if (!Boolean.TRUE.equals(user.getIsActive())) {
    return ResponseEntity.status(403).body(Map.of("error", "Account is disabled"));
}
```

### Switch Statement (Java 14+ Enhanced Switch):
```java
// From AuthController.java — Auto-assign entityId based on role:
switch (user.getRole()) {
    case CLINIC   -> user.setEntityId("clinic-demo-001");
    case HOSPITAL -> user.setEntityId("1");
    default       -> {}  // ADMIN doesn't need entityId
}
```

### Ternary Operator (compact if/else):
```java
// From VigilService.java:
int eta = (distanceKm == null) ? 30 : (int) Math.ceil((distanceKm / 40.0) * 60) + 5;
// If distanceKm is null, return 30. Otherwise, calculate based on 40 km/h speed.
```

---

## 🔁 Loops in Java

### For Loop:
```java
// Count flagged vitals:
int[] flags = {hrFlag?1:0, tempFlag?1:0, rrFlag?1:0, bpFlag?1:0, spo2Flag?1:0};
int flagCount = 0;
for (int flag : flags) {
    flagCount += flag;
}
// The project uses a more concise form:
int flagCount = (hrFlag?1:0)+(tempFlag?1:0)+(rrFlag?1:0)+(bpFlag?1:0)+(spo2Flag?1:0);
```

### Stream + forEach (Java 8+ functional style):
```java
// From VigilService.java — Score each hospital and find the best:
return hospitals.stream()
    .map(h -> {
        double distance = haversine(lat, lng, h.getLatitude(), h.getLongitude());
        double score = score(h, alert.getEmergencyType(), distance);
        h.setDistanceKm(distance);
        return Map.entry(h, score);
    })
    .sorted(Map.Entry.<Hospital, Double>comparingByValue().reversed()) // sort by score DESC
    .map(Map.Entry::getKey)
    .findFirst()
    .orElseThrow();
// This is the functional "streams" approach — processes a list like a pipeline
```

---

## 🔧 Functions (Methods) in Java

A method is a reusable block of code.

**Syntax:**
```java
accessModifier returnType methodName(parameters) {
    // body
    return value;
}
```

**Examples from VigilAI:**

```java
// From VigilService.java — Haversine distance formula:
private double haversine(double lat1, double lon1, double lat2, double lon2) {
    double dLat = Math.toRadians(lat2 - lat1);
    double dLon = Math.toRadians(lon2 - lon1);
    double a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
             + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
             * Math.sin(dLon / 2) * Math.sin(dLon / 2);
    return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    // Returns the great-circle distance between two GPS coordinates in KM
}

// From JwtUtil.java — Generate JWT token:
public String generateToken(String email, Role role, String entityId, UUID userId) {
    return Jwts.builder()
            .subject(email)
            .claim("role", role.name())
            .claim("entityId", entityId)
            .claim("userId", userId != null ? userId.toString() : null)
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + expirationMs))
            .signWith(getKey())
            .compact();
}
```

### Method Overloading (same name, different parameters):
```java
// From VigilService.java:
private double safeDouble(Number value) {             // 1 parameter
    return value != null ? value.doubleValue() : 0.0;
}

private double safeDouble(Number value, double defaultVal) {  // 2 parameters
    return value != null ? value.doubleValue() : defaultVal;
}
```

---

## 📦 Objects and Classes in Java

A **class** is a blueprint. An **object** is an instance of that blueprint.

**Analogy:** A class is like a hospital admission form template. An object is a filled-out form for a specific patient.

### Model Class Example (Patient entity):
```java
// From Patient.java:
@Entity
@Table(name = "patients")
@Data                    // Lombok: generates getters/setters automatically
@Builder                 // Lombok: provides Patient.builder()...build() pattern
@NoArgsConstructor
@AllArgsConstructor
public class Patient {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer patientId;
    
    private String clinicId;
    private String phoneNumber;
    private String fullName;
    private Integer age;
    private String gender;
    private String medicalHistory;
    
    @Column(insertable = false, updatable = false)
    private String ageGroup;    // computed by database
    
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
```

**Creating and using an object:**
```java
// Building a Patient object using the Builder pattern:
Patient patient = Patient.builder()
    .clinicId("clinic-demo-001")
    .phoneNumber("+919876543210")
    .fullName("Ramesh Patil")
    .age(45)
    .gender("M")
    .medicalHistory("Type 2 Diabetes, Hypertension")
    .build();

// Accessing properties:
String name = patient.getFullName();  // "Ramesh Patil"
int age = patient.getAge();           // 45
```

---

## 🎭 OOP Concepts in Java

### 1. Encapsulation (Data Hiding):
```java
// Private fields — can't be accessed directly from outside
private String email;
private String password;

// Public methods — controlled access
public String getEmail() { return email; }
// Notice: no setPassword exposed — password is only set internally
```

### 2. Inheritance:
```java
// All Spring Boot exceptions extend RuntimeException
public class PatientNotFoundException extends RuntimeException {
    public PatientNotFoundException(Long id) {
        super("Patient not found: " + id);
    }
}
// Used in VitalController:
.orElseThrow(() -> new RuntimeException("Patient not found: " + req.getPatientId()))
```

### 3. Polymorphism (same interface, different behavior):
```java
// AlertRepository can be used as JpaRepository or CrudRepository:
public interface AlertRepository extends JpaRepository<Alert, Long> {
    // Custom method — Spring creates the query automatically:
    List<Alert> findByClinicianDecisionOrderByAlertTimestampDesc(String decision);
    // "find" + "By" + fieldName → Spring generates SQL automatically
}
```

### 4. Abstraction (hiding complexity):
```java
// You just call alertRepo.save(alert) — you don't know HOW it saves to database
Alert saved = alertRepo.save(alert);
// Spring Data JPA handles the SQL: INSERT INTO alerts VALUES (...)
```

---

## ⚡ Annotations in Java (Spring Boot Magic)

Annotations are instructions to the framework. They're the `@Something` decorators you see throughout the project.

| Annotation | Meaning | Where in VigilAI |
|-----------|---------|-----------------|
| `@RestController` | This class handles HTTP requests and returns JSON | All controllers |
| `@RequestMapping("/auth")` | Base URL path for this controller | AuthController |
| `@PostMapping` | This method handles POST requests | login(), submitVitals() |
| `@GetMapping` | This method handles GET requests | getDashboard() |
| `@Service` | This is a business logic class | VigilService, LLMService |
| `@Repository` | This is a database access class | AlertRepository |
| `@Entity` | This class maps to a database table | Patient, Alert, Vital |
| `@Autowired` | Spring injects this dependency automatically | All services in controllers |
| `@Value("${key}")` | Inject value from config file | JWT secret, expiration |
| `@PreAuthorize("hasRole('CLINIC')")` | Only CLINIC role can call this method | VitalController |
| `@Slf4j` | Adds a `log` variable for logging | All classes |

---

## 🔄 Async Programming in Java

**Synchronous** = Wait for each step to finish before moving to the next
**Asynchronous** = Start a task, don't wait, handle the result when it arrives

VigilAI's backend is mostly synchronous (request → process → respond), but the WebSocket alert push is asynchronous:

```java
// From WebSocketService.java — Push alert to hospital browsers:
public void pushAlert(Alert alert) {
    messagingTemplate.convertAndSend("/topic/alerts", alert);
    // "Fire and forget" — we send the alert to all subscribers
    // and immediately continue without waiting for acknowledgment
}
```

---

## 🚨 Error Handling in Java

```java
// Try-catch block:
try {
    LLMService.LLMResult llm = llmService.explain(req, aiResp, patient);
    explanation = llm.getExplanation();
} catch (Exception e) {
    log.warn("LLM failed: {}", e.getMessage());
    // Don't crash the entire vital submission because LLM failed
    // Just log the warning and continue without explanation
}

// More specific exception handling:
Patient patient = patientRepo.findById(req.getPatientId())
    .orElseThrow(() -> new RuntimeException("Patient not found: " + req.getPatientId()));
// orElseThrow = if findById returns empty, throw this exception
```

---

# PART B: JAVASCRIPT (Frontend Language)

---

## 🔤 Variables in JavaScript

```javascript
// Three ways to declare variables:
const API = "https://backend-ysf3.onrender.com";  // const = cannot change
let selectedRole = 'CLINIC';                        // let = can change
var oldStyle = 'avoid this';                        // var = old, avoid using

// Difference between const and let:
// const: API URL never changes → use const
// let: selectedRole changes when user clicks a different role → use let
```

**From `login.html`:**
```javascript
const API = "https://backend-ysf3.onrender.com";
let selectedRole = 'CLINIC';
```

---

## 📊 Data Types in JavaScript

JavaScript is **dynamically typed** — you don't declare the type:

```javascript
// JavaScript figures out the type automatically:
let heartRate = 112;           // Number
let name = "Ramesh Patil";     // String
let isHighRisk = true;         // Boolean
let vitals = [112, 38.8, 24];  // Array
let patient = { age: 45, name: "Ramesh" }; // Object
let nothing = null;            // Null
let missing = undefined;       // Undefined
```

---

## 🔀 Conditions in JavaScript

```javascript
// From login.html:
if (!email || !password) {
    showError('Please enter email and password.'); 
    return;  // Stop the function here
}

// Ternary operator:
const redirectUrl = selectedRole === 'CLINIC' ? 'clinic.html' : 
                    selectedRole === 'HOSPITAL' ? 'hospital.html' : 'admin.html';

// Object as switch (common pattern):
const redirects = {
    CLINIC:   'clinic.html',
    HOSPITAL: 'hospital.html',
    ADMIN:    'admin.html'
};
window.location.href = redirects[data.role] || 'clinic.html';
```

---

## 🔁 Loops in JavaScript

```javascript
// forEach — iterate over array of elements:
document.querySelectorAll('.role-tab').forEach(t => t.classList.remove('active'));
// This removes 'active' class from ALL role tabs (used when switching roles)

// for...of:
const roles = ['CLINIC', 'HOSPITAL', 'ADMIN'];
for (const role of roles) {
    console.log(role);
}
```

---

## 🔧 Functions in JavaScript

```javascript
// Traditional function:
function selectRole(el) {
    document.querySelectorAll('.role-tab').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    selectedRole = el.dataset.role;
}

// Arrow function (modern, concise):
const showError = (msg) => {
    const el = document.getElementById('errMsg');
    el.textContent = msg;
    el.classList.add('show');
};

// Arrow function with single parameter (no parentheses needed):
const tabs = document.querySelectorAll('.role-tab');
tabs.forEach(t => t.classList.remove('active'));
//            ↑ this is an arrow function: t => { t.classList.remove('active') }
```

---

## ⚡ Async Programming in JavaScript (CRITICAL)

This is how JavaScript handles operations that take time (like API calls).

### The Problem:
```javascript
// WRONG — this doesn't work because fetch() takes time:
const result = fetch('/auth/login');  // fetch returns immediately, result is "pending"
console.log(result.json());          // ERROR — result isn't ready yet!
```

### Solution 1: Promises (`.then()`):
```javascript
fetch('/auth/login', { method: 'POST', body: JSON.stringify({email, password}) })
    .then(response => response.json())           // step 1: parse JSON
    .then(data => { 
        localStorage.setItem('token', data.token); // step 2: use the data
    })
    .catch(error => {
        console.error('Login failed:', error);   // handle errors
    });
```

### Solution 2: async/await (modern, readable):
```javascript
// From login.html — the login function:
async function login() {  // ← "async" means this function can use "await"
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    
    // await = "wait for this to finish before continuing"
    const res = await fetch(`${API}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    
    const data = await res.json();  // await again — parsing JSON also takes time
    
    if (!res.ok) {
        showError(data.error || 'Login failed.');
        return;
    }
    
    // Store the JWT token
    localStorage.setItem('vigilai_token', data.token);
    localStorage.setItem('vigilai_role',  data.role);
    
    // Redirect based on role
    window.location.href = redirects[data.role] || 'clinic.html';
}
```

### Try-Catch with Async/Await:
```javascript
try {
    const res = await fetch(`${API}/auth/login`, { ... });
    const data = await res.json();
    // success path
} catch (e) {
    // Network error — server is offline
    showError('Cannot reach server. Running in demo mode.');
    // Demo mode fallback:
    localStorage.setItem('vigilai_token', 'demo-token');
    localStorage.setItem('vigilai_role', selectedRole);
} finally {
    // This runs whether success or failure:
    btn.textContent = 'Sign In →';
    btn.classList.remove('loading');
}
```

---

## 📦 Objects and Arrays in JavaScript

### Objects (Key-Value pairs):
```javascript
// Creating an object:
const loginPayload = {
    email: "clinic@vigilai.health",
    password: "Clinic@123"
};

// Accessing properties:
console.log(loginPayload.email);       // dot notation
console.log(loginPayload["email"]);    // bracket notation (same result)

// Destructuring (extract properties):
const { email, password } = loginPayload;
console.log(email);   // "clinic@vigilai.health"
```

### Arrays:
```javascript
// Array of redirect mappings:
const redirects = {
    CLINIC:   'clinic.html',
    HOSPITAL: 'hospital.html',
    ADMIN:    'admin.html'
};

// forEach on DOM elements:
document.querySelectorAll('.role-tab').forEach(tab => {
    tab.classList.toggle('active', tab.dataset.role === role);
    // toggle(class, condition) = add if true, remove if false
});
```

---

## 🔍 DOM Manipulation (JavaScript + HTML Interaction)

The DOM (Document Object Model) is how JavaScript interacts with HTML.

```javascript
// From login.html — pre-filling demo credentials:
function fillCred(email, pass, role) {
    // Get elements by their ID attribute:
    document.getElementById('email').value    = email;    // set input value
    document.getElementById('password').value = pass;
    
    // Toggle active class on role tabs:
    document.querySelectorAll('.role-tab').forEach(t => {
        t.classList.toggle('active', t.dataset.role === role);
        // dataset.role reads the HTML: data-role="CLINIC"
    });
    
    selectedRole = role;
}
```

### localStorage — Storing Data in Browser:
```javascript
// After login, store session data:
localStorage.setItem('vigilai_token',    data.token);    // save
localStorage.setItem('vigilai_role',     data.role);

// Later, in clinic.html:
const token = localStorage.getItem('vigilai_token');     // retrieve
const role  = localStorage.getItem('vigilai_role');

// On logout:
localStorage.removeItem('vigilai_token');                // delete
// or:
localStorage.clear();                                     // delete all
```

---

# PART C: PYTHON (AI Service)

---

## Python Basics Used in VigilAI

```python
# From ai-service/app/main.py:

# Variables:
logger = logging.getLogger("vigilai-ai")

# Function with type hints:
def map_risk(prob: float) -> str:
    # Conditional (if/elif/else):
    if prob >= 0.80: return "CRITICAL"
    if prob >= 0.60: return "HIGH ALERT"
    if prob >= 0.30: return "MEDIUM"
    return "LOW"

# Function with list comprehension:
def top_features(vitals: VitalsRequest) -> list[str]:
    features = []
    if vitals.spo2 < 92:
        features.append(f"SpO2 critically low ({vitals.spo2}%) ↓")
    if vitals.systolic_bp < 100:
        features.append(f"Hypotension ({vitals.systolic_bp} mmHg) ↓")
    return features[:5]  # return max 5 features
```

### FastAPI Route (Decorated Function):
```python
# The @app.post decorator registers this function as a POST endpoint:
@app.post("/predict", response_model=PredictionResponse)
def predict(vitals: VitalsRequest):
    """
    This function:
    1. Receives vitals as JSON (automatically parsed into VitalsRequest object)
    2. First tries age-adaptive rule engine
    3. If no rule triggers, uses XGBoost model
    4. Returns prediction as PredictionResponse JSON
    """
    rule_result = apply_age_adaptive_rules(vitals)
    if rule_result:
        return PredictionResponse(
            risk_score=rule_result["risk_score"],
            risk_level=rule_result["risk_level"],
            source="RULE_ENGINE",
        )
    # ... XGBoost model prediction
```

### F-strings (String Formatting):
```python
# f-strings interpolate variables directly in strings:
explanation = (
    f"The AI model assessed a {req.risk_score*100:.0f}% {lvl} sepsis risk "
    f"for this {age_group.lower()} patient (age {age})."
    # {req.risk_score*100:.0f} = multiply by 100, format as integer (no decimals)
)
```

---

## 🎯 Mini Assignments

### Java:
1. **Write a method** that takes a patient's age and returns "NEONATAL", "PEDIATRIC", or "ADULT" (hint: look at the SQL generated column in `02_core.sql`)
2. **Trace the Builder pattern**: In `VitalController.java`, find where `Vital.builder()` is used and list every field being set.

### JavaScript:
1. **Add a fourth demo credential**: In `login.html`, add a new `<div class="cred">` for a doctor@hospital.com account.
2. **Modify the login function**: After successful login, also log `"Logged in as: [role]"` to the browser console.

### Python:
1. **Extend map_risk**: Add a new risk level "ELEVATED" for probabilities between 0.45 and 0.60.

---

## 💼 Interview Questions & Answers

### Q1: What is the difference between Java and JavaScript?
**A:** Despite the similar name, they're completely different languages. Java is a compiled, strongly-typed, object-oriented language used for server-side applications (like VigilAI's backend). JavaScript is an interpreted, dynamically-typed language that runs in browsers (like VigilAI's frontend). Java requires explicit type declarations; JavaScript figures out types at runtime.

### Q2: What is the difference between `let` and `const` in JavaScript?
**A:** `const` declares a variable that cannot be reassigned after creation. `let` can be reassigned. In VigilAI, `const API = "https://..."` never changes, so `const` is correct. `let selectedRole = 'CLINIC'` changes when the user clicks a different role tab, so `let` is correct.

### Q3: What is async/await and why is it used?
**A:** JavaScript is single-threaded, so long operations (like network requests) use asynchronous patterns to avoid freezing the UI. `async/await` is syntactic sugar over Promises that makes async code look synchronous and easier to read. In VigilAI's login function, `await fetch(...)` waits for the server response without blocking the browser.

### Q4: What is the Builder pattern used in VigilAI?
**A:** The Builder pattern creates complex objects step by step. Instead of a constructor with 20 parameters (error-prone), you chain method calls: `Alert.builder().severity("CRITICAL").riskScore(0.87).build()`. Lombok's `@Builder` annotation auto-generates this pattern in VigilAI's model classes.

### Q5: What is Lombok and why is it used?
**A:** Lombok is a Java library that auto-generates boilerplate code at compile time using annotations. `@Data` generates getters/setters, `@Builder` generates the builder pattern, `@Slf4j` adds a `log` logger, `@RequiredArgsConstructor` generates a constructor. This reduces hundreds of lines of repetitive code.

### Q6: What does `@Autowired` mean in Spring?
**A:** `@Autowired` is Dependency Injection — Spring automatically provides the required object (dependency) without you manually creating it with `new`. In `AuthController`, `@Autowired private JwtUtil jwtUtil` means Spring finds the `JwtUtil` bean it created and injects it, so you don't write `this.jwtUtil = new JwtUtil()`.

### Q7: What is the difference between `==` and `.equals()` in Java?
**A:** `==` compares object references (memory addresses). `.equals()` compares values. For Strings, always use `.equals()` — `"CLINIC" == "CLINIC"` might be `false` even if the values match (different String objects). That's why VigilAI uses `"HIGH".equalsIgnoreCase(aiResp.getRisk_level())` not `"HIGH" == aiResp.getRisk_level()`.

### Q8: What is a Java Stream?
**A:** Java Streams are a functional programming API for processing collections (lists, sets) as pipelines. In `VigilService.java`, `hospitals.stream().map(...).sorted(...).findFirst()` transforms a list of hospitals through a scoring algorithm without a manual for loop. It's more concise, readable, and can be parallelized.

---

## 🔍 Common Mistakes

| Mistake | Language | Example | Fix |
|---------|---------|---------|-----|
| String comparison with `==` | Java | `role == "CLINIC"` | Use `.equals("CLINIC")` |
| Not awaiting async calls | JavaScript | `const data = fetch(...)` | `const data = await fetch(...)` |
| Mutating `const` object's reference | JavaScript | `const obj = {}; obj = {}` | `const` prevents reassignment, not mutation |
| Not handling null | Java | `user.getEntityId().length()` | Check `user.getEntityId() != null` first |
| Hardcoding secrets | Any | `String secret = "mysecret"` | Use `@Value("${jwt.secret}")` |

---

> **Next Module:** Module 3 covers the frontend in depth — HTML/CSS/JavaScript, the login/clinic/hospital/admin pages, state management, API integration, and advanced UI patterns.
# MODULE 3: Frontend Complete Guide
## VigilAI MedLink Frontend — HTML, CSS, JavaScript Mastery

---

> [!NOTE]
> VigilAI's frontend uses pure HTML, CSS, and vanilla JavaScript — no React, no Vue, no Angular. This is actually a great learning experience because you see exactly what frameworks hide from you.

---

## 🗂️ Frontend File Structure

```
frontend/
├── index.html       → Entry point: redirects to login.html
├── login.html       → Authentication page (clinic/hospital/admin login)
├── clinic.html      → Clinic nurse dashboard (submit vitals, view patients)
├── hospital.html    → Hospital doctor dashboard (view alerts, approve dispatch)
└── admin.html       → Admin panel (system management, all users, stats)
```

Each `.html` file contains:
- **HTML** structure (the skeleton)
- **CSS** styling (the appearance, embedded in `<style>` tags)
- **JavaScript** behavior (the interactions, in `<script>` tags)

This is called a **Single-File Component** pattern — not ideal for large apps, but simple and self-contained for learning.

---

## 🏗️ HTML Fundamentals

HTML (HyperText Markup Language) defines the structure of a webpage using **tags**.

### Basic Structure (from login.html):
```html
<!DOCTYPE html>           <!-- Tells browser this is HTML5 -->
<html lang="en">          <!-- Root element, language for accessibility -->
<head>                    <!-- Metadata (not visible) -->
  <meta charset="UTF-8"> <!-- Character encoding (supports all languages) -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- ↑ Makes page responsive on mobile devices -->
  <title>VigilAI MedLink — Login</title>  <!-- Browser tab title -->
  <style>/* CSS goes here */</style>
</head>
<body>                    <!-- Visible content goes here -->
  
  <!-- VigilAI login form: -->
  <div class="card">
    <input type="email" id="email" placeholder="doctor@hospital.org">
    <input type="password" id="password" placeholder="••••••••">
    <button onclick="login()">Sign In →</button>
  </div>
  
  <script>/* JavaScript goes here */</script>
</body>
</html>
```

### Important HTML Attributes:

| Attribute | Example | Purpose |
|-----------|---------|---------|
| `id` | `id="email"` | Unique identifier — `getElementById('email')` |
| `class` | `class="card"` | CSS class for styling |
| `onclick` | `onclick="login()"` | Run function when clicked |
| `type` | `type="email"` | Input type (validates email format) |
| `placeholder` | `placeholder="..."` | Hint text in empty input |
| `data-*` | `data-role="CLINIC"` | Custom data stored on element |

**From login.html — role tabs using `data-role`:**
```html
<div class="role-tab active" data-role="CLINIC" onclick="selectRole(this)">
  <span class="icon">🏨</span>
  <span>Clinic</span>
</div>
```
The `data-role="CLINIC"` stores extra data that JavaScript reads: `el.dataset.role` → `"CLINIC"`.

---

## 🎨 CSS Fundamentals

CSS (Cascading Style Sheets) controls appearance.

### CSS Variables (VigilAI's Design System):
```css
:root {
  /* Color palette — defined once, used everywhere */
  --bg:       #04080f;           /* near-black background */
  --surface:  rgba(13,25,41,0.7); /* card surface with transparency */
  --accent:   #00d4ff;           /* cyan highlight color */
  --accent2:  #0057ff;           /* blue for gradients */
  --danger:   #ff3b5c;           /* error red */
  --success:  #00e5a0;           /* success green */
  --text:     #f0f7ff;           /* near-white text */
  --muted:    #6b8eb0;           /* subdued text */
  
  /* Fonts */
  --mono:     'DM Mono', monospace;    /* for code-like text */
  --sans:     'Plus Jakarta Sans', sans-serif; /* for UI text */
}

/* Using variables: */
body {
  background: var(--bg);      /* use the variable */
  color: var(--text);
  font-family: var(--sans);
}
```

**Why CSS Variables?** Change `--accent: #00d4ff` in one place → the entire app's accent color updates. This is the foundation of a design system.

### Glassmorphism Effect (VigilAI's signature look):
```css
.card {
  background: #080f1a;                /* Dark base */
  border: 1px solid rgba(255,255,255,0.08);  /* subtle border */
  border-radius: 24px;               /* rounded corners */
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);  /* deep shadow */
  backdrop-filter: blur(20px);       /* blur behind the card */
  /* Result: A glass-like dark card floating above the background */
}
```

### The Animated Background Orbs:
```css
/* Blurred circles create the glowing orb effect */
.orb {
  position: absolute;
  border-radius: 50%;       /* makes it circular */
  filter: blur(120px);      /* spreads the color as a glow */
  opacity: 0.3;             /* semi-transparent */
  pointer-events: none;     /* doesn't interfere with clicks */
}
.orb-1 { 
  width: 400px; height: 400px; 
  background: #0057ff;      /* blue glow */
  top: -100px; left: -100px; /* positioned top-left, partially off-screen */
}
```

### CSS Animations:
```css
/* Card entrance animation: */
@keyframes reveal {
  from { opacity: 0; transform: translateY(20px); }  /* starts invisible, 20px lower */
  to   { opacity: 1; transform: none; }               /* ends fully visible, in place */
}
.card {
  animation: reveal 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  /* cubic-bezier = custom animation timing — "spring" feel */
}

/* Pulsing status dot (the green dot indicating system is online): */
@keyframes pulse-glow {
  0%  { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,229,160,0.7); }
  70% { transform: scale(1);    box-shadow: 0 0 0 6px rgba(0,229,160,0); }
  100%{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,229,160,0); }
}
.status-dot {
  animation: pulse-glow 2s infinite;  /* loops forever */
}
```

### Flexbox and Grid Layout:
```css
/* Flexbox — one-dimensional layout (row or column): */
.logo {
  display: flex;
  align-items: center;  /* vertically center logo icon and text */
  gap: 16px;            /* space between items */
}

/* Grid — two-dimensional layout (rows AND columns): */
.role-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;  /* 3 equal columns */
  gap: 12px;
}
```

---

## ⚡ JavaScript Frontend Patterns

### Pattern 1: Event-Driven Programming
In frontend JavaScript, code runs in response to **events** (clicks, keyboard input, page load):

```javascript
// Inline event handler (onclick attribute):
<button onclick="login()">Sign In</button>

// addEventListener (preferred approach):
document.getElementById('loginBtn').addEventListener('click', login);

// Keyboard event:
<input onkeydown="if(event.key==='Enter') login()">
// ↑ Allows pressing Enter in password field to submit
```

### Pattern 2: DOM Manipulation
```javascript
function showError(msg) {
    const el = document.getElementById('errMsg');  // find element by ID
    el.textContent = msg;                           // set its text
    el.classList.add('show');                       // add CSS class (makes it visible)
}

function fillCred(email, pass, role) {
    document.getElementById('email').value    = email;   // change input value
    document.getElementById('password').value = pass;
    
    // Toggle active class:
    document.querySelectorAll('.role-tab').forEach(t => {
        t.classList.toggle('active', t.dataset.role === role);
        // toggle(class, condition):
        // - if condition is true → add the class
        // - if condition is false → remove the class
    });
    
    selectedRole = role;
}
```

### Pattern 3: localStorage (Browser Storage)
```javascript
// After login — save session data:
localStorage.setItem('vigilai_token',    data.token);
localStorage.setItem('vigilai_role',     data.role);
localStorage.setItem('vigilai_entityId', data.entityId || '');
localStorage.setItem('vigilai_name',     data.fullName || email);

// In clinic.html — read saved session:
const token    = localStorage.getItem('vigilai_token');
const role     = localStorage.getItem('vigilai_role');
const clinicId = localStorage.getItem('vigilai_entityId');

// Auth guard — redirect to login if not logged in:
if (!token) {
    window.location.href = 'login.html';
}
```

### Pattern 4: Making API Calls with Fetch
```javascript
// Standard API call pattern used throughout VigilAI frontend:
async function callAPI(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('vigilai_token');
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // JWT in Authorization header
        }
    };
    
    if (body) {
        options.body = JSON.stringify(body);  // convert object to JSON string
    }
    
    const response = await fetch(`${API}${endpoint}`, options);
    
    if (response.status === 401) {
        // Token expired — redirect to login
        localStorage.clear();
        window.location.href = 'login.html';
        return;
    }
    
    return await response.json();
}

// Usage:
const alerts = await callAPI('/api/hospital/alerts');
const result = await callAPI('/api/clinic/vitals', 'POST', vitalData);
```

---

## 📱 Page-by-Page Frontend Walkthrough

### Page 1: `login.html` — Authentication Flow

**Purpose:** Authenticate users and redirect them to their role-specific dashboard.

**Key Features:**
1. **Role selector tabs** (Clinic / Hospital / Admin)
2. **Email + password form**
3. **Demo credentials** (click to auto-fill)
4. **API health check** (pre-warms the backend on page load)
5. **Demo mode fallback** (works offline for demos)

**Complete Login Flow:**
```javascript
async function login() {
    // Step 1: Validate inputs
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    if (!email || !password) { showError('Please enter email and password.'); return; }
    
    // Step 2: Show loading state
    btn.textContent = 'Authenticating…';
    
    // Step 3: API call (wakeup timer for free tier)
    const wakeupTimer = setTimeout(() => {
        btn.textContent = 'Waking up Free Tier Server (~50s)…';
    }, 3000);
    
    try {
        // Step 4: POST to /auth/login
        const res = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await res.json();
        
        if (!res.ok) { showError(data.error || 'Login failed.'); return; }
        
        // Step 5: Store session
        localStorage.setItem('vigilai_token',    data.token);
        localStorage.setItem('vigilai_role',     data.role);
        localStorage.setItem('vigilai_entityId', data.entityId || '');
        localStorage.setItem('vigilai_name',     data.fullName || email);
        localStorage.setItem('vigilai_email',    data.email);
        
        // Step 6: Redirect by role
        const redirects = { CLINIC:'clinic.html', HOSPITAL:'hospital.html', ADMIN:'admin.html' };
        window.location.href = redirects[data.role] || 'clinic.html';
        
    } catch (e) {
        // Step 7: Offline fallback — demo mode
        localStorage.setItem('vigilai_token', 'demo-token');
        localStorage.setItem('vigilai_role', selectedRole);
        setTimeout(() => { window.location.href = redirects[selectedRole]; }, 800);
    } finally {
        clearTimeout(wakeupTimer);
        btn.textContent = 'Sign In →';
    }
}
```

**Server Pre-Warming (Clever UX Trick):**
```javascript
// This IIFE (Immediately Invoked Function Expression) runs as soon as the page loads
// It warms up the free-tier Render.com server BEFORE the user finishes typing
(async () => {
    const r = await fetch(`${API}/health`);  // Wake up the server
    if (r.ok) {
        statusEl.textContent = 'ONLINE';
        // Also pre-warm DB + BCrypt (will 401 but that's fine — just warms the JVM):
        fetch(`${API}/auth/login`, {
            method: 'POST', 
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({email:'warmup@x.x', password:'x'})
        }).catch(() => {});
    }
})();
```

### Page 2: `clinic.html` — Nurse Dashboard

**Purpose:** Enable clinic staff to submit patient vitals and see AI predictions.

**Key Features:**
- Patient search/registration form
- Vitals entry form (HR, Temp, RR, BP, SpO2)
- Emergency type selector
- AI prediction result display
- Patient history table
- WebSocket connection for real-time updates

**Vitals Submission Flow (Frontend Side):**
```javascript
async function submitVitals() {
    const token = localStorage.getItem('vigilai_token');
    const clinicId = localStorage.getItem('vigilai_entityId');
    
    // Build the vitals payload:
    const payload = {
        clinicId: clinicId,
        phoneNumber: document.getElementById('phone').value,
        fullName: document.getElementById('patientName').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        heart_rate: parseInt(document.getElementById('heartRate').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        respiratory_rate: parseInt(document.getElementById('respRate').value),
        systolic_bp: parseInt(document.getElementById('sysBP').value),
        diastolic_bp: parseInt(document.getElementById('diaBP').value),
        spo2: parseInt(document.getElementById('spo2').value),
        clinicalNotes: document.getElementById('notes').value,
        emergencyType: document.getElementById('emergencyType').value
    };
    
    // Send to backend:
    const res = await fetch(`${API}/api/clinic/vitals`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });
    
    const result = await res.json();
    
    // Display the AI prediction result:
    displayPrediction(result);
}

function displayPrediction(result) {
    const riskBadge = document.getElementById('riskBadge');
    riskBadge.textContent = result.riskLevel;
    riskBadge.className = `risk-badge risk-${result.riskLevel.toLowerCase()}`;
    
    document.getElementById('explanation').textContent = result.explanation;
    document.getElementById('riskScore').textContent = 
        `${(result.riskScore * 100).toFixed(1)}%`;
    
    if (result.alertCreated) {
        showNotification('⚠️ Alert created — hospital notified!', 'danger');
    }
}
```

### Page 3: `hospital.html` — Doctor Dashboard

**Purpose:** Let hospital doctors review incoming emergency alerts and decide on ambulance dispatch.

**Key Features:**
- Real-time alert feed (WebSocket)
- Alert cards with AI explanation, vitals, and treatment recs
- Approve / Hold / Dismiss actions
- Hospital statistics dashboard
- Dispatch tracking

**WebSocket Connection (Real-Time Alerts):**
```javascript
// Connect to backend WebSocket for real-time alert push:
function connectWebSocket() {
    const socket = new SockJS(`${API}/ws`);  // SockJS for compatibility
    const stompClient = Stomp.over(socket);
    
    stompClient.connect({}, frame => {
        console.log('WebSocket connected:', frame);
        
        // Subscribe to the alerts topic:
        stompClient.subscribe('/topic/alerts', message => {
            const alert = JSON.parse(message.body);
            // New alert arrived! Add it to the top of the list:
            addAlertToUI(alert);
            showNotification(`🚨 New ${alert.severity} alert — Patient ${alert.patientId}`);
        });
    });
}

// Call this when the page loads:
connectWebSocket();
```

**Alert Decision (Approve/Hold/Dismiss):**
```javascript
async function makeDecision(alertId, decision) {
    const token = localStorage.getItem('vigilai_token');
    
    const res = await fetch(`${API}/api/hospital/alerts/${alertId}/decision`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ decision: decision, notes: 'Doctor reviewed' })
    });
    
    if (res.ok) {
        // If approved, trigger ambulance dispatch:
        if (decision === 'APPROVED') {
            await fetch(`${API}/api/hospital/alerts/${alertId}/dispatch`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
        }
        // Remove alert card from UI:
        document.getElementById(`alert-${alertId}`).remove();
    }
}
```

### Page 4: `admin.html` — System Management

**Purpose:** Full system visibility and control for administrators.

**Key Features:**
- All users management (view, enable/disable)
- All hospitals management
- System-wide statistics
- Audit log viewer
- Alert overview across all clinics

---

## 🔄 State Management (Without a Framework)

Since VigilAI uses vanilla JavaScript (no React/Redux), state is managed through:

### 1. localStorage (persistent, survives page refresh):
```javascript
// Session state:
localStorage.setItem('vigilai_token', token);
localStorage.setItem('vigilai_role', role);
localStorage.setItem('vigilai_entityId', clinicId);
```

### 2. JavaScript Variables (in-memory, lost on refresh):
```javascript
let currentPage = 1;
let totalAlerts = 0;
let selectedPatientId = null;
```

### 3. DOM as State (UI reflects what's visible):
```javascript
// The presence of CSS class represents state:
button.classList.contains('active')  // is this button selected?
modal.style.display === 'none'       // is the modal hidden?
```

---

## 🎯 Frontend Best Practices Demonstrated in VigilAI

### 1. Loading States:
```javascript
btn.textContent = 'Authenticating…';    // show loading
btn.disabled = true;
// ... do the work ...
btn.textContent = 'Sign In →';          // restore
btn.disabled = false;
```

### 2. Error States with Animation:
```css
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
.error-msg {
    animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}
```

### 3. Role-Based UI:
```javascript
// Hide hospital-specific elements for clinic users:
const role = localStorage.getItem('vigilai_role');
if (role !== 'HOSPITAL') {
    document.getElementById('dispatchSection').style.display = 'none';
}
```

### 4. Graceful Degradation (Demo Mode):
```javascript
// If server is down, don't crash — show demo mode:
try {
    const res = await fetch(apiUrl);
    // normal flow
} catch (e) {
    // server offline — demo mode
    localStorage.setItem('vigilai_token', 'demo-token');
    window.location.href = 'clinic.html';
}
```

---

## 📐 UI Architecture — Design System

VigilAI follows a design system with consistent tokens:

```
Color System:
  ├── Background: #04080f (near-black)
  ├── Surface: rgba(13,25,41,0.7) (card backgrounds)  
  ├── Accent: #00d4ff (cyan - primary interactive)
  ├── Accent2: #0057ff (blue - gradients)
  ├── Danger: #ff3b5c (errors, critical alerts)
  └── Success: #00e5a0 (success, operational status)

Typography:
  ├── UI Text: 'Plus Jakarta Sans' (headings, buttons, labels)
  └── Monospace: 'DM Mono' (code-like, API data, credentials)

Spacing:
  ├── Micro: 4px, 8px
  ├── Component: 12px, 16px, 20px
  └── Section: 32px, 40px, 56px

Border Radius:
  ├── Small: 8px (tags, badges)
  ├── Medium: 12px (inputs, role tabs)
  └── Large: 24px (main cards)
```

---

## 💼 Interview Questions & Answers

### Q1: What is the DOM?
**A:** The DOM (Document Object Model) is the browser's in-memory representation of the HTML page as a tree of objects. JavaScript uses the DOM to read and modify HTML dynamically. In VigilAI, `document.getElementById('email')` accesses the email input DOM element, and `.value` reads what the user typed.

### Q2: What is localStorage and when do you use it?
**A:** localStorage is a browser-side key-value store that persists data even after the browser is closed (unlike sessionStorage which clears on tab close). In VigilAI, we store the JWT token and user role in localStorage after login so subsequent pages (clinic.html) know the user is authenticated without making another login request.

### Q3: What is an IIFE and why is it used in login.html?
**A:** An IIFE (Immediately Invoked Function Expression) is a function that runs immediately when defined: `(async () => { ... })()`. In VigilAI's login.html, it's used to pre-warm the backend server as soon as the page loads, before the user even starts typing. This reduces perceived login time.

### Q4: What is the difference between `textContent` and `innerHTML`?
**A:** `textContent` sets plain text (safe, no HTML parsing). `innerHTML` sets HTML markup (dangerous if user-controlled input — XSS attack risk). In VigilAI, `el.textContent = msg` for error messages is safe because it doesn't interpret HTML. Never use `innerHTML` with user input.

### Q5: How does WebSocket differ from regular HTTP?
**A:** HTTP is a request-response protocol (client asks, server responds, connection closes). WebSocket is a persistent, bidirectional channel (server can push data to client anytime). VigilAI uses WebSocket so the hospital dashboard gets instant alert notifications without polling every 5 seconds.

### Q6: What is the purpose of the `Authorization: Bearer TOKEN` header?
**A:** After login, every API request must include the JWT token to prove identity. The header format is `Authorization: Bearer <token>`. The backend's `JwtFilter` intercepts every request, extracts this header, validates the token, and sets the authenticated user in the security context.

### Q7: What is CSS specificity?
**A:** CSS specificity determines which rule wins when multiple rules target the same element. ID selectors (#id) > class selectors (.class) > element selectors (div). In VigilAI, `.role-tab.active` (two classes) has higher specificity than `.role-tab` alone, so the active styling overrides the default.

---

## 🎯 Mini Assignment

1. **Modify the login page**: Add a "Remember Me" checkbox that stores the email in localStorage, pre-filling it next time.

2. **Add form validation**: In the vitals form, validate that heart_rate is between 30 and 300 before submitting. Show an error if invalid.

3. **Add a logout button**: In clinic.html, add a logout button that clears localStorage and redirects to login.html.

4. **Style challenge**: Change the accent color from cyan (#00d4ff) to emerald green (#00d68a) system-wide by modifying the one CSS variable.

---

> **Next Module:** Module 4 covers the backend in depth — Spring Boot, controllers, services, repositories, security, JWT, and the complete request lifecycle.
# MODULE 4: Backend Complete Guide
## Spring Boot + Java — VigilAI Backend Deep Dive

---

> [!NOTE]
> VigilAI's backend is a **Java Spring Boot 3.2** application. This module teaches every layer of the backend architecture from scratch, explaining WHY each layer exists and HOW it fits together.

---

## 🏗️ Spring Boot Overview

**Spring Boot** is a framework that makes building Java web applications easy by:
1. Auto-configuring common settings (database connection, security, JSON serialization)
2. Providing an embedded web server (Tomcat) — no separate server installation needed
3. Managing dependencies and their versions via Maven

**Analogy:** Spring Boot is like a pre-furnished apartment. Instead of buying furniture (configuring everything yourself), you move in and just arrange things to your preference.

### Project Coordinates (from `pom.xml`):
```xml
<groupId>com.vigilai</groupId>
<artifactId>vigilai-backend</artifactId>
<version>2.0.0</version>

<!-- Parent handles all version management: -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>
```

---

## 📁 Backend Package Structure

```
backend/src/main/java/com/vigilai/
├── Application.java          ← Entry point (main method)
├── config/                   ← Security, JWT, CORS, WebSocket
│   ├── JwtUtil.java          ← JWT token creation and validation
│   ├── JwtFilter.java        ← Intercepts every request to check JWT
│   ├── SecurityConfig.java   ← Who can access which endpoint
│   ├── RestConfig.java       ← RestTemplate bean (for calling AI service)
│   └── WebSocketConfig.java  ← WebSocket STOMP endpoint setup
├── controller/               ← HTTP request handlers (entry points)
│   ├── AuthController.java   ← POST /auth/login, POST /auth/register
│   ├── VitalController.java  ← POST /api/clinic/vitals (main AI flow)
│   ├── AlertController.java  ← Alert management
│   ├── DashboardController.java ← Statistics
│   └── OtherControllers.java ← Patient, Hospital, Admin endpoints
├── service/                  ← Business logic
│   ├── VigilService.java     ← Hospital selection, dispatch
│   ├── AIService.java        ← Calls Python AI service
│   ├── LLMService.java       ← Clinical explanation generation
│   ├── PatientService.java   ← Patient find-or-create
│   ├── AuditLogService.java  ← Immutable audit trail
│   └── WebSocketService.java ← Push alerts to hospital dashboards
├── repository/               ← Database access (SQL operations)
│   ├── AlertRepository.java
│   ├── PatientRepository.java
│   ├── VitalRepository.java
│   ├── HospitalRepository.java
│   └── ...
├── model/                    ← Entity classes (map to DB tables)
│   ├── User.java
│   ├── Patient.java
│   ├── Vital.java
│   ├── Alert.java
│   ├── Hospital.java
│   └── ...
└── dto/                      ← Data Transfer Objects (request/response shapes)
    ├── AuthDTOs.java
    ├── VitalDTOs.java
    └── ...
```

---

## 🎯 The MVC Pattern (Model-View-Controller)

Spring Boot follows the MVC architectural pattern:

```
HTTP Request
    ↓
CONTROLLER (receives request, validates, delegates)
    ↓
SERVICE (business logic, orchestrates operations)
    ↓
REPOSITORY (database query)
    ↓
MODEL/ENTITY (database row as Java object)
    ↓
DTO (what gets returned to client)
    ↓
HTTP Response (JSON)
```

**In VigilAI — vitals submission:**
```
POST /api/clinic/vitals
    ↓
VitalController.submitVitals()   ← receives HTTP request
    ↓ calls
PatientService.findOrCreate()    ← business logic: find existing or create new patient
AIService.getPrediction()        ← calls Python AI service
LLMService.explain()             ← generates clinical explanation
AlertRepository.save()           ← saves alert to database
WebSocketService.pushAlert()     ← pushes real-time notification
    ↓ returns
ResponseEntity<Map<String,Object>>  ← JSON response to clinic.html
```

---

## 🚪 Entry Point — Application.java

```java
package com.vigilai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication  // = @Configuration + @ComponentScan + @EnableAutoConfiguration
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
        // This starts the embedded Tomcat server on port 8080
        // and scans all classes in com.vigilai package for Spring annotations
    }
}
```

---

## 🎮 Controllers — The Entry Points

A Controller is the first Java code that executes when an HTTP request arrives.

### AuthController — Login/Register:
```java
@RestController              // Returns JSON (not HTML views)
@RequestMapping("/auth")     // Base URL: all methods start with /auth
@Slf4j                       // Adds: private static final Logger log = ...
public class AuthController {

    @Autowired private UserRepository userRepo;
    @Autowired private PasswordEncoder passwordEncoder;
    @Autowired private JwtUtil jwtUtil;
    @Autowired private AuditLogService auditLog;

    @PostMapping("/login")   // Handles: POST /auth/login
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest req) {
        //                   ↑ Returns any type    ↑ Reads JSON body into LoginRequest
        //              @Valid = validate the request (email format, not empty)
        
        User user = userRepo.findByEmail(req.getEmail()).orElse(null);
        
        if (user == null || !passwordEncoder.matches(req.getPassword(), user.getPassword())) {
            return ResponseEntity.status(401).body(Map.of("error", "Invalid email or password"));
            //     ↑ ResponseEntity wraps the HTTP response (status code + body)
        }
        
        String token = jwtUtil.generateToken(user.getEmail(), user.getRole(), 
                                             user.getEntityId(), user.getId());
        
        return ResponseEntity.ok(new AuthResponse(token, user.getRole().name(), ...));
        //                    ↑ ok() = status 200
    }
}
```

### VitalController — The Core Flow (7 Steps):
```java
@RestController
@RequestMapping("/api/clinic/vitals")
@RequiredArgsConstructor  // Constructor injection (preferred over @Autowired field injection)
@Slf4j
public class VitalController {

    private final VitalRepository vitalRepo;      // database access
    private final PatientRepository patientRepo;
    private final PatientService patientService;  // business logic
    private final AIService aiService;            // calls Python AI
    private final LLMService llmService;          // clinical explanations
    private final AuditLogService auditLog;       // WORM logging
    private final WebSocketService wsService;     // real-time push
    private final TriageFlagRepository triageRepo;

    @PostMapping           // POST /api/clinic/vitals
    @PreAuthorize("hasAnyRole('CLINIC','ADMIN')")  // Authorization check
    public ResponseEntity<Map<String, Object>> submitVitals(@RequestBody VitalRequest req) {
        
        // STEP 1: Find or create patient
        Patient patient = (req.getPatientId() != null)
            ? patientRepo.findById(req.getPatientId()).orElseThrow(...)
            : patientService.findOrCreate(req.getClinicId(), req.getPhoneNumber(), ...);
        
        // STEP 2: Auto-detect emergency type
        String emergencyType = autoDetectEmergencyType(req);
        
        // STEP 3: Save vital signs to database
        Vital vital = Vital.builder()...build();
        vitalRepo.save(vital);
        
        // STEP 4: Run triage rules
        TriageFlag triage = runTriage(vital, patient);
        
        // STEP 5: Get AI prediction
        AIPredictionResponse aiResp = aiService.getPrediction(buildAIRequest(req, patient));
        
        // STEP 6: Get LLM explanation (if high/medium risk)
        if (isHighRisk || isMediumRisk) {
            LLMService.LLMResult llm = llmService.explain(req, aiResp, patient);
        }
        
        // STEP 7: Create alert + WebSocket push (if high/medium risk)
        if (isHighRisk || isMediumRisk) {
            Alert saved = alertRepo.save(alert);
            wsService.pushAlert(saved);
            auditLog.logAction("ALERT_CREATED", ...);
        }
        
        return ResponseEntity.ok(response);
    }
}
```

---

## ⚙️ Services — Business Logic Layer

Services contain the "thinking" of your application — rules, calculations, orchestration.

### VigilService — Hospital Selection Algorithm:
```java
@Service
@Slf4j
public class VigilService {

    // Hospital scoring formula (weighted multi-criteria):
    private double score(Hospital h, String emergencyType, double distance) {
        double score = 0;
        
        // Weight 1: Lower mortality rate = better hospital (35% weight)
        score += (100 - mortality) * 0.35;
        
        // Weight 2: More available ICU beds = better (30% weight)
        score += Math.min(availableBeds * 10.0, 100) * 0.30;
        
        // Weight 3: Closer distance = better (20% weight)
        score += Math.max(0, 100 - distance) * 0.20;
        
        // Weight 4: Level 1 trauma center bonus (10% weight)
        score += (Boolean.TRUE.equals(h.getIsLevel1Trauma()) ? 100 : 0) * 0.10;
        
        // Bonus: If hospital specializes in this emergency type
        if (h.getSpecializations().contains(emergencyType)) {
            score += 5;
        }
        
        return score;
    }
    
    // Haversine formula — calculates distance between two GPS coordinates:
    private double haversine(double lat1, double lon1, double lat2, double lon2) {
        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);
        double a = Math.sin(dLat/2)*Math.sin(dLat/2)
                 + Math.cos(Math.toRadians(lat1))*Math.cos(Math.toRadians(lat2))
                 * Math.sin(dLon/2)*Math.sin(dLon/2);
        return 6371 * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        // 6371 = Earth's radius in km
    }
    
    // ETA calculation (assumes 40 km/h ambulance speed + 5 min preparation):
    private int calculateETA(Double distanceKm) {
        if (distanceKm == null) return 30;
        return (int) Math.ceil((distanceKm / 40.0) * 60) + 5;
    }
}
```

### AIService — Calling Python Service:
```java
@Service
public class AIService {

    @Value("${ai.service.url}")   // reads from application.properties
    private String aiServiceUrl;  // = "http://ai-service:8000/predict"

    @Autowired
    private RestTemplate restTemplate;

    public AIPredictionResponse getPrediction(AIPredictionRequest request) {
        try {
            // HTTP POST to Python AI service:
            ResponseEntity<AIPredictionResponse> response = restTemplate.postForEntity(
                aiServiceUrl,
                request,
                AIPredictionResponse.class
            );
            return response.getBody();
        } catch (Exception e) {
            log.error("AI service unavailable: {}", e.getMessage());
            // Fallback — assume medium risk:
            return new AIPredictionResponse(0.5, "MEDIUM", 0.5, "FALLBACK", null);
        }
    }
}
```

### AuditLogService — Immutable WORM Log:
```java
@Service
public class AuditLogService {

    @Autowired private AuditLogRepository auditRepo;

    public void logAction(String action, String entityType, String entityId,
                          String userId, String oldValue, String newValue) {
        
        // Create a hash of the log entry (tamper-proof):
        String content = action + entityType + entityId + userId + 
                        (newValue != null ? newValue : "");
        String hash = sha256(content);
        
        AuditLogEntry entry = AuditLogEntry.builder()
            .action(action)
            .entityType(entityType)
            .entityId(entityId)
            .userId(userId)
            .oldValue(oldValue)
            .newValue(newValue)
            .hashCurrent(hash)
            .timestamp(LocalDateTime.now())
            .immutable(true)  // signals this should never be modified
            .build();
        
        auditRepo.save(entry);
    }
}
```

---

## 🗄️ Repositories — Database Access Layer

Spring Data JPA repositories provide database operations without writing SQL.

```java
// AlertRepository.java — Spring auto-generates ALL the SQL:
public interface AlertRepository extends JpaRepository<Alert, Long> {
    // find = SELECT, By = WHERE, OrderBy = ORDER BY
    List<Alert> findByClinicianDecisionOrderByAlertTimestampDesc(String decision);
    // Generated SQL: SELECT * FROM alerts WHERE clinician_decision = ? ORDER BY alert_timestamp DESC
    
    List<Alert> findByClinicIdAndStatusOrderByAlertTimestampDesc(String clinicId, String status);
    // Generated SQL: SELECT * FROM alerts WHERE clinic_id = ? AND status = ? ORDER BY...
    
    long countByClinicId(String clinicId);
    // Generated SQL: SELECT COUNT(*) FROM alerts WHERE clinic_id = ?
}

// JpaRepository provides these for free:
alertRepo.findById(123L)    // SELECT * FROM alerts WHERE alert_id = 123
alertRepo.save(alert)       // INSERT or UPDATE
alertRepo.delete(alert)     // DELETE
alertRepo.findAll()         // SELECT * FROM alerts
alertRepo.count()           // SELECT COUNT(*) FROM alerts
```

### Custom JPQL Query:
```java
@Query("SELECT v FROM Vital v WHERE v.patient.patientId = :patientId ORDER BY v.vitalTimestamp DESC")
List<Vital> findPatientHistory(@Param("patientId") Long patientId);
// JPQL uses entity class names, not SQL table names
```

---

## 📋 DTO (Data Transfer Objects)

DTOs are simple classes that define the shape of data coming in (request) or going out (response).

**Why DTOs instead of using Model classes directly?**
- Don't expose internal fields (like `password_hash`)
- Can validate incoming data
- Can shape the response differently from how data is stored

```java
// From AuthDTOs.java:

// LoginRequest — what the frontend sends:
public record LoginRequest(
    @Email @NotBlank String email,
    @NotBlank String password
) {}
// @Email = must be valid email format
// @NotBlank = cannot be empty or just spaces

// AuthResponse — what the backend returns after login:
public record AuthResponse(
    String token,    // JWT token
    String role,     // "CLINIC", "HOSPITAL", "ADMIN"  
    String entityId, // clinic ID or hospital ID
    String fullName,
    String email
) {}
```

```java
// VitalRequest — vitals submission from clinic:
@Data  // Lombok generates getters/setters
public class VitalRequest {
    private String clinicId;
    private String phoneNumber;
    private Integer patientId;
    private String fullName;
    private int age;
    private String gender;
    private String medicalHistory;
    private int heart_rate;
    private double temperature;
    private int respiratory_rate;
    private int systolic_bp;
    private int diastolic_bp;
    private double spo2;
    private String clinicalNotes;
    private String emergencyType;
}
```

---

## 🛡️ Middleware — JwtFilter

The JwtFilter intercepts EVERY HTTP request before it reaches a controller.

```java
@Component
public class JwtFilter extends OncePerRequestFilter {
    // "OncePerRequestFilter" = runs exactly once per request (not twice on redirects)
    
    @Autowired private JwtUtil jwtUtil;
    @Autowired private UserRepository userRepo;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {
        
        // Step 1: Extract Authorization header
        String authHeader = request.getHeader("Authorization");
        
        // Step 2: Check if it starts with "Bearer "
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7); // remove "Bearer " prefix
            
            // Step 3: Extract email from token
            String email = jwtUtil.extractEmail(token);
            
            // Step 4: Load user from database
            User user = userRepo.findByEmail(email).orElseThrow();
            
            // Step 5: Validate token
            if (jwtUtil.validateToken(token, email)) {
                
                // Step 6: Create authentication object with role
                UsernamePasswordAuthenticationToken auth = 
                    new UsernamePasswordAuthenticationToken(
                        user, null, 
                        List.of(new SimpleGrantedAuthority("ROLE_" + user.getRole().name()))
                        // "ROLE_CLINIC", "ROLE_HOSPITAL", "ROLE_ADMIN"
                    );
                
                // Step 7: Store in Security Context (other code can access this)
                SecurityContextHolder.getContext().setAuthentication(auth);
            }
        }
        
        // Step 8: Continue to the next filter/controller
        chain.doFilter(request, response);
    }
}
```

---

## 🔒 SecurityConfig — Access Control

SecurityConfig defines WHO can access WHAT endpoints.

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity  // enables @PreAuthorize on methods
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            // ↑ Allow cross-origin requests (frontend on port 3000 → backend on 8080)
            
            .csrf(csrf -> csrf.disable())
            // ↑ Disable CSRF (safe because we use JWT stateless auth, not sessions+cookies)
            
            .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            // ↑ No server-side sessions — each request must carry its own JWT
            
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/auth/**", "/health", "/ws/**").permitAll()
                // ↑ Public: login, health check, WebSocket — no token required
                
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                // ↑ Only ADMIN can access admin endpoints
                
                .requestMatchers("/api/hospital/**").hasAnyRole("HOSPITAL", "ADMIN")
                // ↑ Hospital OR Admin can access hospital endpoints
                
                .requestMatchers("/api/clinic/**").hasAnyRole("CLINIC", "ADMIN")
                // ↑ Clinic OR Admin can access clinic endpoints
                
                .anyRequest().authenticated()
                // ↑ All other requests need to be authenticated
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
            // ↑ Run our JWT filter BEFORE Spring's default auth filter
        
        return http.build();
    }
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(10);
        // BCrypt with strength=10 → takes ~100ms to hash (brute-force protection)
    }
    
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOriginPatterns(List.of("*"));  // allow all origins
        config.setAllowedMethods(List.of("GET","POST","PUT","DELETE","OPTIONS","PATCH"));
        config.setAllowedHeaders(List.of("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);  // cache preflight for 1 hour
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
```

---

## 🔑 JwtUtil — Token Management

```java
@Component
public class JwtUtil {

    @Value("${vigilai.jwt.secret}")       // from environment variable or application.properties
    private String secret;

    @Value("${vigilai.jwt.expiration-ms}")
    private long expirationMs;  // 86400000 = 24 hours

    // Create a JWT token:
    public String generateToken(String email, Role role, String entityId, UUID userId) {
        return Jwts.builder()
                .subject(email)                    // who the token is for
                .claim("role", role.name())        // custom claim
                .claim("entityId", entityId)       // clinic/hospital ID
                .claim("userId", userId.toString())
                .issuedAt(new Date())              // current time
                .expiration(new Date(System.currentTimeMillis() + expirationMs))
                .signWith(getKey())                // sign with HMAC-SHA256
                .compact();                        // create the compact string
    }
    
    // Validate a token:
    public boolean validateToken(String token, String email) {
        try {
            return extractEmail(token).equals(email) && !isExpired(token);
        } catch (Exception e) {
            return false;  // invalid signature, malformed, etc.
        }
    }
    
    private SecretKey getKey() {
        return Keys.hmacShaKeyFor(secret.getBytes());
        // HMAC-SHA256 key derived from the secret string
    }
}
```

---

## 🔌 WebSocket — Real-Time Communication

```java
// WebSocketConfig.java:
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")   // clients connect to: ws://server:8080/ws
                .setAllowedOriginPatterns("*")
                .withSockJS();        // SockJS fallback for browsers that don't support WebSocket
    }

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic");    // server pushes to /topic/...
        config.setApplicationDestinationPrefixes("/app");  // client sends to /app/...
    }
}

// WebSocketService.java:
@Service
public class WebSocketService {

    @Autowired
    private SimpMessagingTemplate messagingTemplate;

    public void pushAlert(Alert alert) {
        messagingTemplate.convertAndSend("/topic/alerts", alert);
        // All browsers subscribed to "/topic/alerts" receive this alert instantly
        log.info("WebSocket: pushed alert #{}", alert.getAlertId());
    }
}
```

---

## 📊 Configuration Files

### application.properties (or application.yml):
```properties
# Server:
server.port=8080

# Database:
spring.datasource.url=jdbc:postgresql://localhost:5432/vigilai
spring.datasource.username=postgres
spring.datasource.password=${SPRING_DATASOURCE_PASSWORD}
spring.jpa.hibernate.ddl-auto=update

# JWT:
vigilai.jwt.secret=${JWT_SECRET:vigilai_default_secret_32chars_min}
vigilai.jwt.expiration-ms=86400000

# AI Service:
ai.service.url=${AI_SERVICE_URL:http://localhost:8000/predict}
llm.service.url=${LLM_SERVICE_URL:http://localhost:8000/explain}

# Logging:
logging.level.com.vigilai=INFO
```

Note the `${VARIABLE:default}` pattern — reads from environment variable, falls back to default.

---

## 🚨 Error Handling

### Global Exception Handler:
```java
@RestControllerAdvice  // applies to all controllers
public class GlobalExceptionHandler {

    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRuntime(RuntimeException e) {
        log.error("Runtime error: {}", e.getMessage());
        return ResponseEntity.status(500)
            .body(Map.of("error", e.getMessage()));
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(
            MethodArgumentNotValidException e) {
        // Collects all @Valid errors:
        Map<String, String> errors = new HashMap<>();
        e.getBindingResult().getFieldErrors()
         .forEach(err -> errors.put(err.getField(), err.getDefaultMessage()));
        return ResponseEntity.badRequest().body(Map.of("errors", errors));
    }
}
```

---

## 📝 Logging with SLF4J (Lombok's @Slf4j)

```java
@Slf4j  // adds: private static final Logger log = LoggerFactory.getLogger(ThisClass.class);
public class VitalController {

    public void submitVitals(...) {
        log.info("Vitals received: patient={}, clinic={}", patient.getPatientId(), clinicId);
        // INFO = normal operations
        
        log.warn("LLM failed: {}", e.getMessage());
        // WARN = something unexpected but recoverable
        
        log.error("Database error: {}", e.getMessage(), e);
        // ERROR = serious problem that needs attention
        
        log.debug("AI Request: {}", aiRequest);
        // DEBUG = detailed info for debugging (disabled in production)
    }
}
```

---

## 🌐 Complete Request Lifecycle

Trace what happens for `POST /api/clinic/vitals`:

```
1. Nginx (port 3000) → proxies to Spring Boot (port 8080)

2. JwtFilter.doFilterInternal()
   - Extracts "Authorization: Bearer eyJhbG..." header
   - Validates JWT signature and expiry
   - Sets authentication in SecurityContext

3. SecurityConfig authorization check
   - Endpoint is /api/clinic/vitals
   - Rule: .requestMatchers("/api/clinic/**").hasAnyRole("CLINIC","ADMIN")
   - User has ROLE_CLINIC → ALLOWED

4. VitalController.submitVitals(VitalRequest req)
   - Jackson deserializes JSON body → VitalRequest object
   - @Valid runs validation checks

5. PatientService.findOrCreate()
   - SQL: SELECT * FROM patients WHERE clinic_id=? AND phone_number=?
   - If not found: INSERT INTO patients (...)

6. vitalRepo.save(vital)
   - INSERT INTO vitals (patient_id, clinic_id, heart_rate, ...)

7. runTriage(vital, patient)
   - Check HR > 100, Temp > 38.5, etc.
   - INSERT INTO triage_flags (...)

8. aiService.getPrediction()
   - HTTP POST to http://ai-service:8000/predict
   - Python XGBoost returns {risk_score: 0.87, risk_level: "CRITICAL"}

9. llmService.explain()
   - HTTP POST to http://ai-service:8000/explain
   - Returns clinical explanation text

10. alertRepo.save(alert)
    - INSERT INTO alerts (patient_id, risk_score, severity, ...)

11. wsService.pushAlert(alert)
    - SimpMessagingTemplate → sends to /topic/alerts WebSocket channel
    - Hospital browser receives instant notification

12. auditLog.logAction("ALERT_CREATED", ...)
    - INSERT INTO audit_log_worm (...)

13. Return ResponseEntity.ok(response)
    - Jackson serializes Map → JSON
    - HTTP 200 with body: {vitalId, riskLevel, explanation, ...}
```

---

## 💼 Interview Questions & Answers

### Q1: What is Spring Boot and why is it used?
**A:** Spring Boot is an opinionated framework for building Java applications that auto-configures common settings, provides an embedded web server, and manages dependencies. In VigilAI, it handles: HTTP routing (controllers), database ORM (JPA), security (Spring Security), JSON serialization (Jackson), and WebSocket — all with minimal configuration.

### Q2: What is Dependency Injection?
**A:** Dependency Injection (DI) is a pattern where objects receive their dependencies from an external provider instead of creating them. In VigilAI, `VitalController` needs `AIService` — instead of writing `new AIService()` inside the controller, Spring creates one `AIService` instance and injects it everywhere via `@Autowired`. This enables loose coupling and easy testing.

### Q3: What is the difference between @Component, @Service, @Repository, @Controller?
**A:** All four are Spring-managed beans (Spring creates and manages their lifecycle). They differ in semantic meaning and additional features: `@Controller/@RestController` adds HTTP request handling. `@Service` is for business logic (conceptual). `@Repository` adds database exception translation. `@Component` is the generic base. VigilAI uses all four in their appropriate layers.

### Q4: What is JPA and how does Spring Data JPA help?
**A:** JPA (Java Persistence API) maps Java objects to database tables. Spring Data JPA adds automatic repository generation — you define an interface (`AlertRepository extends JpaRepository`) and Spring generates all the SQL queries from method names. `findByClinicianDecision("PENDING")` → `SELECT * FROM alerts WHERE clinician_decision = 'PENDING'`.

### Q5: What is CORS and why is it disabled in VigilAI for now?
**A:** CORS (Cross-Origin Resource Sharing) is a browser security feature that blocks JavaScript from making requests to a different domain/port than the page it's on. Since the VigilAI frontend (port 3000) calls the backend (port 8080), CORS configuration is needed. The current config allows all origins (`*`) which is fine for development but should be restricted in production.

### Q6: Why is CSRF disabled?
**A:** CSRF (Cross-Site Request Forgery) attacks work by tricking a browser into making authenticated requests using cookies. Since VigilAI uses JWT in the `Authorization` header (not cookies), CSRF attacks don't apply — an attacker's page can't access localStorage tokens from a different origin. So CSRF protection is safely disabled.

### Q7: What is the Builder pattern and why use it over constructors?
**A:** The Builder pattern creates objects step by step using method chaining. `Alert.builder().severity("CRITICAL").riskScore(0.87).build()` is more readable than a constructor with 20 parameters where the order matters. Lombok's `@Builder` annotation auto-generates this pattern, eliminating boilerplate code.

### Q8: What is the difference between `@RequestBody` and `@PathVariable`?
**A:** `@RequestBody` reads the HTTP request body (usually JSON) and maps it to a Java object — used for POST/PUT data. `@PathVariable` extracts a value from the URL path — used for `GET /alerts/{alertId}` where alertId is `@PathVariable Long alertId`. `@RequestParam` reads URL query parameters: `/alerts?status=PENDING` would use `@RequestParam String status`.

---

> **Next Module:** Module 5 covers the database in depth — PostgreSQL, every table, relationships, indexes, and how to query VigilAI's data.
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
# MODULE 6: Project Deep Dive
## VigilAI MedLink — Every File, Every Function, Every Decision

---

> [!IMPORTANT]
> This is the most comprehensive module. It explains EVERY file and function in the project, WHY each exists, and HOW the entire system works together. Read this module after understanding Modules 1–5.

---

## 📁 Complete Project Directory Map

```
modified-vigilai-medlink/
├── .git/                          ← Git version control (hidden)
├── .gitignore                     ← Files Git should ignore (node_modules, target/, *.env)
├── README.md                      ← Project documentation for developers
├── docker-compose.yml             ← Orchestrates all 4 services together
├── scratch.js                     ← Developer scratch pad (NOT production code)
├── seed_users.sql                 ← SQL to create demo users
├── seed_v2.sql                    ← SQL to seed hospitals, patients, vitals
│
├── database/
│   └── schema/
│       ├── 01_users.sql           ← users table + auth schema
│       └── 02_core.sql            ← patients, vitals, hospitals, alerts, audit
│
├── frontend/                      ← Pure HTML/CSS/JS (no build step!)
│   ├── index.html                 ← Redirect entry point
│   ├── login.html                 ← Authentication (475 lines)
│   ├── clinic.html                ← Clinic nurse dashboard (900+ lines)
│   ├── hospital.html              ← Hospital doctor dashboard (800+ lines)
│   └── admin.html                 ← Admin management panel (1000+ lines)
│
├── backend/                       ← Java Spring Boot application
│   ├── Dockerfile                 ← How to containerize the backend
│   ├── pom.xml                    ← Maven: Java dependencies + build config
│   └── src/main/
│       ├── java/com/vigilai/
│       │   ├── Application.java
│       │   ├── config/            ← Security, JWT, CORS, WebSocket
│       │   ├── controller/        ← HTTP endpoints
│       │   ├── service/           ← Business logic
│       │   ├── repository/        ← Database queries
│       │   ├── model/             ← Database entity classes
│       │   └── dto/               ← Request/Response data shapes
│       └── resources/
│           └── application.properties ← Configuration
│
└── ai-service/                    ← Python FastAPI ML service
    ├── Dockerfile                 ← How to containerize the AI service
    ├── requirements.txt           ← Python dependencies
    ├── runtime.txt                ← Python version (3.11)
    ├── models/
    │   └── xgboost_model.pkl      ← Trained XGBoost model (binary file)
    ├── data/
    │   └── vitals_dataset.csv     ← 10,000 row synthetic training dataset
    └── app/
        ├── main.py                ← FastAPI app + all endpoints
        ├── schema.py              ← Pydantic request/response models
        ├── inference/
        │   └── xgboost_model.py   ← Model loading, training, prediction
        └── triage/
            └── rule_engine.py     ← Age-adaptive clinical rules
```

---

## 🔍 File-by-File Deep Dive

### `docker-compose.yml` — The Orchestrator

This file defines all 4 services and how they connect:

```yaml
services:
  
  postgres:                              # Service 1: Database
    image: postgres:16-alpine            # Use official Postgres 16 image (alpine = small)
    container_name: vigilai-db
    environment:
      POSTGRES_DB:       vigilai         # Database name
      POSTGRES_USER:     postgres        # Admin username
      POSTGRES_PASSWORD: OMKAR@111       # Admin password (⚠️ should be env var in prod)
    ports:
      - "5432:5432"                      # host_port:container_port
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Persist data between restarts
      - ./database/schema/01_users.sql:/docker-entrypoint-initdb.d/01_users.sql
      - ./database/schema/02_core.sql:/docker-entrypoint-initdb.d/02_core.sql
      # docker-entrypoint-initdb.d = files here run on FIRST startup automatically
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]  # Check if Postgres is ready
      interval: 5s
      retries: 10

  ai-service:                            # Service 2: Python AI
    build: ./ai-service                  # Build from Dockerfile in ./ai-service/
    container_name: vigilai-ai
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1              # Show Python output immediately in logs

  backend:                              # Service 3: Java Backend
    build: ./backend
    container_name: vigilai-backend
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/vigilai
      # Note: "postgres" = the container name (Docker internal DNS resolves it)
      AI_SERVICE_URL: http://ai-service:8000/predict
      JWT_SECRET: vigilai_prod_secret_key_min_32_chars_long_!@#
    depends_on:
      postgres:
        condition: service_healthy      # Wait for Postgres to be ready
      ai-service:
        condition: service_healthy      # Wait for AI service to be ready

  frontend:                             # Service 4: Web Server
    image: nginx:alpine                 # Nginx serves static HTML files
    ports:
      - "3000:80"
    volumes:
      - ./frontend:/usr/share/nginx/html:ro  # Mount frontend files (read-only)
    depends_on:
      backend:
        condition: service_healthy

volumes:
  postgres_data:                        # Named volume (data survives container restart)
```

**Docker Networking:** All containers in a `docker-compose.yml` are on the same virtual network. The backend can reach the database at `postgres:5432` (container name as hostname), not `localhost:5432`.

---

### `backend/pom.xml` — Maven Build Configuration

Maven is the Java build tool (like npm for Node.js). `pom.xml` lists all dependencies.

```xml
<dependencies>
    
    <!-- spring-boot-starter-web -->
    <!-- Provides: Tomcat server, @RestController, @RequestMapping, ResponseEntity, Jackson JSON -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- spring-boot-starter-data-jpa -->
    <!-- Provides: @Entity, @Repository, JpaRepository, Hibernate ORM, automatic SQL generation -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <!-- postgresql -->
    <!-- The JDBC driver that lets Java talk to PostgreSQL -->
    <!-- scope=runtime: only needed at runtime, not for compilation -->
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    
    <!-- spring-boot-starter-security -->
    <!-- Provides: SecurityFilterChain, @PreAuthorize, BCryptPasswordEncoder, CSRF protection -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    
    <!-- spring-boot-starter-validation -->
    <!-- Provides: @Valid, @NotBlank, @Email, @Min, @Max on DTOs -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    
    <!-- jjwt (JJWT library) — JWT token creation and validation -->
    <!-- Three artifacts needed: api (compile), impl (runtime), jackson (runtime) -->
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-api</artifactId>
        <version>0.12.3</version>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-impl</artifactId>  <!-- implementation, runtime only -->
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-jackson</artifactId>  <!-- JSON serialization for JWT -->
        <scope>runtime</scope>
    </dependency>
    
    <!-- Lombok — eliminates boilerplate code -->
    <!-- @Data, @Builder, @Slf4j, @RequiredArgsConstructor, etc. -->
    <!-- optional=true: not included in final JAR (compile-time only) -->
    <dependency>
        <groupId>org.projectlombok</groupId>
        <artifactId>lombok</artifactId>
        <version>1.18.36</version>
        <optional>true</optional>
    </dependency>
    
    <!-- spring-boot-starter-websocket -->
    <!-- Provides: WebSocket, STOMP protocol, SockJS support -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-websocket</artifactId>
    </dependency>
    
    <!-- spring-boot-starter-test -->
    <!-- Provides: JUnit 5, Mockito, AssertJ, MockMvc for testing -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    
</dependencies>
```

---

### `ai-service/requirements.txt` — Python Dependencies

```txt
fastapi           # Web framework (like Spring Boot for Python)
uvicorn           # ASGI server (like Tomcat for FastAPI)
pydantic          # Data validation (like Spring @Valid)
xgboost           # Gradient boosting ML model
scikit-learn      # ML utilities (train_test_split, classification_report)
numpy             # Numerical arrays
pandas            # Data manipulation (for training)
httpx             # HTTP client
```

---

## 🏗️ Complete Application Flow

### Flow 1: New Patient Vitals Submission (Happy Path)

```
1. Nurse on clinic.html enters patient vitals
   
   Patient: Ramesh Patil, age 45, Male
   Vitals: HR=112, Temp=38.8°C, RR=24, BP=95/60, SpO2=91%
   
2. JavaScript builds JSON payload and POSTs to backend:
   POST /api/clinic/vitals
   Authorization: Bearer eyJhbGc...
   Body: { phoneNumber: "+919876543210", heart_rate: 112, ... }

3. JwtFilter intercepts:
   - Extracts token
   - Finds user: clinic@vigilai.health, role=CLINIC, entityId=clinic-demo-001
   - Sets authentication in SecurityContext

4. SecurityConfig checks: /api/clinic/** → hasAnyRole('CLINIC','ADMIN')
   User has ROLE_CLINIC → ✅ AUTHORIZED

5. VitalController.submitVitals() begins:

   [STEP 1] PatientService.findOrCreate()
   - Query: SELECT * FROM patients WHERE clinic_id='clinic-demo-001' 
            AND phone_number='+919876543210'
   - Found: patient_id=1, Ramesh Patil
   
   [STEP 2] autoDetectEmergencyType()
   - Notes: "high fever difficulty breathing"
   - HR=112 > normal → not CARDIAC (not > 150)
   - SpO2=91 < 88 is not true
   - Temp=38.8 > 38.5 && HR=112 > 90 && RR=24 > 20 → SEPSIS ✓
   - detectedEmergencyType = "SEPSIS"
   
   [STEP 3] Save Vital to database:
   INSERT INTO vitals (patient_id, clinic_id, heart_rate, temperature, ...)
   VALUES (1, 'clinic-demo-001', 112, 38.80, 24, 95, 60, 91, ...)
   vital_id = 47

   [STEP 4] runTriage():
   - hrFlag: 112 > 100 → TRUE
   - tempFlag: 38.8 > 38.5 → TRUE  
   - rrFlag: 24 > 24 is FALSE (boundary condition: > not >=)
   - bpFlag: 95 < 100 → TRUE
   - spo2Flag: 91 < 92 → TRUE
   - flagCount = 4
   - severity = "PRIORITY" (4 >= 2)
   INSERT INTO triage_flags (patient_id, vital_id, rule_severity='PRIORITY', 
                              hr_flag=T, temp_flag=T, rr_flag=F, bp_flag=T, spo2_flag=T,
                              flag_count=4)

   [STEP 5] AIService.getPrediction():
   HTTP POST to http://ai-service:8000/predict
   Body: {age: 45, heart_rate: 112, spo2: 91, respiratory_rate: 24,
          systolic_bp: 95, diastolic_bp: 60, temperature: 38.8, age_group: "ADULT"}
   
   Inside Python AI Service:
   - apply_age_adaptive_rules(vitals):
     - Adult rules: spo2 < 88? No (91). systolic < 80? No (95). HR > 150? No.
     - No critical override triggered
   - XGBoost model:
     features = [45, 112, 91, 24, 95, 60, 38.8]
     prob = model.predict_proba([[45,112,91,24,95,60,38.8]])[0][1]
     prob = 0.8732 (87.32% sepsis risk)
     level = "CRITICAL" (>= 0.80)
     confidence = abs(0.8732 - 0.5) * 2 = 0.7464
   - top_features:
     "SpO2 critically low (91%) ↓" ... "Tachycardia (112 bpm) ↑"
   
   Returns: {risk_score: 0.8732, risk_level: "CRITICAL", confidence: 0.7464,
             source: "XGBOOST_MODEL", top_features: [...]}

   [STEP 6] isHighRisk = TRUE (CRITICAL)
   LLMService.explain():
   HTTP POST to http://ai-service:8000/explain
   Returns clinical explanation, treatment recommendations, paramedic protocol
   
   [STEP 7] Create Alert:
   INSERT INTO alerts (patient_id=1, clinic_id='clinic-demo-001',
                       risk_score=0.8732, severity='CRITICAL', risk_level='CRITICAL',
                       emergency_type='SEPSIS', confidence=0.7464,
                       heart_rate=112, temperature=38.80, spo2=91, ...
                       llm_explanation='The AI model assessed 87% CRITICAL...',
                       treatment_recs='IMMEDIATE ACTIONS: O₂...',
                       status='NEW', clinician_decision='PENDING', ...)
   alert_id = 23
   
   WebSocketService.pushAlert(alert):
   messagingTemplate.convertAndSend("/topic/alerts", alert)
   → All hospital dashboards connected to WebSocket receive this alert INSTANTLY
   
   AuditLog: INSERT INTO audit_log_worm (action='ALERT_CREATED', entity_id='23', ...)

6. Response to clinic.html:
   {
     "vitalId": 47,
     "patientId": 1,
     "ageGroup": "ADULT",
     "riskLevel": "CRITICAL",
     "riskScore": 0.8732,
     "triageSeverity": "PRIORITY",
     "flagCount": 4,
     "alertCreated": true,
     "explanation": "The AI model assessed a 87% CRITICAL sepsis risk...",
     "treatmentRecs": "IMMEDIATE ACTIONS:\n• O₂ supplementation...",
     "paramedicGuidance": "EN-ROUTE PROTOCOL (ADULT):..."
   }

7. clinic.html displays:
   🚨 CRITICAL RISK — 87.32%
   Alert created — hospital notified!
   [Shows treatment recommendations to nurse]
```

---

### Flow 2: Hospital Doctor Reviews Alert

```
1. Doctor's hospital.html has an active WebSocket connection to /topic/alerts

2. Alert 23 arrives via WebSocket:
   {alertId: 23, severity: "CRITICAL", patientId: 1, ...}
   Browser adds alert card to the dashboard

3. Doctor reads: Ramesh Patil, 45M, CRITICAL SEPSIS, 87% risk
   Treatment recs: O₂, IV fluids, blood cultures, antibiotics

4. Doctor clicks "APPROVE"
   POST /api/hospital/alerts/23/decision
   Authorization: Bearer eyJhbGc...(hospital token)
   Body: {decision: "APPROVED", notes: "Sepsis confirmed by clinical presentation"}

5. AlertController.makeDecision():
   - Load alert 23 from database
   - Verify user role = HOSPITAL
   - Update: clinician_decision='APPROVED', decision_at=now, clinician_id='hospital-1'
   - Call VigilService.dispatchToAmbulance(alert)

6. VigilService.dispatchToAmbulance():
   - Load active hospitals from database (4 hospitals)
   - For each hospital, calculate:
     
     BMCRI (lat=12.96, lng=77.5725):
       distance = haversine(clinic_lat, clinic_lng, 12.96, 77.5725) = 8.2 km
       score = (100-12.5)*0.35 + min(12*10,100)*0.30 + max(0,100-8.2)*0.20 + 100*0.10 + 5
             = 30.625 + 30 + 18.36 + 10 + 5 = 93.985
     
     SJMC (lat=12.9279, lng=77.6271):
       distance = 12.1 km
       score = (100-15.2)*0.35 + min(7*10,100)*0.30 + max(0,87.9)*0.20 + 0 + 5
             = 29.68 + 21 + 17.58 + 0 + 5 = 73.26
     
     MHW (lat=12.9698, lng=77.75):
       distance = 18.7 km
       available = 50-35 = 15 beds
       score = (100-9.8)*0.35 + min(15*10,100)*0.30 + max(0,81.3)*0.20 + 100*0.10 + 5
             = 31.57 + 30 + 16.26 + 10 + 5 = 92.83
     
     → BEST HOSPITAL: BMCRI (score 93.985)
   
   - ETA = ceil((8.2/40)*60) + 5 = ceil(12.3) + 5 = 18 minutes
   - Update alert: dispatch_status='DISPATCHED', hospital_id=1, dispatched_at=now
   - AuditLog: action='DISPATCH_SENT', "Hospital=BMCRI, ETA=18min"

7. Response to hospital.html:
   {success: true, hospital: "Bangalore Medical College & RI", eta: 18}

8. Doctor sees: "Ambulance dispatched to BMCRI — ETA 18 minutes"
```

---

## 🤖 AI Service Deep Dive

### `app/schema.py` — Pydantic Models

Pydantic validates incoming data automatically:

```python
class VitalsRequest(BaseModel):
    age:              int   = Field(..., ge=0, le=120)
    # ge=0 means "greater than or equal to 0"
    # le=120 means "less than or equal to 120"
    # "..." means required (no default)
    
    heart_rate:       float = Field(..., ge=20, le=300)
    spo2:             float = Field(..., ge=0,  le=100)
    respiratory_rate: float = Field(..., ge=1,  le=100)
    systolic_bp:      float = Field(..., ge=40, le=300)
    diastolic_bp:     float = Field(..., ge=20, le=200)
    temperature:      float = Field(..., ge=28, le=45)
    age_group:        str   = Field(default="ADULT")
    emergency_type:   Optional[str] = None
# If any field fails validation, FastAPI returns 422 Unprocessable Entity automatically
```

### `app/inference/xgboost_model.py` — The AI Model

#### Singleton Pattern:
```python
_model_instance = None  # Module-level variable — shared across all requests

def get_model() -> XGBoostModel:
    global _model_instance
    if _model_instance is None:
        _model_instance = XGBoostModel()  # Load model ONCE
    return _model_instance               # Return the same instance always
# Why? Loading an XGBoost model takes ~200ms. Loading it once at startup
# and reusing it makes each prediction take ~1ms instead.
```

#### Model Loading:
```python
class XGBoostModel:
    def __init__(self):
        with open(MODEL_PATH, "rb") as f:
            self.model = pickle.load(f)
        # pickle = Python's built-in serialization
        # "rb" = read binary (the .pkl file is binary)
    
    def predict(self, features: list) -> tuple[float, int]:
        data = np.array(features, dtype=float).reshape(1, -1)
        # reshape(1, -1) = make it a 2D array with 1 row, N columns
        # XGBoost expects shape (n_samples, n_features)
        
        prob = float(self.model.predict_proba(data)[0][1])
        # predict_proba returns [[prob_class_0, prob_class_1]]
        # [0] = first (only) sample
        # [1] = probability of class 1 (sepsis)
        
        return prob, int(prob > 0.5)
        # Returns: (probability, binary_prediction)
        # e.g., (0.8732, 1) = 87.32% risk, classified as sepsis
```

#### Training Pipeline:
```python
def train():
    """Called once to create models/xgboost_model.pkl"""
    
    # 1. Generate or load dataset:
    df = pd.read_csv(DATASET)  # 10,000 rows of synthetic vitals
    
    # 2. Feature/Label split:
    X = df[["age", "heart_rate", "spo2", "respiratory_rate",
            "systolic_bp", "diastolic_bp", "temperature"]]
    y = df["sepsis_label"]  # 0=normal, 1=sepsis
    
    # 3. Train/test split:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    # 80% training, 20% test
    # stratify=y ensures equal class distribution in both splits
    
    # 4. XGBoost model:
    model = XGBClassifier(
        n_estimators=200,      # 200 decision trees
        max_depth=6,           # each tree can be 6 levels deep
        learning_rate=0.05,    # how much each tree contributes
        subsample=0.8,         # use 80% of data per tree (prevents overfitting)
        colsample_bytree=0.8,  # use 80% of features per tree
        scale_pos_weight=(y_train == 0).sum() / (y_train == 1).sum()
        # Handle class imbalance: if 70% normal, 30% sepsis →
        # scale_pos_weight = 7000/3000 ≈ 2.33
        # This tells the model to weight sepsis cases 2.33x more
    )
    
    # 5. Train:
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    
    # 6. Evaluate:
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    # Shows: precision, recall, F1-score for each class
    
    # 7. Save model:
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)  # Serialize to binary file
```

#### Synthetic Dataset Generation:
```python
def _generate_synthetic(path: str):
    """Creates a realistic synthetic training dataset"""
    n = 10_000  # 10,000 patients
    
    # Normal patients — vitals drawn from normal distributions:
    normal = pd.DataFrame({
        "heart_rate": rng.normal(75, 12, n//2).clip(55, 95),
        # Normal HR: mean=75, std=12, clipped between 55-95
        "spo2": rng.normal(97, 1.5, n//2).clip(94, 100),
        "temperature": rng.normal(36.8, 0.3, n//2).clip(36, 37.5),
        "sepsis_label": 0,
    })
    
    # Septic patients — vitals from distributions shifted toward danger zones:
    septic = pd.DataFrame({
        "heart_rate": rng.normal(115, 20, n//2).clip(90, 180),
        # Septic HR: mean=115 (tachycardia), std=20
        "spo2": rng.normal(88, 4, n//2).clip(70, 93),
        # Septic SpO2: mean=88 (hypoxia)
        "temperature": rng.normal(39.1, 0.8, n//2).clip(35, 42),
        # Septic Temp: mean=39.1 (fever)
        "sepsis_label": 1,
    })
    
    # Shuffle and combine:
    df = pd.concat([normal, septic]).sample(frac=1, random_state=42)
```

---

## 📊 Service Architecture Decisions

### Why Microservices? (AI as separate service)

**Alternative:** Embed ML in Java using DL4J or similar
**Why separate Python service instead:**
1. Python has the best ML ecosystem (XGBoost, scikit-learn, SHAP)
2. Independent scaling — AI service can have more CPU/RAM
3. Can update ML model without redeploying Java backend
4. Different deployment cadences (model retraining ≠ API changes)

### Why XGBoost for Sepsis Detection?

| Model | Why Not |
|-------|---------|
| Deep Neural Network | Too complex, needs huge data, not interpretable |
| Logistic Regression | Too simple, can't capture non-linear relationships |
| Random Forest | Good, but XGBoost generally outperforms it |
| **XGBoost** ✅ | Best for tabular medical data, interpretable, handles class imbalance |

### Why PostgreSQL with Arrays?

```sql
specializations TEXT[] DEFAULT '{}'
-- Alternatives:
-- Option A: Separate table (specializations_table) → requires JOIN
-- Option B: Comma-separated string ('CARDIAC,SEPSIS') → hard to query
-- Option C: PostgreSQL ARRAY → native support, queryable with ANY()
-- VigilAI chose Option C for simplicity (small dataset, no need for separate table)
```

### Why Denormalized Vitals in Alerts?

```
Option A: Store only vital_id in alerts, JOIN to get values:
  - Pro: No data duplication
  - Con: If vitals are archived, can't reconstruct the alert that triggered
  - Con: One more JOIN per query

Option B: Denormalize vitals into alerts table (current approach):
  - Pro: Alert is self-contained (audit/legal requirement)
  - Pro: No JOIN needed for alert display
  - Con: Data duplication (~7 extra columns)
  - VigilAI chose this for medical-legal compliance
```

---

## 🔁 Data Flow Diagrams

### JWT Authentication Flow:
```
login.html                Backend                    Database
    │                        │                           │
    │─── POST /auth/login ───►│                           │
    │    {email, password}    │                           │
    │                         │──── SELECT * FROM users ─►│
    │                         │    WHERE email=?          │
    │                         │◄─── User row ─────────────│
    │                         │                           │
    │                         │ BCrypt.matches(pass, hash)│
    │                         │                           │
    │                         │ JwtUtil.generateToken()   │
    │                         │ → "eyJhbGc.eyJzdWI.xxx"   │
    │                         │                           │
    │◄── 200 OK ──────────────│                           │
    │    {token, role, id}    │                           │
    │                         │                           │
    │ localStorage.setItem()  │                           │
    │ → redirect to clinic.html                           │

All subsequent requests:
clinic.html              JwtFilter              SecurityConfig
    │                        │                       │
    │─── POST /api/clinic ───►│                       │
    │    Authorization: Bearer│                       │
    │    eyJhbGc...           │                       │
    │                         │ extractEmail()        │
    │                         │ validateToken()       │
    │                         │ setAuthentication()   │
    │                         │────────────────────────►│
    │                         │                        │ hasRole('CLINIC')?
    │                         │◄───────────────────────│ YES → continue
    │                         │                        │
    │                         │── VitalController.submitVitals()
```

---

## 📋 Complete Dependency Graph

```
VitalController
    ├── depends on: VitalRepository → PostgreSQL
    ├── depends on: PatientRepository → PostgreSQL
    ├── depends on: AlertRepository → PostgreSQL
    ├── depends on: TriageFlagRepository → PostgreSQL
    ├── depends on: PatientService
    │                   └── PatientRepository
    ├── depends on: AIService
    │                   └── RestTemplate → Python AI Service (port 8000)
    ├── depends on: LLMService
    │                   └── RestTemplate → Python AI Service (port 8000)
    ├── depends on: AuditLogService
    │                   └── AuditLogRepository → PostgreSQL
    └── depends on: WebSocketService
                        └── SimpMessagingTemplate → WebSocket (hospital browsers)
```

---

## 💼 Architecture Decision Record (ADR) — Why These Choices?

| Decision | Options Considered | Choice Made | Reason |
|---------|-------------------|-------------|--------|
| Backend language | Java, Python, Node.js | Java + Spring Boot | Enterprise-grade, type-safe, Spring Security |
| Frontend framework | React, Vue, Angular | Vanilla HTML/JS | Simplicity, no build step, easy to deploy with Nginx |
| Database | PostgreSQL, MySQL, MongoDB | PostgreSQL | ACID, arrays, UUID, generated columns |
| ML framework | TensorFlow, PyTorch, XGBoost | XGBoost | Best for tabular data, interpretable, fast inference |
| Auth mechanism | Session-based, OAuth, JWT | JWT | Stateless, works across services, mobile-ready |
| Real-time | Polling, SSE, WebSocket | WebSocket (STOMP) | True bidirectional, low latency for emergency alerts |
| Containerization | Docker, VMs | Docker Compose | Reproducible, each service isolated |
| Audit logging | Application logs, DB trigger | WORM table | Tamper-evident, queryable, HIPAA-ready |

---

## 🎯 Mini Assignment — Trace a Complete Flow

Without looking at the code, describe what happens when:
1. A PEDIATRIC patient (age 10) with HR=180 is submitted by a clinic
2. The AI says CRITICAL
3. A HOSPITAL doctor dismisses the alert (instead of approving)

Then check your answer against:
- The triage logic for PEDIATRIC age group (Module 4)
- The `clinician_decision = 'DISMISSED'` path in AlertController
- What gets written to `audit_log_worm`

---

> **Next Module:** Module 7 covers Authentication, Security, and Best Practices — JWT deep dive, OWASP, password hashing, session management, and how VigilAI protects patient data.
# MODULE 7: Authentication, Security & Best Practices
## VigilAI MedLink — Securing Patient Data

---

> [!IMPORTANT]
> Healthcare applications handle sensitive patient data. Security is not optional — it's a legal requirement (HIPAA). This module teaches every security concept used in VigilAI.

---

## 🔐 Authentication vs Authorization

**Authentication = Who are you?**
- Proving your identity (login with email + password)
- VigilAI: `POST /auth/login` → validates credentials → issues JWT

**Authorization = What can you do?**
- Checking your permissions after identity is proven
- VigilAI: `@PreAuthorize("hasRole('CLINIC')")` → CLINIC can submit vitals, cannot manage hospitals

```
Authentication Journey:
Nurse → enters email/password → backend verifies → issues JWT token
           ↓ from now on ↓
Every API call → sends JWT → backend validates → identity confirmed ✓

Authorization Check:
JWT confirmed identity → Spring checks role → 
  CLINIC role accessing /api/clinic/** → ✅ ALLOWED
  CLINIC role accessing /api/admin/** → ❌ FORBIDDEN (403)
```

---

## 🎫 JWT — JSON Web Token (Deep Dive)

### What is a JWT?

A JWT is a digitally signed, compact, URL-safe token. It has three parts separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjbGluaWNAdmlnaWxhaS5oZWFsdGgi.8Kxyz...
        ↑                              ↑                              ↑
   Header (Base64)              Payload (Base64)              Signature
```

### Decoding a VigilAI JWT:

**Header:**
```json
{
  "alg": "HS256"   // HMAC-SHA-256 signing algorithm
}
```

**Payload (Claims):**
```json
{
  "sub": "clinic@vigilai.health",  // subject (who the token is for)
  "role": "CLINIC",                // custom claim
  "entityId": "clinic-demo-001",   // custom claim
  "userId": "550e8400-e29b-41d4",  // custom claim
  "iat": 1717401600,               // issued at (Unix timestamp)
  "exp": 1717488000                // expiry (24 hours later)
}
```

**Signature:**
```
HMAC-SHA256(
  base64url(header) + "." + base64url(payload),
  secretKey
)
```

### JwtUtil.java — Line by Line:

```java
@Component
public class JwtUtil {

    @Value("${vigilai.jwt.secret}")
    private String secret;  // "vigilai_prod_secret_key_min_32_chars_long_!@#"
    // Must be at least 256 bits (32 characters) for HMAC-SHA256
    // ⚠️ NEVER commit the real secret to Git!
    
    @Value("${vigilai.jwt.expiration-ms}")
    private long expirationMs;  // 86400000 = 86,400,000 ms = 24 hours

    private SecretKey getKey() {
        return Keys.hmacShaKeyFor(secret.getBytes());
        // Converts the string secret to a proper HMAC key object
    }

    public String generateToken(String email, Role role, String entityId, UUID userId) {
        return Jwts.builder()
                .subject(email)
                // Standard claim: "sub" = who this token represents
                
                .claim("role", role.name())
                // Custom claim: stores the role string ("CLINIC", "HOSPITAL", "ADMIN")
                
                .claim("entityId", entityId)
                // Custom claim: clinic/hospital ID (so backend knows which clinic)
                
                .claim("userId", userId != null ? userId.toString() : null)
                // Custom claim: user's UUID
                
                .issuedAt(new Date())
                // Standard claim: "iat" = current timestamp
                
                .expiration(new Date(System.currentTimeMillis() + expirationMs))
                // Standard claim: "exp" = current time + 24 hours
                
                .signWith(getKey())
                // Signs the token — tamper-proof (anyone modifying the token 
                // breaks the signature, and it will be rejected)
                
                .compact();
                // Creates the final "xxxxx.yyyyy.zzzzz" string
    }

    public boolean validateToken(String token, String email) {
        try {
            // If email matches AND token is not expired → valid
            return extractEmail(token).equals(email) && !isExpired(token);
        } catch (Exception e) {
            // Catches: ExpiredJwtException, MalformedJwtException, SignatureException
            return false;
        }
    }

    private Claims getClaims(String token) {
        return Jwts.parser()
                .verifyWith(getKey())    // verifies signature
                .build()
                .parseSignedClaims(token)  // parses and verifies
                .getPayload();             // returns the claims
        // Throws exception if token is expired, invalid, or tampered with
    }
}
```

### JWT Security Properties:

| Property | How JWT Achieves It |
|----------|-------------------|
| **Tamper-proof** | Signature covers header + payload. Any modification breaks signature |
| **Self-contained** | All user info (email, role) inside token — no database lookup needed per request |
| **Stateless** | Server doesn't store sessions — each token is independently verifiable |
| **Expirable** | `exp` claim causes automatic rejection after 24 hours |

### What JWT Does NOT Provide:

| Property | Why JWT Doesn't Help | VigilAI Mitigation |
|----------|---------------------|-------------------|
| **Revocation** | Can't invalidate a valid token before expiry | Short expiry (24h), change JWT secret to invalidate all |
| **Confidentiality** | Payload is Base64 encoded, not encrypted | Never put truly sensitive data in JWT payload |
| **Storage security** | localStorage is XSS-vulnerable | Use httpOnly cookies in production |

---

## 🔑 Password Hashing — BCrypt

### Why Hash Passwords?

**Never store plain passwords.** If your database is leaked:
- Plain password: "Clinic@123" → attacker can immediately login
- BCrypt hash: "$2a$12$Q3ZO/62p8o966iGm..." → attacker cannot reverse this

### How BCrypt Works:

```java
// Hashing (at registration/seeding):
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(10);
// "10" = cost factor (2^10 = 1024 iterations of SHA-256)
// Higher cost = slower hashing = harder to brute-force

String hash = encoder.encode("Clinic@123");
// Result: "$2a$10$randomSalt16chars...hashedValue..."
// The hash ALWAYS changes even for the same password (random salt)

// Verifying (at login):
boolean matches = encoder.matches("Clinic@123", storedHash);
// BCrypt extracts the salt from the hash and applies it
// Returns true if they match, false otherwise
```

### BCrypt Properties:

```
$2a$12$XrHoZRJVJvXbIZ1/kKg.Zug8S/Nx6WO40MfkLaIMtSnJzYMWlFBka
  ↑  ↑  ↑─────────────────────────────────────────────────────────
  │  │  └ 53-char hash
  │  └── cost factor 12 (2^12 = 4096 iterations — takes ~100ms)
  └───── version "2a"
```

**Why cost factor 10-12?**
- At cost 12: ~100ms to hash → User doesn't notice
- Attacker trying 1 million passwords: 100ms × 1,000,000 = 100,000 seconds = 27 hours
- With a GPU farm: still computationally expensive

---

## 🛡️ Spring Security Configuration Deep Dive

### SecurityConfig.java Explained:

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        // 1. CORS Configuration
        .cors(cors -> cors.configurationSource(corsConfigurationSource()))
        // CORS (Cross-Origin Resource Sharing):
        // Browser security policy: scripts from origin A cannot call origin B
        // Frontend: http://localhost:3000 calling Backend: http://localhost:8080
        // Without CORS config: browser blocks the request!
        // With CORS config: server tells browser "this origin is allowed"
        
        // 2. CSRF Disabled
        .csrf(csrf -> csrf.disable())
        // CSRF (Cross-Site Request Forgery): attacker tricks your browser into
        // making a request to a site you're logged into (using your cookies)
        // JWT in Authorization header (not cookies) is NOT vulnerable to CSRF
        // So we safely disable CSRF protection
        
        // 3. Stateless Sessions
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        // Don't create server-side sessions (no JSESSIONID cookie)
        // Each request is authenticated independently via JWT
        // This makes the application horizontally scalable (any server can handle any request)
        
        // 4. URL-based Authorization
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/auth/**", "/health", "/ws/**").permitAll()
            // These endpoints need NO authentication:
            // /auth/login, /auth/register — you're not logged in yet!
            // /health — monitoring tools check this without tokens
            // /ws/** — WebSocket handshake
            
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            // hasRole("ADMIN") = ROLE_ADMIN in security context
            // Only admins can: manage users, view all clinics, system config
            
            .requestMatchers("/api/hospital/**").hasAnyRole("HOSPITAL", "ADMIN")
            // Doctors AND admins can view hospital alerts
            
            .requestMatchers("/api/clinic/**").hasAnyRole("CLINIC", "ADMIN")
            // Nurses AND admins can submit vitals
            
            .anyRequest().authenticated()
            // Everything else just needs a valid JWT (any role)
        )
        
        // 5. JWT Filter Position
        .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
        // Run OUR filter before Spring's default filter
        // Our filter: reads JWT, extracts user/role, sets authentication
        // Spring's filter: would try form-login, which we don't use
    
    return http.build();
}
```

---

## 🌐 CORS — Cross-Origin Resource Sharing

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    
    config.setAllowedOriginPatterns(List.of("*"));
    // ⚠️ In production, restrict to your actual domains:
    // List.of("https://vigilai.health", "https://app.vigilai.health")
    
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));
    // OPTIONS = preflight request (browser sends OPTIONS before actual request)
    
    config.setAllowedHeaders(List.of("*"));
    // Allow all headers (including Authorization, Content-Type)
    
    config.setAllowCredentials(true);
    // Required when using cookies or Authorization header
    
    config.setMaxAge(3600L);
    // Browser caches preflight response for 1 hour (reduces OPTIONS requests)
    
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", config);
    // Apply to ALL endpoints
    return source;
}
```

### CORS Preflight Flow:
```
Browser                          Backend
    │                                │
    │─── OPTIONS /api/clinic/vitals ─►│  (preflight check)
    │    Origin: http://localhost:3000│
    │    Access-Control-Request-Method: POST
    │                                 │
    │◄── 200 OK ─────────────────────│
    │    Access-Control-Allow-Origin: *
    │    Access-Control-Allow-Methods: POST
    │                                 │
    │─── POST /api/clinic/vitals ────►│  (actual request)
    │    Authorization: Bearer xxx    │
    │                                 │
    │◄── 200 OK ─────────────────────│
```

---

## 🔒 OWASP Top 10 — How VigilAI Addresses Each

The OWASP Top 10 is the industry standard list of most critical web security risks.

### A01: Broken Access Control

**Risk:** User can access data/actions they shouldn't.

**VigilAI Protection:**
```java
// Method-level authorization:
@PreAuthorize("hasAnyRole('CLINIC','ADMIN')")
public ResponseEntity<?> submitVitals(...) { ... }

// Also validates that clinic user can only access THEIR clinic's data:
String entityId = jwtUtil.extractEntityId(token);
if (!entityId.equals(req.getClinicId())) {
    return ResponseEntity.status(403).body("Access denied");
}
```

### A02: Cryptographic Failures

**Risk:** Sensitive data not properly encrypted.

**VigilAI Protection:**
- Passwords hashed with BCrypt (not MD5/SHA1)
- JWT signed with HMAC-SHA256
- HTTPS in production (TLS 1.3)
- `is_encrypted` flag on vitals table (should use field-level encryption)

### A03: Injection

**Risk:** Attacker injects SQL/code into your application.

**SQL Injection Example:**
```
Attacker types: ' OR '1'='1 as email
Vulnerable code: "SELECT * FROM users WHERE email = '" + email + "'"
→ SQL becomes: SELECT * FROM users WHERE email = '' OR '1'='1'
→ Returns ALL users!
```

**VigilAI Protection:** Spring Data JPA uses parameterized queries:
```java
// This is SAFE:
userRepo.findByEmail(req.getEmail())
// JPA generates: SELECT * FROM users WHERE email = ?
// The ? is a parameter — user input NEVER becomes part of SQL syntax
```

### A04: Insecure Design

**Risk:** Security not considered in architecture.

**VigilAI Good Design:**
- WORM audit log (tamper-evident)
- Role-based access control
- AI alerts require human approval before dispatch

### A05: Security Misconfiguration

**Risk:** Default credentials, open ports, verbose errors.

**VigilAI Concerns:**
```yaml
# ⚠️ In docker-compose.yml:
POSTGRES_PASSWORD: OMKAR@111  # Should be environment variable, not hardcoded!
JWT_SECRET: vigilai_prod_secret_key...  # Should never be in source code!

# Production fix:
POSTGRES_PASSWORD: ${DB_PASSWORD}  # Read from environment variable
JWT_SECRET: ${JWT_SECRET}          # Set in deployment platform secrets
```

### A06: Vulnerable Components

**Risk:** Using outdated libraries with known vulnerabilities.

**VigilAI Practice:**
```xml
<!-- spring-boot-starter-parent 3.2.0 manages versions of 100+ dependencies -->
<!-- Run: mvn dependency-check to find known vulnerabilities -->
```

### A07: Identification and Authentication Failures

**Risk:** Weak passwords, no brute-force protection.

**VigilAI Current:**
- BCrypt for password hashing ✅
- JWT for stateless auth ✅

**VigilAI Missing (should add):**
```java
// Rate limiting — prevent brute-force attacks:
// After 5 failed logins, lock account for 15 minutes
@Bean
public UserDetailsService userDetailsService() {
    // Track failed attempts in database or Redis
}
```

### A08: Software and Data Integrity Failures

**Risk:** Using unsigned updates, untrusted dependencies.

**VigilAI:**
- WORM audit log with hash chain ✅
- Docker images from official sources ✅

### A09: Security Logging and Monitoring Failures

**Risk:** Can't detect attacks because there's no logging.

**VigilAI:**
```java
// All login attempts logged:
auditLog.logAction("USER_LOGIN", "USER", user.getId().toString(), ...);

// All alert decisions logged:
auditLog.logAction("ALERT_APPROVED", "ALERT", alertId, clinicianId, ...);

// All dispatch events logged:
auditLog.logAction("DISPATCH_SENT", "DISPATCH", alertId, "SYSTEM", ...);
```

### A10: Server-Side Request Forgery (SSRF)

**Risk:** Attacker tricks server into making requests to internal resources.

**VigilAI Concern:**
```java
// AI service URL is configurable:
@Value("${ai.service.url}")
private String aiServiceUrl;

// Mitigation: Validate that aiServiceUrl matches expected pattern
// Use allowlist: only allow "http://ai-service:8000/predict"
```

---

## 🔒 HIPAA Compliance Considerations

HIPAA (Health Insurance Portability and Accountability Act) governs how Protected Health Information (PHI) must be handled.

### Technical Safeguards Required:

| Requirement | VigilAI Implementation |
|-------------|----------------------|
| Access Control | JWT + Role-based access |
| Audit Controls | WORM audit log with hash chain |
| Integrity | Hash verification of audit entries |
| Transmission Security | HTTPS (required in production) |
| Authentication | BCrypt passwords + JWT tokens |

### What VigilAI Should Add for Full HIPAA:
1. **Field-level encryption** for PII (patient names, phone numbers)
2. **Automatic session timeout** (currently JWT doesn't expire on logout)
3. **IP-based access logging**
4. **Data retention policies** (when to delete patient records)
5. **Backup encryption**

---

## 🔑 Session Management

### VigilAI's Stateless Architecture:

```
Traditional Session-Based (what VigilAI does NOT use):
  Login → Server creates session {sessionId: "abc123", user: {...}} in memory/DB
  Every request → sends JSESSIONID cookie → server looks up session
  
  Problems:
  - If server restarts, sessions are lost
  - Multiple servers need shared session storage
  - CSRF vulnerability with cookies

JWT-Based (what VigilAI uses):
  Login → Server creates JWT token, sends to client
  Client stores token in localStorage
  Every request → sends "Authorization: Bearer <token>"
  Server validates token (no database lookup needed!)
  
  Benefits:
  - Stateless → any server can validate any token
  - No shared session storage needed
  - Works across domains
```

### Token Refresh Pattern (VigilAI improvement):
```javascript
// Currently, VigilAI tokens expire after 24 hours and user must re-login
// Better pattern (not implemented but should be):

// When token is close to expiry, silently request a new one:
async function refreshTokenIfNeeded() {
    const token = localStorage.getItem('vigilai_token');
    const payload = JSON.parse(atob(token.split('.')[1]));  // decode payload
    const expiresIn = payload.exp * 1000 - Date.now();
    
    if (expiresIn < 5 * 60 * 1000) {  // less than 5 minutes left
        const res = await fetch('/auth/refresh', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const { newToken } = await res.json();
        localStorage.setItem('vigilai_token', newToken);
    }
}
```

---

## 🔐 Secure Coding Best Practices

### 1. Never Log Sensitive Data:
```java
// ❌ BAD:
log.info("Login attempt: email={}, password={}", email, password);

// ✅ GOOD:
log.info("Login: {} [{}]", user.getEmail(), user.getRole());
// Never log passwords, tokens, or sensitive patient data
```

### 2. Always Validate Input:
```java
// Frontend validation (UX, not security):
if (!email || !password) { showError("..."); return; }

// Backend validation (SECURITY — always validate server-side):
@PostMapping("/login")
public ResponseEntity<?> login(@Valid @RequestBody LoginRequest req) {
    // @Valid triggers Bean Validation:
    // @Email checks format, @NotBlank prevents empty
}

// Additional business validation:
if (user.getAge() < 0 || user.getAge() > 150) {
    return ResponseEntity.badRequest().body("Invalid age");
}
```

### 3. Use Parameterized Queries (already done via JPA):
```java
// ✅ JPA handles this safely:
patientRepo.findByClinicIdAndPhoneNumber(clinicId, phone);
// Never do:
// entityManager.createQuery("SELECT p FROM Patient p WHERE p.clinicId = '" + clinicId + "'");
```

### 4. Minimal Exposure — Don't Return Sensitive Data:
```java
// ❌ BAD — returns the password hash!
return ResponseEntity.ok(user);

// ✅ GOOD — return only what's needed:
return ResponseEntity.ok(new AuthResponse(
    token, user.getRole().name(), user.getEntityId(), user.getFullName(), user.getEmail()
    // password_hash is NOT included!
));
```

### 5. Environment Variables for Secrets:
```properties
# application.properties — safe to commit:
vigilai.jwt.secret=${JWT_SECRET:default_dev_secret_32chars_min}

# Set in deployment:
# Docker: environment: JWT_SECRET: "real_secret_here"
# Render.com: Environment Variables section
# Kubernetes: Secrets
```

---

## 🔒 HTTPS and TLS

In production, ALL traffic must be encrypted with HTTPS (HTTP + TLS).

```
Without HTTPS (plain HTTP):
  Clinic → [HR=112, Temp=38.8, Patient: Ramesh Patil] → Server
  Anyone on the network can READ this! (Patient data breach)

With HTTPS (TLS 1.3):
  Clinic → [gibberish encrypted data] → Server
  Even if intercepted, nobody can read it
```

### How TLS Works (Simplified):
1. Browser connects to server
2. Server sends its certificate (issued by a Certificate Authority)
3. Browser verifies certificate is legitimate
4. Both agree on an encryption key using asymmetric cryptography
5. All data is encrypted with that key

VigilAI on Render.com: Render provides automatic HTTPS with Let's Encrypt certificates.

---

## 💼 Interview Questions & Answers

### Q1: How does JWT authentication work in VigilAI?
**A:** When a user logs in with email/password, the backend: 1) finds the user in the database, 2) verifies the password against the BCrypt hash, 3) generates a JWT containing the user's email, role, and entity ID (signed with HMAC-SHA256), 4) returns the token to the client. The client stores this in localStorage and includes it as `Authorization: Bearer <token>` in every subsequent request. The JwtFilter intercepts each request, validates the token, and sets the authenticated user in the Spring Security context.

### Q2: Why is BCrypt used instead of SHA256 for passwords?
**A:** SHA256 is a fast hash (designed for speed). An attacker can try billions of SHA256 hashes per second. BCrypt is deliberately slow (cost factor 12 = ~100ms). More importantly, BCrypt automatically generates and embeds a random salt, preventing rainbow table attacks (pre-computed hash tables). Each BCrypt hash is unique even for identical passwords.

### Q3: What is the difference between authentication and authorization?
**A:** Authentication verifies identity (who are you?) via login. Authorization determines permissions (what can you do?). In VigilAI, authentication happens at `/auth/login` (JwtFilter validates tokens). Authorization happens via Spring Security rules — CLINIC role can access `/api/clinic/**` but not `/api/admin/**`. `@PreAuthorize("hasRole('CLINIC')")` enforces method-level authorization.

### Q4: What is CORS and why is it needed?
**A:** CORS is a browser security policy that prevents JavaScript on one origin (domain:port) from making requests to another origin. VigilAI frontend (port 3000) needs to call backend (port 8080) — different origins. The backend's `CorsConfigurationSource` tells browsers which origins are allowed. Without CORS configuration, browsers would block all cross-origin requests.

### Q5: Why is CSRF disabled in VigilAI?
**A:** CSRF attacks work by exploiting cookies (the browser automatically sends cookies to the target site). VigilAI uses JWT in the `Authorization` header instead of cookies. Since a malicious third-party site can't access localStorage tokens from another origin, CSRF is not applicable. Therefore, CSRF protection is safely disabled.

### Q6: What is an OWASP Top 10 vulnerability?
**A:** OWASP Top 10 is the industry-standard list of most critical web security risks. Key risks relevant to VigilAI: A01 (Broken Access Control) — mitigated by @PreAuthorize; A02 (Cryptographic Failures) — mitigated by BCrypt + HTTPS; A03 (Injection) — mitigated by JPA parameterized queries; A09 (Insufficient Logging) — mitigated by WORM audit log.

### Q7: What is the WORM audit log and why is it used?
**A:** WORM (Write Once, Read Many) means records can never be modified after creation. VigilAI's `audit_log_worm` table uses a hash chain — each entry contains the SHA-256 hash of the previous entry. If anyone tampers with an old record, all subsequent hashes become invalid. This provides a tamper-evident audit trail required for medical-legal compliance and HIPAA.

---

> **Next Module:** Module 8 covers Testing, Debugging, and Development Workflow — how to find and fix bugs in VigilAI, Git workflow, testing strategies, and industry practices.
# MODULE 8: Testing, Debugging & Development Workflow
## VigilAI MedLink — Finding and Fixing Problems Like a Pro

---

> [!NOTE]
> Debugging is the most important skill a developer can have. This module teaches you how to systematically find and fix every type of problem in VigilAI.

---

## 🐛 Debugging Philosophy

> "Debugging is twice as hard as writing code. If you write code as cleverly as you can, you're not clever enough to debug it." — Brian Kernighan

**The Scientific Method for Debugging:**
1. **Observe** — What is the exact error/behavior?
2. **Hypothesize** — What could cause this?
3. **Test** — Make one change to test your hypothesis
4. **Analyze** — Did it fix it? If yes, done. If no, new hypothesis.

---

## 🌐 Browser DevTools — Frontend Debugging

Every browser has built-in developer tools. Press `F12` to open them.

### Tab 1: Console — JavaScript Errors

```javascript
// Add these to debug frontend:
console.log("Login function called");
console.log("Email:", email, "Role:", selectedRole);
console.log("API Response:", data);
console.error("Error:", e.message);

// In VigilAI login.html, add temporarily:
async function login() {
    console.log("=== LOGIN START ===");
    const email = document.getElementById('email').value.trim();
    console.log("Email:", email);
    
    const res = await fetch(`${API}/auth/login`, { ... });
    console.log("Response status:", res.status);
    
    const data = await res.json();
    console.log("Response data:", data);
    // ...
}
```

**Common Console Errors in VigilAI:**

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to fetch` | Backend server is down or wrong URL | Check `const API = "..."` URL, ensure backend is running |
| `CORS error` | Backend CORS not configured for frontend origin | Check SecurityConfig CORS settings |
| `401 Unauthorized` | Wrong credentials or expired token | Re-login, check credentials |
| `403 Forbidden` | Role doesn't have permission | Check which role you're logged in as |
| `Cannot read properties of null` | Element with that ID doesn't exist | Check HTML element IDs match JavaScript |

### Tab 2: Network — API Requests

The Network tab shows every HTTP request the browser makes:

```
How to debug a failed vitals submission:
1. Open DevTools → Network tab
2. Check "Preserve log" (keeps requests after redirect)
3. Submit vitals
4. Find POST /api/clinic/vitals in the list
5. Click on it → see:
   - Request Headers (is Authorization header present?)
   - Request Payload (is the JSON correct?)
   - Response (what did the backend return?)
   - Status Code (200? 401? 500?)
```

**Reading the Network Tab:**

```
Name                    Status   Method  Response
GET /auth/health         200      GET    {"status":"healthy"}
POST /auth/login         200      POST   {"token":"eyJ...","role":"CLINIC"}
POST /api/clinic/vitals  500      POST   {"error":"Patient not found: null"}
                          ↑
                    Look at response body to understand the error!
```

### Tab 3: Application — localStorage

```
Storage → Local Storage → http://localhost:3000
Shows: vigilai_token, vigilai_role, vigilai_entityId, vigilai_name
If these are missing → user is not logged in
If token is "demo-token" → user is in demo mode
```

### Tab 4: Elements — CSS Debugging

```
Right-click on any element → "Inspect"
Hover over elements to see their computed CSS
Uncheck/modify CSS properties in real-time
Find which CSS class is causing a styling issue
```

---

## 🖥️ Backend Debugging — Spring Boot

### 1. Reading Spring Boot Logs

Spring Boot logs to the console. Learn to read them:

```
2024-06-04 11:30:15 INFO  c.v.controller.VitalController - Vitals received: patient=1, clinic=clinic-demo-001
2024-06-04 11:30:15 INFO  c.v.service.AIService - AI call: POST http://ai-service:8000/predict
2024-06-04 11:30:16 WARN  c.v.controller.VitalController - LLM failed: Connection refused
2024-06-04 11:30:16 WARN  c.v.controller.VitalController - 🚨 ALERT #23 — CRITICAL
2024-06-04 11:30:16 INFO  c.v.service.WebSocketService - WebSocket: pushed alert #23
```

**Log levels:**
- `DEBUG` = Verbose detail (disabled in production)
- `INFO` = Normal operations (green flag)
- `WARN` = Something unexpected but handled (yellow flag)
- `ERROR` = Serious problem that needs attention (red flag)

### 2. Enable Debug Logging for VigilAI:

In `application.properties`:
```properties
# Show all SQL queries:
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# More verbose logging:
logging.level.com.vigilai=DEBUG
logging.level.org.springframework.security=DEBUG
logging.level.org.springframework.web=DEBUG
```

With security debug enabled, you'll see:
```
FilterSecurityInterceptor - Secure object: POST /api/clinic/vitals
FilterSecurityInterceptor - Previously Authenticated: ...CLINIC
FilterSecurityInterceptor - Authorization successful
```

### 3. Common Spring Boot Errors:

#### Error: `DataIntegrityViolationException`
```
Caused by: org.postgresql.util.PSQLException: 
ERROR: duplicate key value violates unique constraint "patients_clinic_id_phone_number_key"
```
**Cause:** Trying to create a patient that already exists (clinic_id + phone_number is unique)
**Fix:** Use `findOrCreate` pattern — check if exists before inserting

#### Error: `HttpClientErrorException: 401 Unauthorized`
```
2024-06-04 AIService - AI call failed: 401 Unauthorized
```
**Cause:** AI service (Python) returned 401
**Fix:** Check if AI service has authentication enabled (it shouldn't for internal calls)

#### Error: `BeanCreationException`
```
Caused by: java.lang.IllegalStateException: 
@Bean method SecurityConfig.passwordEncoder not found
```
**Cause:** Spring can't find a required bean
**Fix:** Add `@Configuration` annotation to the class that defines the bean

#### Error: `LazyInitializationException`
```
org.hibernate.LazyInitializationException: 
failed to lazily initialize a collection of role: Alert.vitals
```
**Cause:** Trying to access a lazily-loaded relationship outside of a transaction
**Fix:** Use `@Transactional` on the service method, or use `EAGER` fetch type

### 4. Connecting IntelliJ Debugger to Docker:

```bash
# In backend Dockerfile, add Java debug port:
CMD ["java", "-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:5005", 
     "-jar", "app.jar"]

# In docker-compose.yml, expose debug port:
backend:
  ports:
    - "8080:8080"
    - "5005:5005"  # Debug port
```

Then in IntelliJ: Run → Attach Debugger → Port 5005
Set breakpoints in VitalController.submitVitals() and step through!

---

## 🔌 API Debugging with Postman

Postman is the industry-standard tool for testing APIs.

### Setting Up Postman for VigilAI:

**Step 1: Create a Collection**
```
VigilAI MedLink
├── Auth
│   ├── Login (POST /auth/login)
│   └── Register (POST /auth/register)
├── Clinic
│   ├── Submit Vitals (POST /api/clinic/vitals)
│   └── Patient History (GET /api/clinic/vitals/patient/1)
└── Hospital
    ├── Get Alerts (GET /api/hospital/alerts)
    └── Make Decision (POST /api/hospital/alerts/23/decision)
```

**Step 2: Set Up Authentication**
```
In Collection → Authorization → Bearer Token → {{token}}
({{token}} is a Postman variable you set after login)
```

**Step 3: Login Request**
```json
POST http://localhost:8080/auth/login
Content-Type: application/json

{
    "email": "clinic@vigilai.health",
    "password": "Clinic@123"
}
```
After response, set the token:
```javascript
// In Postman Tests tab:
const response = pm.response.json();
pm.collectionVariables.set("token", response.token);
```

**Step 4: Submit Vitals**
```json
POST http://localhost:8080/api/clinic/vitals
Authorization: Bearer {{token}}
Content-Type: application/json

{
    "clinicId": "clinic-demo-001",
    "phoneNumber": "+919876543210",
    "fullName": "Test Patient",
    "age": 45,
    "gender": "M",
    "heart_rate": 115,
    "temperature": 39.2,
    "respiratory_rate": 26,
    "systolic_bp": 88,
    "diastolic_bp": 55,
    "spo2": 89,
    "clinicalNotes": "Severe fever, difficulty breathing",
    "emergencyType": "AUTO-DETECT"
}
```

---

## 🗄️ Database Debugging

### Connect to PostgreSQL via Docker:

```bash
# Shell into the running Postgres container:
docker exec -it vigilai-db psql -U postgres -d vigilai

# Now you can run SQL:
\dt                          -- list all tables
\d patients                  -- describe patients table
SELECT count(*) FROM alerts;
SELECT * FROM alerts ORDER BY created_at DESC LIMIT 5;

# Useful debugging queries:
-- Check users:
SELECT id, email, role, entity_id, is_active FROM users;

-- Check recent vitals:
SELECT v.*, p.full_name, p.age_group 
FROM vitals v JOIN patients p ON v.patient_id = p.patient_id
ORDER BY v.created_at DESC LIMIT 10;

-- Check audit log:
SELECT action, entity_type, entity_id, user_id, new_value, timestamp 
FROM audit_log_worm 
ORDER BY timestamp DESC LIMIT 20;

-- Verify triage logic:
SELECT tf.*, p.age, p.age_group
FROM triage_flags tf JOIN patients p ON tf.patient_id = p.patient_id
WHERE tf.flag_count >= 2 ORDER BY tf.flagged_at DESC;
```

---

## 🐍 AI Service Debugging

### Testing Python FastAPI:

```bash
# FastAPI has automatic interactive docs!
# Open: http://localhost:8000/docs
# You can test all endpoints directly in the browser (Swagger UI)

# Or use curl:
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 45, "heart_rate": 115, "spo2": 89, "respiratory_rate": 26,
       "systolic_bp": 88, "diastolic_bp": 55, "temperature": 39.2,
       "age_group": "ADULT"}'
```

### AI Service Logs:

```bash
# View AI service logs in Docker:
docker logs vigilai-ai -f

# Expected output:
INFO:vigilai-ai:Predict: age=45, HR=115, SpO2=89, RR=26, BP=88/55, Temp=39.2, group=ADULT
INFO:vigilai-ai:✅ XGBoost model loaded  (on first request)
```

### Common AI Service Issues:

| Issue | Error | Fix |
|-------|-------|-----|
| Model file missing | `FileNotFoundError: Model not found` | Run training: `python -c "from app.inference.xgboost_model import train; train()"` |
| Port already in use | `Address already in use: 8000` | `pkill -f uvicorn` |
| Memory error | `MemoryError during model load` | Increase Docker container memory limit |
| Import error | `ModuleNotFoundError: No module named 'xgboost'` | `pip install -r requirements.txt` |

---

## 🧪 Testing — Writing Tests for VigilAI

### Unit Testing (Java — JUnit 5 + Mockito):

**What is Unit Testing?**
Testing a single method/class in isolation, mocking all dependencies.

```java
// Test file: src/test/java/com/vigilai/service/VigilServiceTest.java
@ExtendWith(MockitoExtension.class)
class VigilServiceTest {

    @Mock
    private AlertRepository alertRepo;    // mock — doesn't hit database
    @Mock
    private HospitalRepository hospitalRepo;
    @Mock
    private AuditLogService auditLog;
    
    @InjectMocks
    private VigilService vigilService;    // real service with mocked dependencies

    @Test
    void testSelectBestHospital_prefers_closer_hospital() {
        // Arrange — set up test data:
        Hospital close = new Hospital();
        close.setHospitalId(1);
        close.setLatitude(new BigDecimal("12.9600"));  // 8km away
        close.setLongitude(new BigDecimal("77.5725"));
        close.setTotalIcuBeds(40);
        close.setOccupiedBeds(28);
        close.setSepsisMortalityRate(new BigDecimal("12.5"));
        close.setIsLevel1Trauma(true);
        close.setSpecializations(new String[]{"SEPSIS","CARDIAC"});
        
        Hospital far = new Hospital();
        far.setHospitalId(2);
        far.setLatitude(new BigDecimal("13.1000"));   // 20km away
        far.setLongitude(new BigDecimal("77.8000"));
        far.setTotalIcuBeds(40);
        far.setOccupiedBeds(28);
        far.setSepsisMortalityRate(new BigDecimal("12.5"));
        far.setIsLevel1Trauma(true);
        
        when(hospitalRepo.findByIsActiveTrue()).thenReturn(List.of(close, far));
        
        Alert alert = new Alert();
        alert.setClinicLatitude(12.9716);
        alert.setClinicLongitude(77.5946);
        alert.setEmergencyType("SEPSIS");
        
        // Act — call the method:
        Hospital result = vigilService.selectBestHospital(alert);
        
        // Assert — verify the result:
        assertEquals(1, result.getHospitalId(), "Should select the closer hospital");
    }
    
    @Test
    void testCalculateETA_correctForKnownDistance() {
        // 8 km at 40 km/h = 12 min + 5 prep = 17 min → ceil = 17
        // But formula: ceil(8/40 * 60) + 5 = ceil(12) + 5 = 17
        // Access via reflection or make method package-private:
        // ...
    }
}
```

### Integration Testing (MockMvc):

**What is Integration Testing?**
Testing the full request → controller → service → repository flow with a real (or in-memory) database.

```java
@SpringBootTest
@AutoConfigureMockMvc
@Transactional  // rollback after each test
class VitalControllerTest {

    @Autowired
    private MockMvc mockMvc;     // simulates HTTP requests
    
    @Autowired
    private ObjectMapper objectMapper;  // JSON serialization
    
    @MockBean
    private AIService aiService;   // mock AI service (don't call Python in tests)
    
    @MockBean
    private LLMService llmService;

    @Test
    void testSubmitVitals_withHighRisk_createsAlert() throws Exception {
        // Arrange: mock AI response:
        AIPredictionResponse mockAI = new AIPredictionResponse(
            0.87, "CRITICAL", 0.75, "XGBOOST_MODEL",
            new String[]{"SpO2 critically low"}
        );
        when(aiService.getPrediction(any())).thenReturn(mockAI);
        
        // Build valid JWT token for test:
        String token = "Bearer " + generateTestToken("clinic@test.com", Role.CLINIC, "clinic-test-001");
        
        // Build request:
        Map<String, Object> req = new HashMap<>();
        req.put("clinicId", "clinic-test-001");
        req.put("phoneNumber", "+919999999999");
        req.put("age", 45);
        req.put("heart_rate", 115);
        // ... other vitals
        
        // Act:
        mockMvc.perform(post("/api/clinic/vitals")
                .header("Authorization", token)
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(req)))
                
        // Assert:
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.riskLevel").value("CRITICAL"))
            .andExpect(jsonPath("$.alertCreated").value(true))
            .andExpect(jsonPath("$.riskScore").value(0.87));
    }
    
    @Test
    void testSubmitVitals_withoutToken_returns401() throws Exception {
        mockMvc.perform(post("/api/clinic/vitals")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
            .andExpect(status().isUnauthorized());
    }
    
    @Test
    void testSubmitVitals_withHospitalRole_returns403() throws Exception {
        String hospitalToken = "Bearer " + generateTestToken("hospital@test.com", Role.HOSPITAL, "1");
        
        mockMvc.perform(post("/api/clinic/vitals")
                .header("Authorization", hospitalToken)
                .contentType(MediaType.APPLICATION_JSON)
                .content("{}"))
            .andExpect(status().isForbidden());
    }
}
```

### Python Testing with pytest:

```python
# test_ai_service.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_critical_vitals():
    response = client.post("/predict", json={
        "age": 45,
        "heart_rate": 120,
        "spo2": 87,        # critically low
        "respiratory_rate": 28,
        "systolic_bp": 85,  # hypotension
        "diastolic_bp": 55,
        "temperature": 39.5,
        "age_group": "ADULT"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["HIGH ALERT", "CRITICAL"]
    assert data["risk_score"] > 0.5

def test_predict_normal_vitals():
    response = client.post("/predict", json={
        "age": 30,
        "heart_rate": 72,
        "spo2": 98,
        "respiratory_rate": 14,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "temperature": 36.8,
        "age_group": "ADULT"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["LOW", "MEDIUM"]

def test_predict_invalid_vitals():
    response = client.post("/predict", json={
        "age": -5,   # invalid age
        "heart_rate": 72,
        "spo2": 98,
        "respiratory_rate": 14,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "temperature": 36.8
    })
    assert response.status_code == 422  # Validation error
```

---

## 🔄 Git Workflow — Industry Standard

### Basic Git Commands:

```bash
# Check current status:
git status

# See what changed:
git diff

# Stage changes:
git add src/main/java/com/vigilai/service/VigilService.java
git add .   # stage everything (careful!)

# Commit:
git commit -m "feat: add Haversine distance calculation to hospital selection"

# Push to remote:
git push origin main

# Pull latest changes:
git pull origin main

# Check commit history:
git log --oneline -10
```

### Branch Strategy (Git Flow):

```
main ─────────────────────────────────────────────────► production
  │
  ├── develop ────────────────────────────────────────► staging
  │     │
  │     ├── feature/jwt-auth ────► (merge to develop when done)
  │     ├── feature/ai-integration
  │     ├── feature/websocket-alerts
  │     └── bugfix/null-patient-id
  │
  └── hotfix/critical-security-patch ────► (merge to main AND develop)
```

### Commit Message Convention (Conventional Commits):

```
feat: add ambulance dispatch algorithm
fix: handle null clinicId in vitals submission
docs: add API documentation for /auth/login
refactor: extract hospital scoring into separate method
test: add unit tests for VigilService.selectBestHospital
chore: update Spring Boot to 3.2.1

Format:
<type>: <description>

Types: feat, fix, docs, style, refactor, test, chore
```

---

## 🔍 Common VigilAI Bugs and How to Fix Them

### Bug 1: Login Works But Redirects to Wrong Page

```
Symptom: Clinic user logs in and gets redirected to hospital.html

Debug Steps:
1. Check localStorage after login (DevTools → Application → Local Storage)
2. Look at vigilai_role value
3. Is it "CLINIC" or something else?

Root Cause: Backend returning wrong role
Fix: Check AuthController:
  return ResponseEntity.ok(new AuthResponse(
      token,
      user.getRole().name(),  ← must be "CLINIC", "HOSPITAL", or "ADMIN"
      ...
  ));
```

### Bug 2: Vitals Submission Returns 500 Error

```
Symptom: POST /api/clinic/vitals returns 500

Debug Steps:
1. Check backend logs: docker logs vigilai-backend
2. Look for the stack trace
3. Common: "Patient not found" or "NullPointerException"

Common Causes:
a) PhoneNumber is null → clinicId is null → patient can't be found
b) AI service is down → service returns 500 error
c) Database constraint violation → duplicate patient

Root Cause A Fix:
  Check frontend payload is complete
  Add null check:
  if (req.getPhoneNumber() == null) {
      return ResponseEntity.badRequest().body(Map.of("error", "Phone number required"));
  }
```

### Bug 3: WebSocket Alerts Not Appearing in Hospital Dashboard

```
Symptom: Alert is created in database but hospital.html doesn't show it

Debug Steps:
1. Check if WebSocket is connected: browser console → "WebSocket connected"
2. Check backend logs: "WebSocket: pushed alert #23"
3. Check network tab for WebSocket frames (Protocol = ws or wss)

Common Causes:
a) Frontend not subscribing to correct topic (/topic/alerts)
b) SockJS library not loaded
c) Backend WebSocket URL wrong

Fix for (a):
  stompClient.subscribe('/topic/alerts', message => { ... });
  // Make sure this EXACT topic matches what backend sends to:
  // messagingTemplate.convertAndSend("/topic/alerts", alert);
```

### Bug 4: AI Service Returns 500 — Model Not Found

```
Symptom: POST /predict returns 500
Log: "FileNotFoundError: Model not found: .../models/xgboost_model.pkl"

Cause: Model hasn't been trained yet

Fix:
  # Run training script once:
  docker exec -it vigilai-ai python -c "from app.inference.xgboost_model import train; train()"
  
  # Or train locally:
  cd ai-service
  pip install -r requirements.txt
  python -c "from app.inference.xgboost_model import train; train()"
```

---

## 📋 Testing Checklist for VigilAI

Before submitting code, verify:

```
Authentication:
  [ ] Login with clinic credentials → goes to clinic.html
  [ ] Login with hospital credentials → goes to hospital.html
  [ ] Login with wrong password → shows error message
  [ ] Access /api/clinic/vitals without token → 401 returned

Vitals Submission:
  [ ] Submit normal vitals → LOW risk, no alert created
  [ ] Submit critical vitals (SpO2=85, BP=80) → CRITICAL, alert created
  [ ] Submit vitals for new patient → patient created in DB
  [ ] Submit vitals for existing patient (same phone) → patient reused

Alert Flow:
  [ ] Alert appears in hospital dashboard after submit
  [ ] Doctor can approve alert → dispatch triggered
  [ ] Doctor can dismiss alert → status=DISMISSED
  [ ] Audit log entry created for each action

Error Cases:
  [ ] Missing required field → 400 with error message
  [ ] Invalid vital sign range → validation error
  [ ] Hospital role accessing clinic endpoint → 403
```

---

## 💼 Interview Questions & Answers

### Q1: How do you debug a production bug when you can't reproduce it locally?
**A:** First, examine production logs for the exact error and stack trace. Check the audit log for the sequence of actions leading to the error. If the bug involves specific data, query the database to see the state. Add more logging around the suspected area and redeploy. Use error monitoring tools (Sentry, Datadog). Never modify production data without a rollback plan.

### Q2: What is the difference between unit tests and integration tests?
**A:** Unit tests test one function/class in isolation — all dependencies are mocked. They're fast and test business logic. Integration tests test multiple components together (controller + service + database). They use a real (or in-memory) database and verify the entire request-response flow. VigilAI uses JUnit + Mockito for unit tests and MockMvc for integration tests.

### Q3: What is a mock in testing?
**A:** A mock is a fake object that simulates the behavior of a real dependency. In VigilAI tests, `@Mock AIService aiService` creates a fake AI service — `when(aiService.getPrediction(any())).thenReturn(mockResponse)`. This lets you test VitalController without actually calling the Python AI service, making tests fast and deterministic.

### Q4: What is Git branching strategy and why is it important?
**A:** Git Flow uses separate branches: `main` (production), `develop` (integration), `feature/*` (new features), `bugfix/*` (bug fixes), `hotfix/*` (critical production fixes). This prevents untested code from reaching production, allows parallel development, and provides a clear history. VigilAI should use this pattern to manage releases safely.

### Q5: How do you test a REST API?
**A:** Use Postman or curl to send HTTP requests and verify responses. Test: happy path (correct inputs), validation errors (missing fields, wrong formats), authentication (no token → 401, wrong role → 403), edge cases (boundary values), error handling (when dependencies fail). Automate with MockMvc for regression testing.

---

> **Next Module:** Module 9 covers Deployment and DevOps — Docker, environment variables, hosting on Render.com, CI/CD, monitoring, scaling, and production best practices.
# MODULE 9: Deployment & DevOps
## VigilAI MedLink — From Local Development to Production

---

> [!NOTE]
> This module teaches you how to take VigilAI from your laptop to a real production server accessible anywhere in the world.

---

## 🐳 Docker — Containerization

### What is Docker?

**The Problem Without Docker:**
```
Works on my machine!
- Developer A: Java 17, PostgreSQL 15
- Developer B: Java 11, PostgreSQL 14
- Production: Java 21, PostgreSQL 16
→ Different versions = different behavior = bugs

With Docker:
- Packages the app + its exact environment into a container
- Container runs identically on any machine
- "Build once, run anywhere"
```

**Analogy:** Docker is like a shipping container. Instead of wondering if the cargo will fit different ships/trucks, you pack everything into a standardized container that any transport can carry.

### Docker Concepts:

| Concept | Description | VigilAI Example |
|---------|-------------|-----------------|
| **Image** | Read-only template (like a blueprint) | `postgres:16-alpine` |
| **Container** | Running instance of an image | `vigilai-db` (running Postgres) |
| **Dockerfile** | Instructions to build a custom image | `backend/Dockerfile` |
| **Volume** | Persistent storage outside container | `postgres_data` |
| **Network** | Virtual network connecting containers | docker-compose default network |
| **Port mapping** | `host:container` port binding | `"8080:8080"` |

---

## 📄 Dockerfile Analysis

### Backend Dockerfile:
```dockerfile
# Use a two-stage build (best practice for Java)

# Stage 1: BUILD (has JDK + Maven — large)
FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app

# Copy only pom.xml first (takes advantage of Docker layer caching)
COPY pom.xml .
# Download all dependencies (this layer is cached if pom.xml hasn't changed)
RUN mvn dependency:go-offline

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests
# -DskipTests = don't run tests during Docker build (speeds up build)
# Result: target/vigilai-backend-2.0.0.jar

# Stage 2: RUNTIME (has only JRE — smaller)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Copy ONLY the JAR from the build stage (not Maven, not source code)
COPY --from=build /app/target/vigilai-backend-*.jar app.jar

# Non-root user for security:
RUN addgroup -S vigilai && adduser -S vigilai -G vigilai
USER vigilai

EXPOSE 8080

# Start the Spring Boot app:
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Why Two-Stage Build?**
- Stage 1 image: ~600MB (JDK + Maven + source code)
- Stage 2 image: ~150MB (JRE + JAR only)
- Production only ships the small Stage 2 image

### AI Service Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies first (cached if requirements.txt unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Start FastAPI with Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# "0.0.0.0" = listen on all interfaces (accessible from other containers)
```

---

## 🔧 Environment Variables — Secrets Management

**The Golden Rule:** Never hardcode secrets in source code. Use environment variables.

### Why Environment Variables?

```
Scenario A (BAD — in docker-compose.yml):
  JWT_SECRET: "my-super-secret-key-hardcoded"
  → If someone forks your GitHub repo → they have your secret!
  → Anyone with database access → they have your production password!

Scenario B (GOOD — environment variables):
  JWT_SECRET: ${JWT_SECRET}
  → Actual value set in deployment platform, never in code
  → GitHub sees: ${JWT_SECRET} (harmless placeholder)
  → Production sees: "xK9#mN2@pL8..." (real secret)
```

### How Spring Boot Reads Them:

```properties
# application.properties — safe to commit:
spring.datasource.url=${SPRING_DATASOURCE_URL:jdbc:postgresql://localhost:5432/vigilai}
# Format: ${VARIABLE_NAME:default_if_not_set}

vigilai.jwt.secret=${JWT_SECRET:dev_secret_min_32_chars_long_!!!}
# In development: uses the default (dev_secret...)
# In production: uses the actual JWT_SECRET environment variable
```

```java
// Reading in Java code:
@Value("${vigilai.jwt.secret}")
private String secret;
// Spring reads from application.properties, which reads from environment variable
```

### Setting Environment Variables in Docker Compose:

```yaml
# docker-compose.yml — for local development:
backend:
  environment:
    SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/vigilai
    SPRING_DATASOURCE_USERNAME: postgres
    SPRING_DATASOURCE_PASSWORD: OMKAR@111  # ⚠️ OK for local dev only!
    JWT_SECRET: vigilai_dev_secret_key_min_32_chars_long
    AI_SERVICE_URL: http://ai-service:8000/predict
    LLM_SERVICE_URL: http://ai-service:8000/explain
    SPRING_JPA_HIBERNATE_DDL_AUTO: update
```

### Setting Environment Variables for Production (Render.com):

```
Dashboard → Select Service → Environment → Add Environment Variable
  SPRING_DATASOURCE_URL = jdbc:postgresql://external-host:5432/vigilai
  SPRING_DATASOURCE_PASSWORD = [a strong random password]
  JWT_SECRET = [64+ character random string]
```

---

## 🏗️ Build Process

### Java Build (Maven):

```bash
# Clean + compile + package:
mvn clean package
# clean: delete previous build artifacts
# package: compile, run tests, create JAR

# Skip tests (faster):
mvn clean package -DskipTests

# Run locally (without Docker):
java -jar target/vigilai-backend-2.0.0.jar

# The Spring Boot JAR is "fat" — it contains:
# - Your compiled classes
# - All dependencies (Spring, Jackson, JPA, etc.)
# - Embedded Tomcat server
# - Everything needed to run (no external server needed!)
```

### Python Build (pip):

```bash
# Install dependencies:
pip install -r requirements.txt

# Run locally:
uvicorn app.main:app --reload --port 8000
# --reload = auto-restart when code changes (development only)

# Run in production:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
# --workers 4 = 4 processes for handling concurrent requests
```

---

## 🌐 Docker Compose — Orchestrating All Services

### Starting the Complete Stack:

```bash
# Start all 4 services:
docker-compose up

# Start in background (detached mode):
docker-compose up -d

# Start with rebuild (after code changes):
docker-compose up --build

# Stop all services:
docker-compose down

# Stop and delete volumes (clears database!):
docker-compose down -v
```

### Checking Service Status:

```bash
# View running containers:
docker ps
# Output:
# CONTAINER ID   IMAGE          PORTS                    STATUS
# abc123         vigilai-backend 0.0.0.0:8080->8080/tcp  Up (healthy)
# def456         vigilai-ai      0.0.0.0:8000->8000/tcp  Up (healthy)
# ghi789         postgres:16     0.0.0.0:5432->5432/tcp  Up (healthy)
# jkl012         nginx:alpine    0.0.0.0:3000->80/tcp    Up

# View logs from all services:
docker-compose logs

# View logs from specific service:
docker-compose logs backend -f    # -f = follow (live)
docker-compose logs ai-service
docker-compose logs postgres

# Shell into a container:
docker exec -it vigilai-backend /bin/sh
docker exec -it vigilai-db psql -U postgres -d vigilai
```

### Health Checks (from docker-compose.yml):

```yaml
# Backend health check:
healthcheck:
  test: ["CMD-SHELL", "wget --quiet --tries=1 --spider http://localhost:8080/health || exit 1"]
  interval: 10s   # check every 10 seconds
  timeout: 5s     # fail if no response in 5 seconds
  retries: 5      # mark unhealthy after 5 failures

# AI service health check:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 10s
  retries: 5

# Backend depends_on ai-service with condition: service_healthy
# This means backend won't start until AI service health check passes!
```

---

## ☁️ Production Deployment — Render.com

Render.com is where the live VigilAI demo is deployed. It's a Platform as a Service (PaaS).

### Render.com Architecture:

```
Internet
    │
    ▼
Render Load Balancer (HTTPS termination)
    │
    ├── vigilai-backend (Web Service, Java)
    │   Port: 8080 (internally)
    │   URL: https://backend-ysf3.onrender.com
    │
    ├── vigilai-ai (Web Service, Python)
    │   Port: 8000 (internally)
    │   URL: https://ai-service-xxx.onrender.com
    │
    ├── vigilai-frontend (Static Site)
    │   Serves: login.html, clinic.html, etc.
    │   URL: https://vigilai.onrender.com
    │
    └── PostgreSQL (Managed Database)
        External URL: postgres://user:pass@host:5432/vigilai
```

### Why the "Server Waking Up" Delay?

```javascript
// In login.html:
btn.textContent = 'Waking up Free Tier Server (takes ~50s)…';
```

Render.com's free tier **spins down** services after 15 minutes of inactivity to save resources. When the first request arrives, the container must restart — which takes up to 50 seconds for a Spring Boot app.

**The pre-warming trick:**
```javascript
// login.html runs this IMMEDIATELY on page load (before user types anything):
(async () => {
    await fetch(`${API}/health`);  // This wakes up the server!
    // By the time user types email/password (~10 seconds), server is ready
})();
```

### Deployment Steps on Render.com:

```
1. Push code to GitHub

2. Create services on render.com:

   Service 1: PostgreSQL Database
   - Type: PostgreSQL
   - Name: vigilai-db
   - Plan: Free
   - Note the connection URL

   Service 2: AI Service (Python)
   - Type: Web Service
   - Repository: your-github/modified-vigilai-medlink
   - Root directory: ai-service
   - Build command: pip install -r requirements.txt
   - Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   - Note the service URL

   Service 3: Backend (Java)
   - Type: Web Service
   - Repository: same repo
   - Root directory: backend
   - Build command: mvn clean package -DskipTests
   - Start command: java -jar target/vigilai-backend-2.0.0.jar
   - Environment Variables:
     SPRING_DATASOURCE_URL = [postgres connection URL from step 2.1]
     SPRING_DATASOURCE_USERNAME = [from Render]
     SPRING_DATASOURCE_PASSWORD = [from Render]
     AI_SERVICE_URL = [ai service URL from step 2.2]/predict
     LLM_SERVICE_URL = [ai service URL]/explain
     JWT_SECRET = [random 64-char string]
     SPRING_JPA_HIBERNATE_DDL_AUTO = create  (first run only, then change to update)

   Service 4: Frontend (Static Site)
   - Type: Static Site
   - Repository: same repo
   - Root directory: frontend
   - No build command (pure HTML)
   
   Update API URL in login.html:
   const API = "https://your-backend.onrender.com";
```

---

## 📊 Monitoring & Health Checks

### Spring Boot Actuator (Built-in Monitoring):

```xml
<!-- Add to pom.xml: -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```properties
# application.properties:
management.endpoints.web.exposure.include=health,metrics,info
management.endpoint.health.show-details=when-authorized
```

**Available endpoints:**
```
GET /actuator/health → {"status":"UP","components":{"db":{"status":"UP"}}}
GET /actuator/metrics → list of available metrics
GET /actuator/metrics/jvm.memory.used → memory usage
GET /actuator/metrics/http.server.requests → request count/latency
```

### VigilAI's Custom Health Endpoint:

```java
@GetMapping("/health")
public ResponseEntity<?> health() {
    return ResponseEntity.ok(Map.of(
        "status", "healthy",
        "service", "VigilAI Backend v2.0",
        "timestamp", LocalDateTime.now()
    ));
}
```

---

## 🚀 CI/CD — Continuous Integration / Continuous Deployment

### What is CI/CD?

**Continuous Integration (CI):**
- Every code push → automatically run tests
- If tests fail → reject the push
- Prevents broken code from reaching the team

**Continuous Deployment (CD):**
- Every successful CI → automatically deploy to production
- No manual deployment steps
- Faster, more reliable releases

### GitHub Actions CI/CD for VigilAI:

```yaml
# .github/workflows/deploy.yml
name: VigilAI CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Java 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Run tests
        run: |
          cd backend
          mvn test
      
      - name: Build JAR
        run: |
          cd backend
          mvn clean package -DskipTests

  test-ai-service:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd ai-service
          pip install -r requirements.txt pytest
      
      - name: Run tests
        run: |
          cd ai-service
          pytest tests/

  deploy:
    needs: [test-backend, test-ai-service]  # Only deploy if tests pass
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'     # Only deploy from main branch
    steps:
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST "https://api.render.com/v1/services/$SERVICE_ID/deploys" \
            -H "Authorization: Bearer $RENDER_API_KEY"
```

---

## ⚡ Performance Optimization

### Database Performance:

```sql
-- Use EXPLAIN to see query execution plan:
EXPLAIN ANALYZE SELECT * FROM alerts WHERE clinician_decision = 'PENDING';
-- Output: "Index Scan using idx_alerts_dispatch" ← good (using index)
-- vs: "Seq Scan on alerts" ← bad (scanning all rows)

-- Connection pooling (in application.properties):
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
-- HikariCP maintains a pool of 10 connections (instead of opening/closing per request)
```

### Spring Boot Performance:

```properties
# Lazy initialization (start faster):
spring.main.lazy-initialization=true

# Compress HTTP responses:
server.compression.enabled=true
server.compression.mime-types=application/json,text/html

# Tune JVM heap for small containers:
# In Dockerfile:
# CMD ["java", "-Xmx512m", "-Xms256m", "-jar", "app.jar"]
```

### Python/FastAPI Performance:

```python
# Use multiple workers (Uvicorn):
# uvicorn app.main:app --workers 4

# Cache the model in memory (already done!):
_model_instance = None  # Singleton pattern prevents reload

# Use async routes for I/O-bound operations:
@app.get("/health")
async def health():  # async = non-blocking
    return {"status": "healthy"}
```

---

## 📋 Production Readiness Checklist

Before launching VigilAI for real users:

```
Security:
  [ ] Rotate all secrets (JWT, DB password, API keys)
  [ ] Restrict CORS to specific domains (not "*")
  [ ] Enable HTTPS only (no HTTP)
  [ ] Set secure, httpOnly, sameSite cookie flags (if using cookies)
  [ ] Add rate limiting on /auth/login (brute-force protection)
  [ ] Remove demo credentials from login.html

Database:
  [ ] Change SPRING_JPA_HIBERNATE_DDL_AUTO from "create" to "validate"
  [ ] Set up automated backups (Render.com: daily backups available)
  [ ] Add database connection pool limits

Monitoring:
  [ ] Set up error alerting (PagerDuty, Sentry)
  [ ] Configure uptime monitoring (UptimeRobot, Pingdom)
  [ ] Set up log aggregation (Logtail, Papertrail)

Performance:
  [ ] Enable response compression
  [ ] Test with realistic load (k6, JMeter)
  [ ] Configure connection pool sizes

Compliance (if real patient data):
  [ ] Business Associate Agreement with cloud provider
  [ ] Data encryption at rest
  [ ] HIPAA risk assessment
  [ ] Penetration testing
```

---

## 💼 Interview Questions & Answers

### Q1: What is Docker and why is it used?
**A:** Docker packages an application and its entire environment (OS libraries, dependencies, runtime) into a lightweight, portable container. This solves "works on my machine" problems — the container runs identically on any machine that has Docker. VigilAI uses Docker to package all 4 services (Postgres, AI, Backend, Frontend) so the entire system can be started with one command: `docker-compose up`.

### Q2: What is the difference between an image and a container?
**A:** An image is a read-only blueprint (like a class in OOP). A container is a running instance of an image (like an object). `postgres:16-alpine` is the image; `vigilai-db` is the running container. Multiple containers can be created from the same image.

### Q3: What is a multi-stage Dockerfile and why is it used?
**A:** A multi-stage build uses multiple `FROM` statements. The first stage (build) has all build tools (JDK + Maven). The second stage (runtime) copies only the compiled artifact (JAR). This produces a much smaller final image (~150MB instead of ~600MB) because build tools are not included in the runtime image.

### Q4: What are environment variables and why should secrets use them?
**A:** Environment variables are key-value pairs injected into a process at runtime. Secrets (passwords, API keys, JWT secrets) should use environment variables instead of hardcoded values because: 1) If code is on GitHub, anyone can read hardcoded secrets. 2) Environment variables are set in the deployment platform's secure storage (e.g., Render.com's Environment Variables section), not in code.

### Q5: What is CI/CD?
**A:** Continuous Integration (CI) automatically runs tests on every code push — preventing broken code from being merged. Continuous Deployment (CD) automatically deploys code that passes tests to production. Together they eliminate manual deployment steps, reduce human error, and enable multiple deployments per day.

### Q6: What is the purpose of a health check?
**A:** A health check is an endpoint (typically `GET /health`) that returns 200 OK if the service is running correctly. Docker Compose uses health checks to determine when a service is ready (`depends_on: condition: service_healthy`). Cloud platforms use health checks for load balancing — unhealthy containers don't receive traffic. VigilAI's `/health` endpoint lets monitoring tools detect outages.

### Q7: What is connection pooling and why is it important?
**A:** Opening a new database connection is expensive (~100ms). Connection pooling keeps a pre-opened pool of connections ready. HikariCP (Spring Boot's default) maintains 10 connections. When a request needs the DB, it borrows one from the pool (fast: ~1ms). Without pooling, high traffic would overwhelm the database with connection overhead.

---

> **Final Module:** Module 10 is the complete Mastery & Placement Preparation guide — how to explain VigilAI in interviews, resume points, system design discussion, and your roadmap to becoming a confident full-stack developer.
# MODULE 10: Mastery & Placement Preparation
## VigilAI MedLink — Complete Interview & Career Guide

---

> [!IMPORTANT]
> This is your final module. By this point you have studied every aspect of VigilAI MedLink. This module teaches you how to articulate that knowledge confidently in interviews, on your resume, and during technical discussions.

---

## 🎤 How to Explain VigilAI in Interviews

### The 30-Second Elevator Pitch

> "VigilAI MedLink is a healthcare emergency response platform I built to address the gap between rural PHC clinics and urban hospitals in India. When a nurse submits a patient's vitals, an XGBoost ML model predicts sepsis risk in under 200ms. If the risk is HIGH, an alert with an AI-generated clinical explanation is pushed in real-time to hospital doctors via WebSocket. The doctor reviews and approves ambulance dispatch, and the system selects the optimal hospital using a weighted scoring algorithm based on distance, ICU capacity, and specialization. The entire stack uses Java Spring Boot, PostgreSQL, Python FastAPI, and is containerized with Docker."

### The 5-Minute Technical Walkthrough

Start with architecture, then walk through one complete flow:

```
"Let me walk you through the architecture..."

1. [Draw a box diagram]
   "We have 4 services: React-less vanilla HTML frontend served by Nginx, 
   a Java Spring Boot backend on port 8080, a Python FastAPI AI service on 
   port 8000, and PostgreSQL on port 5432. All containerized with Docker Compose."

2. [Walk through the flow]
   "When a clinic nurse submits vitals, here's what happens:
   - The frontend POSTs to /api/clinic/vitals with a JWT in the Authorization header
   - JwtFilter validates the token and sets the CLINIC role in Spring Security context
   - VitalController orchestrates 7 steps: patient resolution, emergency type detection,
     vital persistence, triage rule evaluation, AI prediction, LLM explanation, and alert creation
   - The AI service receives the 7 vital signs, runs XGBoost classification, returns a risk score
   - If CRITICAL, the alert is saved to PostgreSQL and pushed via STOMP WebSocket to the
     hospital dashboard
   - The hospital doctor approves dispatch, triggering hospital selection via Haversine formula
     and a weighted scoring algorithm (mortality rate, ICU beds, distance, specialization)"

3. [Highlight your decisions]
   "I chose to separate the AI service because Python has the best ML ecosystem,
   and this allows independent scaling and model retraining without redeploying the backend."
```

---

## 📄 Resume Points

Use these bullet points on your resume. Quantify everything.

### Backend Bullet Points:
```
• Built a real-time emergency response platform using Java 17 + Spring Boot 3.2
  with JWT-based stateless authentication, role-based access control (3 roles),
  and BCrypt password hashing

• Designed a multi-criteria hospital selection algorithm using the Haversine formula
  for GPS distance calculation + weighted scoring (mortality rate, ICU availability,
  specialization matching), processing 4+ hospitals per alert in under 50ms

• Implemented WORM (Write Once Read Many) audit logging with SHA-256 hash chaining
  for tamper-evident medical audit trails (HIPAA compliance consideration)

• Integrated real-time WebSocket alerts using STOMP protocol, enabling instant
  emergency notifications to hospital dashboards without polling

• Developed RESTful APIs with Spring Data JPA (auto-generated SQL), @PreAuthorize
  method security, and global exception handling
```

### AI/ML Bullet Points:
```
• Built a Python FastAPI microservice serving an XGBoost binary classifier
  trained on 10,000 synthetic patient vitals with class imbalance handling
  (scale_pos_weight), achieving deployment in under 200ms inference time

• Implemented a dual-path prediction system: age-adaptive rule engine for
  immediate override of extreme vital signs (neonatal/pediatric/adult thresholds),
  with XGBoost model as primary predictor and graceful fallback

• Generated automated clinical explanations, treatment recommendations, and
  paramedic protocols for CRITICAL/HIGH risk predictions using templated
  evidence-based clinical logic
```

### Database Bullet Points:
```
• Designed a normalized PostgreSQL 16 schema with 10 tables, foreign key
  constraints, CHECK constraints on medical value ranges, and PostgreSQL-native
  features (UUID primary keys, ARRAY columns, generated columns)

• Implemented strategic database indexing (partial indexes, composite indexes)
  for high-frequency query patterns (email lookup, clinic-based filtering, 
  timestamp-ordered alerts)
```

### DevOps Bullet Points:
```
• Containerized a 4-service distributed system (Frontend, Backend, AI, Database)
  using Docker Compose with dependency ordering via health checks

• Deployed to Render.com with environment-variable-based configuration,
  multi-stage Docker builds (reducing image size from 600MB to 150MB),
  and automatic HTTPS via Let's Encrypt
```

---

## 🏗️ System Design Discussion

If asked "How would you scale VigilAI to 10,000 clinics?", here's how to discuss it:

### Current Architecture (Single Server):
```
Single Server handles: Nginx + Spring Boot + PostgreSQL + AI Service
Limit: ~100 concurrent users, limited by database connections and JVM heap
```

### Scaled Architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION SCALE ARCHITECTURE                 │
│                                                                   │
│  CDN (CloudFront)                                                │
│  └── Static Assets (HTML/CSS/JS)                                 │
│                                                                   │
│  Load Balancer (nginx or AWS ALB)                                │
│  ├── Spring Boot Instance 1  ─┐                                  │
│  ├── Spring Boot Instance 2  ─┤─── Shared PostgreSQL             │
│  └── Spring Boot Instance 3  ─┘    (RDS Multi-AZ)               │
│                                          │                        │
│  AI Service Cluster                      │                        │
│  ├── FastAPI Instance 1 (GPU)            │                        │
│  ├── FastAPI Instance 2 (GPU)            │                        │
│  └── FastAPI Instance 3 (GPU)            │                        │
│                                          │                        │
│  Message Queue (Redis Pub/Sub)           │                        │
│  └── WebSocket notifications ───────────┘                        │
│                                                                   │
│  Cache Layer (Redis)                                              │
│  └── Hospital data (changes rarely)                              │
└─────────────────────────────────────────────────────────────────┘
```

### Key Scalability Decisions:

**1. Stateless Backend → Easy Horizontal Scaling**
```
Because we use JWT (no server-side sessions), any backend instance can handle 
any request. Load balancer can distribute requests round-robin.

If we had sessions: User must always go to the same server (sticky sessions)
With JWT: Any server validates the token independently
```

**2. Database Scaling**
```
Read replicas for heavy reads (hospital dashboard loads):
  - Primary DB: handles writes (INSERT alerts, UPDATE dispatch)
  - Read Replica 1, 2: handles reads (GET alerts, GET patients)

Read/write split in Spring:
  @Transactional(readOnly = true) → routes to read replica
  @Transactional → routes to primary
```

**3. WebSocket at Scale**
```
Problem: WebSocket connections are server-specific
  - User A connected to Server 1
  - Alert created on Server 2
  - Server 2 can't push to User A!

Solution: Redis Pub/Sub as message broker
  - All servers subscribe to Redis channel
  - When alert created on any server → publish to Redis
  - All servers receive it → push to their connected clients
```

**4. AI Service Scaling**
```
AI inference is CPU/GPU intensive. Scale independently:
  - Add more AI containers when prediction load increases
  - Add GPU instances for faster XGBoost inference
  - Queue predictions if AI is overwhelmed (don't block clinic submission)
```

**5. Caching**
```
Hospital data rarely changes → cache in Redis (TTL: 1 hour)
  - First request: hit PostgreSQL, store in Redis
  - Subsequent requests: serve from Redis (1ms instead of 50ms)

Patient data per clinic → could cache per clinic session
```

---

## 🎯 Architecture Discussion — Questions to Anticipate

### "Why not use GraphQL instead of REST?"
```
REST was the right choice for VigilAI because:
- Simple, well-understood, easy to test with Postman
- Spring Boot has excellent REST support with Spring MVC
- Clients (clinic.html) have simple, predictable data needs
- GraphQL's benefit (flexible queries) isn't needed when the frontend is controlled by us

GraphQL would be better if: we had many different clients with varying data needs 
(mobile app, partner APIs, third-party integrations)
```

### "Why use XGBoost and not a neural network?"
```
XGBoost was chosen because:
1. Tabular data (7 vital signs) → XGBoost typically outperforms neural networks
2. Interpretability → XGBoost importance scores help doctors understand the prediction
3. Small dataset (10,000 rows) → Neural networks need millions of rows to generalize
4. Fast inference → XGBoost < 1ms, CNN/LSTM would be 10-100ms
5. Production-ready → XGBoost is stable, widely used in healthcare AI

Neural networks would be better for: imaging (X-rays), NLP (clinical notes), 
time series (ICU waveforms)
```

### "Why not use React for the frontend?"
```
Pure HTML/CSS/JS was chosen because:
1. No build step required (no npm, webpack, babel)
2. Files can be served directly by Nginx without any processing
3. Complete transparency — students see exactly what runs in the browser
4. Lower complexity for learning

React would be better for: complex SPA with many interactive components, 
state management across many pages, large teams, component reuse
```

### "How would you handle offline clinics?"
```
Rural clinics often have intermittent connectivity. The current vitals table has:
  sync_status VARCHAR(20) DEFAULT 'PENDING'  -- PENDING, SYNCED, FAILED

An offline-first architecture would:
1. Use Service Workers to cache clinic.html in the browser
2. Use IndexedDB to store vitals locally when offline
3. Background sync API to upload when connectivity returns
4. The sync_status column already supports this — just needs the client implementation

This is a significant architecture enhancement that would require:
- Progressive Web App (PWA) setup
- Conflict resolution strategy (what if same patient submitted twice offline?)
- Partial sync (what's already synced?)
```

---

## 📝 Viva Questions — Three Levels

### Level 1: Beginner Questions

**Q: What does VigilAI MedLink do?**
A: It's a healthcare platform that helps rural clinics detect sepsis early. When a nurse records patient vitals (heart rate, temperature, blood pressure, SpO2), an AI model predicts if the patient has sepsis. If the risk is high, an alert is sent to a hospital doctor who can approve ambulance dispatch. The system selects the best hospital based on distance, ICU beds, and specialization.

**Q: What technologies did you use?**
A: Java 17 with Spring Boot 3.2 for the backend REST API, PostgreSQL 16 for the database, Python FastAPI with XGBoost for the AI service, and vanilla HTML/CSS/JavaScript for the frontend. All containerized with Docker Compose.

**Q: What is a REST API?**
A: REST (Representational State Transfer) is an architectural style for APIs. Resources are accessed via URLs, and operations are performed with HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove). VigilAI has endpoints like `POST /api/clinic/vitals` (submit vitals) and `GET /api/hospital/alerts` (get pending alerts).

**Q: What is a database and what tables does VigilAI have?**
A: A database persistently stores structured data. VigilAI has 10 tables: `users`, `patients`, `vitals`, `triage_flags`, `hospitals`, `doctors`, `alerts`, `documents`, `outcomes`, and `audit_log_worm`. The most important is `alerts` which stores AI-generated emergency alerts with risk scores, severity, clinical explanations, and dispatch status.

**Q: What is JWT?**
A: JWT (JSON Web Token) is a compact, signed token used for authentication. After login, the server issues a JWT containing the user's email, role, and entity ID. The client sends this token in every request header (`Authorization: Bearer <token>`). The server validates the signature without a database lookup, making it stateless.

---

### Level 2: Intermediate Questions

**Q: Walk me through the complete flow when a nurse submits vitals.**
A: [Answer with the 7-step flow from Module 6]
1. Patient lookup/creation
2. Emergency type auto-detection
3. Vital signs saved to database
4. Triage flag evaluation
5. XGBoost AI prediction
6. LLM clinical explanation
7. Alert creation + WebSocket push

**Q: How does hospital selection work?**
A: The `VigilService.selectBestHospital()` method scores each active hospital using a weighted formula: mortality rate (35%), ICU bed availability (30%), proximity via Haversine formula (20%), Level 1 trauma center status (10%), plus a 5-point specialization bonus if the hospital treats the emergency type. The hospital with the highest score wins. ETA is calculated assuming 40 km/h ambulance speed plus 5 minutes preparation.

**Q: How does Spring Security work in this project?**
A: Spring Security intercepts all HTTP requests. The JwtFilter runs first — it extracts the `Authorization: Bearer <token>` header, validates the JWT signature and expiry, loads the user from the database, and sets the authentication in Spring Security's SecurityContext. SecurityConfig then checks if the authenticated user's role is allowed for the requested endpoint. `@PreAuthorize("hasRole('CLINIC')")` on controller methods provides method-level authorization.

**Q: What is the triage rule engine and how does it differ from the AI model?**
A: The rule engine is deterministic — it applies fixed clinical thresholds (HR > 100, SpO2 < 92, BP < 100) to flag individual vital signs. If 2+ vitals are flagged, it's PRIORITY severity. The AI model is probabilistic — it runs XGBoost on all 7 vital signs simultaneously, considering their interactions, and outputs a continuous risk probability (0-1). The rule engine provides immediate, interpretable flags; the AI model provides a nuanced risk score. VigilAI uses both: rule engine for triage flagging, AI model for overall risk classification.

**Q: Explain the WORM audit log.**
A: WORM stands for Write Once Read Many. The `audit_log_worm` table stores every system action (login, alert created, dispatch sent) with a SHA-256 hash of each entry. Each entry also contains the hash of the previous entry, forming a chain. If anyone modifies an old record, all subsequent hashes become invalid, mathematically proving tampering occurred. This is essential for medical-legal compliance.

---

### Level 3: Advanced Questions

**Q: How would you handle a scenario where the AI service is down?**
A: VigilAI already has graceful degradation. In `AIService.java`:
```java
} catch (Exception e) {
    log.error("AI service unavailable: {}", e.getMessage());
    return new AIPredictionResponse(0.5, "MEDIUM", 0.5, "FALLBACK", null);
}
```
For production resilience, I would add: circuit breaker pattern (Resilience4j), retry with exponential backoff, and a queue (RabbitMQ/Redis) to store vitals when AI is down and process them when it recovers. The rule engine provides a safety net — if XGBoost fails, `apply_rules()` runs as fallback in the Python service.

**Q: What are the security vulnerabilities in the current implementation?**
A: Several known areas for improvement:
1. **JWT stored in localStorage** — vulnerable to XSS. Production should use httpOnly cookies.
2. **Wildcard CORS** (`*`) — should restrict to specific origins.
3. **No rate limiting** — login endpoint is brute-forceable.
4. **No token revocation** — a stolen token is valid until expiry.
5. **Hardcoded credentials in docker-compose.yml** — should be environment variables.
6. **No field-level encryption** — patient PII (name, phone) stored in plaintext.
7. **No input sanitization for free-text fields** — clinical notes vulnerable to stored XSS.

**Q: How would you add real-time vital sign monitoring (streaming vitals from IoT devices)?**
A: I would add: 1) A new WebSocket endpoint at `/ws/vitals/{deviceId}` that IoT devices stream to. 2) The backend processes vital streams as time series, applying Kalman filtering for noise reduction. 3) A circular buffer (Redis Sorted Set) stores the last N readings per patient. 4) Trend analysis detects deterioration (HR increasing over 10 minutes). 5) MQTT protocol would be more appropriate than WebSocket for IoT due to its lightweight pub/sub model. 6) The AI model would need to be retrained on time-series features (delta HR, variability) not just point-in-time values.

**Q: How does XGBoost work and why is it good for sepsis detection?**
A: XGBoost (Extreme Gradient Boosting) is an ensemble of decision trees built sequentially, each correcting the errors of the previous. Each tree is a series of IF-THEN splits on vital sign thresholds. The final prediction is the weighted sum of all trees' outputs, passed through a sigmoid to get a probability. For sepsis: 1) It handles non-linear relationships (SpO2 alone matters less than SpO2 + BP + HR together). 2) It handles class imbalance (sepsis is rare — we use `scale_pos_weight`). 3) It's interpretable (feature importance shows which vitals matter most). 4) It's fast at inference (<1ms for 7 features).

**Q: How would you implement multi-tenancy (hundreds of separate clinic organizations)?**
A: Current VigilAI uses `clinic_id` as a tenant identifier (row-level security). For true multi-tenancy at scale:
- **Schema-per-tenant**: Each organization gets a separate PostgreSQL schema. Strong isolation, but complex to manage.
- **Database-per-tenant**: Each organization gets a separate database. Maximum isolation, highest cost.
- **Row-level security (current approach)**: All tenants in same tables, `clinic_id` column filters data. Cheapest, but requires careful query filtering.
I would add PostgreSQL Row-Level Security (RLS) policies to enforce that a clinic can only see its own patients:
```sql
CREATE POLICY clinic_isolation ON patients
  USING (clinic_id = current_setting('app.clinic_id'));
```
This enforces tenant isolation at the database level, preventing application bugs from leaking cross-tenant data.

---

## 🛠️ Real-World Improvements

If you were to take VigilAI to production with real patients, here's what to add:

### Priority 1 — Critical for Real Patients:
1. **HIPAA compliance**: Business Associate Agreement with cloud provider, field-level encryption for PII
2. **Input sanitization**: Prevent XSS in clinical notes
3. **Rate limiting**: Max 5 login attempts per 15 minutes
4. **Proper CORS**: Restrict to specific domains
5. **Token revocation**: Redis-based token blacklist
6. **Automated backups**: Database backups every 6 hours

### Priority 2 — Important for Scale:
7. **Offline-first clinic**: Service Worker + IndexedDB for unstable connectivity
8. **Internationalization**: Hindi, Kannada, Tamil language support
9. **SMS/WhatsApp alerts**: Backup notification when internet is down
10. **Model retraining pipeline**: Weekly retraining with new outcome data

### Priority 3 — Nice to Have:
11. **Mobile app**: React Native app for clinic nurses
12. **Voice input**: Dictate vitals in regional language
13. **Wearable integration**: Bluetooth pulse oximeter → auto-fill SpO2
14. **Electronic Health Record integration**: HL7 FHIR standard

---

## 🎯 Self-Assessment Rubric

Rate yourself 1-5 on each area:

| Area | Topics to Know | Your Rating |
|------|---------------|-------------|
| Frontend | HTML/CSS/JS, DOM, localStorage, fetch, WebSocket | /5 |
| Java | OOP, Spring Boot, annotations, streams, generics | /5 |
| Spring Security | JWT, BCrypt, SecurityFilterChain, @PreAuthorize | /5 |
| JPA/Database | Entity mapping, repositories, SQL, indexes | /5 |
| AI/ML | XGBoost, classification, training pipeline, inference | /5 |
| Docker | Images, containers, Dockerfile, docker-compose | /5 |
| Architecture | Microservices, REST, WebSocket, scalability | /5 |
| Security | OWASP, authentication vs authorization, HIPAA | /5 |
| Debugging | Browser DevTools, Spring logs, SQL debugging | /5 |
| System Design | Scaling, caching, load balancing, trade-offs | /5 |

**Score Guide:**
- 40-50: Senior developer level — confidently discuss any aspect
- 30-40: Mid-level developer — can explain and modify the project
- 20-30: Junior developer — can work on the project with guidance
- Below 20: Revisit Modules 1-9

---

## 📚 Continuing Your Learning Journey

### Month 1: Solidify VigilAI
- [ ] Run the project locally with Docker Compose
- [ ] Modify the triage thresholds and observe the difference
- [ ] Add a new API endpoint (e.g., GET /api/clinic/patients)
- [ ] Write 5 unit tests for VigilService
- [ ] Deploy your own instance to Render.com

### Month 2: Extend the Project
- [ ] Add a new role (e.g., PARAMEDIC) with limited permissions
- [ ] Implement the ambulance tracking table and API
- [ ] Add rate limiting with Bucket4j or Redis
- [ ] Implement refresh token rotation

### Month 3: Level Up Skills
- [ ] Learn React — rebuild clinic.html as a React component
- [ ] Learn Kubernetes — deploy VigilAI on a K8s cluster
- [ ] Learn Spring Boot testing — achieve 80% code coverage
- [ ] Study SHAP values — add real feature importance to AI explanations

### Month 4: Interview Ready
- [ ] Mock interview: explain VigilAI in 5 minutes without notes
- [ ] System design: "Design VigilAI for 1 million patients" on whiteboard
- [ ] Solve 50 LeetCode problems (arrays, strings, trees, graphs)
- [ ] Contribute to an open-source Spring Boot or FastAPI project

---

## 💬 Final Message

You now have the knowledge to:

✅ Understand every line of code in VigilAI MedLink
✅ Explain the architecture and technology choices confidently
✅ Modify and extend the project with new features
✅ Debug issues across all four services
✅ Deploy the project to production
✅ Discuss scalability, security, and trade-offs
✅ Answer interview questions at all levels

**The most important thing:** Don't just read — BUILD. Run the project, break things, fix them, add features. The hands-on experience will make everything click.

---

> [!TIP]
> Remember: Every expert was once a beginner. The fact that you've studied all 10 modules of this roadmap puts you ahead of 90% of candidates who only know surface-level facts about their projects. Own this project — because you now understand it completely.

---

*VigilAI MedLink Learning Roadmap — Complete*
*Modules 1-10 | Technology → Language → Frontend → Backend → Database → Deep Dive → Security → Testing → Deployment → Mastery*

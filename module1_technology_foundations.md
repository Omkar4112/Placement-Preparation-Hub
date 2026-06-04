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

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

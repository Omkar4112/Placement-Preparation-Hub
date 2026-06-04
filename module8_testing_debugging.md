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

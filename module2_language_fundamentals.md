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

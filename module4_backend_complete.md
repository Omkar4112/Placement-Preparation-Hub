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

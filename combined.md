# VigilAI MedLink v2.0 Complete Learning & Interview Guide

This guide covers everything about the VigilAI MedLink architecture, including the basics, project working configurations, advanced software concepts, and tech interview deep dives across 10 core modules.

---

# Module 1: Microservices Architecture (Spring Boot & FastAPI)

This module explains the fundamental concepts of microservices, how they are implemented in VigilAI MedLink, advanced orchestration concepts, and technical interview preparations.

## 1. Basics & Fundamentals

### What is a Microservice Architecture?
A **Microservices Architecture** is an architectural style that structures an application as a collection of small, autonomous services modeled around a business domain. Unlike a monolithic application where frontend, backend, and database logic are bundled into a single unit, microservices are:
* **Highly maintainable and testable**: Small services are easier to understand and verify.
* **Loosely coupled**: Services can be updated, redeployed, and scaled independently.
* **Polyglot-friendly**: Different services can use different programming languages, databases, and technologies.

```
                  ┌───────────────┐
                  │    Browser    │
                  └───────┬───────┘
                          │ (REST / WebSockets)
                          ▼
             ┌─────────────────────────┐
             │   Spring Boot Backend   │
             └────────────┬────────────┘
                          │ (REST Client)
                          ▼
              ┌───────────────────────┐
              │  FastAPI AI Service   │
              └───────────────────────┘
```

### Key Trade-offs: Monolith vs. Microservices
| Feature | Monolith | Microservices |
| :--- | :--- | :--- |
| **Complexity** | Low initially, high as it grows | High initial infrastructure, scales better |
| **Deployment** | All-or-nothing (Riskier) | Independent, continuous deployments |
| **Performance** | Low in-memory latency | Network latency overhead between services |
| **Data Integrity** | Simple database transactions (ACID) | Distributed data management (Eventual consistency) |

---

## 2. Working in MedLink

VigilAI MedLink v2.0 uses a dual-microservice design:
1. **Spring Boot (Java) Backend**: Manages CRUD data operations, authenticates users, tracks ICU beds, handles WebSockets, and manages the database.
2. **FastAPI (Python) AI Service**: Conducts XGBoost machine learning predictions and constructs clinical explanation generation.

### Service Coordination via Docker Compose
The system defines service dependencies, environments, and network configurations in [docker-compose.yml](file:///c:/Users/omkar/modified-vigilai-medlink/docker-compose.yml):

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    container_name: vigilai-db
    environment:
      POSTGRES_DB: vigilai
      POSTGRES_USER: vigil
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"

  ai-service:
    build: ./ai-service
    container_name: vigilai-ai
    ports:
      - "8000:8000"
    environment:
      - PORT=8000

  backend:
    build: ./backend
    container_name: vigilai-backend
    ports:
      - "8080:8080"
    depends_on:
      - db
      - ai-service
    environment:
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/vigilai
      - SPRING_DATASOURCE_USERNAME=vigil
      - SPRING_DATASOURCE_PASSWORD=password123
      - AI_SERVICE_URL=http://ai-service:8000
```

### Inter-Service Communication
The backend communicates synchronously with the AI service using a REST client. In [AIService.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/service/AIService.java), a POST request is executed to transmit vitals payload to the AI service:

```java
public PredictionResponse predictVitals(VitalsRequest request) {
    String url = aiServiceUrl + "/predict";
    return restTemplate.postForObject(url, request, PredictionResponse.class);
}
```

---

## 3. Advanced Concepts

### Docker Networking & Domain Name Resolution
When services run within Docker, they join a shared virtual network. Docker provides an embedded DNS server that resolves container names (`db`, `ai-service`) to their internal IP addresses, preventing the need to hardcode absolute IPs.

### Handling Network Failures & Latency
To make microservices resilient:
* **Circuit Breakers**: Prevent cascading failure when a downstream service is down (e.g., if the AI service goes offline, Spring Boot falls back to the Java rule engine).
* **Connection Pooling**: Managing HTTP client connection limits to avoid socket exhaustion.

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is the difference between Synchronous and Asynchronous microservice communication?
**Answer**: 
* **Synchronous (REST/gRPC)**: The sender sends a request and blocks waiting for a response. Best for immediate dependencies (e.g., getting vital risk validation results before saving).
* **Asynchronous (RabbitMQ/Kafka)**: The sender publishes a message and immediately moves on. The receiver processes it asynchronously. Best for loose coupling, notification triggers, and handling heavy workloads.

#### Q2: How do you handle distributed transactions in a Microservice Architecture?
**Answer**: Since each microservice has its own database in a pure architectural setup, standard ACID transactions don't work. Instead, we use:
1. **Saga Pattern**: A sequence of local transactions. Each transaction updates database state and publishes an event. If a step fails, compensation transactions are executed in reverse order.
2. **Two-Phase Commit (2PC)**: A coordinator coordinates with database nodes to prepare and commit. Highly blocking and doesn't scale well.

#### Q3: How do you solve service discovery in a cloud environment?
**Answer**: By using service registries like **Netflix Eureka** or cloud native solutions like **Kubernetes DNS**. Services register themselves with their dynamic host and port, and other services query the registry to resolve paths.

---
---

# Module 2: Security & Authentication (JWT & Role-Based Access Control)

This module details JWT token-based authentication, password security with BCrypt, Spring Security filter configuration, role-based authorization, and interview preparation.

## 1. Basics & Fundamentals

### Stateless vs. Stateful Authentication
* **Stateful (Session-based)**: The server stores session data in memory or a database (e.g., Redis). The client receives a `JSESSIONID` cookie and sends it with every request. The server must look up this ID to authenticate the user. This makes scaling horizontally difficult since session state must be synchronized.
* **Stateless (Token-based)**: The server authenticates user credentials once and returns a cryptographically signed JSON Web Token (JWT). The client stores it (e.g., in `localStorage`) and attaches it to the `Authorization: Bearer <token>` HTTP header. The server verifies the cryptographic signature without looking up session records.

### Anatomy of a JSON Web Token (JWT)
A JWT consists of three parts separated by dots (`.`):
1. **Header**: Metadata containing the hashing algorithm (e.g., HMAC SHA-256) and type (`JWT`).
2. **Payload**: The core claims (data) about the user, such as username, user ID, expiration timestamp (`exp`), and authorization roles.
3. **Signature**: Validates that the token hasn't been altered en route. Generated by hashing the base64-encoded header and payload with a secret key.

---

## 2. Working in MedLink

### User Roles
The database maps users to roles (defined in [Role.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/model/Role.java)):
* `CLINIC`: Submits patient vitals.
* `HOSPITAL`: Manages bed capacities, doctors, and triage alert responses.
* `ADMIN`: Views audit logs, validates database integrity, and inspects dashboards.

### Password Security via BCrypt
To avoid storing raw passwords, MedLink applies BCrypt in [SecurityConfig.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/config/SecurityConfig.java#L56-L59):
```java
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(10); // Strength factor 10
}
```
BCrypt automatically incorporates a secure random salt to protect passwords against rainbow table attacks.

### Request Interception & Authentication Filter
Every incoming HTTP request undergoes filter validation in [JwtFilter.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/config/JwtFilter.java):

```java
@Override
protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
        throws ServletException, IOException {
    final String authHeader = request.getHeader("Authorization");

    if (authHeader == null || !authHeader.startsWith("Bearer ")) {
        chain.doFilter(request, response);
        return;
    }

    String token = authHeader.substring(7);
    try {
        String email    = jwtUtil.extractEmail(token);
        String role     = jwtUtil.extractRole(token);
        String entityId = jwtUtil.extractEntityId(token);

        if (email != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            if (jwtUtil.validateToken(token, email)) {
                UsernamePasswordAuthenticationToken auth =
                    new UsernamePasswordAuthenticationToken(email, null, List.of(new SimpleGrantedAuthority("ROLE_" + role)));
                auth.setDetails(entityId); // Attach target hospital or clinic context ID
                SecurityContextHolder.getContext().setAuthentication(auth);
            }
        }
    } catch (Exception e) {
        // Handle invalid token signatures
    }
    chain.doFilter(request, response);
}
```

### Authorization Rules
In [SecurityConfig.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/config/SecurityConfig.java#L29-L54), path prefixes map directly to user permissions:

```java
http
    .csrf(csrf -> csrf.disable())
    .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
    .authorizeHttpRequests(auth -> auth
        .requestMatchers("/auth/**", "/health", "/ws/**").permitAll()
        .requestMatchers("/api/admin/**").hasRole("ADMIN")
        .requestMatchers("/api/hospital/**").hasAnyRole("HOSPITAL", "ADMIN")
        .requestMatchers("/api/clinic/**").hasAnyRole("CLINIC", "ADMIN")
        .anyRequest().authenticated()
    );
```

---

## 3. Advanced Concepts

### Revoking Stateless JWTs
Since JWT validation is stateless, a token remains valid until its expiration timestamp is reached. If a user logs out or has their account disabled, they can still access resources. Solutions include:
* **Short Lifetime + Refresh Tokens**: Issue JWTs with 15-minute validity, and maintain a database-backed or Redis-backed Refresh Token with a longer lifespan (e.g., 7 days) to acquire new access tokens.
* **Blacklisting**: Store revoked tokens in a fast-access in-memory cache (Redis) with TTL matching the remaining token expiration time. The request filter queries Redis before authorizing access.

### JWT Security Best Practices
* **Never store sensitive data in payload**: Payload data is simply Base64-URL encoded and visible to anyone who decodes the token.
* **Cryptographic Signature Algorithms**: Use robust algorithms like HMAC-SHA256 (symmetric) or RS256 (asymmetric).

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is a Salt in hashing, and why does BCrypt use it?
**Answer**: A salt is a random sequence of bytes appended to a password before hashing. Salt ensures that two users with identical passwords will produce completely different hashes. BCrypt embeds the salt directly within the output hash string, ensuring protection against precomputed dictionary lookup tables (rainbow tables).

#### Q2: How does asymmetric token signing (RS256) differ from symmetric (HS256)?
**Answer**:
* **HS256 (Symmetric)**: The token signer and verifier use the same shared secret key. If a third-party microservice wants to verify a token, they need the secret key, giving them the ability to also generate fake tokens.
* **RS256 (Asymmetric)**: The authentication service signs the token with a private key, and external consumers use the corresponding public key to verify it. The consumers cannot forge tokens because they do not have access to the private key.

#### Q3: How do you prevent cross-site scripting (XSS) and cross-site request forgery (CSRF) in web authentication?
**Answer**:
* **XSS**: Caused by running malicious client-side JS script to steal cookies or local storage. Prevented by escaping user input, configuring Content Security Policy (CSP) headers, and storing JWTs in `HttpOnly` cookies.
* **CSRF**: Caused by a browser sending session cookies automatically during third-party requests. Prevented by using stateless JWTs (which must be appended programmatically as an Authorization header, which browsers don't do automatically) or setting `SameSite=Strict` cookies.

---
---

# Module 3: Database Modeling & SQL (PostgreSQL & JPA)

This module focuses on PostgreSQL schema design, object-relational mapping (ORM) with Hibernate/JPA, relationships, indexes, query optimizations, and technical interview scenarios.

## 1. Basics & Fundamentals

### What is JPA/Hibernate?
* **JPA (Java Persistence API)**: A specification that defines how to map Java objects (POJOs) to relational database tables.
* **Hibernate**: An ORM framework that implements the JPA specification, writing raw SQL queries on behalf of the developer.

### Key Database Relationships
* **One-to-One (`@OneToOne`)**: A row in Table A maps to exactly one row in Table B (e.g., User has a Profile).
* **Many-to-One / One-to-Many (`@ManyToOne` / `@OneToMany`)**: Multiple rows in Table A map to one row in Table B (e.g., multiple Patients belong to one Clinic).
* **Many-to-Many (`@ManyToMany`)**: Multiple rows in Table A map to multiple rows in Table B (e.g., Doctors and Patients, requiring a join table).

---

## 2. Working in MedLink

### PostgreSQL Schema
The database configuration uses Postgres. Look at the primary relational tables defined in [02_core.sql](file:///c:/Users/omkar/modified-vigilai-medlink/database/schema/02_core.sql):

```sql
-- Patients table
CREATE TABLE patients (
    patient_id VARCHAR(100) PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(20) NOT NULL,
    clinic_id VARCHAR(100) REFERENCES users(entity_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Triage Vitals table
CREATE TABLE vitals (
    vital_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(100) REFERENCES patients(patient_id),
    heart_rate INT NOT NULL,
    spo2 INT NOT NULL,
    respiratory_rate INT NOT NULL,
    systolic_bp INT NOT NULL,
    diastolic_bp INT NOT NULL,
    temperature NUMERIC(4,1) NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Real-time Alerts table
CREATE TABLE alerts (
    alert_id SERIAL PRIMARY KEY,
    patient_id VARCHAR(100) REFERENCES patients(patient_id),
    clinic_id VARCHAR(100),
    hospital_id INT,
    risk_score NUMERIC(4,3) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    clinician_decision VARCHAR(50) DEFAULT 'PENDING',
    dispatch_status VARCHAR(50) DEFAULT 'NONE',
    alert_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### JPA Entity Definitions
Let's see how [Patient.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/model/Patient.java) is mapped:

```java
@Entity
@Table(name = "patients")
@Getter @Setter @NoArgsConstructor @AllArgsConstructor
public class Patient {
    @Id
    @Column(name = "patient_id")
    private String patientId;

    @Column(name = "full_name", nullable = false)
    private String fullName;

    @Column(nullable = false)
    private Integer age;

    @Column(nullable = false, length = 20)
    private String gender;

    @Column(name = "clinic_id")
    private String clinicId;

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
}
```

---

## 3. Advanced Concepts

### Database Indexing
Indexes speed up read queries at the cost of slower writes and additional disk storage.
* **B-Tree Index (Default)**: Best for equality and range queries (e.g., searching for vitals recorded in a timestamp range).
* **Hash Index**: Best for quick equality comparisons (e.g., finding a patient by a unique `patient_id` string).

### JPA N+1 Query Problem
This occurs when you fetch a list of entities with a lazy-loaded relationship. Hibernate executes 1 query to fetch the parent entities, and then N separate queries to fetch the child entities for each parent.

**Example**:
```java
// Fetching all patients, each triggering an additional query to lookup their clinic.
List<Patient> patients = patientRepository.findAll();
```
**Fix using Entity Graphs or JOIN FETCH**:
```java
@Query("SELECT p FROM Patient p JOIN FETCH p.vitalsList")
List<Patient> findAllWithVitals();
```

### Transaction Isolation Levels
1. **Read Uncommitted**: Can read uncommitted data (dirty reads).
2. **Read Committed**: Can only read committed data (prevents dirty reads, allows non-repeatable reads).
3. **Repeatable Read**: Guarantees that multiple reads of the same data in a transaction return the same values (prevents dirty & non-repeatable reads, allows phantom reads).
4. **Serializable**: Full isolation by locking resources (prevents all concurrency issues, low throughput).

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is the difference between Lazy and Eager loading in JPA?
**Answer**:
* **Eager Loading (`FetchType.EAGER`)**: Database relationships are loaded immediately alongside the parent entity using a JOIN query.
* **Lazy Loading (`FetchType.LAZY`)**: Related entities are not loaded from the database until they are accessed (e.g., calling `patient.getVitals()`). This helps conserve system memory and database performance.

#### Q2: How does HikariCP Connection Pool work, and why is it used?
**Answer**: Opening and closing physical database connections is expensive (involving TCP handshakes, socket allocation, and credentials verification). HikariCP maintains a pool of pre-opened active connections. When a query is executed, Spring Boot borrows a connection from the pool, runs the query, and immediately returns it, maximizing throughput.

#### Q3: What is the difference between Optimistic Locking and Pessimistic Locking?
**Answer**:
* **Optimistic Locking (`@Version`)**: Assumes conflicts are rare. Every table row has a version column. When updating, the application verifies the version hasn't changed. If it has, an `OptimisticLockException` is thrown, prompting a retry.
* **Pessimistic Locking**: Assumes conflicts are frequent. Locks rows at the database level using `SELECT ... FOR UPDATE`, blocking other transactions until the lock is released.

---
---

# Module 4: REST API Design & Integration

This module focuses on REST architectural principles, designing robust HTTP endpoints, utilizing Data Transfer Objects (DTOs), pagination, CORS management, and REST API interview patterns.

## 1. Basics & Fundamentals

### What is REST?
**REST (Representational State Transfer)** is an architectural style for building APIs using HTTP protocol. It enforces the following constraints:
1. **Client-Server**: Separates user interface concerns from data storage concerns.
2. **Stateless**: Each request from a client must contain all the information needed to understand and process the request. No session state is stored on the server.
3. **Cacheable**: Response data must declare itself cacheable or not to improve network efficiency.
4. **Uniform Interface**: Uses standard HTTP methods:
   * `GET`: Retrieve data.
   * `POST`: Create data.
   * `PUT`: Replace resource.
   * `PATCH`: Partially update resource.
   * `DELETE`: Remove resource.

### HTTP Response Status Codes
* **2xx (Success)**: `200 OK`, `201 Created`
* **4xx (Client Error)**: `400 Bad Request`, `401 Unauthorized` (no token), `403 Forbidden` (no role permission), `404 Not Found`
* **5xx (Server Error)**: `500 Internal Server Error`, `503 Service Unavailable`

---

## 2. Working in MedLink

### API Controllers
Look at [AlertController.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/controller/AlertController.java) mapping triage alerts endpoints:

```java
@RestController
@RequestMapping("/api/alerts")
public class AlertController {

    @Autowired private AlertRepository alertRepo;
    @Autowired private WebSocketService wsService;
    @Autowired private AuditLogService auditService;

    @GetMapping("/active")
    public List<Alert> getActiveAlerts() {
        return alertRepo.findActiveAlerts();
    }

    @PostMapping("/{id}/respond")
    public ResponseEntity<?> respondToAlert(
            @PathVariable Long id,
            @RequestBody Map<String, String> body,
            Authentication auth) {
        
        Alert alert = alertRepo.findById(id)
                .orElseThrow(() -> new RuntimeException("Alert not found"));
        
        String decision = body.get("decision"); // APPROVED, HELD, DISMISSED
        String originalDecision = alert.getClinicianDecision();
        
        alert.setClinicianDecision(decision);
        alertRepo.save(alert);

        // Audit Logging & Real-time WS Dispatch
        auditService.logAction("RESPOND_ALERT", "ALERT", id.toString(), 
                auth.getName(), originalDecision, decision);
        wsService.pushAlertUpdate(alert);

        return ResponseEntity.ok(Map.of("message", "Response registered successfully"));
    }
}
```

### Data Transfer Objects (DTOs)
Directly exposing database entities can expose sensitive columns or cause infinite serialization loops in JSON. MedLink leverages DTOs to encapsulate payloads, as seen in [VitalDTOs.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/dto/VitalDTOs.java):

```java
public class VitalDTOs {
    @Getter @Setter
    public static class SubmitRequest {
        private String patientId;
        private Integer heartRate;
        private Integer spo2;
        private Integer respiratoryRate;
        private Integer systolicBp;
        private Integer diastolicBp;
        private Double temperature;
    }
}
```

---

## 3. Advanced Concepts

### CORS (Cross-Origin Resource Sharing)
By default, browsers prevent scripts running on one origin (e.g., `localhost:3000`) from requesting data from another origin (e.g., `localhost:8080`). To enable this secure coordination, [SecurityConfig.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/config/SecurityConfig.java#L61-L73) configures a custom `CorsConfigurationSource`:

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOriginPatterns(List.of("*"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"));
    config.setAllowedHeaders(List.of("*"));
    config.setAllowCredentials(true);
    return config;
}
```

### Server Side Pagination
Returning thousands of records in a single REST request degrades database performance and network bandwidth. Spring Boot uses `Pageable` to request chunked records:

```java
@GetMapping("/logs")
public Page<AuditLogEntry> getLogs(@RequestParam(defaultValue = "0") int page) {
    return auditLogService.getPagedLogs(page, 50);
}
```

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is the difference between POST, PUT, and PATCH?
**Answer**:
* `POST`: Creates a new resource. It is **not idempotent**; hitting POST multiple times creates multiple duplicate resources.
* `PUT`: Replaces an existing resource or creates it if it doesn't exist. It is **idempotent**; sending the same PUT payload multiple times has the same final system state as sending it once.
* `PATCH`: Applies a **partial update** to a resource (e.g., changing only a patient's heart rate without replacing their entire name and age record). It can be idempotent or non-idempotent depending on the implementation.

#### Q2: What is API Idempotency and why is it important in payment/medical actions?
**Answer**: An API endpoint is idempotent if making multiple identical requests has the same effect as making a single request. 
* **Importance**: If a network timeout occurs while submitting a triage response, the client retries the request. If the endpoint isn't idempotent, it could result in duplicate alerts or conflicts in treatment logs.
* **Implementation**: Clients generate a unique UUID `Idempotency-Key` and pass it in the headers. The server caches this key in Redis, and if it receives a duplicate key within a timeframe, it returns the cached response instead of processing the action again.

#### Q3: How do you version a REST API?
**Answer**:
1. **URI Versioning (Recommended)**: `/api/v1/patients`
2. **Query Parameter Versioning**: `/api/patients?version=1`
3. **Accept Header Versioning (Media Type)**: `Accept: application/vnd.company.v1+json`

---
---

# Module 5: Real-time Communication (WebSockets & STOMP)

This module explains real-time data streaming over HTTP, the mechanics of WebSockets and STOMP sub-protocol, implementation patterns, horizontal scaling, and web socket interview challenges.

## 1. Basics & Fundamentals

### Real-Time Web Protocols Compared
| Protocol | Connection Type | Directional Flow | Overhead | Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **Short Polling** | Repeated HTTP requests | Client-to-Server | High header overhead | Simplistic update feeds |
| **Long Polling** | Server hangs response until changes occur | Client-to-Server | Medium | Chat apps (Legacy) |
| **SSE (Server-Sent Events)** | Persistent HTTP connection | Server-to-Client | Low | One-way status feeds |
| **WebSockets** | Persistent TCP connection (via Upgrade) | Bi-directional | Extremely Low | Real-time dashboards |

### What is STOMP?
**STOMP (Simple Text Oriented Messaging Protocol)** is a sub-protocol that runs on top of WebSockets. Standard WebSockets only transmit raw frames. STOMP introduces messaging patterns:
* **Frame Structure**: COMMAND (e.g., `CONNECT`, `SUBSCRIBE`, `SEND`), Headers, and Body.
* **Topics/Queues**: Facilitates pub-sub message routing.

---

## 2. Working in MedLink

### WebSocket Config
Spring Boot sets up the WebSocket infrastructure in [WebSocketConfig.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/config/WebSocketConfig.java):

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry registry) {
        registry.enableSimpleBroker("/topic"); // In-memory message broker prefix
        registry.setApplicationDestinationPrefixes("/app");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws")
                .setAllowedOriginPatterns("*")
                .withSockJS(); // Fallback for browsers that don't support WebSockets
    }
}
```

### Server Side Message Dispatching
In [WebSocketService.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/service/WebSocketService.java), `SimpMessagingTemplate` sends notifications to specific broker paths:

```java
@Autowired private SimpMessagingTemplate ws;

public void pushAlert(Alert alert) {
    ws.convertAndSend("/topic/alerts", Map.of(
        "type",      "NEW_ALERT",
        "alertId",   alert.getAlertId(),
        "riskLevel", alert.getRiskLevel(),
        "riskScore", alert.getRiskScore(),
        "clinicId",  alert.getClinicId(),
        "patientAge", alert.getPatientAge(),
        "timestamp", alert.getAlertTimestamp().toString()
    ));
}
```

### Client Side Subscription (JS)
The hospital dashboard listens for real-time notifications in [hospital.html](file:///c:/Users/omkar/modified-vigilai-medlink/frontend/hospital.html):

```javascript
let socket = new SockJS('https://backend-ysf3.onrender.com/ws');
let stompClient = Stomp.over(socket);

stompClient.connect({}, function (frame) {
    console.log('Connected to WS: ' + frame);
    
    // Subscribe to new emergency alerts
    stompClient.subscribe('/topic/alerts', function (message) {
        let alertData = JSON.parse(message.body);
        if (alertData.type === 'NEW_ALERT') {
            triggerVisualAlert(alertData);
        }
    });
});
```

---

## 3. Advanced Concepts

### Scaling WebSockets Horizontally
Spring Boot's default simple broker runs in-memory. If we scale out to multiple server instances behind a load balancer, a client subscribed on Server A won't receive messages published from Server B.

```
Client A ──► Server A ── (In-Memory Broker) ──► No connection to Client B
Client B ──► Server B ── (In-Memory Broker)
```

**Solution: External Message Broker**
By routing STOMP messages to a dedicated container cluster running **RabbitMQ** or **ActiveMQ**:
```java
registry.enableStompBrokerRelay("/topic")
        .setRelayHost("rabbitmq-cluster")
        .setRelayPort(61613);
```
Now, all backend instances relay subscription events to the central broker, synchronizing messages system-wide.

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: How does the WebSocket handshake protocol work?
**Answer**: A WebSocket connection begins with an ordinary HTTP request. The client sends a GET request with specific headers:
* `Connection: Upgrade`
* `Upgrade: websocket`
* `Sec-WebSocket-Key: <random base64>`

If the server supports the protocol, it returns an HTTP `101 Switching Protocols` response with a validation hash `Sec-WebSocket-Accept`. Once the handshake is complete, the underlying TCP socket remains open, and communication switches to bidirectional binary/text frames.

#### Q2: How do you authenticate users connecting via WebSockets?
**Answer**: WebSockets do not support sending custom HTTP headers during the browser's standard handshake instantiation. We authenticate by:
1. **Query Parameters**: Passing the token as a query string during handshake (e.g., `/ws?token=JWT_STRING`). The server extracts the token and validates it inside a custom interceptor.
2. **STOMP Connect Payload**: Establishing a connection and immediately transmitting the JWT inside the STOMP `CONNECT` frame header, allowing the socket interceptor to authorize or terminate the socket.

#### Q3: What is the C10K / C10M problem and how does it relate to WebSockets?
**Answer**: The C10K (Handling 10,000 concurrent connections) and C10M (10 million connections) problems refer to web server scaling limitations. For stateless REST APIs, threads exist momentarily. For WebSockets, connections remain open.
* **Solution**: Rely on asynchronous, non-blocking I/O event loops (like Netty or Spring WebFlux) rather than allocating one OS thread per connection, which would quickly exhaust server memory allocations.

---
---

# Module 6: Machine Learning Integration (FastAPI & XGBoost)

This module explains how machine learning models are deployed for production, the design of FastAPI web endpoints, age-adaptive rule overrides, fallback mechanics, and ML engineering interviews.

## 1. Basics & Fundamentals

### Why FastAPI for Machine Learning?
* **High Performance**: Built on top of Starlette and Pydantic, FastAPI is one of the fastest Python frameworks available, matching Node.js and Go performance levels.
* **Async Support**: Leverages Python's `asyncio` to run non-blocking concurrent request loops.
* **Automatic Schema Validation**: Pydantic models automatically validate incoming request JSON parameters and generate Interactive OpenAPI documentation (Swagger UI).

### What is XGBoost?
**XGBoost (Extreme Gradient Boosting)** is an optimized distributed gradient boosting library. It uses a machine learning algorithm based on decision trees.
* **Ideal for Tabular Data**: It outperforms deep learning for structured dataset inputs (e.g., patient vitals like heart rate, blood pressure).
* **Speed & Regularization**: Employs regularization (L1/L2) to prevent overfitting and supports parallel tree construction.

---

## 2. Working in MedLink

### Data Flow for Risk Inference
```
[Clinic Frontend] ──► [Spring Boot] ──► [FastAPI Service]
                                             │
                            ┌────────────────┴────────────────┐
                     (Severe vitals?)                 (Normal vitals?)
                            │                                 │
                            ▼                                 ▼
                 [Age-Adaptive Rules]                  [XGBoost Model]
             (Override: CRITICAL / HIGH)           (Compute Sepsis Prob)
```

### FastAPI Server Design
In [main.py](file:///c:/Users/omkar/modified-vigilai-medlink/ai-service/app/main.py), vitals requests are routed through a validation pipeline:

```python
@app.post("/predict", response_model=PredictionResponse)
def predict(vitals: VitalsRequest):
    # 1. Rule Engine Check (Age-Adaptive SIRS thresholds)
    rule_result = apply_age_adaptive_rules(vitals)
    if rule_result:
        return PredictionResponse(
            **rule_result,
            source="RULE_ENGINE",
            top_features=top_features(vitals)
        )

    # 2. Model Inference
    try:
        model = get_model()
        features = [
            vitals.age, vitals.heart_rate, vitals.spo2,
            vitals.respiratory_rate, vitals.systolic_bp,
            vitals.diastolic_bp, vitals.temperature
        ]
        prob, _ = model.predict(features)
        level    = map_risk(float(prob))
        
        return PredictionResponse(
            risk_score=float(prob),
            risk_level=level,
            confidence=max(abs(float(prob) - 0.5) * 2, 0.5),
            source="XGBOOST_MODEL",
            top_features=top_features(vitals)
        )
    except Exception as e:
        # 3. Fallback to Simple Rules if model loads fail
        return apply_rules_fallback(vitals)
```

### Age-Adaptive Rules
Medical thresholds differ across patient demographics. The rules in [rule_engine.py](file:///c:/Users/omkar/modified-vigilai-medlink/ai-service/app/triage/rule_engine.py) override predictions:

```python
ADULT = dict(hr_high=90, hr_low=None, temp_high=38.3, temp_low=36.0, rr_high=20, bp_sys_low=100, spo2_low=94)
NEONATAL = dict(hr_high=180, hr_low=100, temp_high=38.0, temp_low=36.5, rr_high=60, bp_sys_low=60, spo2_low=90)

def apply_age_adaptive_rules(vitals: VitalsRequest) -> Optional[dict]:
    t = _thresholds(vitals)
    flags = 0
    if vitals.spo2 < t["spo2_low"] - 4:           flags += 2
    if vitals.systolic_bp < t["bp_sys_low"]:       flags += 2
    if vitals.heart_rate > t["hr_high"] + 20:      flags += 2
    if vitals.temperature < t["temp_low"]:         flags += 2

    if flags >= 6:
        return {"risk_score": 0.92, "risk_level": "CRITICAL", "confidence": 0.97}
    if flags >= 4:
        return {"risk_score": 0.78, "risk_level": "HIGH", "confidence": 0.90}
    return None
```

---

## 3. Advanced Concepts

### Model Explainability in Production
In clinical settings, "black box" models are not acceptable. Paramedics must know *why* a patient is flagged.
* **SHAP (SHapley Additive exPlanations)**: Calculates the game-theoretic contribution of each vital input.
* **Heuristic Proxy**: MedLink models this by checking which physiological parameters deviate from standard thresholds, mapping features like `"Tachycardia (110 bpm) ↑"` or `"Hypotension (85 mmHg) ↓"` in the API response.

### Model Drift & Retraining Pipeline
Over time, patient demographics or hospital procedures change, causing the model's prediction accuracy to degrade (known as **Model Drift**).
* **Retraining Pipeline**: Establish a cron script to run offline model retraining periodically using new patient data stored in the database.
* **Model Versioning**: Instead of hardcoding paths, use tools like **MLflow** or **DVC (Data Version Control)** to manage and serve model versions.

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: Why use an XGBoost model instead of a Deep Learning Neural Network?
**Answer**: For structured tabular data, XGBoost almost always matches or outperforms neural networks. It has fewer hyperparameters to tune, requires significantly less computation power, handles missing values natively, and runs inference faster (low CPU footprint), making it ideal for low-latency clinical endpoints.

#### Q2: How does a decision boundary work in binary classification?
**Answer**: A classifier outputs a probability score between `0.0` and `1.0`. The **Decision Boundary** (typically `0.5`) acts as the threshold. Score `≥ 0.5` is labeled positive (e.g., sepsis risk), while `< 0.5` is negative. In medical triage, we sometimes lower this boundary (e.g., `0.3`) to increase sensitivity, minimizing dangerous false negatives.

#### Q3: Explain pickle serialization and its potential vulnerabilities.
**Answer**: Pickle is Python's native tool for serializing objects to byte streams.
* **Vulnerability**: Loading untrusted pickle files is highly unsafe. During deserialization, pickle can execute arbitrary code inside `__reduce__` methods.
* **Mitigation**: Use model serialization formats like **ONNX (Open Neural Network Exchange)** or **Joblib** in secure storage buckets with restricted access controls.

---
---

# Module 7: Cryptography & Data Auditing (SHA-256 Hash Chaining)

This module discusses cryptographic verification, building secure Write Once Read Many (WORM) logs, audit chain implementation details, and database security interview strategies.

## 1. Basics & Fundamentals

### Hashing vs. Encryption vs. Encoding
* **Encoding (e.g., Base64)**: Transforms data formats for compatibility. It requires no key and is easily reversible.
* **Encryption (e.g., AES, RSA)**: Obfuscates data to keep it confidential. It is two-way and requires a key to decrypt.
* **Hashing (e.g., SHA-256)**: Generates a fixed-length signature of data. It is a one-way mathematical function; you cannot reverse a hash back to original text, and even a tiny change in source data completely changes the hash (Avalanche Effect).

```
Data Block A ──► [SHA-256] ──► Hash A
                                  │
                                  ▼
Data Block B + Hash A ────────► [SHA-256] ──► Hash B
                                                │
                                                ▼
Data Block C + Hash B ────────► [SHA-256] ──► Hash C
```

---

## 2. Working in MedLink

### Write Once Read Many (WORM) Audit Trail
To comply with medical standards like HIPAA, critical system modifications (such as changing triage decisions or assigning patients) must be logged in a tamper-evident manner.

MedLink achieves this using **Hash Chaining** in [AuditLogService.java](file:///c:/Users/omkar/modified-vigilai-medlink/backend/src/main/java/com/vigilai/service/AuditLogService.java). Each new entry incorporates the hash of the preceding entry, linking all records chronologically.

### Log Generation & Chain Linking
When a record changes, `logAction()` computes a new hash link:

```java
public synchronized void logAction(String action, String entityType, String entityId,
                      String userId, Object oldValue, Object newValue) {
    try {
        // Fetch the hash of the latest record in the DB
        String hashPrev = auditRepo.findLatest()
                .map(AuditLogEntry::getHashCurrent)
                .orElse("GENESIS"); // The starting link

        AuditLogEntry entry = AuditLogEntry.builder()
                .action(action).entityType(entityType).entityId(entityId)
                .userId(userId)
                .oldValue(oldValue != null ? oldValue.toString() : null)
                .newValue(newValue != null ? newValue.toString() : null)
                .timestamp(LocalDateTime.now().truncatedTo(ChronoUnit.SECONDS))
                .hashPrevious(hashPrev)
                .build();

        // Calculate current hash based on current values + previous hash
        String hash = sha256(entry);
        entry.setHashCurrent(hash);
        entry.setSignature("HMAC_" + hash.substring(0, 16));

        auditRepo.save(entry);
    } catch (Exception e) {
        log.error("AUDIT WRITE FAILED: {}", e.getMessage());
    }
}
```

### Hashing Formula
The hash is computed over a deterministic payload concatenation inside `sha256()`:

```java
private String sha256(AuditLogEntry e) throws Exception {
    String tsStr = e.getTimestamp() != null ? e.getTimestamp().format(HASH_FORMAT) : "NULL";
    String oldV = e.getOldValue() != null ? e.getOldValue() : "NULL";
    String newV = e.getNewValue() != null ? e.getNewValue() : "NULL";
    
    String data = String.join("|", 
            e.getAction(), 
            e.getEntityType(), 
            e.getEntityId(),
            tsStr, 
            oldV, 
            newV, 
            e.getHashPrevious());
            
    byte[] hash = MessageDigest.getInstance("SHA-256")
            .digest(data.getBytes(StandardCharsets.UTF_8));
    return HexFormat.of().formatHex(hash);
}
```

### Checking for Tampering
If a rogue user updates a log entry in the database (e.g., changes an old value from "HIGH" to "LOW"), two things will break:
1. The modified entry's computed hash will no longer match its stored `hash_current`.
2. The subsequent entry's `hash_previous` will no longer match the modified entry's new hash.

The integrity validation method `verifyIntegrity()` detects this immediately:

```java
public boolean verifyIntegrity() {
    List<AuditLogEntry> entries = auditRepo.findAllOrdered();
    String prev = "GENESIS";
    for (AuditLogEntry e : entries) {
        // 1. Verify connection to the parent link
        if (e.getHashPrevious() != null && !e.getHashPrevious().equals(prev)) {
            lastIntegrityReport = "AUDIT BREACH: Hash chain broken at log_id=" + e.getLogId();
            return false;
        }
        // 2. Verify values inside this link
        String computed = sha256(e);
        if (!computed.equals(e.getHashCurrent())) {
            lastIntegrityReport = "HASH MISMATCH at log_id=" + e.getLogId();
            return false;
        }
        prev = e.getHashCurrent();
    }
    return true;
}
```

---

## 3. Advanced Concepts

### HMAC (Hash-Based Message Authentication Code)
To verify that the logs were written by the server and not constructed by a database administrator, we sign them using an HMAC. HMAC runs the hashing algorithm using a secret key held by the server. Even if an attacker recreates a valid hash chain, they cannot generate the matching HMAC signatures without the secret key.

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is a cryptographic Hash Collision?
**Answer**: A hash collision occurs when two different inputs produce the exact same output hash. While theoretically possible due to infinite inputs mapping to a finite hash range (e.g., 256 bits), modern algorithms like SHA-256 make finding a collision computationally infeasible.

#### Q2: If a database administrator has root access, how do you prevent them from modifying audit logs?
**Answer**:
1. **Cryptographic Chaining (WORM)**: Chaining prevents silent edits because altering any historical record invalidates the entire subsequent hash chain.
2. **External Log Streams**: Stream log events to an external system with write-only credentials (e.g., AWS CloudWatch with access policies that deny delete/update permissions).
3. **Off-site backup**: Periodically sign and push the latest hash state to an independent decentralized ledger.

#### Q3: What is the difference between SHA-256 and bcrypt/scrypt?
**Answer**:
* **SHA-256**: A fast cryptographic hash designed for high-speed integrity checks. It is optimized for hardware and is relatively easy to compute in bulk.
* **bcrypt / scrypt**: Adaptive slow hashing algorithms designed for passwords. They introduce a configurable computational complexity (work factor) and memory footprint to resist high-speed GPU brute-force attacks.

---
---

# Module 8: Offline-First & Resiliency

This module explores building web applications that remain fully operational during internet disruptions, queue-based data synchronization, retry mechanisms, and offline resiliency interview questions.

## 1. Basics & Fundamentals

### What is Offline-First?
**Offline-First** is a software design approach that ensures core application logic operates seamlessly without an active internet connection. Instead of crashing or showing blank screen error states when offline, the application stores data locally first and syncs it with backend servers asynchronously when connectivity is restored.

### Benefits
* **High Availability**: Users can perform critical work in remote or underground areas (e.g., triage clinics with poor cellular reception).
* **Improved UX**: Submitting forms is instantaneous since it touches local memory instead of blocking on network requests.

---

## 2. Working in MedLink

### Client-Side Local Queue
In the clinic dashboard ([clinic.html](file:///c:/Users/omkar/modified-vigilai-medlink/frontend/clinic.html)), when vitals are submitted, the application first checks network availability. If offline, the payload is buffered to a local execution queue stored in `localStorage`.

```javascript
function submitVitalsForm(vitalsData) {
    if (!navigator.onLine) {
        queueOfflineVitals(vitalsData);
        showToast("Offline mode: Vitals queued locally!");
        return;
    }

    // Direct REST API send if online
    sendVitalsToServer(vitalsData);
}

function queueOfflineVitals(data) {
    let queue = JSON.parse(localStorage.getItem('vitals_sync_queue') || '[]');
    queue.push({
        id: generateUUID(),
        data: data,
        timestamp: Date.now()
    });
    localStorage.setItem('vitals_sync_queue', JSON.stringify(queue));
}
```

### Automatic Sync Trigger
The application registers listener events to detect when the browser regains internet connectivity:

```javascript
window.addEventListener('online', () => {
    showToast("Internet connection restored. Synchronizing queued data…");
    processOfflineQueue();
});

async function processOfflineQueue() {
    let queue = JSON.parse(localStorage.getItem('vitals_sync_queue') || '[]');
    if (queue.length === 0) return;

    for (let item of [...queue]) {
        try {
            let success = await sendVitalsToServer(item.data);
            if (success) {
                // Remove from queue upon successful HTTP 201 response
                queue = queue.filter(q => q.id !== item.id);
                localStorage.setItem('vitals_sync_queue', JSON.stringify(queue));
            }
        } catch (error) {
            console.error("Sync failed for item: ", item.id, error);
            break; // Stop and retry later to maintain record sequence
        }
    }
}
```

---

## 3. Advanced Concepts

### Exponential Backoff with Jitter
When synchronizing client data or calling external microservices, simple loops that retry immediately can overload databases and downstream APIs (known as **Thundering Herd Problem**). Instead, implement **Exponential Backoff**:

$$\text{Delay} = \text{Base} \times 2^{\text{attempt}} + \text{Random Jitter}$$

Adding random jitter spreads out concurrent client requests, smoothing server CPU spikes.

### Conflict Resolution Strategies
When multiple offline clients edit the same resource independently and then sync:
* **Last-Write-Wins (LWW)**: The server keeps the record with the most recent timestamp. Simple but risks overwriting legitimate updates.
* **CRDTs (Conflict-Free Replicated Data Types)**: Special data structures (like Grow-Only sets) that merge changes mathematically without conflicts.

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is the difference between LocalStorage, SessionStorage, and IndexedDB?
**Answer**:
* `SessionStorage`: Volatile; data is wiped when the browser tab is closed. Holds up to 5MB.
* `LocalStorage`: Persistent; data survives browser restarts. Simple key-value string interface, limited to ~5-10MB. Synchronous (blocks UI thread).
* `IndexedDB`: Persistent, asynchronous transactional database. Can store complex JSON structures, files, and blobs. Scalable (often up to 80% of disk space). Best for heavy offline buffering.

#### Q2: How does a Service Worker enable offline capabilities?
**Answer**: A Service Worker is a background script registered by the browser. It acts as a client-side network proxy, intercepting all HTTP requests. If the client is offline, the Service Worker serves static assets and API data directly from the **Cache API**, allowing web pages to load without internet connection.

#### Q3: How do you handle authentication during offline durations?
**Answer**: Local sessions rely on the expiration time stored in the JWT payload. The client-side app can decode the JWT to check if it's still valid. However, the client cannot check if the user's password was changed or their account disabled until connection is restored.

---
---

# Module 9: Modern Frontend Architecture & CSS

This module outlines styling systems, state synchronization in vanilla JavaScript, visual optimizations, CSS variables, and modern web frontend interview questions.

## 1. Basics & Fundamentals

### Vanilla JS vs. Frameworks
While frameworks (like React, Vue, Angular) are powerful, vanilla JavaScript remains the foundation of all web browsers.
* **Benefits of Vanilla JS**: Zero build-step requirements, zero dependency bloat, smaller bundle sizes, faster initial loading, and direct browser performance.
* **Benefits of Frameworks**: Component modularity, declarative rendering (virtual DOM), automated state binding, and scalable ecosystem libraries.

---

## 2. Working in MedLink

### Premium Styling System
MedLink v2.0 uses a highly polished Dark theme with custom property variables declared in the `:root` scope of HTML documents, as seen in [login.html](file:///c:/Users/omkar/modified-vigilai-medlink/frontend/login.html#L12-L26):

```css
:root {
  --bg:       #04080f;
  --surface:  rgba(13, 25, 41, 0.7);
  --surface2: rgba(20, 35, 55, 0.8);
  --border:   rgba(255, 255, 255, 0.08);
  --accent:   #00d4ff;
  --accent2:  #0057ff;
  --danger:   #ff3b5c;
  --success:  #00e5a0;
  --text:     #f0f7ff;
  --muted:    #6b8eb0;
  --sans:     'Plus Jakarta Sans', sans-serif;
}
```

### Glassmorphism & UI Accents
To achieve a premium modern glass effect, cards combine transparency, subtle borders, and background blurs:

```css
.card {
  background: var(--surface);
  backdrop-filter: blur(12px); /* Blurred glass effect */
  border: 1px solid var(--border);
  border-radius: 24px;
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
}
```

### Micro-Animations
Subtle visual micro-interactions alert users and indicate state transitions. For example, input validations use shake animations:

```css
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}

.error-msg.show {
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}
```

---

## 3. Advanced Concepts

### Layout Systems: Flexbox vs. Grid
* **Flexbox (1D Layout)**: Best for laying out items in a single row or column (e.g., a header navigation bar, a logo + title group).
* **Grid (2D Layout)**: Best for complex rows AND columns layouts (e.g., dashboard grids containing modular widget cards).

### Browser Rendering Lifecycle
Understanding how browsers render HTML elements is crucial for visual optimization:
```
HTML ──► DOM Tree ──┐
                    ├─► Render Tree ──► Layout ──► Paint ──► Composite
CSS  ──► CSSOM  ────┘
```
Modifying properties like `width`, `height`, or `left` forces the browser to recalculate the positions of elements, triggering a costly **Layout** (or Reflow) phase. Modifying `transform` or `opacity` skips Layout and Paint, proceeding directly to the **Composite** phase executed on the GPU, yielding smooth 60fps animations.

---

## 4. Tech Interview Point of View

### Common Interview Questions & Answers

#### Q1: What is the Event Loop in JavaScript?
**Answer**: JavaScript is single-threaded. To perform asynchronous non-blocking calls (like Fetch or setTimeout), the browser provides Web APIs. When an async task completes, its callback is pushed to the **Callback Queue** (or Microtask Queue for Promises). The **Event Loop** continually checks if the Call Stack is empty. If it is, it pushes the first task from the queue onto the stack for execution.

#### Q2: What is Event Delegation and how does it optimize memory?
**Answer**: Instead of attaching event listeners to hundreds of individual list items (e.g., patient rows), you attach a single listener to their parent element. When an event fires, it bubbles up the DOM tree. The parent's listener inspects `event.target` to identify which child was clicked. This reduces memory usage and automatically supports dynamic elements added later.

#### Q3: What is the difference between Reflow and Repaint?
**Answer**:
* **Reflow (Layout)**: The browser recalculates the geometry (position and size) of elements. Triggered by changing layout properties (`width`, `margin`, `font-size`) or resizing the window. Very resource-intensive.
* **Repaint**: The browser redraws pixels on the screen without changing positions. Triggered by changing visual styles (`color`, `background-color`, `visibility`).
* **Optimization**: Use `transform: translate()` instead of changing absolute top/left coordinates to avoid triggering reflows.

---
---

# Module 10: Tech Interview Deep Dive

This module consolidates system design configurations, common coding challenges, concurrency management, scaling mechanisms, and high-availability interview preparation.

## 1. System Design: Scaling VigilAI MedLink to National Scale

### System Architecture Diagram
To scale MedLink to support thousands of clinics and hospitals, we replace simple in-memory components with distributed infrastructure:

```
[Clinics] ──► [Load Balancer] ──► [API Gateways] ──► [Spring Boot App Instances]
                                                        │              │
                     ┌──────────────────────────────────┘              ▼
                     ▼                                           [Redis Cache]
              [Kafka Clusters]                                (Tokens / Rate Limits)
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
 [Hospital Consumers]    [AI inference Service] ──► [GPU Cluster]
 (Real-time alerts)      (XGBoost / Sepsis)
         │
         ▼
[Postgres (Primary)] ◄──► [Postgres (Read Replicas)]
```

### High-Scale Component Mapping
1. **API Gateway**: Handles rate-limiting, SSL termination, and routes authentication requests before hitting microservices.
2. **Redis Cache**: Caches active user JWT validation statuses and transient real-time stats like ICU bed availability.
3. **Apache Kafka (Message Queue)**: Decouples vitals submissions from alerting triggers. Vitals are pushed to a Kafka topic; the AI inference service and database ingestion workers consume messages asynchronously at their own pace.
4. **Database Read Replicas**: Directs write operations to a primary Postgres instance, while replicating data to secondary read-only replicas to optimize dashboard analytics queries.

---

## 2. Coding Challenge: Hash Chain Verification

An interviewer asks: *"Implement a function to verify the integrity of a hash-chained ledger database."*

### Python Implementation
```python
import hashlib

def verify_chain(ledger: list[dict]) -> bool:
    """
    Verifies that a list of dictionary log entries forms a valid hash chain.
    Each entry format:
    {
        "log_id": int,
        "data": str,
        "hash_prev": str,
        "hash_curr": str
    }
    """
    prev_hash = "GENESIS"
    
    for entry in ledger:
        # 1. Verify link back to previous record
        if entry["hash_prev"] != prev_hash:
            print(f"Chain broken at entry {entry['log_id']}")
            return False
        
        # 2. Recompute the hash of this entry
        payload = f"{entry['log_id']}|{entry['data']}|{entry['hash_prev']}"
        computed_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        
        # 3. Check if stored hash matches computed hash
        if entry["hash_curr"] != computed_hash:
            print(f"Hash mismatch at entry {entry['log_id']}")
            return False
            
        # Update pointer
        prev_hash = entry["hash_curr"]
        
    return True
```

---

## 3. Concurrency & Threading: Race Conditions

### The ICU Bed Allocation Conflict
If two clinic users attempt to book the last available ICU bed at a hospital at the exact same millisecond:
1. Client A queries: `select available_beds from hospitals where id = 1` (returns 1).
2. Client B queries: `select available_beds from hospitals where id = 1` (returns 1).
3. Client A executes: `update hospitals set available_beds = 0 where id = 1` (Success).
4. Client B executes: `update hospitals set available_beds = 0 where id = 1` (Success).
Both clinics believe they successfully reserved the bed, resulting in a critical overbooking collision.

### Mitigations
* **Pessimistic Locking**: Use database locks during query phase:
  ```sql
  SELECT available_beds FROM hospitals WHERE id = 1 FOR UPDATE;
  ```
  This blocks client B's transaction until client A commits their update.
* **Optimistic Locking**: Add a `@Version` annotation to the JPA entity. When a conflict occurs, Spring throws an `OptimisticLockingFailureException` and rolls back client B's request.
* **Thread-Safe JVM Handlers**: In Java, use `synchronized` blocks or `ReentrantLock` wrappers around singleton service reservation scopes.

---

## 4. Behavioral & Case Studies

### Meeting Latency SLAs (Service Level Agreements)
* **Problem**: An AI model takes too long to run inference, exceeding the 200ms API response SLA.
* **Solution**: Offload explainability calculations to an asynchronous worker queue. Return the risk classification first, and dispatch detailed SHAP interpretations or paramedic guidance protocols via WebSockets or background jobs.

### HIPAA Data Security & Privacy
* **Problem**: Patient logs contain protected health information (PHI) which cannot be stored as raw text in public logs.
* **Solution**: Ensure all PHI (names, SSNs, medical histories) is encrypted at rest using AES-256 before being committed to the database, and scrub all audit logs to replace name strings with transient database reference UUID keys.

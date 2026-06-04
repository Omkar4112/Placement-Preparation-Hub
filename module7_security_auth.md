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

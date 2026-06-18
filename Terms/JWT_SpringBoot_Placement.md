# 🔐 JWT Authentication — Placement Interview Guide
> Easy Language | Nothing Missing | Spring Boot Focused | 30-Minute Read

---

## 📌 Table of Contents
1. [What is Authentication?](#1-what-is-authentication)
2. [What is Authorization?](#2-what-is-authorization)
3. [Authentication vs Authorization](#3-authentication-vs-authorization)
4. [What is JWT?](#4-what-is-jwt)
5. [Full Form of JWT](#5-full-form-of-jwt)
6. [Why JWT Instead of Sessions?](#6-why-jwt-instead-of-sessions)
7. [Structure of JWT](#7-structure-of-jwt)
8. [JWT Login Flow — Step by Step](#8-jwt-login-flow--step-by-step)
9. [JWT in Spring Boot Project](#9-jwt-in-spring-boot-project)
10. [JWT in React + Spring Boot](#10-jwt-in-react--spring-boot)
11. [Advantages of JWT](#11-advantages-of-jwt)
12. [Limitations of JWT](#12-limitations-of-jwt)
13. [Common Interview Q&A](#13-common-interview-qa)
14. [Top 10 Interview Questions](#14-top-10-interview-questions)
15. [1-Minute JWT Explanation](#15-1-minute-jwt-explanation)
16. [Last-Minute Revision Cheat Sheet](#16-last-minute-revision-cheat-sheet)

---

## 1. What is Authentication?

**What it means:**
Authentication = **"Prove who you are"**

When you enter your username and password, the system verifies:
*"Is this a real registered user?"*

**Interview Answer (30 seconds):**
> Authentication is the process of verifying a user's identity.
> The user provides credentials (username + password), and the server checks if they are valid.
> It answers the question: **"Who are you?"**

**Analogy:**
> Showing your Aadhaar card at a hotel.
> The receptionist checks your ID → confirms you are who you say → that is Authentication.

**In Spring Boot:**
```java
authenticationManager.authenticate(
    new UsernamePasswordAuthenticationToken(email, password)
);
```
This single line:
- Checks if the email exists in the DB
- Verifies the password using BCrypt
- Throws an exception if credentials are wrong

---

## 2. What is Authorization?

**What it means:**
Authorization = **"What are you allowed to do?"**

Even after login, every API has rules:
- Only ADMIN can delete users
- Only USER can view their own profile

**Interview Answer (30 seconds):**
> Authorization is the process of checking whether an authenticated user has permission to access a resource.
> It happens **after** authentication.
> It answers the question: **"What can you do?"**

**Analogy:**
> Your Aadhaar card got you into the hotel (Authentication).
> But your room key only opens **your room**, not the server room or other floors.
> That access restriction is Authorization.

**In Spring Boot:**
```java
.requestMatchers("/api/admin/**").hasRole("ADMIN")   // Only ADMIN
.requestMatchers("/api/user/**").hasRole("USER")     // Only USER
.requestMatchers("/api/auth/**").permitAll()         // Everyone (login/register)
```

---

## 3. Authentication vs Authorization

| | Authentication | Authorization |
|---|---|---|
| **Question** | Who are you? | What can you do? |
| **When** | First (Login) | Second (After login) |
| **Example** | Email + Password check | Role-based access (ADMIN/USER) |
| **Failure HTTP code** | **401 Unauthorized** | **403 Forbidden** |
| **What it uses** | Credentials | Roles / Permissions |

> 💡 **Key rule:** Authentication always comes first. Authorization is impossible without authentication.

**401 vs 403 — must know:**
- `401` = Token is missing, expired, or invalid → *"We don't know who you are"*
- `403` = Token is valid, but you don't have permission → *"We know who you are, but you can't do this"*

---

## 4. What is JWT?

**Simple explanation:**
JWT is a **token** — a signed string — that the server gives you after successful login.

You carry this token.
For every protected API request, you send this token.
The server reads the token, verifies it, and knows **who you are and what role you have** — without touching the database.

**Interview Answer (30 seconds):**
> JWT is an open standard (RFC 7519) for securely transmitting information between client and server as a JSON object.
> After login, the server generates a JWT and sends it to the client.
> The client stores it and sends it with every request.
> The server validates the token — **no database call needed**.
> JWT is **stateless** — the server stores nothing.

**Analogy:**
> A movie ticket with your name, seat number, and show time printed.
> At the entrance, the usher reads your ticket.
> They don't call the box office to verify — the ticket itself is proof.
> JWT works exactly like that.

---

## 5. Full Form of JWT

> **JWT = JSON Web Token**

| Word | Meaning |
|---|---|
| **JSON** | Data inside the token is in JSON format |
| **Web** | Designed for web-based (HTTP) communication |
| **Token** | A signed string used as proof of identity |

- Defined by **RFC 7519**
- Open standard — supported in Java, JavaScript, Python, Go, etc.

---

## 6. Why JWT Instead of Sessions?

### How Sessions Work (Old Way)
1. User logs in
2. Server creates a session, stores it in **server memory or DB**
3. Server gives client a **Session ID** (cookie)
4. Every request → client sends Session ID → server checks DB → response

**Problem with sessions:**
- Server has to **store data** for every logged-in user
- If you have 3 servers, all must share the same session storage
- Does not scale well for REST APIs and microservices

---

### How JWT Works (Modern Way)
1. User logs in
2. Server creates a JWT, **stores nothing on the server**
3. JWT sent to client — client stores it
4. Every request → client sends JWT → server **reads and validates the token** (no DB hit)

**JWT is STATELESS** — the server does not remember anything between requests.
Each request carries everything the server needs inside the token itself.

---

### Session vs JWT Comparison

| | Session | JWT |
|---|---|---|
| **Storage** | Server (DB/Memory) | Client (localStorage/cookie) |
| **Stateful / Stateless** | Stateful | **Stateless** |
| **Server needs to remember?** | ✅ Yes | ❌ No |
| **DB call per request?** | ✅ Yes | ❌ No |
| **Scales easily?** | ❌ No | ✅ Yes |
| **Good for microservices?** | ❌ No | ✅ Yes |
| **Good for mobile apps?** | ❌ No | ✅ Yes |
| **Easy logout?** | ✅ Yes (delete session) | ❌ Hard (token lives until expiry) |

**Analogy:**
> **Session** = Waiter memorises your order (he must serve you every time — not scalable).
> **JWT** = You carry a printed receipt (any waiter can serve you by reading your receipt).

---

## 7. Structure of JWT

A JWT looks like this:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGdtYWlsLmNvbSIsInJvbGUiOiJVU0VSIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
       ↑                                            ↑                                              ↑
    HEADER                                       PAYLOAD                                       SIGNATURE
```

**Three parts separated by dots (`.`)**
```
Header . Payload . Signature
```

---

### Part 1 — Header

Tells the receiver what type of token this is and which algorithm was used to sign it.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

| Field | Meaning |
|---|---|
| `alg` | Algorithm used to create the signature — `HS256` is most common |
| `typ` | Token type — always `JWT` |

This JSON is then **Base64URL encoded** → becomes the first part of the token.

**HS256 = HMAC + SHA-256** → uses one shared secret key to sign and verify.

---

### Part 2 — Payload (Claims)

Contains **user data**. These are called **claims**.

```json
{
  "sub": "user@gmail.com",
  "role": "USER",
  "iat": 1700000000,
  "exp": 1700086400
}
```

**Standard Claims (must know):**

| Claim | Full Form | Meaning |
|---|---|---|
| `sub` | Subject | Who the token belongs to (email or userId) |
| `iat` | Issued At | When the token was created (Unix timestamp) |
| `exp` | Expiration | When the token expires (Unix timestamp) |
| `iss` | Issuer | Who issued the token (e.g., your app name) |

**Custom Claims:**
You can add anything — like `role`, `userId`, `name`, etc.

> ⚠️ **CRITICAL — Must say this in interviews:**
> The payload is **NOT encrypted**.
> It is only **Base64URL encoded**.
> Anyone can decode it and read the data.
> **NEVER put passwords, sensitive data, or PII in the payload.**

---

### Part 3 — Signature

The signature is what makes JWT **secure and tamper-proof**.

**How it is created:**
```
Signature = HMACSHA256(
    Base64URL(header) + "." + Base64URL(payload),
    secretKey
)
```

- The server uses a **secret key** to create this signature.
- When a token arrives, the server **re-computes** the signature using the same secret key.
- If the computed signature matches the token's signature → token is **valid and untampered**.
- If someone changes even one character in the payload → signature won't match → **token rejected**.

> 💡 The signature guarantees **integrity** (not tampered), NOT **confidentiality** (not encrypted).

**Analogy:**
> A signed cheque — the bank verifies the signature to confirm it's genuine.
> If someone changes the amount, the signature no longer matches → cheque rejected.

---

## 8. JWT Login Flow — Step by Step

```
USER                    REACT (Client)              SPRING BOOT (Server)           DATABASE
 |                           |                               |                         |
 | enters email+password     |                               |                         |
 |-------------------------->|                               |                         |
 |                           | POST /api/auth/login          |                         |
 |                           | {email, password}             |                         |
 |                           |------------------------------>|                         |
 |                           |                               | find user by email      |
 |                           |                               |------------------------>|
 |                           |                               | return user data        |
 |                           |                               |<------------------------|
 |                           |                               | verify BCrypt password  |
 |                           |                               | generate JWT token      |
 |                           | return { token: "eyJ..." }    |                         |
 |                           |<------------------------------|                         |
 |                           | store in localStorage         |                         |
 |                           |                               |                         |
 | clicks "My Profile"       |                               |                         |
 |-------------------------->|                               |                         |
 |                           | GET /api/user/profile         |                         |
 |                           | Header: Bearer eyJ...         |                         |
 |                           |------------------------------>|                         |
 |                           |                               | JwtAuthFilter runs      |
 |                           |                               | extract email from token|
 |                           |                               | validate signature      |
 |                           |                               | check expiry            |
 |                           |                               | set user in Security    |
 |                           |                               | Context                 |
 |                           |                               | check role/permission   |
 |                           | return profile data           |                         |
 |                           |<------------------------------|                         |
 | sees profile              |                               |                         |
```

**Step-by-step summary:**

| Step | What Happens |
|---|---|
| 1 | User sends email + password to `/api/auth/login` |
| 2 | Spring Boot checks credentials against DB |
| 3 | If valid, `JwtService` generates a signed JWT |
| 4 | JWT returned to React in the response |
| 5 | React stores JWT in `localStorage` |
| 6 | For every protected request, React adds `Authorization: Bearer <token>` header |
| 7 | `JwtAuthFilter` intercepts the request |
| 8 | Filter extracts email from token, validates signature, checks expiry |
| 9 | If valid → user set in `SecurityContextHolder` → request proceeds |
| 10 | Controller runs, checks role if needed, returns data |
| 11 | If token is invalid/expired → **401 Unauthorized** returned |

---

## 9. JWT in Spring Boot Project

### Project File Structure
```
src/main/java/
├── config/
│   └── SecurityConfig.java           ← Security rules, filter chain, CORS
├── controller/
│   └── AuthController.java           ← /login and /register endpoints
├── filter/
│   └── JwtAuthFilter.java            ← Validates JWT on every request
├── service/
│   ├── JwtService.java               ← Generate, parse, validate tokens
│   └── UserDetailsServiceImpl.java   ← Load user from DB by email
├── model/
│   └── User.java                     ← User entity
└── repository/
    └── UserRepository.java           ← JPA DB access
```

---

### 1. JwtService.java — Token logic
```java
@Service
public class JwtService {

    // Secret key — stored securely in application.properties
    @Value("${jwt.secret}")
    private String secret;

    // Generate JWT after successful login
    public String generateToken(String email) {
        return Jwts.builder()
                .setSubject(email)                           // who the token is for
                .claim("role", "USER")                       // custom claim
                .setIssuedAt(new Date())                     // current time
                .setExpiration(new Date(                     // expiry = now + 10 hours
                    System.currentTimeMillis() + 1000 * 60 * 60 * 10))
                .signWith(getSignKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    // Extract email (subject) from token
    public String extractEmail(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(getSignKey())
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    // Check if token is valid (not expired + correct user)
    public boolean isTokenValid(String token, UserDetails userDetails) {
        String email = extractEmail(token);
        return email.equals(userDetails.getUsername()) && !isTokenExpired(token);
    }

    // Check if token is expired
    private boolean isTokenExpired(String token) {
        Date expiry = Jwts.parserBuilder()
                .setSigningKey(getSignKey())
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getExpiration();
        return expiry.before(new Date());
    }

    private Key getSignKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secret);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

---

### 2. JwtAuthFilter.java — Runs on every request
```java
@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    @Autowired
    private JwtService jwtService;

    @Autowired
    private UserDetailsServiceImpl userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
                                    throws ServletException, IOException {

        // Step 1: Read Authorization header
        String authHeader = request.getHeader("Authorization");

        // Step 2: If no token or wrong format → skip (will fail later with 401)
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        // Step 3: Extract token (remove "Bearer " prefix)
        String token = authHeader.substring(7);

        // Step 4: Extract email from token
        String email = jwtService.extractEmail(token);

        // Step 5: If email found and not already authenticated
        if (email != null && SecurityContextHolder.getContext().getAuthentication() == null) {

            // Step 6: Load user from DB
            UserDetails userDetails = userDetailsService.loadUserByUsername(email);

            // Step 7: Validate token
            if (jwtService.isTokenValid(token, userDetails)) {

                // Step 8: Set authenticated user in Security Context
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails, null, userDetails.getAuthorities());

                authToken.setDetails(
                    new WebAuthenticationDetailsSource().buildDetails(request));

                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        // Step 9: Continue to next filter / controller
        filterChain.doFilter(request, response);
    }
}
```

> 💡 **Why `OncePerRequestFilter`?**
> It guarantees this filter executes **exactly once per HTTP request** — not multiple times.
> This is important because Spring's filter chain can sometimes call filters more than once.

---

### 3. SecurityConfig.java — Security rules
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Disable CSRF — not needed when using JWT (CSRF is for cookie-based sessions)
            .csrf(csrf -> csrf.disable())

            // STATELESS — server will NOT create or use HTTP sessions
            // Every request must carry JWT — server remembers nothing
            .sessionManagement(sess ->
                sess.sessionCreationPolicy(SessionCreationPolicy.STATELESS))

            // URL access rules
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()  // login/register = open
                .anyRequest().authenticated()                 // everything else needs JWT
            )

            // Add our JWT filter BEFORE Spring's default auth filter
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(); // BCrypt for hashing passwords
    }
}
```

> 💡 **Why `SessionCreationPolicy.STATELESS`?**
> This tells Spring Security: *"Don't create sessions. Don't store anything. Each request must prove itself."*
> This is what makes JWT truly stateless.

---

### 4. AuthController.java — Login endpoint
```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtService jwtService;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {

        // Step 1: Authenticate (throws exception if wrong credentials)
        authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                request.getEmail(), request.getPassword())
        );

        // Step 2: If no exception → generate JWT
        String token = jwtService.generateToken(request.getEmail());

        // Step 3: Return token to client
        return ResponseEntity.ok(Map.of("token", token));
    }
}
```

---

### Request Flow in Spring Boot
```
HTTP Request arrives
        ↓
JwtAuthFilter runs         ← Extracts token, validates, sets user in SecurityContext
        ↓
Spring Security checks     ← Is this URL allowed? Does user have the right role?
        ↓
DispatcherServlet
        ↓
Controller method runs     ← Your actual business logic
        ↓
HTTP Response sent
```

---

## 10. JWT in React + Spring Boot

### Step 1 — Login (save the token)
```javascript
const login = async (email, password) => {
    const response = await fetch('http://localhost:8080/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem('token', data.token);  // Save JWT in browser
    }
};
```

### Step 2 — Protected API call (send the token)
```javascript
const getProfile = async () => {
    const token = localStorage.getItem('token');  // Read JWT from browser

    const response = await fetch('http://localhost:8080/api/user/profile', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,   // Send JWT in header
            'Content-Type': 'application/json'
        }
    });

    return response.json();
};
```

### Step 3 — Logout (remove the token)
```javascript
const logout = () => {
    localStorage.removeItem('token');  // Delete JWT from browser
    window.location.href = '/login';
};
```

> 💡 **Important note on localStorage:**
> Storing JWT in `localStorage` is simple but vulnerable to **XSS attacks** (malicious JavaScript can steal it).
> In production, **HttpOnly cookies** are more secure (JavaScript cannot access them at all).
> For interviews: *"In our project we used localStorage for simplicity. In production, HttpOnly cookies are recommended."*

---

## 11. Advantages of JWT

| Advantage | Explanation |
|---|---|
| ✅ **Stateless** | Server stores nothing — each request is independent. Scales perfectly. |
| ✅ **No DB hit per request** | Server validates token cryptographically — no database query |
| ✅ **Self-contained** | Token itself carries all info (email, role, expiry) |
| ✅ **Cross-domain** | Works across different domains — perfect for REST APIs |
| ✅ **Mobile friendly** | Easy to send in HTTP `Authorization` header from any platform |
| ✅ **Microservices ready** | Any service validates the token using the shared secret key |
| ✅ **Open standard** | RFC 7519 — supported in Java, JavaScript, Python, Go, etc. |

---

## 12. Limitations of JWT

| Limitation | Explanation |
|---|---|
| ❌ **Cannot revoke a token** | Once issued, JWT is valid until expiry. Even after logout, it still works. |
| ❌ **Payload is not encrypted** | Anyone can Base64 decode the payload and read its contents |
| ❌ **Token size** | JWT is larger than a session ID — adds overhead to every request |
| ❌ **Secret key risk** | If the secret key is leaked, an attacker can forge any token |
| ❌ **Expiry trade-off** | Short expiry = frequent re-login. Long expiry = security risk |
| ❌ **XSS risk** | If stored in localStorage, JavaScript malware can steal the token |

### JWT Logout (Easy Interview Answer)

JWT is stored on the **client side**, so the server **cannot directly destroy it**.

**1. Short Expiry Token**
- Keep JWT valid for only **15–30 minutes**
- After logout, delete it from browser/mobile storage
- Even if someone gets it, it will expire soon

**2. Blacklist Method**
- When user logs out, save the JWT in **Redis blacklist**
- On every request, check whether the token is blacklisted
- If blacklisted → reject the request

**3. Refresh Token Method (Most Common)**
- **Access Token** → short expiry (15 min)
- **Refresh Token** → long expiry (days/weeks)
- On logout, delete/invalidate the refresh token
- User cannot get a new access token after logout

**One-Line Interview Answer:**
> JWT logout is usually handled by deleting the token on the client, using short-lived access tokens, and often invalidating refresh tokens or maintaining a blacklist for extra security.

---

## 13. Common Interview Q&A

**Q: What is JWT? Define it in one line.**
> JWT (JSON Web Token) is a compact, URL-safe, self-contained token used to securely transmit user identity and claims between client and server, signed with a secret key to prevent tampering.

---

**Q: What are the 3 parts of JWT?**
> **Header** — algorithm and token type
> **Payload** — user data (sub, role, iat, exp)
> **Signature** — HMAC hash of header+payload using secret key

---

**Q: Is JWT encrypted?**
> No. JWT is **encoded** (Base64URL), not **encrypted**.
> The signature ensures it wasn't **tampered**, but the payload is **readable** by anyone.
> Use JWE (JSON Web Encryption) if you need to encrypt the payload.

---

**Q: Why is JWT called stateless?**
> Because the server does **not store any session data**.
> The JWT itself contains all user information.
> Any server can validate it using just the secret key.
> No shared storage, no database session table, no server-side state.

---

**Q: What is the difference between stateless and stateful?**
> **Stateful** (Sessions) → Server remembers user state between requests (stores in memory/DB)
> **Stateless** (JWT) → Server remembers nothing. Each request proves itself by carrying the token.

---

**Q: What is `SecurityContextHolder`?**
> It is Spring Security's holder for the current user's authentication details.
> When `JwtAuthFilter` validates a token, it stores the authenticated user here.
> Controllers can then access the current user using `SecurityContextHolder.getContext().getAuthentication()`.

---

**Q: Why do we disable CSRF in JWT-based apps?**
> CSRF attacks exploit browser cookies sent automatically.
> Since JWT is sent manually in the `Authorization` header — **not automatically by the browser** — CSRF is not a threat.
> So we disable CSRF protection in `SecurityConfig`.

---

**Q: What is BCrypt and why use it?**
> BCrypt is a password hashing algorithm.
> Passwords are **never stored as plain text** in the database.
> BCrypt hashes the password before saving and verifies by comparing hashes.
> It includes a **salt** (random value) to prevent rainbow table attacks.

---

**Q: What is a Refresh Token?**
> An Access Token has a short life (15–60 min) for security.
> A Refresh Token has a long life (7–30 days) and is used to get a new Access Token when it expires.
> The user doesn't need to log in again — the Refresh Token silently gets a new Access Token.

```
Access Token  → short-lived (15 min) → used in Authorization header for API calls
Refresh Token → long-lived (7 days)  → used to get new Access Token when expired
```

---

**Q: What algorithm does JWT use? What is HS256?**
> **HS256 = HMAC + SHA-256**
> It uses a **single shared secret key** to both sign and verify the token.
> Suitable for single-server apps.
>
> **RS256 = RSA + SHA-256**
> Uses a **private key** to sign and a **public key** to verify.
> Suitable for distributed systems / microservices where verification must happen on multiple servers.

---

**Q: What HTTP status codes are related to JWT?**
| Code | Meaning | Cause |
|---|---|---|
| **200** | OK | Valid token, access granted |
| **401** | Unauthorized | Token missing, expired, or signature invalid |
| **403** | Forbidden | Valid token, but role insufficient |

---

**Q: What happens when the JWT secret key is compromised?**
> All tokens signed with that key can be **forged by the attacker**.
> Immediate action: **Rotate the secret key** → all existing tokens become invalid → all users forced to re-login.
> The new key should be stored securely (environment variable, secrets manager — NOT hardcoded).

---

## 14. Top 10 Interview Questions

```
1.  What is JWT? What does it stand for?
2.  What are the 3 parts of JWT? Explain each.
3.  Why is JWT stateless? What does stateless mean?
4.  Is the JWT payload encrypted? What is the risk?
5.  Difference between Authentication and Authorization?
6.  401 vs 403 — what is the difference?
7.  Why JWT over sessions in REST APIs?
8.  What does JwtAuthFilter do? What class does it extend?
9.  What is SessionCreationPolicy.STATELESS and why do we use it?
10. How do you handle logout with JWT? What is a Refresh Token?
```

---

## 15. 1-Minute JWT Explanation

> *Use this when asked: "Explain JWT" or "How did authentication work in your project?"*

---

> *"In our React + Spring Boot project, we implemented stateless authentication using JWT — JSON Web Token.*
>
> *When a user logs in, Spring Boot verifies the email and BCrypt-hashed password against the database.*
> *If valid, we generate a JWT — a signed token with 3 parts: Header, Payload, and Signature.*
> *The Payload contains the user's email, role, and expiry time.*
> *The Signature is created using HMAC-SHA256 with a secret key — it ensures no one can tamper with the token.*
>
> *This JWT is returned to React, which stores it in localStorage.*
> *For every protected API call, React sends this token in the Authorization header as a Bearer token.*
>
> *On the Spring Boot side, a filter called JwtAuthFilter — which extends OncePerRequestFilter — runs before every request.*
> *It extracts the token, validates the signature, checks expiry, and sets the user in Spring's SecurityContextHolder.*
>
> *We configured Spring Security with SessionCreationPolicy.STATELESS — which means the server creates no sessions.*
> *Every request is independent and self-contained — that's what makes JWT stateless and scalable."*

---

## 16. Last-Minute Revision Cheat Sheet

### 🔑 Must-Know Facts

```
JWT = JSON Web Token (RFC 7519)
3 parts = Header . Payload . Signature (dot separated)
Encoding = Base64URL (NOT encryption — anyone can decode)
Signature = HMACSHA256(header + payload, secretKey) — tamper detection only
Algorithm = HS256 (single secret key) or RS256 (public/private key pair)
Stateless = server stores NOTHING — JWT carries everything
Session policy = SessionCreationPolicy.STATELESS
JWT stored in React = localStorage (simple) or HttpOnly Cookie (secure)
JWT sent via = Authorization: Bearer <token>
401 = Invalid/missing/expired token
403 = Valid token, insufficient role
Filter class = JwtAuthFilter extends OncePerRequestFilter
User stored in = SecurityContextHolder after token validation
CSRF disabled = because JWT is sent in header, not cookies
BCrypt = for password hashing (never store plain text passwords)
```

---

### 📦 4 Key Spring Boot Classes

| Class | Job |
|---|---|
| **`JwtService`** | `generateToken()`, `extractEmail()`, `isTokenValid()`, `isTokenExpired()` |
| **`JwtAuthFilter`** | Extends `OncePerRequestFilter` — reads header, validates token, sets SecurityContext |
| **`SecurityConfig`** | Configures URL rules, disables CSRF, sets STATELESS, adds JwtAuthFilter |
| **`AuthController`** | `/login` endpoint — authenticates and returns JWT |

---

### ⚠️ Never Say These in an Interview

| ❌ Wrong | ✅ Correct |
|---|---|
| "JWT stores passwords" | JWT stores email, role, expiry — NEVER passwords |
| "JWT is encrypted" | JWT is Base64URL encoded — payload is readable |
| "JWT uses sessions" | JWT is stateless — it replaces sessions |
| "Server queries DB to validate JWT" | Signature is verified using the secret key — no DB query |
| "JWT can be revoked easily" | JWT cannot be revoked before expiry — use blacklist or refresh tokens |

---

### 🚀 JWT Flow Summary (3 lines)
```
1. Login   → Server verifies credentials → Generates JWT → Returns to client
2. Request → Client sends JWT in header → JwtAuthFilter validates → User set in SecurityContext
3. Invalid → Expired / tampered token → 401 Unauthorized returned
```

---

> 📌 Part of [Placement-Preparation-Hub](https://github.com/Omkar4112/Placement-Preparation-Hub)

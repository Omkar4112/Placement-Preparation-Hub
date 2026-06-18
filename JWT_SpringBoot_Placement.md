# 🔐 JWT Authentication — Placement Interview Guide
### For Freshers | Java + Spring Boot Focus | Interview-Ready in 30 Minutes

---

> 💡 **How to use this guide:**
> Read each section, memorize the 30-second answer, relate it to the analogy, and link it to your Spring Boot project.
> That's all an interviewer expects from a fresher.

---

## 📌 Table of Contents

1. [What is Authentication?](#1-what-is-authentication)
2. [What is Authorization?](#2-what-is-authorization)
3. [Authentication vs Authorization](#3-authentication-vs-authorization)
4. [What is JWT?](#4-what-is-jwt)
5. [Full Form of JWT](#5-full-form-of-jwt)
6. [Why JWT instead of Sessions?](#6-why-jwt-instead-of-sessions)
7. [Structure of JWT](#7-structure-of-jwt)
8. [JWT Login Flow — Step by Step](#8-jwt-login-flow--step-by-step)
9. [JWT Flow in a Spring Boot Project](#9-jwt-flow-in-a-spring-boot-project)
10. [JWT in React + Spring Boot Application](#10-jwt-in-react--spring-boot-application)
11. [Advantages of JWT](#11-advantages-of-jwt)
12. [Limitations of JWT](#12-limitations-of-jwt)
13. [Common Interview Q&A](#13-common-interview-qa)
14. [Top 10 Interview Questions](#14-top-10-interview-questions)
15. [1-Minute JWT Explanation](#15-1-minute-jwt-explanation-for-hrtech-rounds)
16. [Last-Minute Revision Points](#16-last-minute-revision-points-before-interview)

---

## 1. What is Authentication?

### ⏱️ 30-Second Interview Answer
> Authentication is the process of **verifying WHO you are**.
> When a user provides their username and password, the system checks if those credentials are valid.
> It answers the question: **"Are you really who you claim to be?"**

### 🌍 Real-World Analogy
> Think of showing your **Aadhaar card** at a hotel reception.
> The receptionist checks your ID to confirm you are who you say you are.
> That check is **Authentication**.

### 💻 Spring Boot Project Example
```java
// AuthController.java
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody LoginRequest request) {
    // 1. Check if user exists in DB
    // 2. Verify password using BCrypt
    // 3. If valid → issue JWT token
    authenticationManager.authenticate(
        new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
    );
    String token = jwtService.generateToken(request.getEmail());
    return ResponseEntity.ok(new AuthResponse(token));
}
```
> Here, `authenticationManager.authenticate()` is the **Authentication step** — it checks if the credentials are correct.

---

## 2. What is Authorization?

### ⏱️ 30-Second Interview Answer
> Authorization is the process of **verifying WHAT you are allowed to do**.
> Even after you are authenticated (logged in), the system checks if you have permission to access a specific resource.
> It answers the question: **"Are you allowed to do this?"**

### 🌍 Real-World Analogy
> After the hotel receptionist verifies your Aadhaar (Authentication),
> they give you a **room key card** that only opens your assigned room — not every room.
> That restriction is **Authorization**.

### 💻 Spring Boot Project Example
```java
// SecurityConfig.java
http.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/admin/**").hasRole("ADMIN")   // Only ADMIN can access
    .requestMatchers("/api/user/**").hasRole("USER")     // Only USER can access
    .requestMatchers("/api/auth/**").permitAll()         // Anyone can login/register
);
```
> Once the JWT is validated, Spring checks the user's **role** to decide if they can access the endpoint. That is **Authorization**.

---

## 3. Authentication vs Authorization

### ⏱️ 30-Second Interview Answer
> **Authentication** = Verifying identity → *Who are you?*
> **Authorization** = Verifying permissions → *What can you do?*
> Authentication always happens **first**, Authorization happens **after**.

### 📊 Comparison Table

| Feature | Authentication | Authorization |
|:--------|:--------------|:-------------|
| **Purpose** | Verify identity | Verify permissions |
| **Question** | Who are you? | What can you do? |
| **When** | First step (Login) | Second step (Access check) |
| **Example** | Username + Password check | Role-based access (ADMIN/USER) |
| **Failure result** | 401 Unauthorized | 403 Forbidden |
| **JWT relevance** | JWT is issued after auth | JWT carries roles for authz |

### 🌍 Real-World Analogy
> **Authentication** = Security guard checking your office ID card.
> **Authorization** = Your ID card only gives you access to your floor, not the server room.

---

## 4. What is JWT?

### ⏱️ 30-Second Interview Answer
> JWT (JSON Web Token) is a **compact, URL-safe token** used to securely transmit information between a client and a server.
> After login, the server generates a JWT containing the user's identity and roles.
> The client sends this token with every subsequent request, and the server validates it without needing to check a database every time.

### 🌍 Real-World Analogy
> JWT is like a **movie ticket with your name, seat, and show time printed on it**.
> The ticket itself proves you paid and tells the usher everything they need.
> They don't need to call the box office to verify — the ticket is **self-contained proof**.

### 💻 Spring Boot Project Example
> When a user logs in to your Spring Boot REST API, instead of creating a session on the server,
> you generate a JWT token like this:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGdtYWlsLmNvbSIsInJvbGUiOiJVU0VSIiwiaWF0IjoxNjAwMDAwMDAwfQ.abc123signature
```
> This token is returned to the React frontend, stored in `localStorage`, and sent with every API call.

---

## 5. Full Form of JWT

### ⏱️ 30-Second Interview Answer
> **JWT = JSON Web Token**
> - **JSON** → The data inside the token is in JSON format
> - **Web** → Designed for web-based communication
> - **Token** → It acts as a proof/credential
>
> It is defined by **RFC 7519** and is an open standard.

### 🌍 Real-World Analogy
> Like a **digital signed certificate** — it's in a readable format (JSON),
> travels over the web, and acts as your proof of identity (token).

---

## 6. Why JWT Instead of Sessions?

### ⏱️ 30-Second Interview Answer
> Traditional sessions store user data **on the server**. This doesn't scale well when you have multiple servers.
> JWT stores user data **inside the token itself**, so the server doesn't need to remember anything.
> JWT is **stateless** — any server can validate the token without shared memory.

### 📊 Session vs JWT Comparison

| Feature | Sessions | JWT |
|:--------|:---------|:----|
| **Storage** | Server-side (DB/Memory) | Client-side (localStorage/cookie) |
| **Stateful/Stateless** | Stateful | Stateless |
| **Scalability** | Poor (needs sticky sessions) | Excellent (any server validates) |
| **Mobile support** | Difficult (cookies) | Easy (Authorization header) |
| **Performance** | DB lookup per request | No DB lookup (self-contained) |
| **Logout** | Easy (delete session) | Hard (token lives until expiry) |

### 🌍 Real-World Analogy
> **Session** = Receptionist remembers your face every visit (they need a good memory / single person).
> **JWT** = You carry a signed visitor pass — any security guard at any entrance can verify it without calling reception.

### 💻 Spring Boot Project Example
> In a microservices Spring Boot project, if you have 3 instances of your app running on different servers,
> JWT works seamlessly because each server validates the token using the **same secret key**,
> without needing to share session data between servers.

---

## 7. Structure of JWT

### ⏱️ 30-Second Interview Answer
> A JWT has **3 parts** separated by dots (`.`):
> **Header.Payload.Signature**
> - **Header** → Algorithm and token type
> - **Payload** → User data (claims like username, role, expiry)
> - **Signature** → Ensures the token wasn't tampered with

```
xxxxx.yyyyy.zzzzz
  ↑      ↑      ↑
Header Payload Signature
```

---

### 7a. 📦 Header

> The Header is a **Base64URL-encoded JSON** describing the token type and signing algorithm.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

| Field | Meaning |
|:------|:--------|
| `alg` | Algorithm used for signing — `HS256` (HMAC-SHA256) is most common |
| `typ` | Token type — always `JWT` |

> **Base64URL encoded →** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9`

🌍 **Analogy:** The **envelope** that says "this is a letter, sealed using a wax stamp."

---

### 7b. 📋 Payload (Claims)

> The Payload contains **claims** — statements about the user and additional metadata.

```json
{
  "sub": "user@gmail.com",
  "role": "USER",
  "iat": 1700000000,
  "exp": 1700086400
}
```

| Claim | Full Form | Meaning |
|:------|:----------|:--------|
| `sub` | Subject | User identifier (email/username/userId) |
| `iat` | Issued At | When the token was created (Unix timestamp) |
| `exp` | Expiration | When the token expires |
| `role` | Custom claim | User's role (USER, ADMIN) |

> ⚠️ **Important:** Payload is only **Base64URL encoded, NOT encrypted.**
> Anyone can decode it. **Never put passwords or sensitive data here.**

🌍 **Analogy:** The **letter inside the envelope** — contains all the information, but anyone who opens it can read it.

---

### 7c. 🔏 Signature

> The Signature **verifies the token was not tampered with**.
> It is created by taking the encoded header + encoded payload and signing them with a **secret key**.

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secretKey
)
```

> The server holds the `secretKey`. When a token arrives, the server re-computes the signature and checks if it matches.
> If anyone modifies the payload, the signature won't match → **token rejected**.

🌍 **Analogy:** The **wax seal on the envelope** — if someone opens and reseals it, the seal breaks. Tampering is obvious.

### 💻 Spring Boot Example (JwtService.java)
```java
@Service
public class JwtService {

    private static final String SECRET_KEY = "mySecretKey123456789012345678901234"; // min 256-bit

    // Generate token
    public String generateToken(String username) {
        return Jwts.builder()
                .setSubject(username)
                .claim("role", "USER")
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 10)) // 10 hrs
                .signWith(getSignKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    // Validate token
    public boolean isTokenValid(String token, UserDetails userDetails) {
        final String username = extractUsername(token);
        return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
    }

    // Extract username from token
    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    private Key getSignKey() {
        byte[] keyBytes = Decoders.BASE64.decode(SECRET_KEY);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

---

## 8. JWT Login Flow — Step by Step

### ⏱️ 30-Second Interview Answer
> User sends credentials → Server verifies → Server generates JWT → Client stores token →
> Client sends token in every request → Server validates token → Access granted/denied.

### 🔄 Complete Flow Diagram

```
┌──────────┐          ┌──────────────┐          ┌──────────┐
│  CLIENT  │          │    SERVER    │          │    DB    │
│ (React)  │          │ (Spring Boot)│          │(MySQL)   │
└────┬─────┘          └──────┬───────┘          └────┬─────┘
     │                       │                       │
     │  1. POST /login        │                       │
     │  {email, password}     │                       │
     │──────────────────────► │                       │
     │                       │  2. Find user by email │
     │                       │───────────────────────►│
     │                       │  3. Return user data   │
     │                       │◄───────────────────────│
     │                       │  4. Verify BCrypt pwd  │
     │                       │  5. Generate JWT       │
     │  6. Return JWT token   │                       │
     │◄──────────────────────│                       │
     │                       │                       │
     │  7. Store JWT in       │                       │
     │     localStorage       │                       │
     │                       │                       │
     │  8. GET /api/profile   │                       │
     │  Header: Bearer <JWT>  │                       │
     │──────────────────────► │                       │
     │                       │  9. Extract token      │
     │                       │  10. Validate signature│
     │                       │  11. Check expiry      │
     │                       │  12. Check role/access │
     │  13. Return data       │                       │
     │◄──────────────────────│                       │
     │                       │                       │
```

### 📋 Step-by-Step Explanation

| Step | What Happens |
|:-----|:------------|
| **1** | User enters email + password → React sends POST `/api/auth/login` |
| **2** | Spring Boot controller receives request |
| **3** | `AuthenticationManager` verifies credentials against DB |
| **4** | If valid, `JwtService.generateToken()` creates a signed JWT |
| **5** | JWT returned in the response body |
| **6** | React stores JWT in `localStorage` or `sessionStorage` |
| **7** | For every protected API call, React adds `Authorization: Bearer <token>` header |
| **8** | Spring Boot `JwtAuthFilter` intercepts the request |
| **9** | Filter extracts and validates the token (signature + expiry) |
| **10** | If valid, sets user in `SecurityContext` |
| **11** | Request reaches controller — user is authenticated + authorized |

---

## 9. JWT Flow in a Spring Boot Project

### ⏱️ 30-Second Interview Answer
> In Spring Boot, JWT is implemented using Spring Security.
> A custom filter (`JwtAuthFilter`) intercepts every request, extracts the token,
> validates it using a `JwtService`, and sets the authenticated user into `SecurityContextHolder`.

### 🏗️ Project File Structure

```
src/
├── config/
│   └── SecurityConfig.java          ← Spring Security configuration
├── controller/
│   └── AuthController.java          ← /login and /register endpoints
├── filter/
│   └── JwtAuthFilter.java           ← Intercepts every request, validates JWT
├── service/
│   ├── JwtService.java              ← Token generation & validation logic
│   └── UserDetailsServiceImpl.java  ← Loads user from DB
├── model/
│   └── User.java                    ← User entity
└── repository/
    └── UserRepository.java          ← DB access
```

### 💻 Key Code Files

#### 🔹 JwtAuthFilter.java
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
                                    FilterChain filterChain) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");

        // 1. Extract token from "Bearer <token>"
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        String token = authHeader.substring(7); // Remove "Bearer "
        String username = jwtService.extractUsername(token);

        // 2. Validate token and set authentication
        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);

            if (jwtService.isTokenValid(token, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(userDetails, null, userDetails.getAuthorities());
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        filterChain.doFilter(request, response); // Continue to next filter/controller
    }
}
```

#### 🔹 SecurityConfig.java
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Autowired
    private JwtAuthFilter jwtAuthFilter;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(sess -> sess.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }

    @Bean
    public AuthenticationManager authenticationManager(AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

#### 🔹 AuthController.java
```java
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtService jwtService;

    @Autowired
    private UserDetailsServiceImpl userDetailsService;

    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest request) {
        authenticationManager.authenticate(
            new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );
        String token = jwtService.generateToken(request.getEmail());
        return ResponseEntity.ok(Map.of("token", token));
    }
}
```

### 🔁 Request Processing Order in Spring Boot
```
HTTP Request
     ↓
JwtAuthFilter           ← Extracts + Validates JWT
     ↓
SecurityContextHolder   ← User identity stored here
     ↓
DispatcherServlet
     ↓
Controller Method       ← Handles business logic
     ↓
HTTP Response
```

---

## 10. JWT in React + Spring Boot Application

### ⏱️ 30-Second Interview Answer
> In our React + Spring Boot project, React sends login credentials to the Spring Boot REST API.
> The API validates credentials and returns a JWT.
> React stores the JWT in `localStorage` and sends it as a `Bearer` token in the `Authorization` header for every protected API call.

### 💻 React Side Implementation

#### 🔹 Login API Call (api.js / authService.js)
```javascript
// Login function — calls Spring Boot backend
export const loginUser = async (email, password) => {
    const response = await fetch('http://localhost:8080/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem('token', data.token); // Store JWT
        return data.token;
    } else {
        throw new Error(data.message || 'Login failed');
    }
};
```

#### 🔹 Protected API Call with JWT Header
```javascript
// Fetch user profile — sends JWT in header
export const getUserProfile = async () => {
    const token = localStorage.getItem('token'); // Retrieve JWT

    const response = await fetch('http://localhost:8080/api/user/profile', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,  // Attach JWT
            'Content-Type': 'application/json'
        }
    });

    return response.json();
};
```

#### 🔹 Logout
```javascript
export const logout = () => {
    localStorage.removeItem('token'); // Simply remove JWT
    window.location.href = '/login';
};
```

### 🌍 Real-World Analogy
> React = The **customer** at a restaurant.
> Spring Boot = The **kitchen** that prepares food.
> JWT = The **order token** given when you place an order.
> Every time you ask for extra sauce (protected API), you show your order token.
> Kitchen verifies the token and serves you — no need to place the full order again.

---

## 11. Advantages of JWT

### ⏱️ 30-Second Interview Answer
> JWT is stateless, scalable, and self-contained.
> The server doesn't need to store session data, making it perfect for microservices and mobile apps.

| Advantage | Explanation |
|:----------|:-----------|
| ✅ **Stateless** | Server doesn't store sessions — scales easily |
| ✅ **Self-contained** | Token carries all user info — no DB lookup per request |
| ✅ **Cross-domain** | Works across different domains (unlike cookies) |
| ✅ **Mobile-friendly** | Easy to send in HTTP headers from mobile apps |
| ✅ **Microservices** | Any service can validate the token with the shared secret |
| ✅ **Performance** | No session DB query on every request |
| ✅ **Standard** | Open standard (RFC 7519) — supported by all languages |

---

## 12. Limitations of JWT

### ⏱️ 30-Second Interview Answer
> The biggest limitation is that JWT tokens **cannot be invalidated before they expire**.
> If a token is stolen, it remains valid until expiry.
> Also, the payload is Base64 encoded, not encrypted — so sensitive data should never be stored in it.

| Limitation | Explanation |
|:-----------|:-----------|
| ❌ **Cannot revoke** | Once issued, token is valid until expiry (logout doesn't invalidate it) |
| ❌ **Token theft** | If stored in localStorage, vulnerable to XSS attacks |
| ❌ **Not encrypted** | Payload is only encoded — anyone can read it |
| ❌ **Large size** | JWT is bigger than session ID — increases request size |
| ❌ **Expiry management** | Short expiry = frequent re-login; Long expiry = security risk |
| ❌ **Secret key risk** | If secret key leaks, all tokens can be forged |

### 💡 How to Handle These in Interviews
> **"How do you handle logout with JWT?"**
> → Maintain a **token blacklist** in Redis with short TTL.
> Or use **short-lived access tokens (15 min) + refresh tokens (7 days)**.

---

## 13. Common Interview Q&A

### Q1: What happens if the JWT secret key is compromised?
> **Answer:** All existing tokens can be forged and are considered compromised.
> The solution is to **immediately rotate the secret key** — this invalidates all existing tokens and forces all users to log in again.

---

### Q2: Where should JWT be stored on the client side?
> **Answer:** Two options:
> - **localStorage** → Easier but vulnerable to **XSS attacks**
> - **HttpOnly Cookie** → More secure (not accessible via JavaScript), but vulnerable to **CSRF**
>
> For interviews: *"We stored in localStorage for simplicity in our project, but in production, HttpOnly cookies are recommended."*

---

### Q3: What is the difference between `iat` and `exp` in JWT?
> **Answer:**
> - `iat` (Issued At) → Unix timestamp when the token was created
> - `exp` (Expiration) → Unix timestamp when the token expires
> Both are standard JWT claims in the payload.

---

### Q4: What is a Refresh Token?
> **Answer:** A **Refresh Token** is a long-lived token (e.g., 7 days) used to get a new Access Token when the short-lived one (e.g., 15 min) expires.
> The user doesn't need to log in again — the refresh token is silently used to get a new access token.

```
Access Token:  expires in 15 minutes  (used for API calls)
Refresh Token: expires in 7 days       (used to renew access token)
```

---

### Q5: What HTTP status codes relate to JWT?
| Status | Meaning | When |
|:-------|:--------|:-----|
| **200** | OK | Valid token, access granted |
| **401** | Unauthorized | Token missing or invalid |
| **403** | Forbidden | Valid token but insufficient role |

---

### Q6: Is JWT encrypted?
> **Answer:** **No, JWT is NOT encrypted by default.**
> The header and payload are only **Base64URL encoded** (easily decoded).
> The **signature** ensures integrity (not tampered), not confidentiality.
> If encryption is needed, use **JWE (JSON Web Encryption)**.

---

### Q7: What algorithm does JWT commonly use?
> **Answer:** **HS256 (HMAC SHA-256)** is most commonly used.
> It uses a **single shared secret key** for both signing and verification.
> **RS256 (RSA)** uses a **public/private key pair** and is used in distributed systems.

---

### Q8: What is `SessionCreationPolicy.STATELESS` in Spring Security?
> **Answer:** It tells Spring Security to **never create or use HTTP sessions**.
> Since JWT is stateless, we don't need sessions.
> This is configured in `SecurityConfig` to ensure every request must carry a valid JWT.

---

### Q9: How does the server validate a JWT without hitting the database?
> **Answer:** The server re-computes the HMAC signature using the stored secret key and the received header + payload.
> If the computed signature matches the token's signature, the token is valid.
> This requires **no database query** — pure cryptographic verification.

---

### Q10: What is `OncePerRequestFilter`?
> **Answer:** `OncePerRequestFilter` is a Spring Security base class that **guarantees the filter executes exactly once per HTTP request**.
> Our `JwtAuthFilter` extends it to intercept every request, extract the JWT, and authenticate the user before the request reaches the controller.

---

## 14. Top 10 Interview Questions

| # | Question |
|:--|:---------|
| 1 | What is JWT and why is it used? |
| 2 | Explain the 3 parts of a JWT. |
| 3 | What is the difference between Authentication and Authorization? |
| 4 | Why is JWT preferred over sessions in REST APIs? |
| 5 | How do you implement JWT in Spring Boot? Name the key classes. |
| 6 | What is `JwtAuthFilter` and how does it work? |
| 7 | How do you handle JWT expiry and logout? |
| 8 | Where is JWT stored on the React/frontend side? What are the risks? |
| 9 | What is a Refresh Token? How is it different from an Access Token? |
| 10 | What HTTP status codes are returned for invalid or missing JWT? |

---

## 15. 1-Minute JWT Explanation for HR/Tech Rounds

> *Use this when asked: "Tell me about JWT" or "How did authentication work in your project?"*

---

> **"In our React + Spring Boot project, we implemented JWT-based authentication.**
>
> **When a user logs in, the Spring Boot backend verifies the username and password against the database.**
> **If valid, it generates a JWT token — a digitally signed string containing the user's email and role.**
> **This token is sent back to the React frontend, which stores it in localStorage.**
>
> **For every subsequent API call — like fetching the dashboard or user profile — React sends this JWT in the `Authorization` header as a Bearer token.**
>
> **On the server side, a custom filter called `JwtAuthFilter` intercepts every request.**
> **It extracts the token, validates the signature, checks if it's expired, and if everything is fine, sets the user in the Spring Security context.**
> **Based on the user's role, access to protected endpoints is granted or denied.**
>
> **JWT made our application stateless — the server doesn't store session data, making it scalable and suitable for REST APIs."**

---

## 16. Last-Minute Revision Points Before Interview

### 🎯 Must-Remember Facts

```
JWT = JSON Web Token (RFC 7519)
Structure = Header.Payload.Signature (Base64URL.Base64URL.Signature)
Algorithm = HS256 (HMAC SHA-256) — most common
Storage = localStorage (simple) / HttpOnly Cookie (secure)
Header sent as = Authorization: Bearer <token>
Filter class = JwtAuthFilter extends OncePerRequestFilter
Stateless = SessionCreationPolicy.STATELESS in SecurityConfig
```

### 🔑 Key Classes in Spring Boot JWT Implementation

| Class | Role |
|:------|:-----|
| `JwtService` | Generates and validates JWT tokens |
| `JwtAuthFilter` | Intercepts requests, extracts and validates token |
| `SecurityConfig` | Configures security rules, filter chain, CORS |
| `AuthController` | Handles `/login` and `/register` endpoints |
| `UserDetailsServiceImpl` | Loads user from DB by username |
| `AuthenticationManager` | Verifies username + password |

### ⚡ Quick Cheat Sheet

| Concept | One-line Answer |
|:--------|:---------------|
| JWT stands for | JSON Web Token |
| JWT parts | Header, Payload, Signature |
| Payload encrypted? | No — only Base64 encoded |
| Stateful or Stateless? | Stateless |
| Token stored where? | Client side (localStorage/cookie) |
| Invalid JWT response | 401 Unauthorized |
| Insufficient role response | 403 Forbidden |
| Can JWT be revoked? | Not directly — use token blacklist or refresh tokens |
| Common algorithm | HS256 |
| Spring filter class | `OncePerRequestFilter` |

### 🚨 Red Flags (Never Say These in Interviews)

- ❌ "JWT stores passwords" → **No! Never store sensitive data in JWT payload**
- ❌ "JWT is encrypted" → **No! It is encoded, not encrypted**
- ❌ "We use sessions with JWT" → **No! JWT replaces sessions — it is stateless**
- ❌ "JWT validates against the database" → **No! Signature is validated cryptographically**

---

> 📌 **Created for Placement Preparation | Spring Boot + React + JWT | Interview-Ready Guide**
> 🔗 Part of: [Placement-Preparation-Hub](https://github.com/Omkar4112/Placement-Preparation-Hub)

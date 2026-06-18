# 🔐 JWT Authentication — Interview Guide
> Simple | Correct | Spring Boot Focused | 30-Minute Read

---

## 1. What is Authentication?

**Simple answer:**
Authentication means **"Prove who you are"**.

When you enter your username and password, the system checks — *"Is this a real user?"*

**Analogy:**
> Showing your Aadhaar card at a hotel reception.
> The guard checks your ID → that's Authentication.

**In Spring Boot:**
```java
authenticationManager.authenticate(
    new UsernamePasswordAuthenticationToken(email, password)
);
```
This one line checks if the email + password match in the database.

---

## 2. What is Authorization?

**Simple answer:**
Authorization means **"What are you allowed to do?"**

After you log in, the system checks — *"Can this user access this page/API?"*

**Analogy:**
> Your Aadhaar card got you into the hotel.
> But your room key only opens **your room**, not every room.
> That restriction → Authorization.

**In Spring Boot:**
```java
.requestMatchers("/api/admin/**").hasRole("ADMIN")
.requestMatchers("/api/user/**").hasRole("USER")
```
Even after login, only ADMIN can access admin APIs.

---

## 3. Authentication vs Authorization — Key Difference

| | Authentication | Authorization |
|---|---|---|
| **Meaning** | Who are you? | What can you do? |
| **When** | At Login | After Login |
| **Failure code** | 401 Unauthorized | 403 Forbidden |
| **Example** | Checking email + password | Checking if user is ADMIN |

> 💡 **Authentication happens first, Authorization happens second.**

---

## 4. What is JWT?

**Simple answer:**
JWT is a **token** (a special string) that the server gives you after login.

You carry this token and show it every time you access a protected page.
The server reads the token and knows **who you are** — without checking the database again.

**Analogy:**
> Think of a **movie ticket**.
> After buying it, you don't go back to the counter before entering the hall.
> You just show the ticket → they verify it → you enter.
> JWT works the same way.

---

## 5. Full Form of JWT

> **JWT = JSON Web Token**

- **JSON** → Data inside is in JSON format
- **Web** → Used for web communication
- **Token** → Acts as your proof/credential

---

## 6. Why JWT Instead of Sessions?

**Old way (Sessions):**
- User logs in → server creates a session and stores it in memory/DB
- Every request → server checks the session in DB
- Problem: If you have 3 servers, they all need to share session data

**New way (JWT):**
- User logs in → server creates a JWT and sends it to the client
- Every request → client sends the JWT → server just reads it (no DB needed)
- Works on any server — no sharing needed

**Analogy:**
> **Session** = Waiter remembers your order in his head (needs same waiter every time)
> **JWT** = You carry a printed receipt (any waiter can serve you)

| | Session | JWT |
|---|---|---|
| Stored where? | Server (DB/Memory) | Client (browser/app) |
| Scales easily? | ❌ No | ✅ Yes |
| DB hit per request? | ✅ Yes | ❌ No |
| Good for REST APIs? | ❌ No | ✅ Yes |

---

## 7. Structure of JWT

A JWT looks like this:

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyQGdtYWlsLmNvbSJ9.abc123xyz
        ↑                        ↑                            ↑
     HEADER                   PAYLOAD                    SIGNATURE
```

**It has 3 parts, separated by dots (`.`)**

---

### Part 1 — Header
Tells what type of token and which algorithm was used.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
- `alg` → Algorithm used to sign (HS256 is most common)
- `typ` → Always JWT

---

### Part 2 — Payload
Contains **user information** (called "claims").

```json
{
  "sub": "user@gmail.com",
  "role": "USER",
  "iat": 1700000000,
  "exp": 1700086400
}
```
- `sub` → Subject = who this token belongs to (usually email or userId)
- `role` → User's role (USER, ADMIN)
- `iat` → Issued At = when token was created
- `exp` → Expiry = when token becomes invalid

> ⚠️ **Important:** Payload is NOT encrypted. Anyone can decode and read it.
> **Never store passwords here.**

---

### Part 3 — Signature
This is the **security part**. It ensures no one has tampered with the token.

```
Signature = HMAC_SHA256(header + "." + payload, secretKey)
```

The server signs the token with a **secret key**.
If anyone changes the payload, the signature won't match → token rejected.

**Analogy:**
> Like a **wax seal on a letter**.
> If someone opens and re-seals it, the seal looks broken.
> Server detects tampering immediately.

---

## 8. JWT Login Flow — Step by Step

```
Step 1: User types email + password → clicks Login

Step 2: React sends POST request to /api/auth/login

Step 3: Spring Boot checks credentials in DB

Step 4: If correct → Spring Boot generates a JWT token

Step 5: JWT sent back to React

Step 6: React stores JWT in localStorage

Step 7: User clicks "View Profile" → React sends GET /api/user/profile
        with header:  Authorization: Bearer <JWT token>

Step 8: Spring Boot reads the token → checks signature → checks expiry

Step 9: If valid → returns user data
        If invalid → returns 401 Unauthorized
```

---

## 9. JWT in Spring Boot — Key Classes

You need to know these 4 things for interviews:

### 1. JwtService.java — Creates and reads tokens
```java
// Generate token after login
public String generateToken(String email) {
    return Jwts.builder()
        .setSubject(email)
        .claim("role", "USER")
        .setIssuedAt(new Date())
        .setExpiration(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 10)) // 10 hours
        .signWith(secretKey, SignatureAlgorithm.HS256)
        .compact();
}

// Read email from token
public String extractEmail(String token) {
    return Jwts.parserBuilder()
        .setSigningKey(secretKey)
        .build()
        .parseClaimsJws(token)
        .getBody()
        .getSubject();
}
```

---

### 2. JwtAuthFilter.java — Intercepts every request
```java
// This runs before every API call
@Override
protected void doFilterInternal(HttpServletRequest request,
                                HttpServletResponse response,
                                FilterChain filterChain) throws ServletException, IOException {

    String authHeader = request.getHeader("Authorization");

    // If no token → skip (let Spring Security handle 401)
    if (authHeader == null || !authHeader.startsWith("Bearer ")) {
        filterChain.doFilter(request, response);
        return;
    }

    String token = authHeader.substring(7); // Remove "Bearer " prefix
    String email = jwtService.extractEmail(token);

    // Validate and set user in Spring Security
    if (email != null) {
        UserDetails user = userDetailsService.loadUserByUsername(email);
        if (jwtService.isTokenValid(token, user)) {
            UsernamePasswordAuthenticationToken authToken =
                new UsernamePasswordAuthenticationToken(user, null, user.getAuthorities());
            SecurityContextHolder.getContext().setAuthentication(authToken);
        }
    }

    filterChain.doFilter(request, response);
}
```

---

### 3. SecurityConfig.java — Security rules
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf.disable())                          // Disable CSRF (we use JWT)
        .sessionManagement(sess ->
            sess.sessionCreationPolicy(SessionCreationPolicy.STATELESS)) // No sessions
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/api/auth/**").permitAll()       // Login/Register = open
            .anyRequest().authenticated()                      // Everything else = needs JWT
        )
        .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class);

    return http.build();
}
```

---

### 4. AuthController.java — Login endpoint
```java
@PostMapping("/login")
public ResponseEntity<?> login(@RequestBody LoginRequest request) {
    // 1. Verify credentials
    authenticationManager.authenticate(
        new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
    );
    // 2. Generate and return token
    String token = jwtService.generateToken(request.getEmail());
    return ResponseEntity.ok(Map.of("token", token));
}
```

---

## 10. JWT in React + Spring Boot Project

### How React uses the token:

**After Login — save the token:**
```javascript
const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
});
const data = await response.json();
localStorage.setItem('token', data.token); // Save JWT
```

**For every protected API call — send the token:**
```javascript
const token = localStorage.getItem('token');
const response = await fetch('/api/user/profile', {
    headers: { 'Authorization': `Bearer ${token}` }  // Send JWT
});
```

**Logout — just remove the token:**
```javascript
localStorage.removeItem('token');
```

---

## 11. Advantages of JWT

| Advantage | Why it matters |
|---|---|
| ✅ No DB hit per request | Fast — server just reads the token |
| ✅ Stateless | Works with multiple servers, microservices |
| ✅ Works on mobile | Easy to send in HTTP headers |
| ✅ Self-contained | Token has everything — no extra lookup |
| ✅ Standard format | Supported in every programming language |

---

## 12. Limitations of JWT

| Limitation | Simple explanation |
|---|---|
| ❌ Can't invalidate before expiry | Even after logout, token works until it expires |
| ❌ Payload is readable | Don't store passwords or private data |
| ❌ If secret key leaks, all tokens compromised | Keep the key safe (use env variables) |
| ❌ Token gets bigger over time | More claims = bigger token = more data per request |

> 💡 **Interview tip:** When asked about logout —
> *"We use short-lived tokens (15–60 min). For proper logout, a token blacklist in Redis can be used."*

---

## 13. Common Interview Questions & Answers

**Q: What is JWT?**
> JWT is a token issued by the server after login. It contains user info (like email and role) in a signed format. The client sends it with every request, and the server validates it without hitting the database.

---

**Q: What are the 3 parts of JWT?**
> Header (algorithm info) → Payload (user data) → Signature (tamper proof)

---

**Q: Is JWT encrypted?**
> No. JWT is only **encoded** (Base64URL), not encrypted. Anyone can decode the payload. The **signature** only verifies it wasn't changed — it doesn't hide the data.

---

**Q: Why use JWT instead of sessions?**
> Sessions store data on the server — hard to scale. JWT stores data in the token itself on the client — the server needs nothing. Any server can validate it using just the secret key.

---

**Q: What happens when a JWT expires?**
> The server returns **401 Unauthorized**. The user must log in again. To avoid frequent logins, we can use a **Refresh Token** strategy.

---

**Q: What is a Refresh Token?**
> A Refresh Token is a separate long-lived token (e.g., 7 days). When the Access Token (15 min) expires, the client uses the Refresh Token to get a new Access Token silently — without asking the user to log in again.

---

**Q: What is `OncePerRequestFilter`?**
> It's a Spring class. Our `JwtAuthFilter` extends it. It ensures our JWT validation logic runs **exactly once per HTTP request** — not multiple times.

---

**Q: What is `SessionCreationPolicy.STATELESS`?**
> It tells Spring Security to never create or use HTTP sessions. Since JWT is stateless, we don't need sessions at all.

---

**Q: What is 401 vs 403?**
> `401 Unauthorized` = Token is missing, expired, or invalid — user is not authenticated.
> `403 Forbidden` = Token is valid, but user doesn't have permission (wrong role).

---

**Q: Where do you store JWT in React?**
> In `localStorage`. It's simple but vulnerable to XSS. In production, `HttpOnly cookies` are more secure.

---

## 14. Top 10 Interview Questions — Quick List

```
1.  What is JWT? What does it stand for?
2.  What are the 3 parts of a JWT?
3.  Is JWT encrypted or just encoded?
4.  Difference between Authentication and Authorization?
5.  Why JWT over sessions in REST APIs?
6.  How does JwtAuthFilter work in Spring Boot?
7.  What is OncePerRequestFilter?
8.  What is SessionCreationPolicy.STATELESS?
9.  How do you handle logout with JWT?
10. What is a Refresh Token?
```

---

## 15. 1-Minute JWT Explanation (Say This in Interviews)

> *"In our React + Spring Boot project, we used JWT for authentication.*
>
> *When a user logs in, the Spring Boot backend checks the credentials.*
> *If valid, it generates a JWT token — which contains the user's email and role — and sends it to React.*
>
> *React stores this token in localStorage.*
> *For every protected API call, React sends this token in the Authorization header as a Bearer token.*
>
> *On the Spring Boot side, a filter called JwtAuthFilter intercepts every request.*
> *It extracts the token, validates the signature, checks expiry, and sets the user in the SecurityContext.*
>
> *This makes our app stateless — no session storage — and it scales well for REST APIs."*

---

## 16. Last-Minute Revision

### 🔑 Must-Know Facts

```
JWT = JSON Web Token
Parts = Header . Payload . Signature
Payload = NOT encrypted (anyone can read)
Signature = tamper detection only
Algorithm = HS256 (most common)
Stored in React = localStorage
Sent in header = Authorization: Bearer <token>
401 = Invalid/missing token
403 = Valid token, wrong role
Spring filter = JwtAuthFilter extends OncePerRequestFilter
Spring config = SessionCreationPolicy.STATELESS
```

### 📦 4 Key Spring Boot Classes

| Class | Job |
|---|---|
| `JwtService` | Create token, extract email, validate token |
| `JwtAuthFilter` | Run before every request, validate JWT |
| `SecurityConfig` | Define which URLs need JWT |
| `AuthController` | `/login` endpoint — returns the JWT |

### ❌ Never Say These

- "JWT stores password" → **Wrong. Never store passwords in JWT**
- "JWT is encrypted" → **Wrong. It's only encoded**
- "JWT uses sessions" → **Wrong. JWT replaces sessions**
- "Server queries DB to validate JWT" → **Wrong. Signature is verified cryptographically**

---

> 📌 Part of [Placement-Preparation-Hub](https://github.com/Omkar4112/Placement-Preparation-Hub)

# MODULE 9: Deployment & DevOps
## VigilAI MedLink — From Local Development to Production

---

> [!NOTE]
> This module teaches you how to take VigilAI from your laptop to a real production server accessible anywhere in the world.

---

## 🐳 Docker — Containerization

### What is Docker?

**The Problem Without Docker:**
```
Works on my machine!
- Developer A: Java 17, PostgreSQL 15
- Developer B: Java 11, PostgreSQL 14
- Production: Java 21, PostgreSQL 16
→ Different versions = different behavior = bugs

With Docker:
- Packages the app + its exact environment into a container
- Container runs identically on any machine
- "Build once, run anywhere"
```

**Analogy:** Docker is like a shipping container. Instead of wondering if the cargo will fit different ships/trucks, you pack everything into a standardized container that any transport can carry.

### Docker Concepts:

| Concept | Description | VigilAI Example |
|---------|-------------|-----------------|
| **Image** | Read-only template (like a blueprint) | `postgres:16-alpine` |
| **Container** | Running instance of an image | `vigilai-db` (running Postgres) |
| **Dockerfile** | Instructions to build a custom image | `backend/Dockerfile` |
| **Volume** | Persistent storage outside container | `postgres_data` |
| **Network** | Virtual network connecting containers | docker-compose default network |
| **Port mapping** | `host:container` port binding | `"8080:8080"` |

---

## 📄 Dockerfile Analysis

### Backend Dockerfile:
```dockerfile
# Use a two-stage build (best practice for Java)

# Stage 1: BUILD (has JDK + Maven — large)
FROM maven:3.9-eclipse-temurin-17-alpine AS build
WORKDIR /app

# Copy only pom.xml first (takes advantage of Docker layer caching)
COPY pom.xml .
# Download all dependencies (this layer is cached if pom.xml hasn't changed)
RUN mvn dependency:go-offline

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests
# -DskipTests = don't run tests during Docker build (speeds up build)
# Result: target/vigilai-backend-2.0.0.jar

# Stage 2: RUNTIME (has only JRE — smaller)
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Copy ONLY the JAR from the build stage (not Maven, not source code)
COPY --from=build /app/target/vigilai-backend-*.jar app.jar

# Non-root user for security:
RUN addgroup -S vigilai && adduser -S vigilai -G vigilai
USER vigilai

EXPOSE 8080

# Start the Spring Boot app:
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Why Two-Stage Build?**
- Stage 1 image: ~600MB (JDK + Maven + source code)
- Stage 2 image: ~150MB (JRE + JAR only)
- Production only ships the small Stage 2 image

### AI Service Dockerfile:
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies first (cached if requirements.txt unchanged)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

# Start FastAPI with Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# "0.0.0.0" = listen on all interfaces (accessible from other containers)
```

---

## 🔧 Environment Variables — Secrets Management

**The Golden Rule:** Never hardcode secrets in source code. Use environment variables.

### Why Environment Variables?

```
Scenario A (BAD — in docker-compose.yml):
  JWT_SECRET: "my-super-secret-key-hardcoded"
  → If someone forks your GitHub repo → they have your secret!
  → Anyone with database access → they have your production password!

Scenario B (GOOD — environment variables):
  JWT_SECRET: ${JWT_SECRET}
  → Actual value set in deployment platform, never in code
  → GitHub sees: ${JWT_SECRET} (harmless placeholder)
  → Production sees: "xK9#mN2@pL8..." (real secret)
```

### How Spring Boot Reads Them:

```properties
# application.properties — safe to commit:
spring.datasource.url=${SPRING_DATASOURCE_URL:jdbc:postgresql://localhost:5432/vigilai}
# Format: ${VARIABLE_NAME:default_if_not_set}

vigilai.jwt.secret=${JWT_SECRET:dev_secret_min_32_chars_long_!!!}
# In development: uses the default (dev_secret...)
# In production: uses the actual JWT_SECRET environment variable
```

```java
// Reading in Java code:
@Value("${vigilai.jwt.secret}")
private String secret;
// Spring reads from application.properties, which reads from environment variable
```

### Setting Environment Variables in Docker Compose:

```yaml
# docker-compose.yml — for local development:
backend:
  environment:
    SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/vigilai
    SPRING_DATASOURCE_USERNAME: postgres
    SPRING_DATASOURCE_PASSWORD: OMKAR@111  # ⚠️ OK for local dev only!
    JWT_SECRET: vigilai_dev_secret_key_min_32_chars_long
    AI_SERVICE_URL: http://ai-service:8000/predict
    LLM_SERVICE_URL: http://ai-service:8000/explain
    SPRING_JPA_HIBERNATE_DDL_AUTO: update
```

### Setting Environment Variables for Production (Render.com):

```
Dashboard → Select Service → Environment → Add Environment Variable
  SPRING_DATASOURCE_URL = jdbc:postgresql://external-host:5432/vigilai
  SPRING_DATASOURCE_PASSWORD = [a strong random password]
  JWT_SECRET = [64+ character random string]
```

---

## 🏗️ Build Process

### Java Build (Maven):

```bash
# Clean + compile + package:
mvn clean package
# clean: delete previous build artifacts
# package: compile, run tests, create JAR

# Skip tests (faster):
mvn clean package -DskipTests

# Run locally (without Docker):
java -jar target/vigilai-backend-2.0.0.jar

# The Spring Boot JAR is "fat" — it contains:
# - Your compiled classes
# - All dependencies (Spring, Jackson, JPA, etc.)
# - Embedded Tomcat server
# - Everything needed to run (no external server needed!)
```

### Python Build (pip):

```bash
# Install dependencies:
pip install -r requirements.txt

# Run locally:
uvicorn app.main:app --reload --port 8000
# --reload = auto-restart when code changes (development only)

# Run in production:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
# --workers 4 = 4 processes for handling concurrent requests
```

---

## 🌐 Docker Compose — Orchestrating All Services

### Starting the Complete Stack:

```bash
# Start all 4 services:
docker-compose up

# Start in background (detached mode):
docker-compose up -d

# Start with rebuild (after code changes):
docker-compose up --build

# Stop all services:
docker-compose down

# Stop and delete volumes (clears database!):
docker-compose down -v
```

### Checking Service Status:

```bash
# View running containers:
docker ps
# Output:
# CONTAINER ID   IMAGE          PORTS                    STATUS
# abc123         vigilai-backend 0.0.0.0:8080->8080/tcp  Up (healthy)
# def456         vigilai-ai      0.0.0.0:8000->8000/tcp  Up (healthy)
# ghi789         postgres:16     0.0.0.0:5432->5432/tcp  Up (healthy)
# jkl012         nginx:alpine    0.0.0.0:3000->80/tcp    Up

# View logs from all services:
docker-compose logs

# View logs from specific service:
docker-compose logs backend -f    # -f = follow (live)
docker-compose logs ai-service
docker-compose logs postgres

# Shell into a container:
docker exec -it vigilai-backend /bin/sh
docker exec -it vigilai-db psql -U postgres -d vigilai
```

### Health Checks (from docker-compose.yml):

```yaml
# Backend health check:
healthcheck:
  test: ["CMD-SHELL", "wget --quiet --tries=1 --spider http://localhost:8080/health || exit 1"]
  interval: 10s   # check every 10 seconds
  timeout: 5s     # fail if no response in 5 seconds
  retries: 5      # mark unhealthy after 5 failures

# AI service health check:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 10s
  retries: 5

# Backend depends_on ai-service with condition: service_healthy
# This means backend won't start until AI service health check passes!
```

---

## ☁️ Production Deployment — Render.com

Render.com is where the live VigilAI demo is deployed. It's a Platform as a Service (PaaS).

### Render.com Architecture:

```
Internet
    │
    ▼
Render Load Balancer (HTTPS termination)
    │
    ├── vigilai-backend (Web Service, Java)
    │   Port: 8080 (internally)
    │   URL: https://backend-ysf3.onrender.com
    │
    ├── vigilai-ai (Web Service, Python)
    │   Port: 8000 (internally)
    │   URL: https://ai-service-xxx.onrender.com
    │
    ├── vigilai-frontend (Static Site)
    │   Serves: login.html, clinic.html, etc.
    │   URL: https://vigilai.onrender.com
    │
    └── PostgreSQL (Managed Database)
        External URL: postgres://user:pass@host:5432/vigilai
```

### Why the "Server Waking Up" Delay?

```javascript
// In login.html:
btn.textContent = 'Waking up Free Tier Server (takes ~50s)…';
```

Render.com's free tier **spins down** services after 15 minutes of inactivity to save resources. When the first request arrives, the container must restart — which takes up to 50 seconds for a Spring Boot app.

**The pre-warming trick:**
```javascript
// login.html runs this IMMEDIATELY on page load (before user types anything):
(async () => {
    await fetch(`${API}/health`);  // This wakes up the server!
    // By the time user types email/password (~10 seconds), server is ready
})();
```

### Deployment Steps on Render.com:

```
1. Push code to GitHub

2. Create services on render.com:

   Service 1: PostgreSQL Database
   - Type: PostgreSQL
   - Name: vigilai-db
   - Plan: Free
   - Note the connection URL

   Service 2: AI Service (Python)
   - Type: Web Service
   - Repository: your-github/modified-vigilai-medlink
   - Root directory: ai-service
   - Build command: pip install -r requirements.txt
   - Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   - Note the service URL

   Service 3: Backend (Java)
   - Type: Web Service
   - Repository: same repo
   - Root directory: backend
   - Build command: mvn clean package -DskipTests
   - Start command: java -jar target/vigilai-backend-2.0.0.jar
   - Environment Variables:
     SPRING_DATASOURCE_URL = [postgres connection URL from step 2.1]
     SPRING_DATASOURCE_USERNAME = [from Render]
     SPRING_DATASOURCE_PASSWORD = [from Render]
     AI_SERVICE_URL = [ai service URL from step 2.2]/predict
     LLM_SERVICE_URL = [ai service URL]/explain
     JWT_SECRET = [random 64-char string]
     SPRING_JPA_HIBERNATE_DDL_AUTO = create  (first run only, then change to update)

   Service 4: Frontend (Static Site)
   - Type: Static Site
   - Repository: same repo
   - Root directory: frontend
   - No build command (pure HTML)
   
   Update API URL in login.html:
   const API = "https://your-backend.onrender.com";
```

---

## 📊 Monitoring & Health Checks

### Spring Boot Actuator (Built-in Monitoring):

```xml
<!-- Add to pom.xml: -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

```properties
# application.properties:
management.endpoints.web.exposure.include=health,metrics,info
management.endpoint.health.show-details=when-authorized
```

**Available endpoints:**
```
GET /actuator/health → {"status":"UP","components":{"db":{"status":"UP"}}}
GET /actuator/metrics → list of available metrics
GET /actuator/metrics/jvm.memory.used → memory usage
GET /actuator/metrics/http.server.requests → request count/latency
```

### VigilAI's Custom Health Endpoint:

```java
@GetMapping("/health")
public ResponseEntity<?> health() {
    return ResponseEntity.ok(Map.of(
        "status", "healthy",
        "service", "VigilAI Backend v2.0",
        "timestamp", LocalDateTime.now()
    ));
}
```

---

## 🚀 CI/CD — Continuous Integration / Continuous Deployment

### What is CI/CD?

**Continuous Integration (CI):**
- Every code push → automatically run tests
- If tests fail → reject the push
- Prevents broken code from reaching the team

**Continuous Deployment (CD):**
- Every successful CI → automatically deploy to production
- No manual deployment steps
- Faster, more reliable releases

### GitHub Actions CI/CD for VigilAI:

```yaml
# .github/workflows/deploy.yml
name: VigilAI CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Java 17
        uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Run tests
        run: |
          cd backend
          mvn test
      
      - name: Build JAR
        run: |
          cd backend
          mvn clean package -DskipTests

  test-ai-service:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          cd ai-service
          pip install -r requirements.txt pytest
      
      - name: Run tests
        run: |
          cd ai-service
          pytest tests/

  deploy:
    needs: [test-backend, test-ai-service]  # Only deploy if tests pass
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'     # Only deploy from main branch
    steps:
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST "https://api.render.com/v1/services/$SERVICE_ID/deploys" \
            -H "Authorization: Bearer $RENDER_API_KEY"
```

---

## ⚡ Performance Optimization

### Database Performance:

```sql
-- Use EXPLAIN to see query execution plan:
EXPLAIN ANALYZE SELECT * FROM alerts WHERE clinician_decision = 'PENDING';
-- Output: "Index Scan using idx_alerts_dispatch" ← good (using index)
-- vs: "Seq Scan on alerts" ← bad (scanning all rows)

-- Connection pooling (in application.properties):
spring.datasource.hikari.maximum-pool-size=10
spring.datasource.hikari.minimum-idle=5
-- HikariCP maintains a pool of 10 connections (instead of opening/closing per request)
```

### Spring Boot Performance:

```properties
# Lazy initialization (start faster):
spring.main.lazy-initialization=true

# Compress HTTP responses:
server.compression.enabled=true
server.compression.mime-types=application/json,text/html

# Tune JVM heap for small containers:
# In Dockerfile:
# CMD ["java", "-Xmx512m", "-Xms256m", "-jar", "app.jar"]
```

### Python/FastAPI Performance:

```python
# Use multiple workers (Uvicorn):
# uvicorn app.main:app --workers 4

# Cache the model in memory (already done!):
_model_instance = None  # Singleton pattern prevents reload

# Use async routes for I/O-bound operations:
@app.get("/health")
async def health():  # async = non-blocking
    return {"status": "healthy"}
```

---

## 📋 Production Readiness Checklist

Before launching VigilAI for real users:

```
Security:
  [ ] Rotate all secrets (JWT, DB password, API keys)
  [ ] Restrict CORS to specific domains (not "*")
  [ ] Enable HTTPS only (no HTTP)
  [ ] Set secure, httpOnly, sameSite cookie flags (if using cookies)
  [ ] Add rate limiting on /auth/login (brute-force protection)
  [ ] Remove demo credentials from login.html

Database:
  [ ] Change SPRING_JPA_HIBERNATE_DDL_AUTO from "create" to "validate"
  [ ] Set up automated backups (Render.com: daily backups available)
  [ ] Add database connection pool limits

Monitoring:
  [ ] Set up error alerting (PagerDuty, Sentry)
  [ ] Configure uptime monitoring (UptimeRobot, Pingdom)
  [ ] Set up log aggregation (Logtail, Papertrail)

Performance:
  [ ] Enable response compression
  [ ] Test with realistic load (k6, JMeter)
  [ ] Configure connection pool sizes

Compliance (if real patient data):
  [ ] Business Associate Agreement with cloud provider
  [ ] Data encryption at rest
  [ ] HIPAA risk assessment
  [ ] Penetration testing
```

---

## 💼 Interview Questions & Answers

### Q1: What is Docker and why is it used?
**A:** Docker packages an application and its entire environment (OS libraries, dependencies, runtime) into a lightweight, portable container. This solves "works on my machine" problems — the container runs identically on any machine that has Docker. VigilAI uses Docker to package all 4 services (Postgres, AI, Backend, Frontend) so the entire system can be started with one command: `docker-compose up`.

### Q2: What is the difference between an image and a container?
**A:** An image is a read-only blueprint (like a class in OOP). A container is a running instance of an image (like an object). `postgres:16-alpine` is the image; `vigilai-db` is the running container. Multiple containers can be created from the same image.

### Q3: What is a multi-stage Dockerfile and why is it used?
**A:** A multi-stage build uses multiple `FROM` statements. The first stage (build) has all build tools (JDK + Maven). The second stage (runtime) copies only the compiled artifact (JAR). This produces a much smaller final image (~150MB instead of ~600MB) because build tools are not included in the runtime image.

### Q4: What are environment variables and why should secrets use them?
**A:** Environment variables are key-value pairs injected into a process at runtime. Secrets (passwords, API keys, JWT secrets) should use environment variables instead of hardcoded values because: 1) If code is on GitHub, anyone can read hardcoded secrets. 2) Environment variables are set in the deployment platform's secure storage (e.g., Render.com's Environment Variables section), not in code.

### Q5: What is CI/CD?
**A:** Continuous Integration (CI) automatically runs tests on every code push — preventing broken code from being merged. Continuous Deployment (CD) automatically deploys code that passes tests to production. Together they eliminate manual deployment steps, reduce human error, and enable multiple deployments per day.

### Q6: What is the purpose of a health check?
**A:** A health check is an endpoint (typically `GET /health`) that returns 200 OK if the service is running correctly. Docker Compose uses health checks to determine when a service is ready (`depends_on: condition: service_healthy`). Cloud platforms use health checks for load balancing — unhealthy containers don't receive traffic. VigilAI's `/health` endpoint lets monitoring tools detect outages.

### Q7: What is connection pooling and why is it important?
**A:** Opening a new database connection is expensive (~100ms). Connection pooling keeps a pre-opened pool of connections ready. HikariCP (Spring Boot's default) maintains 10 connections. When a request needs the DB, it borrows one from the pool (fast: ~1ms). Without pooling, high traffic would overwhelm the database with connection overhead.

---

> **Final Module:** Module 10 is the complete Mastery & Placement Preparation guide — how to explain VigilAI in interviews, resume points, system design discussion, and your roadmap to becoming a confident full-stack developer.

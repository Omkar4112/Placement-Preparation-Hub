# MODULE 3: Frontend Complete Guide
## VigilAI MedLink Frontend — HTML, CSS, JavaScript Mastery

---

> [!NOTE]
> VigilAI's frontend uses pure HTML, CSS, and vanilla JavaScript — no React, no Vue, no Angular. This is actually a great learning experience because you see exactly what frameworks hide from you.

---

## 🗂️ Frontend File Structure

```
frontend/
├── index.html       → Entry point: redirects to login.html
├── login.html       → Authentication page (clinic/hospital/admin login)
├── clinic.html      → Clinic nurse dashboard (submit vitals, view patients)
├── hospital.html    → Hospital doctor dashboard (view alerts, approve dispatch)
└── admin.html       → Admin panel (system management, all users, stats)
```

Each `.html` file contains:
- **HTML** structure (the skeleton)
- **CSS** styling (the appearance, embedded in `<style>` tags)
- **JavaScript** behavior (the interactions, in `<script>` tags)

This is called a **Single-File Component** pattern — not ideal for large apps, but simple and self-contained for learning.

---

## 🏗️ HTML Fundamentals

HTML (HyperText Markup Language) defines the structure of a webpage using **tags**.

### Basic Structure (from login.html):
```html
<!DOCTYPE html>           <!-- Tells browser this is HTML5 -->
<html lang="en">          <!-- Root element, language for accessibility -->
<head>                    <!-- Metadata (not visible) -->
  <meta charset="UTF-8"> <!-- Character encoding (supports all languages) -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- ↑ Makes page responsive on mobile devices -->
  <title>VigilAI MedLink — Login</title>  <!-- Browser tab title -->
  <style>/* CSS goes here */</style>
</head>
<body>                    <!-- Visible content goes here -->
  
  <!-- VigilAI login form: -->
  <div class="card">
    <input type="email" id="email" placeholder="doctor@hospital.org">
    <input type="password" id="password" placeholder="••••••••">
    <button onclick="login()">Sign In →</button>
  </div>
  
  <script>/* JavaScript goes here */</script>
</body>
</html>
```

### Important HTML Attributes:

| Attribute | Example | Purpose |
|-----------|---------|---------|
| `id` | `id="email"` | Unique identifier — `getElementById('email')` |
| `class` | `class="card"` | CSS class for styling |
| `onclick` | `onclick="login()"` | Run function when clicked |
| `type` | `type="email"` | Input type (validates email format) |
| `placeholder` | `placeholder="..."` | Hint text in empty input |
| `data-*` | `data-role="CLINIC"` | Custom data stored on element |

**From login.html — role tabs using `data-role`:**
```html
<div class="role-tab active" data-role="CLINIC" onclick="selectRole(this)">
  <span class="icon">🏨</span>
  <span>Clinic</span>
</div>
```
The `data-role="CLINIC"` stores extra data that JavaScript reads: `el.dataset.role` → `"CLINIC"`.

---

## 🎨 CSS Fundamentals

CSS (Cascading Style Sheets) controls appearance.

### CSS Variables (VigilAI's Design System):
```css
:root {
  /* Color palette — defined once, used everywhere */
  --bg:       #04080f;           /* near-black background */
  --surface:  rgba(13,25,41,0.7); /* card surface with transparency */
  --accent:   #00d4ff;           /* cyan highlight color */
  --accent2:  #0057ff;           /* blue for gradients */
  --danger:   #ff3b5c;           /* error red */
  --success:  #00e5a0;           /* success green */
  --text:     #f0f7ff;           /* near-white text */
  --muted:    #6b8eb0;           /* subdued text */
  
  /* Fonts */
  --mono:     'DM Mono', monospace;    /* for code-like text */
  --sans:     'Plus Jakarta Sans', sans-serif; /* for UI text */
}

/* Using variables: */
body {
  background: var(--bg);      /* use the variable */
  color: var(--text);
  font-family: var(--sans);
}
```

**Why CSS Variables?** Change `--accent: #00d4ff` in one place → the entire app's accent color updates. This is the foundation of a design system.

### Glassmorphism Effect (VigilAI's signature look):
```css
.card {
  background: #080f1a;                /* Dark base */
  border: 1px solid rgba(255,255,255,0.08);  /* subtle border */
  border-radius: 24px;               /* rounded corners */
  box-shadow: 0 30px 60px rgba(0,0,0,0.5);  /* deep shadow */
  backdrop-filter: blur(20px);       /* blur behind the card */
  /* Result: A glass-like dark card floating above the background */
}
```

### The Animated Background Orbs:
```css
/* Blurred circles create the glowing orb effect */
.orb {
  position: absolute;
  border-radius: 50%;       /* makes it circular */
  filter: blur(120px);      /* spreads the color as a glow */
  opacity: 0.3;             /* semi-transparent */
  pointer-events: none;     /* doesn't interfere with clicks */
}
.orb-1 { 
  width: 400px; height: 400px; 
  background: #0057ff;      /* blue glow */
  top: -100px; left: -100px; /* positioned top-left, partially off-screen */
}
```

### CSS Animations:
```css
/* Card entrance animation: */
@keyframes reveal {
  from { opacity: 0; transform: translateY(20px); }  /* starts invisible, 20px lower */
  to   { opacity: 1; transform: none; }               /* ends fully visible, in place */
}
.card {
  animation: reveal 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  /* cubic-bezier = custom animation timing — "spring" feel */
}

/* Pulsing status dot (the green dot indicating system is online): */
@keyframes pulse-glow {
  0%  { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,229,160,0.7); }
  70% { transform: scale(1);    box-shadow: 0 0 0 6px rgba(0,229,160,0); }
  100%{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0,229,160,0); }
}
.status-dot {
  animation: pulse-glow 2s infinite;  /* loops forever */
}
```

### Flexbox and Grid Layout:
```css
/* Flexbox — one-dimensional layout (row or column): */
.logo {
  display: flex;
  align-items: center;  /* vertically center logo icon and text */
  gap: 16px;            /* space between items */
}

/* Grid — two-dimensional layout (rows AND columns): */
.role-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;  /* 3 equal columns */
  gap: 12px;
}
```

---

## ⚡ JavaScript Frontend Patterns

### Pattern 1: Event-Driven Programming
In frontend JavaScript, code runs in response to **events** (clicks, keyboard input, page load):

```javascript
// Inline event handler (onclick attribute):
<button onclick="login()">Sign In</button>

// addEventListener (preferred approach):
document.getElementById('loginBtn').addEventListener('click', login);

// Keyboard event:
<input onkeydown="if(event.key==='Enter') login()">
// ↑ Allows pressing Enter in password field to submit
```

### Pattern 2: DOM Manipulation
```javascript
function showError(msg) {
    const el = document.getElementById('errMsg');  // find element by ID
    el.textContent = msg;                           // set its text
    el.classList.add('show');                       // add CSS class (makes it visible)
}

function fillCred(email, pass, role) {
    document.getElementById('email').value    = email;   // change input value
    document.getElementById('password').value = pass;
    
    // Toggle active class:
    document.querySelectorAll('.role-tab').forEach(t => {
        t.classList.toggle('active', t.dataset.role === role);
        // toggle(class, condition):
        // - if condition is true → add the class
        // - if condition is false → remove the class
    });
    
    selectedRole = role;
}
```

### Pattern 3: localStorage (Browser Storage)
```javascript
// After login — save session data:
localStorage.setItem('vigilai_token',    data.token);
localStorage.setItem('vigilai_role',     data.role);
localStorage.setItem('vigilai_entityId', data.entityId || '');
localStorage.setItem('vigilai_name',     data.fullName || email);

// In clinic.html — read saved session:
const token    = localStorage.getItem('vigilai_token');
const role     = localStorage.getItem('vigilai_role');
const clinicId = localStorage.getItem('vigilai_entityId');

// Auth guard — redirect to login if not logged in:
if (!token) {
    window.location.href = 'login.html';
}
```

### Pattern 4: Making API Calls with Fetch
```javascript
// Standard API call pattern used throughout VigilAI frontend:
async function callAPI(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('vigilai_token');
    
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`  // JWT in Authorization header
        }
    };
    
    if (body) {
        options.body = JSON.stringify(body);  // convert object to JSON string
    }
    
    const response = await fetch(`${API}${endpoint}`, options);
    
    if (response.status === 401) {
        // Token expired — redirect to login
        localStorage.clear();
        window.location.href = 'login.html';
        return;
    }
    
    return await response.json();
}

// Usage:
const alerts = await callAPI('/api/hospital/alerts');
const result = await callAPI('/api/clinic/vitals', 'POST', vitalData);
```

---

## 📱 Page-by-Page Frontend Walkthrough

### Page 1: `login.html` — Authentication Flow

**Purpose:** Authenticate users and redirect them to their role-specific dashboard.

**Key Features:**
1. **Role selector tabs** (Clinic / Hospital / Admin)
2. **Email + password form**
3. **Demo credentials** (click to auto-fill)
4. **API health check** (pre-warms the backend on page load)
5. **Demo mode fallback** (works offline for demos)

**Complete Login Flow:**
```javascript
async function login() {
    // Step 1: Validate inputs
    const email    = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    if (!email || !password) { showError('Please enter email and password.'); return; }
    
    // Step 2: Show loading state
    btn.textContent = 'Authenticating…';
    
    // Step 3: API call (wakeup timer for free tier)
    const wakeupTimer = setTimeout(() => {
        btn.textContent = 'Waking up Free Tier Server (~50s)…';
    }, 3000);
    
    try {
        // Step 4: POST to /auth/login
        const res = await fetch(`${API}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        const data = await res.json();
        
        if (!res.ok) { showError(data.error || 'Login failed.'); return; }
        
        // Step 5: Store session
        localStorage.setItem('vigilai_token',    data.token);
        localStorage.setItem('vigilai_role',     data.role);
        localStorage.setItem('vigilai_entityId', data.entityId || '');
        localStorage.setItem('vigilai_name',     data.fullName || email);
        localStorage.setItem('vigilai_email',    data.email);
        
        // Step 6: Redirect by role
        const redirects = { CLINIC:'clinic.html', HOSPITAL:'hospital.html', ADMIN:'admin.html' };
        window.location.href = redirects[data.role] || 'clinic.html';
        
    } catch (e) {
        // Step 7: Offline fallback — demo mode
        localStorage.setItem('vigilai_token', 'demo-token');
        localStorage.setItem('vigilai_role', selectedRole);
        setTimeout(() => { window.location.href = redirects[selectedRole]; }, 800);
    } finally {
        clearTimeout(wakeupTimer);
        btn.textContent = 'Sign In →';
    }
}
```

**Server Pre-Warming (Clever UX Trick):**
```javascript
// This IIFE (Immediately Invoked Function Expression) runs as soon as the page loads
// It warms up the free-tier Render.com server BEFORE the user finishes typing
(async () => {
    const r = await fetch(`${API}/health`);  // Wake up the server
    if (r.ok) {
        statusEl.textContent = 'ONLINE';
        // Also pre-warm DB + BCrypt (will 401 but that's fine — just warms the JVM):
        fetch(`${API}/auth/login`, {
            method: 'POST', 
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({email:'warmup@x.x', password:'x'})
        }).catch(() => {});
    }
})();
```

### Page 2: `clinic.html` — Nurse Dashboard

**Purpose:** Enable clinic staff to submit patient vitals and see AI predictions.

**Key Features:**
- Patient search/registration form
- Vitals entry form (HR, Temp, RR, BP, SpO2)
- Emergency type selector
- AI prediction result display
- Patient history table
- WebSocket connection for real-time updates

**Vitals Submission Flow (Frontend Side):**
```javascript
async function submitVitals() {
    const token = localStorage.getItem('vigilai_token');
    const clinicId = localStorage.getItem('vigilai_entityId');
    
    // Build the vitals payload:
    const payload = {
        clinicId: clinicId,
        phoneNumber: document.getElementById('phone').value,
        fullName: document.getElementById('patientName').value,
        age: parseInt(document.getElementById('age').value),
        gender: document.getElementById('gender').value,
        heart_rate: parseInt(document.getElementById('heartRate').value),
        temperature: parseFloat(document.getElementById('temperature').value),
        respiratory_rate: parseInt(document.getElementById('respRate').value),
        systolic_bp: parseInt(document.getElementById('sysBP').value),
        diastolic_bp: parseInt(document.getElementById('diaBP').value),
        spo2: parseInt(document.getElementById('spo2').value),
        clinicalNotes: document.getElementById('notes').value,
        emergencyType: document.getElementById('emergencyType').value
    };
    
    // Send to backend:
    const res = await fetch(`${API}/api/clinic/vitals`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
    });
    
    const result = await res.json();
    
    // Display the AI prediction result:
    displayPrediction(result);
}

function displayPrediction(result) {
    const riskBadge = document.getElementById('riskBadge');
    riskBadge.textContent = result.riskLevel;
    riskBadge.className = `risk-badge risk-${result.riskLevel.toLowerCase()}`;
    
    document.getElementById('explanation').textContent = result.explanation;
    document.getElementById('riskScore').textContent = 
        `${(result.riskScore * 100).toFixed(1)}%`;
    
    if (result.alertCreated) {
        showNotification('⚠️ Alert created — hospital notified!', 'danger');
    }
}
```

### Page 3: `hospital.html` — Doctor Dashboard

**Purpose:** Let hospital doctors review incoming emergency alerts and decide on ambulance dispatch.

**Key Features:**
- Real-time alert feed (WebSocket)
- Alert cards with AI explanation, vitals, and treatment recs
- Approve / Hold / Dismiss actions
- Hospital statistics dashboard
- Dispatch tracking

**WebSocket Connection (Real-Time Alerts):**
```javascript
// Connect to backend WebSocket for real-time alert push:
function connectWebSocket() {
    const socket = new SockJS(`${API}/ws`);  // SockJS for compatibility
    const stompClient = Stomp.over(socket);
    
    stompClient.connect({}, frame => {
        console.log('WebSocket connected:', frame);
        
        // Subscribe to the alerts topic:
        stompClient.subscribe('/topic/alerts', message => {
            const alert = JSON.parse(message.body);
            // New alert arrived! Add it to the top of the list:
            addAlertToUI(alert);
            showNotification(`🚨 New ${alert.severity} alert — Patient ${alert.patientId}`);
        });
    });
}

// Call this when the page loads:
connectWebSocket();
```

**Alert Decision (Approve/Hold/Dismiss):**
```javascript
async function makeDecision(alertId, decision) {
    const token = localStorage.getItem('vigilai_token');
    
    const res = await fetch(`${API}/api/hospital/alerts/${alertId}/decision`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ decision: decision, notes: 'Doctor reviewed' })
    });
    
    if (res.ok) {
        // If approved, trigger ambulance dispatch:
        if (decision === 'APPROVED') {
            await fetch(`${API}/api/hospital/alerts/${alertId}/dispatch`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
        }
        // Remove alert card from UI:
        document.getElementById(`alert-${alertId}`).remove();
    }
}
```

### Page 4: `admin.html` — System Management

**Purpose:** Full system visibility and control for administrators.

**Key Features:**
- All users management (view, enable/disable)
- All hospitals management
- System-wide statistics
- Audit log viewer
- Alert overview across all clinics

---

## 🔄 State Management (Without a Framework)

Since VigilAI uses vanilla JavaScript (no React/Redux), state is managed through:

### 1. localStorage (persistent, survives page refresh):
```javascript
// Session state:
localStorage.setItem('vigilai_token', token);
localStorage.setItem('vigilai_role', role);
localStorage.setItem('vigilai_entityId', clinicId);
```

### 2. JavaScript Variables (in-memory, lost on refresh):
```javascript
let currentPage = 1;
let totalAlerts = 0;
let selectedPatientId = null;
```

### 3. DOM as State (UI reflects what's visible):
```javascript
// The presence of CSS class represents state:
button.classList.contains('active')  // is this button selected?
modal.style.display === 'none'       // is the modal hidden?
```

---

## 🎯 Frontend Best Practices Demonstrated in VigilAI

### 1. Loading States:
```javascript
btn.textContent = 'Authenticating…';    // show loading
btn.disabled = true;
// ... do the work ...
btn.textContent = 'Sign In →';          // restore
btn.disabled = false;
```

### 2. Error States with Animation:
```css
@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}
.error-msg {
    animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}
```

### 3. Role-Based UI:
```javascript
// Hide hospital-specific elements for clinic users:
const role = localStorage.getItem('vigilai_role');
if (role !== 'HOSPITAL') {
    document.getElementById('dispatchSection').style.display = 'none';
}
```

### 4. Graceful Degradation (Demo Mode):
```javascript
// If server is down, don't crash — show demo mode:
try {
    const res = await fetch(apiUrl);
    // normal flow
} catch (e) {
    // server offline — demo mode
    localStorage.setItem('vigilai_token', 'demo-token');
    window.location.href = 'clinic.html';
}
```

---

## 📐 UI Architecture — Design System

VigilAI follows a design system with consistent tokens:

```
Color System:
  ├── Background: #04080f (near-black)
  ├── Surface: rgba(13,25,41,0.7) (card backgrounds)  
  ├── Accent: #00d4ff (cyan - primary interactive)
  ├── Accent2: #0057ff (blue - gradients)
  ├── Danger: #ff3b5c (errors, critical alerts)
  └── Success: #00e5a0 (success, operational status)

Typography:
  ├── UI Text: 'Plus Jakarta Sans' (headings, buttons, labels)
  └── Monospace: 'DM Mono' (code-like, API data, credentials)

Spacing:
  ├── Micro: 4px, 8px
  ├── Component: 12px, 16px, 20px
  └── Section: 32px, 40px, 56px

Border Radius:
  ├── Small: 8px (tags, badges)
  ├── Medium: 12px (inputs, role tabs)
  └── Large: 24px (main cards)
```

---

## 💼 Interview Questions & Answers

### Q1: What is the DOM?
**A:** The DOM (Document Object Model) is the browser's in-memory representation of the HTML page as a tree of objects. JavaScript uses the DOM to read and modify HTML dynamically. In VigilAI, `document.getElementById('email')` accesses the email input DOM element, and `.value` reads what the user typed.

### Q2: What is localStorage and when do you use it?
**A:** localStorage is a browser-side key-value store that persists data even after the browser is closed (unlike sessionStorage which clears on tab close). In VigilAI, we store the JWT token and user role in localStorage after login so subsequent pages (clinic.html) know the user is authenticated without making another login request.

### Q3: What is an IIFE and why is it used in login.html?
**A:** An IIFE (Immediately Invoked Function Expression) is a function that runs immediately when defined: `(async () => { ... })()`. In VigilAI's login.html, it's used to pre-warm the backend server as soon as the page loads, before the user even starts typing. This reduces perceived login time.

### Q4: What is the difference between `textContent` and `innerHTML`?
**A:** `textContent` sets plain text (safe, no HTML parsing). `innerHTML` sets HTML markup (dangerous if user-controlled input — XSS attack risk). In VigilAI, `el.textContent = msg` for error messages is safe because it doesn't interpret HTML. Never use `innerHTML` with user input.

### Q5: How does WebSocket differ from regular HTTP?
**A:** HTTP is a request-response protocol (client asks, server responds, connection closes). WebSocket is a persistent, bidirectional channel (server can push data to client anytime). VigilAI uses WebSocket so the hospital dashboard gets instant alert notifications without polling every 5 seconds.

### Q6: What is the purpose of the `Authorization: Bearer TOKEN` header?
**A:** After login, every API request must include the JWT token to prove identity. The header format is `Authorization: Bearer <token>`. The backend's `JwtFilter` intercepts every request, extracts this header, validates the token, and sets the authenticated user in the security context.

### Q7: What is CSS specificity?
**A:** CSS specificity determines which rule wins when multiple rules target the same element. ID selectors (#id) > class selectors (.class) > element selectors (div). In VigilAI, `.role-tab.active` (two classes) has higher specificity than `.role-tab` alone, so the active styling overrides the default.

---

## 🎯 Mini Assignment

1. **Modify the login page**: Add a "Remember Me" checkbox that stores the email in localStorage, pre-filling it next time.

2. **Add form validation**: In the vitals form, validate that heart_rate is between 30 and 300 before submitting. Show an error if invalid.

3. **Add a logout button**: In clinic.html, add a logout button that clears localStorage and redirects to login.html.

4. **Style challenge**: Change the accent color from cyan (#00d4ff) to emerald green (#00d68a) system-wide by modifying the one CSS variable.

---

> **Next Module:** Module 4 covers the backend in depth — Spring Boot, controllers, services, repositories, security, JWT, and the complete request lifecycle.

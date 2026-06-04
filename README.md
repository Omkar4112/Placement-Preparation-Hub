# VigilAI MedLink — Complete Learning Roadmap

> A beginner-to-expert guide for understanding, building, modifying, debugging,
> deploying, and confidently explaining this project in interviews.

---

## 📚 Module Index

| # | File | Topics Covered |
|---|------|---------------|
| 1 | [module1_technology_foundations.md](./module1_technology_foundations.md) | Software development basics, Frontend vs Backend vs Database, HTTP, APIs, JSON, Client-Server, How VigilAI fits the architecture |
| 2 | [module2_language_fundamentals.md](./module2_language_fundamentals.md) | Java 17, JavaScript, Python from scratch — variables, OOP, async, error handling — all using VigilAI code |
| 3 | [module3_frontend_complete.md](./module3_frontend_complete.md) | HTML/CSS/JS, all 4 pages (login, clinic, hospital, admin), localStorage, fetch API, WebSocket, design system |
| 4 | [module4_backend_complete.md](./module4_backend_complete.md) | Spring Boot MVC, Controllers, Services, Repositories, JWT filter, Security config, WebSocket, request lifecycle |
| 5 | [module5_database_complete.md](./module5_database_complete.md) | PostgreSQL, all 10 tables explained, SQL queries, indexes, transactions, normalization, PostgreSQL features |
| 6 | [module6_project_deep_dive.md](./module6_project_deep_dive.md) | Every file and function explained, complete vitals→AI→alert→dispatch flow, AI service deep dive, architecture decisions |
| 7 | [module7_security_auth.md](./module7_security_auth.md) | JWT deep dive, BCrypt, Spring Security, CORS/CSRF, OWASP Top 10, HIPAA compliance, secure coding |
| 8 | [module8_testing_debugging.md](./module8_testing_debugging.md) | Browser DevTools, Spring Boot logs, Postman, JUnit tests, pytest, Git workflow, common bugs and fixes |
| 9 | [module9_deployment_devops.md](./module9_deployment_devops.md) | Docker, Dockerfiles, Docker Compose, environment variables, Render.com deployment, CI/CD, monitoring |
| 10 | [module10_mastery_placement.md](./module10_mastery_placement.md) | Interview scripts, resume bullet points, system design, viva Q&A (beginner→advanced), future improvements |

---

## 🗺️ Recommended Study Plan

| Week | Modules | Focus |
|------|---------|-------|
| Week 1 | 1, 2, 3 | Foundation + Language + Frontend |
| Week 2 | 4, 5, 6 | Backend + Database + Deep Dive |
| Week 3 | 7, 8, 9 | Security + Testing + Deployment |
| Week 4 | 10 + Practice | Mastery + Interview Preparation |

---

## 🚀 Quick Start

```bash
# Run the entire project locally:
docker-compose up --build

# Access:
# Frontend:   http://localhost:3000/login.html
# Backend API: http://localhost:8080
# AI Service: http://localhost:8000/docs
# Database:   localhost:5432

# Demo Credentials:
# clinic@vigilai.health   / Clinic@123
# hospital@vigilai.health / Hospital@123
# admin@vigilai.health    / Admin@123
```

---

*Total: 10 modules | ~250,000 words | Covers every aspect of the VigilAI MedLink stack*

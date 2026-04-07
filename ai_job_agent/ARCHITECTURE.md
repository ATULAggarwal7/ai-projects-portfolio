# 🤖 AI Job Application Agent

## 🚀 Overview

This project implements an **end-to-end agentic pipeline** that automates the job application process.

The system takes a queue of job URLs and autonomously:

* Generates a tailored resume
* Generates a cover letter
* Opens a real browser session
* Detects the ATS platform
* Extracts and fills application form fields intelligently
* Submits the application
* Moves to the next job in the queue

The focus is on **agent architecture, intelligent decision-making, and system reliability**, rather than UI.

---

## 🧠 System Architecture

### 🔁 Agent Flow

1. Job Queue → fetch next job
2. Resume + Cover Letter Generation
3. ATS Detection
4. Browser Automation (Playwright)
5. Form Field Extraction
6. Intelligent Field Resolution:

   * Profile DB
   * Custom Answers
   * AI Inference
   * Human-in-the-Loop (HITL)
7. Form Submission
8. Move to next job

---

## 🗄️ Candidate Database Design

Structured using a relational schema:

### 1. UserProfile

Stores:

* Name, email, phone
* Resume file path

### 2. CustomAnswers (Key-Value Store)

Stores dynamic answers like:

* Notice period
* Salary expectation
* Relocation preference

👉 Designed to be extensible without code changes.

---

### 3. Jobs Table

Tracks:

* URL, company, title
* ATS platform
* Status (pending / applied / backlog / failed)
* Failure reason
* Unanswered fields

---

## 🧠 Intelligent Field Mapping

The agent resolves each form field using a **priority-based reasoning pipeline**:

1. Profile Database
2. Custom Answers
3. AI Inference
4. Human-in-the-Loop (HITL)

### Example Logs:

```
[AI] Resolving field: email
[AI] Found in profile DB

[AI] Resolving field: expected_salary
[AI] Found in custom answers

[AI] Resolving field: unknown_field
[AI] Using AI inference
```

---

## 🤖 AI / LLM Integration

### Current Implementation

The system uses an **LLM abstraction layer**, but due to API quota constraints during development, a **fallback intelligent generator** is used.

### Why this approach?

* Ensures system reliability without external dependency failures
* Maintains consistent demo behavior
* Allows easy plug-in of real LLM APIs (OpenAI / Groq)

👉 The architecture is designed so that:

> Real LLM → Drop-in replacement (no code restructuring required)

---

## 🧑‍💻 Human-in-the-Loop (HITL)

Triggered when:

* Field is ambiguous
* Not present in DB
* Cannot be inferred reliably

### Behavior:

* Prompts user with a 30-second timeout
* If answered:

  * Value is filled
  * Stored in DB for future reuse
* If not answered:

  * Job moves to **backlog**
  * Field logged for future runs

---

## 🌐 ATS Detection

Supports:

* Greenhouse
* Lever
* Workday
* LinkedIn

Detection is based on:

* URL patterns
* Page structure signals

---

## 🧪 Demo Setup

Includes:

* Pre-seeded candidate profile
* Pre-filled custom answers
* Multiple job URLs:

  * Simple forms (for full automation demo)
  * Real ATS links (for detection and partial automation)

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
playwright install
python main.py
```

---

## 📦 Outputs

For each job:

* `outputs/resume_<id>.txt`
* `outputs/cover_letter_<id>.txt`

---

## ⚠️ Real-World Constraints & Design Decisions

### 1. LLM Fallback

Due to API quota limits:

* A fallback generator is used
* Ensures consistent execution
* Architecture supports real LLM integration seamlessly

---

### 2. ATS Automation Limitations

Some platforms:

* Require authentication
* Load forms dynamically

👉 The system handles this gracefully:

* Detects platform
* Attempts automation
* Falls back without breaking pipeline

---

### 3. Form Noise Handling

Web pages often contain irrelevant inputs:

* Search bars
* Filters
* UI controls

👉 The system filters these intelligently.

---

## 📈 Scaling Strategy

Future improvements include:

* Multi-user support (user-scoped DB)
* Distributed job queue (Redis / Celery)
* Parallel agent execution
* Advanced ATS DOM-based detection
* Real LLM integration with caching

---

## 🎥 Demo

A screen recording demonstrates:

* End-to-end job processing
* AI reasoning logs
* HITL interaction
* Browser automation

---

## 🏁 Conclusion

This project demonstrates:

* Agentic system design
* Intelligent automation
* AI-assisted decision making
* Robust handling of real-world constraints

It is designed to be **production-extensible**, not just a prototype.

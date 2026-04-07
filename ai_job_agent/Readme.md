# 🤖 AI Job Application Agent

## 📌 Overview

This project implements an **agentic AI system** that automates the job application process end-to-end.

Given a queue of job URLs, the agent:

* Generates a tailored resume
* Generates a cover letter
* Detects the ATS platform
* Opens and interacts with a real browser
* Extracts and fills application forms intelligently
* Submits applications automatically
* Moves to the next job in the queue

The focus is on **agent orchestration, reliability, and intelligent decision-making**.

---

# 🚀 How to Run the Demo

```bash
pip install -r requirements.txt
playwright install
python main.py
```

### Demo Includes:

* Pre-seeded candidate profile
* Pre-filled custom answers
* Multiple job URLs:

  * Simple forms (for full automation demo)
  * Real ATS platforms (for detection and partial automation)

---

# 🗄️ Candidate Database Design

The system uses a structured relational database:

## 1. UserProfile

Stores:

* Name
* Email
* Phone
* Resume file path

---

## 2. CustomAnswers (Key-Value Store)

Stores dynamic answers required in job forms:

* Notice period
* Salary expectations
* Relocation preference
* Visa sponsorship

### Extensibility:

* Users can add new key-value pairs
* Automatically used in future runs
* No code changes required

---

## 3. Jobs Table

Tracks:

* Job URL
* Company
* Title
* ATS platform
* Status (`pending`, `applied`, `backlog`, `failed`)
* Failure reason
* Unanswered fields

---

# 🌐 ATS Detection

The system detects ATS platforms using URL pattern matching:

Supported:

* Greenhouse
* Lever
* Workday
* LinkedIn

### Example:

```python
if "greenhouse" in url:
    return "greenhouse"
```

### Design Note:

This approach is simple and extensible. It can be enhanced with DOM fingerprinting for production systems.

---

# 🧠 Form Field Mapping Strategy

Each form field is resolved using a **priority-based decision pipeline**:

### 1. Profile DB

Basic personal information:

* Name, email, phone

---

### 2. Custom Answers

Dynamic user-provided values:

* Salary expectations
* Notice period
* Relocation

---

### 3. AI Inference

If not found in DB:

* System generates a reasonable answer using an LLM abstraction layer

---

### 4. Logging

All decisions are logged:

```text
[AI] Found in profile DB
[AI] Found in custom answers
[AI] Using AI inference
```

---

# 🤖 LLM / AI Design

### Current Implementation:

Due to API quota constraints, a **fallback intelligent generator** is used.

### Why:

* Ensures consistent demo behavior
* Avoids dependency failures
* Maintains system reliability

### Architecture:

The system is designed to support:

* OpenAI
* Groq
* Any LLM provider

👉 LLM can be plugged in without changing system design.

---

# 🧑‍💻 Human-in-the-Loop (HITL)

## When it triggers:

* Field not found in DB
* AI cannot confidently infer answer

---

## Behavior:

1. Agent pauses and prompts user
2. Waits **30 seconds**
3. If user responds:

   * Field is filled
   * Value saved to DB
4. If timeout:

   * Job moved to **backlog**
   * Field stored in `unanswered_fields`

---

## Example:

```text
[HITL] Need user input for: expected_salary
Enter value (30s timeout):
```

---

# 🔁 Backlog Handling

If a field remains unresolved:

* Job is marked as `backlog`
* Unanswered fields are tracked

This ensures:

* No silent failures
* Clear feedback for next run

---

# ⚙️ System Reliability Design

* Idempotent database seeding
* Safe retries
* Fallback AI generation
* Graceful handling of ATS limitations
* Intelligent filtering of irrelevant fields

---

# ⚠️ Real-World Constraints

### ATS Platforms:

Some platforms:

* Require login
* Load forms dynamically

👉 System handles this gracefully:

* Detects ATS
* Attempts automation
* Falls back without breaking pipeline

---

# 📈 Scaling Strategy

### Multi-User Support

* Separate user profiles in DB
* User-scoped job queues

---

### Concurrent Agents

* Parallel job execution
* Distributed workers

---

### Job Queue Infrastructure

* Replace DB queue with:

  * Redis
  * Celery
  * Kafka

---

### Future Improvements

* DOM-based ATS detection
* Real LLM integration with caching
* Advanced form understanding
* Resume personalization using embeddings

---

# 🎯 Conclusion

This project demonstrates:

* Agentic workflow design
* AI-assisted automation
* Reliable system architecture
* Real-world constraint handling

The system is built to be **extensible, robust, and production-ready in design**.

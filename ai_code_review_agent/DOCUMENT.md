# 📘 Document

## AI Code Reviewer System (Local LLM + RAG + VS Code Extension)

---

# 🧭 1. Overview

The **AI Code Reviewer System** is an end-to-end solution for automated code analysis using:

* AST-based parsing
* Company coding guidelines (RAG)
* Local LLM (GGUF models)
* FastAPI backend
* VS Code Extension integration

The system enables developers to **analyze code quality locally (offline)** and receive:

* Code quality score
* Detected issues
* Suggestions for improvement

---

# 🎯 2. Objectives

* Automate code review process
* Enforce company coding standards
* Provide developer-friendly feedback
* Enable offline AI-based analysis
* Integrate directly into developer workflow (VS Code)

---

# 🏗️ 3. High-Level Architecture

```
VS Code Extension / API Client
              ↓
        FastAPI Backend
              ↓
   ┌──────────┼──────────┐
   ↓          ↓          ↓
Parser      RAG       LLM Engine
(AST)    (Guidelines)  (Local)
   ↓          ↓          ↓
        Review Agent
              ↓
     Structured Output
```

---

# 🔄 4. End-to-End Flow

1. User uploads file OR triggers extension
2. Backend receives code (`/review-code`)
3. Language detection happens
4. Code is parsed (AST)
5. Guidelines retrieved via RAG
6. LLM processes:

   * Code + Structure + Guidelines
7. Issues extracted and cleaned
8. Score calculated
9. JSON response returned

---

# 📁 5. Project Structure Explanation

## Root Level

### `run.py`

* Starts FastAPI server
* Simplified execution entry point

---

### `load_guidelines.py`

* Converts `.md` guidelines into embeddings
* Stores in `vector_db/`
* **Mandatory before first run**

---

### `requirements.txt`

* Contains all required dependencies

---

## 📚 `guidelines/`

Contains company coding rules:

* `python_guidelines.md`
* `javascript_guidelines.md`

Used by:
➡️ RAG system for contextual review

---

## 🤖 `models/`

Stores local LLM models (GGUF format)

Example:

```
Qwen2.5-7B-Instruct-Q5_K_M.gguf
```

---

## 🧠 `vector_db/`

* ChromaDB storage for embeddings
* Auto-created using:

```
python load_guidelines.py
```

---

# 📦 6. Backend (app/)

---

## `main.py`

* Initializes FastAPI app
* Registers routes

---

## `api/routes.py`

Handles API endpoints

### Main Endpoint:

```
POST /review-code
```

Responsibilities:

* File upload handling
* Language detection
* Calling review agent
* Returning results

---

## `agents/review_agent.py` ⭐ CORE

Main orchestration layer

Responsibilities:

* Retrieve guidelines (RAG)
* Build LLM prompt
* Call LLM
* Parse response
* Return structured output

---

## `llm/local_llm.py`

* Loads local model using `llama-cpp-python`
* Maintains model in memory
* Executes inference

---

## `parsers/python_parser.py`

* Uses AST
* Extracts:

  * Functions
  * Variables
  * Docstrings
  * Line numbers
  * Function complexity

---

## `parsers/javascript_parser.py` (if enabled)

* Handles JS parsing
* Extendable using Tree-sitter

---

## `utils/file_loader.py`

* Reads uploaded files
* Detects language

---

## `models/schemas.py`

* Defines API request/response structure
* Uses Pydantic

---

## `rag/guideline_loader.py`

* Reads guideline files
* Splits into chunks
* Prepares embeddings

---

## `rag/vector_store.py`

* Manages ChromaDB
* Functions:

  * Create DB
  * Load DB
  * Query relevant rules

---

## Optional Components

### `rules/`

* Static rule-based checks

### `scoring/scoring_engine.py`

* Computes code quality score

### `utils/repo_scanner.py`

* Enables full repository scanning

---

# 🧩 7. VS Code Extension

## Overview

Provides **real-time code review inside VS Code**

---

## File

```
ai-code-reviewer-0.0.1.vsix
```

---

## How It Works

```
VS Code → Backend API → AI Review → Results → Editor Highlights
```

---

## Features

* Code review inside editor
* Highlights issues
* Uses backend API
* Supports Python & JavaScript

---

## Installation

1. Open VS Code
2. Extensions → (⋯) → Install from VSIX
3. Select `.vsix` file

---

## Usage

```
Ctrl + Shift + P → AI Code Review
```

---

## Dependency

⚠️ Backend must be running:

```
http://127.0.0.1:8000
```

---

# ⚙️ 8. Setup Instructions

## Step 1: Clone Repo

```
git clone <repo-url>
cd ai_code_reviewer
```

---

## Step 2: Create Environment

```
python -m venv venv
venv\Scripts\activate
```

---

## Step 3: Install Dependencies

```
pip install -r requirements.txt
```

---

## Step 4: Add Model

Place GGUF model in:

```
models/
```

---

## Step 5: Create Vector DB

```
python load_guidelines.py
```

---

## Step 6: Run Backend

```
python run.py
```

OR

```
uvicorn app.main:app --reload
```

---

# 🌐 9. API Documentation

Access:

```
http://localhost:8000/docs
```

---

## Endpoint

```
POST /review-code
```

---

## Sample Response

```
{
 "score": 85,
 "issues": [
  {
   "rule": "function_length",
   "file": "example.py",
   "line": 10,
   "severity": "medium",
   "suggestion": "Refactor function"
  }
 ],
 "summary": "Code needs optimization"
}
```

---

# ⚠️ 10. Important Notes

* Run `load_guidelines.py` before first use
* Ensure model path is correct
* Large files may increase latency
* System is fully offline (no external APIs)

---

# 🐞 11. Troubleshooting

### Issue: Model not loading

* Check model path
* Ensure GGUF format

---

### Issue: No results from RAG

* Re-run:

```
python load_guidelines.py
```

---

### Issue: API not working

* Ensure server is running
* Check port (8000)

---

### Issue: Extension not working

* Verify backend is running
* Check API URL

---

# 🚀 12. Future Enhancements

* Static rule engine (faster checks)
* Multi-language support
* GitHub PR integration
* UI dashboard
* Auto-fix suggestions
* Code heatmaps

---

# 🔐 13. Security & Constraints

* Runs locally (no data leakage)
* No external API dependency
* Depends on local compute power

---

# 📊 14. System Strengths

* Offline AI capability
* Context-aware review (RAG)
* Scalable backend architecture
* Developer-friendly integration

---

# 👨‍💻 15. Ownership & Handover Notes

* Ensure model + vector DB setup before usage
* Extension depends on backend availability
* Modular design allows easy extension
* Review agent is central component

---

# ✅ 16. Summary

This system combines:

* Code parsing
* RAG-based knowledge retrieval
* Local LLM reasoning
* API + Extension integration

➡️ Delivering a **complete AI-powered code review platform**

---

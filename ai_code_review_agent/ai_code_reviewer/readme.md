# 🚀 AI Code Reviewer (Local LLM + RAG)

An **AI-powered code review system** that analyzes source code using **AST parsing, company coding guidelines, RAG (Retrieval-Augmented Generation), and local LLM models (GGUF)**.

It reviews uploaded code files and returns:

* ✅ Code quality score
* ⚠️ Detected issues
* 💡 Improvement suggestions

This project is designed to evolve into a **company-grade automated code review tool** similar to **SonarQube / DeepSource / Codacy**, but powered entirely by **local AI (offline)**.

---

# ✨ Features

* 📂 Upload code files for automatic review
* 🧠 Automatic language detection (Python / JavaScript)
* 🔍 AST-based code structure parsing
* 📚 RAG-based retrieval of company coding guidelines
* 🤖 Local LLM inference (GGUF via llama.cpp)
* 📊 Structured JSON output (score + issues + summary)
* 🌐 FastAPI backend with interactive docs
* 🔒 Fully offline (no external API required)

---

# 🧠 System Architecture

```
User Uploads Code
        ↓
Language Detection (file_loader)
        ↓
Code Parsing (AST)
        ↓
Extract Structure (functions, variables)
        ↓
RAG → Retrieve Guidelines (ChromaDB)
        ↓
LLM Review (local model)
        ↓
Structured Output (Score + Issues + Summary)
```

---

# 📁 Project Folder Structure (Detailed)

```
ai_code_reviewer/
│
├── run.py
├── load_guidelines.py
├── requirements.txt
│
├── guidelines/
│   ├── python_guidelines.md
│   └── javascript_guidelines.md
│
├── models/
│   └── Qwen2.5-7B-Instruct-Q5_K_M.gguf
│
├── vector_db/
│
├── app/
│   ├── main.py
│
│   ├── api/
│   │   └── routes.py
│
│   ├── agents/
│   │   └── review_agent.py
│
│   ├── llm/
│   │   └── local_llm.py
│
│   ├── parsers/
│   │   ├── python_parser.py
│   │   └── javascript_parser.py   (if present / extendable)
│
│   ├── rag/
│   │   ├── guideline_loader.py
│   │   └── vector_store.py
│
│   ├── utils/
│   │   ├── file_loader.py
│   │   └── repo_scanner.py        (optional)
│
│   ├── models/
│   │   └── schemas.py
│
│   ├── rules/
│   │   ├── python_rules.py        (if added)
│   │   └── javascript_rules.py    (if added)
│
│   └── scoring/
│       └── scoring_engine.py      (if added)
```

---

# 📄 Complete File-by-File Explanation

## 🔹 Root Files

### `run.py`

* Entry point of the project
* Starts FastAPI server using Uvicorn
* Simplifies running the app without long commands

Run:

```
python run.py
```

---

### `load_guidelines.py`

* Converts guideline `.md` files into embeddings
* Stores them in **ChromaDB (vector_db/)**
* Must be run **before first use**

---

### `requirements.txt`

* Contains all dependencies required for the project

---

## 📚 `guidelines/`

### `python_guidelines.md`

### `javascript_guidelines.md`

* Contains company coding standards like:

  * Naming conventions
  * Error handling
  * Code structure
  * Security practices

👉 These are used in **RAG retrieval**

---

## 🤖 `models/`

### `Qwen2.5-7B-Instruct-Q5_K_M.gguf`

Link to Download LLM ( https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF)

* Local LLM model file
* Loaded using `llama-cpp-python`
* Used for generating code review responses

---

## 🧠 `vector_db/`

* Stores embeddings of guidelines
* Created automatically after running:

```
python load_guidelines.py
```

---

# 📦 `app/` (Core Backend)

---

## 🔹 `main.py`

* Initializes FastAPI app
* Registers API routes
* Entry point for backend service

---

## 🔹 `api/routes.py`

Defines API endpoints.

### Main Endpoint:

```
POST /review-code
```

Flow:

1. Accept file upload
2. Detect language
3. Parse code
4. Send to review agent
5. Return response

---

## 🔹 `agents/review_agent.py` ⭐ (CORE)

* Central brain of the system

Responsibilities:

* Retrieve relevant guidelines from vector DB
* Build LLM prompt
* Send code + context to model
* Parse LLM response into valid JSON
* Return structured issues

---

## 🔹 `llm/local_llm.py`

* Handles LLM loading and inference
* Uses:

```
llama-cpp-python
```

Key features:

* Loads model once (memory optimized)
* Sends prompts and gets responses

---

## 🔹 `parsers/python_parser.py`

* Uses **AST (Abstract Syntax Tree)**
* Extracts:

  * functions
  * variables
  * docstrings
  * line numbers
  * function length

---

## 🔹 `parsers/javascript_parser.py` (if used)

* Handles JavaScript parsing
* Can be extended using **Tree-sitter**

---

## 🔹 `utils/file_loader.py`

* Reads uploaded files
* Detects programming language

Example:

```
test.py → python
app.js → javascript
```

---

## 🔹 `models/schemas.py`

* Defines API request & response formats using **Pydantic**

Example response:

```
{
 "score": 85,
 "issues": [],
 "summary": ""
}
```

---

## 🔹 `rag/guideline_loader.py`

* Loads `.md` files
* Splits into chunks
* Prepares them for embedding

---

## 🔹 `rag/vector_store.py`

* Handles ChromaDB operations

Functions:

* Create vector DB
* Load vector DB
* Retrieve relevant rules

---

## 🔹 (Optional Advanced Modules)

### `rules/`

* Static rule-based checks (without LLM)

### `scoring/scoring_engine.py`

* Calculates final code quality score

### `utils/repo_scanner.py`

* Scans entire repositories

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```
git clone <your-repo-url>
cd ai_code_reviewer
```

---

## 2️⃣ Create Virtual Environment

```
python -m venv venv
```

Activate (Windows):

```
venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Add LLM Model

Place model inside:

```
models/
```

Example:

```
Qwen2.5-7B-Instruct-Q5_K_M.gguf
```

---

## 5️⃣ Create Vector DB (IMPORTANT)

```
python load_guidelines.py
```

---

# ▶️ Running the Project

### Option 1 (Simple)

```
python run.py
```

### Option 2 (Manual)

```
uvicorn app.main:app --reload
```

---

# 🌐 API Usage

### Endpoint:

```
POST /review-code
```

### Access Swagger Docs:

```
http://localhost:8000/docs
```

---

## 📥 Example Request

Upload file using Swagger UI or Postman

---

## 📤 Example Response

```
{
 "score": 85,
 "issues": [
  {
   "rule": "function_length",
   "file": "example.py",
   "line": 10,
   "severity": "medium",
   "suggestion": "Break function into smaller units"
  }
 ],
 "summary": "Function exceeds recommended length."
}
```

---

# 🧪 Supported Languages

* ✅ Python
* ✅ JavaScript (extendable)

---

# 💡 Future Improvements

* 🔧 Static rule engine (faster checks)
* 🌳 Tree-sitter JS parser
* 📦 Full repository analysis
* 🔗 GitHub PR integration
* 📊 UI dashboard with code quality heatmaps

---

# 🔥 Why This Project Stands Out

This project combines:

* RAG (Guideline-aware AI)
* AST-based code understanding
* Local LLM inference (offline)
* Scalable FastAPI backend

👉 Making it a **real-world production-grade AI system**, not just a demo.

---

# 👨‍💻 Author

Built as an **AI Code Review Agent + VS Code Extension backend**
Using **Python, FastAPI, LangChain, ChromaDB, and Local LLMs**

---

# 📄 License

MIT License (or your preferred license)

---

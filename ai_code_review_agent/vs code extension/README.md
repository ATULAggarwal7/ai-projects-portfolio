## 🧩 VS Code Extension (AI Code Reviewer)

This project also includes a **VS Code Extension** that allows real-time AI-powered code review directly inside the editor.

---

## ✨ Features of Extension

* 🔍 Analyze code directly in VS Code
* ⚡ Detect errors in **Python & JavaScript**
* 📏 Enforces company coding guidelines (RAG-based)
* 🧠 Uses local LLM for intelligent suggestions
* 🚨 Highlights issues with severity levels
* 🔄 Works with your backend API

---

## 📦 Extension File

The extension is packaged as:

```
ai-code-reviewer-0.0.1.vsix
```

---

## 📥 How to Install (VSIX)

### Step-by-step:

1. Open **VS Code**
2. Go to **Extensions panel** (Ctrl + Shift + X)
3. Click on the **three dots (⋯)** in top-right
4. Select **"Install from VSIX..."**
5. Choose the file:

   ```
   ai-code-reviewer-0.0.1.vsix
   ```
6. Click **Install**
7. Reload VS Code if prompted

---

## ▶️ How to Use

1. Open any **Python (.py)** or **JavaScript (.js)** file
2. Right-click inside the editor OR use command palette:

   ```
   Ctrl + Shift + P → "AI Code Review"
   ```
3. The extension will:

   * Send code to backend API
   * Analyze using LLM + rules
   * Show issues in editor

---

## ⚙️ Extension Architecture

The extension works in combination with the backend:

```
VS Code Extension  →  FastAPI Backend  →  LLM + RAG + Rules Engine
```

### Flow:

1. 📄 User opens code file
2. 📤 Extension sends code to API
3. 🧠 Backend processes using:

   * Parsers
   * Rules
   * RAG (guidelines)
   * LLM
4. 📥 Response returned
5. 🚨 Issues displayed in editor

---

## 🔗 Backend Requirement

⚠️ Make sure backend is running before using extension:

```bash
uvicorn app.main:app --reload
```

Default API:

```
http://127.0.0.1:8000
```

---

## 🛠️ How Extension is Built

* Built using **VS Code Extension API**
* Uses:

  * JavaScript / TypeScript
  * REST API calls to backend
* Packaged using:

  ```bash
  vsce package
  ```

---

## 🧪 Testing the Extension

* Open a file with intentional issues:

  * Missing error handling
  * Bad naming conventions
* Run the extension
   

  1. Open the Command Palette with the shortcut:

     * **Windows/Linux:** `Ctrl+Shift+P`
     * **macOS:** `Cmd+Shift+P`
  2. Select AI Review Code
  3. Wait as the process takes time.

* Verify:

  * Issues appear correctly
  * Severity levels are shown

---

## 🔮 Future Enhancements (Extension)

* Inline fix suggestions
* Auto-fix (one-click)
* Code score display in status bar
* Support for more languages
* Cloud API support

---

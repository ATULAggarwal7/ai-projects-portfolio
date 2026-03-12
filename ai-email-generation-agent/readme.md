# 📧 Email AI Agent

An **AI-powered command line Email Assistant** that can draft professional emails and send them using natural language instructions.

The agent uses a **Large Language Model (LLM)** to understand user intent and decide whether to:

* Generate a professional email
* Send the email using an email tool
* Respond normally to questions

This project demonstrates a **basic AI Agent architecture** including:

* LLM reasoning
* Tool calling
* Structured JSON responses
* Email automation

---

# 🚀 Features

* Generate professional emails from simple prompts
* Automatic email signature enforcement
* AI decision making (send email vs normal response)
* Tool-based architecture
* Safe confirmation before sending emails
* Clean modular project structure

---

# 🧠 How the AI Agent Works

The system follows a **simple AI Agent pipeline**.

```
User Input
   ↓
LLM understands intent
   ↓
LLM returns structured JSON
   ↓
Agent checks action type
   ↓
If action == send_email
   ↓
Email tool executes
```

Example:

User input:

```
Send an email to Rahul saying the meeting is postponed to tomorrow.
```

LLM Output:

```json
{
 "action": "send_email",
 "to_email": "rahul@email.com",
 "subject": "Meeting Postponed",
 "body": "Professional email body..."
}
```

The agent then:

1. Shows preview
2. Asks confirmation
3. Sends the email

---

# 📂 Project Structure

```
Email-AI-Agent
│
├── main.py
├── requirements.txt
├── .env
│
├── agent
│   ├── agent_core.py
│   ├── llm_loader.py
│   └── tool_registry.py
│
├── tools
│   └── email_tool.py
│
├── config
│   └── settings.py
│
└── models
    └── model_download_link.txt
```

---

# 📄 File Explanations

## main.py

**Entry point of the application**

Responsibilities:

* Starts the AI agent
* Takes user input
* Sends input to the agent
* Prints the agent response

Flow:

```
User Input → EmailAgent.run() → Response
```

---

# agent/

Contains the **core AI agent logic**.

---

## agent_core.py

This is the **brain of the agent**.

Responsibilities:

* Builds the **system prompt**
* Sends prompt to LLM
* Parses JSON response
* Detects required action
* Executes tools if required

Main responsibilities:

```
User Input
   ↓
Prompt Creation
   ↓
LLM Generation
   ↓
JSON Parsing
   ↓
Action Execution
```

It also:

* Displays email preview
* Asks user confirmation before sending

---

## llm_loader.py

Handles **loading and running the LLM model**.

Responsibilities:

* Initialize the language model
* Send prompts to the model
* Return generated output

Example function:

```
generate(prompt)
```

This returns the LLM response used by the agent.

---

## tool_registry.py

Acts as a **tool manager**.

Responsibilities:

* Register available tools
* Execute tools when requested by the agent

Example:

```
ToolRegistry.execute(action_data)
```

If the LLM returns:

```
"action": "send_email"
```

The registry calls the email tool.

---

# tools/

Contains **external actions the agent can perform**.

---

## email_tool.py

Responsible for **sending emails**.

Responsibilities:

* Connect to SMTP server
* Authenticate email credentials
* Send the email

Steps:

```
Connect SMTP
Login
Send Email
Return success message
```

---

# config/

Contains **project configuration files**.

---

## settings.py

Stores user configuration such as:

```
USER_FULL_NAME
USER_TITLE
```

These values are automatically inserted into every generated email signature.

Example signature:

```
Best regards,
Atul Aggarwal
AI Engineer
```

---

# models/

Contains information about the **LLM model used**.

---

## model_download_link.txt

Contains the link to download the model required for the agent.

---

# ⚙️ Installation

## 1️⃣ Clone the repository

```
git clone https://github.com/ATULAggarwal7/ai-projects-portfolio
```

```
cd email-ai-agent
```

---

## 2️⃣ Create virtual environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

## 4️⃣ Configure environment variables

Create a `.env` file.

Example:

```
EMAIL=your_email@gmail.com
PASSWORD=your_app_password
```

⚠️ Use **App Password**, not your real Gmail password.

---

# ▶️ Running the Project

Run:

```
python main.py
```

You will see:

```
Starting Email AI Agent...
```

Then type:

```
You: Send an email to Rahul saying the meeting is tomorrow.
```

The agent will generate an email and show preview.

Example:

```
📧 Drafted Email Preview
--------------------------------------------------
To: rahul@email.com
Subject: Meeting Update

Dear Rahul,

The meeting has been scheduled for tomorrow.

Best regards,
Atul Aggarwal
AI Engineer
--------------------------------------------------
```

Then confirmation:

```
Do you want to send this email? (yes/no)
```

---

# 💡 Example Prompts

```
Send an email to my manager about project completion
```

```
Write an email asking for internship opportunity
```

```
Draft a professional email for meeting reschedule
```

---

# 🧩 Technologies Used

* Python
* Large Language Models (LLM)
* SMTP Email Protocol
* JSON Structured Outputs
* AI Agent Architecture

---

# 📌 AI Concepts Demonstrated

This project demonstrates important **AI Agent concepts**:

* Prompt Engineering
* Tool Calling
* LLM Reasoning
* Agent Architecture
* JSON Action Responses

---

# 🔮 Future Improvements

Possible upgrades:

* Gmail API integration
* Contact database
* Email templates
* Voice command support
* Web interface
* Email summarization

---

# 👨‍💻 Author

**Atul Aggarwal**

AI / ML Engineer
Projects focused on **AI Agents, Computer Vision, and Automation**

---

# ⭐ If you like this project

Consider giving the repository a **star** ⭐ on GitHub.

import json
from agent.llm_loader import LLMLoader
from agent.tool_registry import ToolRegistry
from config.settings import USER_FULL_NAME, USER_TITLE

SYSTEM_PROMPT = f"""
You are an AI Email Assistant Agent.

The user's full name is: {USER_FULL_NAME}
The user's professional title is: {USER_TITLE}

IMPORTANT SIGNATURE RULE:
Every professional email MUST end exactly like this:

Best regards,
{USER_FULL_NAME}
{USER_TITLE}

Do NOT omit the title.
Do NOT modify the signature format.
Do NOT use placeholders.

You must ALWAYS respond in valid JSON format.

If the user wants to send an email, respond ONLY in this format:

{{
  "action": "send_email",
  "to_email": "recipient email",
  "subject": "email subject",
  "body": "full professional email body including exact required signature"
}}

If the user is just chatting or asking something else, respond ONLY in this format:

{{
  "action": "none",
  "response": "normal helpful reply"
}}

DO NOT include any text outside JSON.
Return JSON only.
"""


class EmailAgent:

    def __init__(self):
        self.llm = LLMLoader()

    def run(self, user_input: str):

        full_prompt = f"{SYSTEM_PROMPT}\nUser: {user_input}\nAssistant:"

        raw_output = self.llm.generate(full_prompt)

        try:
            action_data = json.loads(raw_output)
        except json.JSONDecodeError:
            return f"⚠️ Model returned invalid JSON:\n{raw_output}"

        # If email action detected
        if action_data.get("action") == "send_email":

            to_email = action_data.get("to_email")
            subject = action_data.get("subject")
            body = action_data.get("body")

            print("\n📧 Drafted Email Preview:")
            print("--------------------------------------------------")
            print(f"To: {to_email}")
            print(f"Subject: {subject}")
            print("\n" + body)
            print("--------------------------------------------------")

            confirmation = input("\nDo you want to send this email? (yes/no): ")

            if confirmation.lower() == "yes":
                result = ToolRegistry.execute(action_data)
                return f"📨 {result}"
            else:
                return "❌ Email sending cancelled."

        return action_data.get("response", "No response generated.")
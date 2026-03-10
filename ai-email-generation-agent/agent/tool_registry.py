from tools.email_tool import send_email


class ToolRegistry:

    @staticmethod
    def execute(action_data: dict):
        action = action_data.get("action")

        if action == "send_email":
            return send_email(
                to_email=action_data.get("to_email"),
                subject=action_data.get("subject"),
                body=action_data.get("body"),
            )

        return "No valid action found."
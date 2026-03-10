from agent.agent_core import EmailAgent


def main():
    print("Starting Email AI Agent...\n")
    agent = EmailAgent()

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.run(user_input)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
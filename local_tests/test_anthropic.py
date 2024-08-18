from anthropic_service.claude_assistant import ClaudeAssistant


def main():
    anthropic = ClaudeAssistant()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q']:
            break

        response, metrics = anthropic.process_message(user_input)
        print(f"Assistant: {response}")
        print("\nPerformance Metrics:")
        for key, value in metrics.items():
            print(f"{key}: {value}")
        print()


if __name__ == "__main__":
    main()
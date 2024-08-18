import asyncio
from anthropic_service.claude_assistant import ClaudeAssistant

async def main():
    anthropic = ClaudeAssistant()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'q']:
            break

        full_response = ""
        async for chunk in anthropic.generate_response(user_input):
            if chunk["type"] == "token":
                print(chunk["content"], end="", flush=True)
                full_response += chunk["content"]
            elif chunk["type"] == "metrics":
                print("\n\nPerformance Metrics:")
                for key, value in chunk["data"].items():
                    print(f"{key}: {value}")
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())
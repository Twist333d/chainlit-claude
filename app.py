import chainlit as cl
from anthropic_service.claude_assistant import ClaudeAssistant
from dotenv import load_dotenv

load_dotenv()

anthropic_service = None


@cl.on_chat_start
async def start():
    global anthropic_service
    anthropic_service = ClaudeAssistant()

    welcome_message = (
        "Welcome to the Anthropic-powered chatbot! "
        "This chat uses Claude 3.5 Sonnet with prompt caching enabled. "
        "Feel free to ask any questions or request assistance with tasks."
        "After each message, prompt caching stats are sent."
        "Try having a long conversation and see how prompt caching helps!"
    )
    await cl.Message(content=welcome_message).send()


@cl.on_message
async def main(message: cl.Message):
    global anthropic_service

    try:
        response, metrics = anthropic_service.process_message(message.content)

        # Send the AI's response
        await cl.Message(content=response).send()

        # Format and send performance metrics
        metrics_message = (
            "Performance Metrics:\n"
            f"• Time taken: {metrics['time_taken']:.2f} seconds\n"
            f"• Input tokens: {metrics['input_tokens']}\n"
            f"• Output tokens: {metrics['output_tokens']}\n"
            f"• Cached input tokens: {metrics['input_tokens_cache_read']}\n"
            f"• New input tokens: {metrics['input_tokens_cache_create']}\n"
            f"• Percentage cached: {metrics['percentage_cached']:.1f}%\n"
            f"• Total input tokens: {metrics['total_input_tokens']}"
        )
        await cl.Message(content=metrics_message).send()

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()



if __name__ == "__main__":
    cl.run()
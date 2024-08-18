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
        "Welcome to the Anthropic-powered chatbot!\n\n"
        "This chat uses Claude 3.5 Sonnet with prompt caching enabled.\n\n"
        "After each message, prompt caching stats are sent.\n\n"
        "Try having a long conversation and see how prompt caching helps!"
    )
    await cl.Message(content=welcome_message).send()


@cl.on_message
async def main(message: cl.Message):
    global anthropic_service

    try:
        msg = cl.Message(content="")
        await msg.send()

        async for chunk in anthropic_service.generate_response_stream(message.content):
            if chunk["type"] == "token":
                await msg.stream_token(chunk["content"])
            elif chunk["type"] == "metrics":
                metrics = chunk["data"]
                metrics_message = (
                    "📊 Performance Metrics:\n"
                    f"⏱️ Time taken: {metrics['time_taken']:.2f} seconds\n"
                    f"📥 User input tokens: {metrics['input_tokens']}\n"
                    f"📤 Output tokens: {metrics['output_tokens']}\n"
                    f"💾 Input tokens (cache read): {metrics['input_tokens_cache_read']}\n"
                    f"🆕 Input tokens (cache create): {metrics['input_tokens_cache_create']}\n"
                    f"📈 {metrics['percentage_cached']:.1f}% of input prompt cached ({metrics['total_input_tokens']} tokens)"
                )
                await cl.Message(content=metrics_message).send()
            else:
                await msg.stream_token(chunk)

        await msg.update()

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()
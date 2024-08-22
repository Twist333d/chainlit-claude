import chainlit as cl
from src.config import load_config
from src.logger import get_logger
from src.handlers.message_handler import handle_message
from src.assistants.claude_assistant import ClaudeAssistant

config = load_config()
logger = get_logger(__name__)
anthropic_service = None

@cl.on_chat_start
async def start():
    global anthropic_service
    anthropic_service = ClaudeAssistant()
    logger.info("Chat started, ClaudeAssistant initialized")

    welcome_message = (
        "👋 Welcome to the Claude 3.5 Sonnet with prompt caching enabled.\n"
        "📖 After each message, prompt caching stats are sent.\n"
        "💬 Try having a long conversation and see how prompt caching saves time & costs!"
    )
    await cl.Message(content=welcome_message).send()

@cl.on_message
async def main(message: cl.Message):
    global anthropic_service
    await handle_message(message, anthropic_service)
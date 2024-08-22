import chainlit as cl
from src.logger import get_logger

logger = get_logger(__name__)

async def handle_message(message: cl.Message, assistant):
    content = message.content
    images = [file for file in message.elements if "image" in file.mime]

    if images:
        file_names = [image.name for image in images]
        logger.info(f"Received images: {', '.join(file_names)}")

    try:
        response_message = cl.Message(content="")
        async for item in assistant.generate_response(content, images):
            if item["type"] == "chunk":
                await response_message.stream_token(item["content"])
            elif item["type"] == "tool_use":
                with cl.Step(name=f"Using tool: {item['name']}") as step:
                    step.input = item['input']
                    step.output = f"URLs parsed: {item['result']['urls_parsed']}"
                    await step.send()
            elif item["type"] == "final":
                await response_message.send()
                metrics = item["metrics"]
                metrics_message = format_metrics_message(metrics)
                await cl.Message(content=metrics_message).send()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        await cl.Message(content=f"An error occurred: {str(e)}").send()

def format_metrics_message(metrics):
    return (
        "📊 *Performance Metrics*:\n"
        f"⏱️  - Time taken: {metrics['time_taken']:.2f} seconds\n"
        f"📥  - User input tokens: {metrics['input_tokens']}\n"
        f"📤  - Output tokens: {metrics['output_tokens']}\n"
        f"💾  - Input tokens (cache read): {metrics['input_tokens_cache_read']}\n"
        f"🆕  - Input tokens (cache create): {metrics['input_tokens_cache_create']}\n"
        f"📈  - {metrics['percentage_cached']:.1f}% of input prompt cached ({metrics['total_input_tokens']} tokens)"
    )
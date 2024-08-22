import anthropic
import os
import time
import yaml
from src.config import load_config
from src.logger import get_logger
from src.utils.image_utils import get_base64_encoded_image, infer_mime_type
from src.tools.firecrawl_search_tool import firecrawl_search_tool, process_tool_call
from datetime import datetime
import io


config = load_config()
logger = get_logger(__name__)


# Initialize the client
class ClaudeAssistant:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(api_key=config['anthropic_api_key'])
        self.model_name = config['model_name']
        self.temperature = config['temperature']
        self.max_tokens = config['max_tokens']
        self.conversation_history = ConversationHistory(config['cached_turns'])
        self.system_message = self._load_system_prompt()
        self.tools = [firecrawl_search_tool]

    def update_system_prompt(self):
        self.system_message = self._load_system_prompt()

    def _load_system_prompt(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        system_prompt_path = os.path.join(base_dir, 'assistants', 'prompts', 'system_prompt.yaml')

        with open(system_prompt_path, 'r') as file:
            prompts = yaml.safe_load(file)

        system_prompt = prompts.get('system_prompt')
        current_datestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        system_prompt = system_prompt.format(current_datestamp=current_datestamp)

        return [
            {
                'type': 'text',
                'text': system_prompt,
                'cache_control': {'type': 'ephemeral'}
            }
        ]

    async def generate_response(self, user_message, images=None):
        content = []

        if images:
            if len(images) > 20:
                error_message = "Error: Cannot process more than 20 images in a single request."
                logger.error(error_message)
                yield {"type": "text", "content": error_message}
                return

            for image in images:
                try:
                    base64_image = get_base64_encoded_image(image.path)
                    mime_type = infer_mime_type(image.name)
                    logger.info(f"File type: {mime_type}")
                    if "Error" in base64_image:
                        logger.error(base64_image)
                        yield {"type": "text", "content": base64_image}
                        return
                    else:
                        content.append({
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": mime_type,
                                "data": base64_image
                            }
                        })
                    logger.info(f"Successfully processed image: {image.name}")
                except Exception as e:
                    error_message = f"Error processing image {image.name}: {str(e)}"
                    logger.error(error_message)
                    yield {"type": "text", "content": error_message}
                    return

        content.append({"type": "text", "text": f"<user_query>{user_message}</user_query>"})
        self.conversation_history.add_turn_user(content)
        start_time = time.time()
        messages = self.conversation_history.get_turns()

        async with self.client.messages.stream(
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_message,
                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
                messages=messages,
                tools=self.tools
        ) as stream:
            tool_use_event = None
            async for event in stream:
                if event.type == "text":
                    yield {"type": "chunk", "content": event.text}

            first_response_full = await stream.get_final_message()

        if first_response_full.stop_reason == "tool_use":
            tool_use = next(block for block in first_response_full.content if block.type == "tool_use")
            tool_result = await process_tool_call(tool_use.name, tool_use.input)
            yield {"type": "tool_use", "name": tool_use.name, "input": tool_use.input, "result": tool_result}

            # Make a second API call with the tool result
            async with self.client.messages.stream(
                model=self.model_name,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
                system=self.system_message,
                tools=self.tools,
                messages=messages + [
                    {"role": "assistant", "content": first_response_full.content},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": str(tool_result),
                            }
                        ],
                    },
                ],) as tool_results_stream:
                        async for event in tool_results_stream:
                            if event.type == "text":
                                yield {"type": "chunk", "content": event.text}

                        second_response_full = await tool_results_stream.get_final_message()



            final_response = "".join([block.text for block in second_response_full.content if hasattr(block, "text")])
        else:
            final_response = "".join([block.text for block in first_response_full.content if hasattr(block, "text")])

        end_time = time.time()
        self.conversation_history.add_turn_assistant(final_response)
        performance_metrics = self._calculate_performance_metrics(first_response_full, start_time, end_time)
        yield {"type": "final", "content": final_response, "metrics": performance_metrics}

    def _calculate_performance_metrics(self, final_message, start_time, end_time):
        elapsed_time = end_time - start_time
        input_tokens = final_message.usage.input_tokens
        output_tokens = final_message.usage.output_tokens
        input_tokens_cache_read = getattr(final_message.usage, 'cache_read_input_tokens', 0)
        input_tokens_cache_create = getattr(final_message.usage, 'cache_creation_input_tokens', 0)

        # Calculate the percentage of input prompt cached
        total_input_tokens = input_tokens + (
            int(input_tokens_cache_read) if input_tokens_cache_read != "---" else 0
        )
        percentage_cached = (
            int(input_tokens_cache_read) / total_input_tokens * 100
            if input_tokens_cache_read != "---" and total_input_tokens > 0
            else 0
        )

        return {
            "time_taken": elapsed_time,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_tokens_cache_read": input_tokens_cache_read,
            "input_tokens_cache_create": input_tokens_cache_create,
            "percentage_cached": percentage_cached,
            "total_input_tokens": total_input_tokens
        }



# Conversation history class
class ConversationHistory:
    def __init__(self, cached_turns=10):
        # initialize an empty list to store conversation turns
        self.turns = []
        self.cached_turns = cached_turns

    def add_turn_assistant(self, content):
        # add assistants turn
        self.turns.append(
            {"role": "assistant", "content": [{"type": "text", "text": content}]}
        )

    def add_turn_user(self, content):
        # add users turn
        self.turns.append(
            {"role": "user", "content": content}
        )

    def get_turns(self):
        # Retrieve conversation history with specific formatting
        result = []
        user_turns_processed = 0

        for turn in reversed(self.turns):
            if turn["role"] == "user" and user_turns_processed < self.cached_turns:
                processed_content = []

                # Iterate through all content items
                for index, item in enumerate(turn["content"]):
                    if item["type"] == "text" and index == len(turn["content"]) - 1:
                        # Add cache_control only to the last text item
                        processed_content.append({
                            "type": "text",
                            "text": item["text"],
                            "cache_control": {"type": "ephemeral"}
                        })
                    else:
                        # Append other content types (e.g., images) without cache_control
                        processed_content.append(item)

                result.append({
                    "role": "user",
                    "content": processed_content,
                })

                user_turns_processed += 1
            else:
                # Add other turns as they are
                result.append(turn)

        return list(reversed(result))

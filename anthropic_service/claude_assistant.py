import anthropic
import os
import time
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Load the system_prompt.yaml file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
system_prompt_path = os.path.join(base_dir, 'anthropic_service', 'prompts', 'system_prompt.yaml')

with open(system_prompt_path, 'r') as file:
    prompts = yaml.safe_load(file)

# Access the system prompt
system_prompt = prompts.get('system_prompt')

# Initialize the client
class ClaudeAssistant:
    def __init__(self, model_name="claude-3-5-sonnet-20240620", max_tokens=8192, temperature=0.75, cached_turns=3):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = ConversationHistory(cached_turns)
        self.system_message = [
            {
                'type' : 'text',
                'text' : system_prompt,
                'cache_control' : {'type' : 'ephemeral'}
            }
        ]

    def generate_response(self, user_message):
        self.conversation_history.add_turn_user(user_message)

        start_time = time.time()

        response = self.client.messages.create(
            model=self.model_name,
            max_tokens=self.max_tokens,
            extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
            system=self.system_message,
            messages=self.conversation_history.get_turns(),

        )

        end_time = time.time()

        assistant_reply = response.content[0].text
        self.conversation_history.add_turn_assistant(assistant_reply)

        performance_metrics = self._calculate_performance_metrics(response, start_time, end_time)

        return assistant_reply, performance_metrics

    def _calculate_performance_metrics(self, response, start_time, end_time):
        elapsed_time = end_time - start_time
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        input_tokens_cache_read = getattr(response.usage, 'cache_read_input_tokens', 0)
        input_tokens_cache_create = getattr(response.usage, 'cache_creation_input_tokens', 0)

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
            {"role": "user", "content": [{"type": "text", "text": content}]}
        )

    def get_turns(self):
        # retrieve conversation history with specific formatting
        result = []
        user_turns_processed = 0
        # iterate through turns in reverse order
        for turn in reversed(self.turns):
            if turn["role"] == "user" and user_turns_processed < self.cached_turns:
                result.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": turn["content"][0]["text"],
                                "cache_control": {
                                    "type": "ephemeral"
                                },  # take the same content
                            }
                        ],
                    }
                )
                user_turns_processed += 1
            else:
                # add other turns as they are
                result.append(turn)
        return list(reversed(result))  # sort back to first to last
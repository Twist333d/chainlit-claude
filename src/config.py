from dotenv import load_dotenv
import os

def load_config():
    load_dotenv()
    return {
        'anthropic_api_key': os.getenv("ANTHROPIC_API_KEY"),
        'model_name': os.getenv("MODEL_NAME", "claude-3-5-sonnet-20240620"),
        'max_tokens': int(os.getenv("MAX_TOKENS", 8192)),
        'temperature': float(os.getenv("TEMPERATURE", 0.75)),
        'cached_turns': int(os.getenv("CACHED_TURNS", 2)),
        'log_level': os.getenv("LOG_LEVEL", "DEBUG"),
    }
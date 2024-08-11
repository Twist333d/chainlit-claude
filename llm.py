from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    # Ensure the API key is set
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is not set.")

    # Set up the LLM with Claude 3.5 Sonnet model
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        stream=True,  # Enable streaming
    )

    return llm


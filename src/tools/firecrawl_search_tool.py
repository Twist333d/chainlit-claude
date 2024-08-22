from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from src.logger import get_logger
from src.config import load_config

logger = get_logger(__name__)
config = load_config()

# Define the Pydantic schema for the tool input
class FireCrawlInput(BaseModel):
    query: str = Field(..., description="The search query to be sent to FireCrawl")

# Define the schema for the tool
firecrawl_search_tool = {
    'name': "firecrawl_search",
    'description': """
    Uses search and scrape functionality to provide up-to-date information from web pages. This tool should be used when you need current information that may not be in your training data, or to verify and update your existing knowledge.

    Key features and usage guidelines:
    1. Input: A single, focused search query string.
    2. Output: Returns a dictionary with 'urls_parsed' (list of scraped URLs) and 'content' (formatted string of scraped content).
    3. Search scope: It automatically searches the web for the query and returns the most relevant results from the top pages in markdown format. The advantage of this endpoint is that it actually scrap each website on the top result so you always get the full content.
    4. When to use: For current / recent events, recent developments, or when you don't have up to date knowledge.
    5. When not to use: For historical information, well-established facts, or topics that don't require up-to-date data.

    Query formulation best practices:
    - Be specific and focused, targeting the core of the user's question.
    - Include key terms, especially for results, outcomes, or current status.
    - Consider the timeline (past, present, future) of the information needed.
    - Avoid overly broad terms or vague phrasings.

    Examples of effective queries:
    - "2024 Paris Olympics medal standings" (for current or future results)
    - "Latest AI breakthroughs in natural language processing 2023"
    - "SpaceX Starship most recent launch outcomes"

    Examples of ineffective queries:
    - "Olympics" (too broad, lacks specificity)
    - "AI advancements" (too vague, no timeframe)
    - "space exploration" (not focused on specific events or outcomes)

    Limitations:
    - The tool does not generate or create new information; it only retrieves existing web content.

    Always analyze and synthesize the search results to provide a coherent and relevant response to the user's query.
    """,
    'input_schema': {
        'type': 'object',
        'properties': {
            'query': {
                'type': 'string',
                'description': "The search query string. Should be concise, focused, and directly related to the user's question."
            }
        },
        'required': ['query'],
    },
    "cache_control": {"type": "ephemeral"}
}

class FireCrawlSearch:
    def __init__(self):
        self.firecrawl = FirecrawlApp()
        self.params = {
            "pageOptions": {
                "onlyMainContent": True,
                "fetchPageContent": True,
                "includeHtml": False,
                "includeRawHtml": False
            },
            "searchOptions": {
                "limit": 3  # Adjust this value as needed
            }
        }


    async def search(self, query: str) -> str:
        try:
            result = self.firecrawl.search(query=query, params=self.params)
            return {
                'urls_parsed' : [item.get('metadata', {}).get('sourceURL') for item in result],
                'content' : self.format_result(result)
            }

        except Exception as e:
            return f"Error occured during search: {str(e)}"

    def format_result(self, result: list) -> str:
        """Takes as input the list of results from firecrawl.
        Returns a formatted string for LLM consumption."""
        if not isinstance(result, list):
            return f"Error: Unexpected result type. Expected list, got {type(result)}. Result: {result}"

        formatted_results = []
        for item in result:
            if not isinstance(item, dict):
                formatted_results.append(f"Error: Unexpected item type. Expected dict, got {type(item)}. Item: {item}")
                continue

            metadata = item.get('metadata', {})
            formatted_item = (f"# {metadata.get('title', 'No Title')} | Source:"
                              f" {metadata.get('sourceURL', 'Unknown')}\n\n")
            formatted_item += "Content:\n\n"
            formatted_item += item.get('markdown', item.get('content', 'No content available'))
            formatted_item += "\n\n---\n\n"
            formatted_results.append(formatted_item)

        return "\n".join(formatted_results) if formatted_results else "No results found."

async def process_tool_call(tool_name: str, tool_input: dict):
    if tool_name == "firecrawl_search":
        searcher = FireCrawlSearch()
        query = tool_input['query']
        return await searcher.search(query)
    else:
        return "Unknown tool"

# List of available tools
tools = [firecrawl_search_tool]
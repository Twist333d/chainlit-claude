import json

from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import asyncio
from pydantic import BaseModel, Field, ValidationError


load_dotenv()

# Define the Pydantic schema for the tool input
class FireCrawlInput(BaseModel):
    query: str = Field(..., description="The search query to be sent to FireCrawl")

# Define the schema for the tool
firecrawl_search_tool = {
    'name': "firecrawl_search",
    'description' : "Uses search and scrape functionality by FireCrawl to provide the scraped data from all result "
                    "pages and compiled into a clean markdown. All technical details are handled by FireCrawl. User "
                    "just needs to submit a relevant search query just as they would to Google.",
    'input_schema': {
        'type' : 'object',
        'properties': {
            'query' : {
                'type' : 'string',
                'description' : "The search query. Should be concise and focused on the specific information needed. "
                                "Avoid overly broad or vague queries."
            }
        },
        'required': ['query'],
    },
    "cache_control": {"type": "ephemeral"}
}

class FireCrawlSearch:
    def __init__(self):
        self.firecrawl = FirecrawlApp()
        """self.params = {
                        "pageOptions": {
                            "onlyMainContent": True,
                            "fetchPageContent": True,
                            "includeHtml": True,
                            "includeRawHtml": True
                        },
                        "searchOptions": {
                            "limit": 123}
                    }"""

    async def search(self, query: str) -> str:
        try:
            result = self.firecrawl.search(query=query)
            return self.format_result(result)
        except ValidationError as e:
            return f"Input validation error: {str(e)}"
        except Exception as e:
            return f"Error occured during search: {str(e)}"

    def format_result(self, result: dict) -> str:
        """Takes as an input the json of the result from firecrawl.
        Returns a formatted string for LLM consumption."""
        if result.get('success'):
            formatted_results = []
            for item in result['data']:
                formatted_item = f"# {item['metadata'].get('title', 'No Title')}\n\n"
                formatted_item += f"Description: {item['metadata'].get('description', 'No description available')}\n\n"
                formatted_item += f"Source: {item['metadata'].get('sourceURL', 'Unknown')}\n\n"
                formatted_item += "Content:\n\n"
                formatted_item += item.get('markdown', 'No content available')
                formatted_item += "\n\n---\n\n"
                formatted_results.append(formatted_item)
            return "\n".join(formatted_results)
        else:
            return "Error: Search was not successful. Please try again."

async def process_tool_call(tool_name: str, tool_input: dict):
    if tool_name == "firecrawl_search":
        searcher = FireCrawlSearch()
        query = tool_input['query']
        return await searcher.search(query)
    else:
        return "Unknown tool"

# List of available tools
tools = [firecrawl_search_tool]
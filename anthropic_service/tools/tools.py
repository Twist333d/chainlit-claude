from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from pydantic import BaseModel, Field


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
            return self.format_result(result)
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
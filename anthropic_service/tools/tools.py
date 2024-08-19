from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import asyncio
from pydantic import BaseModel, Field

load_dotenv()

# Define the Pydantic schema for the tool input
class FireCrawlInput(BaseModel):
    query: str = Field(..., description="The search query to be sent to FireCrawl")

# Define the schema for the tool
firecrawl_schema = {
    'name': "firecrawl_search",
    'description' : "Uses search and scrape functionality by FireCrawl to provide the scraped data from all result "
                    "pages and compiled into a clean markdown. All technical details are handled by FireCrawl. User "
                    "just needs to submit a relevant search query just as they would to Google.",
    'parameters': {
        'type' : 'object',
        'properties': {
            'query' : {
                'type' : 'string',
                'description' : "The search query. Should be concise and focused on the specific information needed. "
                                "Avoid overly broad or vague queries."
            }
        }
    }
}

class FireCrawlSearch:
    def __init__(self):
        self.firecrawl = FirecrawlApp()
        self.params = {
                        'pageOptions' : {
                            'onlyMainContent' : True,
                            'fetchPageContent' : True,
                        },
                        'searchOptions' : {'limit' : 4}
                    }

    async def search(self, query: str) -> str:
        result = self.firecrawl.search(query=query, **self.params)
        return self.format_result(result)

    def format_result(self, results: list) -> str:
        formatted_results = []
        for result in results:
            formatted_results.append(f"Title: {result['title']}\nURL: {result['url']}\nContent: {result['content']}\n")
        return "\n".join(formatted_results)
import asyncio
from tools import FireCrawlSearch

async def test_search():
    searcher = FireCrawlSearch()
    query = "How do I use Supabase anonymous sign in in React?"
    results = await searcher.search(query)
    print(results)

if __name__ == '__main__':
    asyncio.run(test_search())
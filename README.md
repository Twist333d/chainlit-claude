# 🤖 chainlit-claude 💬

This project demonstrates how to use  [Claude](https://docs.anthropic.com/en/docs/welcome) 3.5 Sonnet model with [Chainlit](https://docs.chainlit.io/) for conversational AI and prompt caching capabilities. 

## ✨ Features

- **Prompt Caching:**  Leverage Claude's prompt caching feature to save on token usage and reduce latency, especially in extended conversations.
- **Performance Insights:**  Get detailed metrics on each interaction, including time taken, token usage, and caching efficiency.
- **Streaming output:** Support streaming of response to improve the UX.
- **FireCrawl web search** (NEW) Support intelligent formulating of queries and searching for info on the web. 
- **Support for image uploads** (NEW) Support for image uploads (JPEG, PNG, GIF, or WebP), max of 20 images per 
  request, limitations of Anthropic API apply.

## 🚀 Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/chainlit-claude.git
   cd chainlit-claude 
   ```
 
2. Install Dependencies (Poetry):
   ```python
   poetry install
   ```
3. Set up Environment Variables:
Create a .env file in the root directory.
Add your API keys:
   ```python
   ANTHROPIC_API_KEY=your_api_key
   FIRECRAWL_API_KEY=your_api_key
   ```

4. Run the Application:
   ```python
   chainlit run app.py
   ```

This will start the Chainlit server, and you can access the application in your web browser.

## ⚙️ Usage
Once the application is running, you can start interacting with Claude 3.5 Sonnet through the Chainlit interface.

Type your messages in the chat input.
The application will send your message to Claude and display its response.
After each response, you'll see performance metrics, including prompt caching statistics.
If user request requires additional information -> it intelligently formulates a query and searches on the web.

## 🚧 Open Issues
- None so far -> please report one, if you spot it

## 🙏 Acknowledgments
Anthropic for developing the Claude language model.
Firecrawl for creating a superb LLM search.
Chainlit for providing the conversational AI framework.

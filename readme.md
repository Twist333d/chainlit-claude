# 🤖 chainlit-claude 💬

This project demonstrates how to use  [Claude](https://docs.anthropic.com/en/docs/welcome) 3.5 Sonnet model with [Chainlit](https://docs.chainlit.io/) for conversational AI and prompt caching capabilities. 

## ✨ Features

- **Prompt Caching:**  Leverage Claude's prompt caching feature to save on token usage and reduce latency, especially in extended conversations.
- **Performance Insights:**  Get detailed metrics on each interaction, including time taken, token usage, and caching efficiency.

## 🚀 Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/chainlit-claude.git
   cd chainlit-claude 
   ```
 
2. Install Dependencies:
   ```bash
   poetry install
   Set up Environment Variables:
   ```

3. Create a .env file in the root directory.
Add your Anthropic API key:
   ```bash
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

4. Run the Application:
   ```bash
   chainlit run app.py
   ```

This will start the Chainlit server, and you can access the application in your web browser.

## ⚙️ Usage
Once the application is running, you can start interacting with Claude 3.5 Sonnet through the Chainlit interface.

Type your messages in the chat input.
The application will send your message to Claude and display its response.
After each response, you'll see performance metrics, including prompt caching statistics.

## 🚧 Open Issues
- Streaming Support: Streaming responses from Claude is not yet implemented.
- Cache Breakpoint Handling: The current implementation doesn't handle cache breakpoints optimally after 4 turns.

## 🙏 Acknowledgments
Anthropic for developing the Claude language model.
Chainlit for providing the conversational AI framework.
# Chainlit AI Assistant

This project is a Chainlit-based AI assistant that uses the Claude 3.5 Sonnet model to provide comprehensive coding support, project management assistance, and data analysis.

## Features

- Interactive AI assistant powered by Claude 3.5 Sonnet
- Conversation memory to maintain context
- Customizable system prompts
- Streaming responses for real-time interaction

## Installation

1. Clone this repository:
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

Raw code

2. Install the required dependencies:
pip install -r requirements.txt

Raw code

3. Set up your environment variables:
Create a `.env` file in the project root and add your Anthropic API key:
ANTHROPIC_API_KEY=your_api_key_here

Raw code

## Usage

To start the Chainlit app, run:

chainlit run app.py

Raw code

Then open your web browser and navigate to `http://localhost:8000` to interact with the AI assistant.

## Configuration

The system prompt for the AI assistant can be customized by editing the `prompts.yaml` file.

## Dependencies

- chainlit
- langchain
- langchain_anthropic
- python-dotenv
- pyyaml

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
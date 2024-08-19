- add tool definition schema into Anthropic class
  - {
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"],
        "description": "The unit of temperature, either 'celsius' or 'fahrenheit'"
      }
    },
    "required": ["location"]
  }
}
Scope
- define Pydantic class for the firecrawl inputs:
  - query: str (and that is it?)
- define the schema with super detailed instructions
- implement function to search and return the results
  - Takes as an input the query
  - Outputs the content of the search
- Process tool_call function
  - if tool_name == 'firecrawl_search':
    - it summarizes the question it wants to search
    - formulates a query that is the most suitable
    - searches it using the function defined above
    - returns the result
- generate the response:
  - check message.stop_reason
    - use the tool
    - get the result
    - process the tool result with additional response call
  - provide final result to the user

- Add support for steps:
  - App.py
    - Add a step specifically referring to tool use (cl.step) (in )
    - Call the step function in the main function of chainlit, if step is called. I think some changes are needed in
      ```python
      try:
          response_message = cl.Message(content="")
          async for item in anthropic_service.generate_response(message.content):
              if item["type"] == "chunk":
                  await response_message.stream_token(item["content"])
              elif item["type"] == "final":
                  await response_message.send()
    
  - claude_assistant.py
    - Not sure if any changes are needed?
  - tools.py
    - However, I don't want to stream the full results of the tool (that's too much.) Tool output should be:
        - Summary statistics:
          - Which URLs are parsed? 

- Add ability to upload files
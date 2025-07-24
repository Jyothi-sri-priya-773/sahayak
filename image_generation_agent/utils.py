# # utils.py
# from google.adk.runners import Runner
# from google.adk.events import Event # Import Event
# from google.genai import types # Import types to create Content objects and access Part structure

# async def call_agent_async(runner: Runner, user_id: str, session_id: str, query: str):
#     """
#     Calls the ADK agent and processes its output events.

#     Args:
#         runner (Runner): The ADK Runner instance.
#         user_id (str): The ID of the current user.
#         session_id (str): The ID of the current session.
#         query (str): The user's input query (plain string).
#     """
#     print("\n--- Running Query ---")
#     try:
#         # Create a types.Content object from the user's query string.
#         user_content_message = types.Content(parts=[types.Part(text=query)])

#         # Call runner.run_async using keyword arguments as required by its signature.
#         async for event in runner.run_async(
#             user_id=user_id,
#             session_id=session_id,
#             new_message=user_content_message,
#         ):
#             # The Event object itself is an LlmResponse, so its content is in event.content
#             if event.content and event.content.parts:
#                 for part in event.content.parts:
#                     if part.text:
#                         # This part contains plain text output from the LLM.
#                         print(f"Agent: {part.text}")
#                     elif part.function_call:
#                         # This part indicates the agent wants to call a tool.
#                         print(f"Agent decided to call tool: {part.function_call.name}({part.function_call.args})")
#                     elif part.function_response:
#                         # This part contains the response from a tool call.
#                         # The output of the tool is within function_response.response.
#                         # For image generation, the image URL will be in this response.
#                         tool_response_output = part.function_response.response

#                         if isinstance(tool_response_output, str) and tool_response_output.startswith("data:image/png;base64,"):
#                             print("\n--- Generated Image ---")
#                             print("Image URL (copy and paste into browser):")
#                             print(tool_response_output) # This will print the long base64 URL
#                             print("-----------------------\n")
#                         else:
#                             # Handle other types of tool responses (e.g., JSON, other text)
#                             print(f"Tool Response: {tool_response_output}")
#                     # You can add more checks for other part types if needed, e.g., part.code_execution_result
#             elif event.actions:
#                 # Events can also contain actions without direct content, e.g., state updates
#                 # For now, we'll just acknowledge them if they are not handled above.
#                 if event.actions.state_delta:
#                     print(f"Agent updated state: {event.actions.state_delta}")
#                 # Add other action types if relevant
#             # Note: The Event class itself doesn't have a direct 'error' attribute as a top-level field.
#             # Errors typically manifest as text output from the LLM or exceptions caught in the runner.
#             # If the LLM generates an error message, it would come through as part.text.

#     except Exception as e:
#         # Catch any unexpected exceptions that might occur during the agent's run.
#         print(f"An unexpected error occurred during agent run: {e}")
#     print("--- Query Finished ---")



# utils.py
import os
import base64 # Import base64 for decoding
import uuid # For unique IDs for filenames
from google.adk.runners import Runner
from google.adk.events import Event
from google.genai import types

async def call_agent_async(runner: Runner, user_id: str, session_id: str, query: str):
    """
    Calls the ADK agent and processes its output events.

    Args:
        runner (Runner): The ADK Runner instance.
        user_id (str): The ID of the current user.
        session_id (str): The ID of the current session.
        query (str): The user's input query (plain string).
    """
    print("\n--- Running Query ---")
    try:
        user_content_message = types.Content(parts=[types.Part(text=query)])

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content_message,
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent: {part.text}")
                    elif part.function_call:
                        print(f"Agent decided to call tool: {part.function_call.name}({part.function_call.args})")
                    elif part.function_response:
                        tool_response_output = part.function_response.response

                        if isinstance(tool_response_output, str) and tool_response_output.startswith("data:image/png;base64,"):
                            # --- NEW: Decode and Save Image to Local File ---
                            image_base64_data = tool_response_output.split(',')[1] # Get base64 part
                            image_binary_data = base64.b64decode(image_base64_data)

                            # Attempt to extract a clean topic for the filename
                            image_topic_raw = query.replace("create image of ", "").replace("generate image of ", "").strip()
                            # Basic sanitization for filename
                            image_topic = "".join(c for c in image_topic_raw if c.isalnum() or c in (' ', '_')).strip()
                            if not image_topic:
                                image_topic = "generated_image"
                            # Replace spaces with underscores and append a unique ID to avoid overwriting
                            filename = f"{image_topic.replace(' ', '_')}_{uuid.uuid4().hex[:8]}.png"

                            try:
                                with open(filename, "wb") as f:
                                    f.write(image_binary_data)
                                print(f"\n--- Image Saved Locally ---")
                                print(f"Image successfully saved as: {filename}")
                                print(f"You can find it in your current directory: {os.getcwd()}")
                                print("---------------------------\n")
                            except Exception as file_error:
                                print(f"Error saving image to file: {file_error}")
                                print("--- Image Generation Complete (but save failed) ---\n")
                        else:
                            print(f"Tool Response: {tool_response_output}")
            elif event.actions:
                if event.actions.state_delta:
                    print(f"Agent updated state: {event.actions.state_delta}")

    except Exception as e:
        print(f"An unexpected error occurred during agent run: {e}")
    print("--- Query Finished ---")
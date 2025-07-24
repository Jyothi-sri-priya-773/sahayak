


# # image_agent/agent.py
# import os
# import aiohttp
# import base64
# import re

# from google.adk.agents import LlmAgent, InvocationContext
# from google.adk.agents.readonly_context import ReadonlyContext
# from google.adk.agents.callback_context import CallbackContext
# from google.adk.models import Gemini, LlmRequest, LlmResponse # LlmResponse is correctly imported
# from google.adk.events import Event, EventActions
# from google.adk.tools import FunctionTool

# from typing import AsyncGenerator, Optional, Union, Awaitable

# from google.genai import types # types is correctly imported

# # --- Configuration for Image Generation API ---
# IMAGE_GENERATION_MODEL = "imagen-3.0-generate-002"
# IMAGE_GENERATION_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model_id}:predict?key={api_key}"

# # --- Tool Function for Image Generation ---
# async def generate_image_tool(topic: str) -> str:
#     """
#     Generates an image based on the given topic using the Imagen API.
#     This function acts as a tool that the LlmAgent can call.

#     Args:
#         topic (str): The subject or theme for the image to be generated.

#     Returns:
#         str: A base64 encoded image URL (data:image/png;base64,...) if successful,
#              or an error message string if image generation fails.
#     """
#     api_key = os.getenv("GOOGLE_API_KEY")
#     if not api_key:
#         return "Error: Google API Key not found. Please ensure GOOGLE_API_KEY is set in your .env file."

#     api_url = IMAGE_GENERATION_API_URL_TEMPLATE.format(model_id=IMAGE_GENERATION_MODEL, api_key=api_key)

#     payload = {
#         "instances": {
#             "prompt": topic
#         },
#         "parameters": {
#             "sampleCount": 1
#         }
#     }

#     try:
#         async with aiohttp.ClientSession() as session:
#             async with session.post(api_url, json=payload) as response:
#                 response.raise_for_status()
#                 result = await response.json()

#                 if result.get("predictions") and len(result["predictions"]) > 0 and result["predictions"][0].get("bytesBase64Encoded"):
#                     image_base64 = result["predictions"][0]["bytesBase64Encoded"]
#                     image_url = f"data:image/png;base64,{image_base64}"
#                     return image_url
#                 else:
#                     return f"Error: Could not generate image for topic '{topic}'. Unexpected API response structure."
#     except aiohttp.ClientError as e:
#         return f"Error connecting to image generation API: {e}. Please check your network and API key."
#     except Exception as e:
#         return f"An unexpected error occurred during image generation: {e}"

# # --- Callback to Intercept Image Generation Requests ---
# async def check_and_call_image_tool(
#     callback_context: CallbackContext, llm_request: LlmRequest
# ) -> Optional[LlmResponse]:
#     """
#     Checks the user's latest message for image generation keywords.
#     If found, it constructs and returns an LlmResponse with a FunctionCall,
#     bypassing the LLM's text generation for that turn.
#     """
#     print("\n--- Running before_model_callback ---") # Debugging print

#     ctx: InvocationContext = callback_context._invocation_context
#     user_message_content = ctx.user_content

#     user_message_text = ""
#     if user_message_content and user_message_content.parts:
#         for part in user_message_content.parts:
#             if part.text:
#                 user_message_text += part.text

#     print(f"User Message captured by callback: '{user_message_text}'") # Debugging print

#     if not user_message_text:
#         print("Callback: No user message text found. Returning None.") # Debugging print
#         return None

#     user_message_lower = user_message_text.lower()

#     image_patterns = [
#         r"\bcreate image of\b", r"\bgenerate image of\b", r"\bdraw a picture of\b",
#         r"\bshow me an image of\b", r"\bpicture of\b", r"\bimage of\b",
#         r"\bmake image of\b", r"\bgenerate a\b", r"\bcreate a\b"
#     ]

#     topic = None
#     for pattern in image_patterns:
#         match = re.search(pattern, user_message_lower)
#         if match:
#             topic = user_message_text[match.end():].strip()
#             break

#     if topic:
#         if not topic:
#             topic = user_message_text.strip()

#         print(f"Callback: Keyword matched. Extracted topic: '{topic}'. Triggering tool.") # Debugging print

#         function_call = types.FunctionCall(
#             name="generate_image_tool",
#             args={"topic": topic}
#         )

#         # CORRECTED: Changed 'contents' to 'content' (singular)
#         return LlmResponse(
#             content=types.Content( # This should be 'content', not 'contents'
#                 parts=[types.Part(function_call=function_call)],
#                 role="model" # Role is still needed for a valid Content object
#             )
#         )
#     else:
#         print("Callback: No image generation keyword found. Returning None.") # Debugging print
#         return None

# # --- Define the LlmAgent for Image Generation ---
# image_generator_agent = LlmAgent(
#     name="image_generator_agent",
#     model=Gemini(model="gemini-1.5-flash-latest"),
#     instruction=(
#         "You are an image generation service. "
#         "Your primary role is to facilitate image creation. "
#         "If the user asks for something that cannot be visualized or is inappropriate, politely decline "
#         "by saying 'I cannot generate an image for that request.' and explain why. "
#         "Otherwise, your behavior is guided by the 'before_model_callback' to generate images."
#     ),
#     tools=[
#         FunctionTool(func=generate_image_tool)
#     ],
#     before_model_callback=check_and_call_image_tool
# )




# image_agent/agent.py
import os
import aiohttp
import base64
import re

from google.adk.agents import LlmAgent, InvocationContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import Gemini, LlmRequest, LlmResponse
from google.adk.events import Event, EventActions
from google.adk.tools import FunctionTool

from typing import AsyncGenerator, Optional, Union, Awaitable

from google.genai import types

# --- Configuration for Image Generation API ---
IMAGE_GENERATION_MODEL = "imagen-3.0-generate-002"
IMAGE_GENERATION_API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/{model_id}:predict?key={api_key}"

# --- Tool Function for Image Generation ---
async def generate_image_tool(topic: str) -> str:
    """
    Generates an image based on the given topic using the Imagen API.
    This function acts as a tool that the LlmAgent can call.

    Args:
        topic (str): The subject or theme for the image to be generated.

    Returns:
        str: A base64 encoded image URL (data:image/png;base64,...) if successful,
             or an error message string if image generation fails.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: Google API Key not found. Please ensure GOOGLE_API_KEY is set in your .env file."

    api_url = IMAGE_GENERATION_API_URL_TEMPLATE.format(model_id=IMAGE_GENERATION_MODEL, api_key=api_key)

    payload = {
        "instances": {
            "prompt": topic
        },
        "parameters": {
            "sampleCount": 1
        }
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                response.raise_for_status()
                result = await response.json()

                if result.get("predictions") and len(result["predictions"]) > 0 and result["predictions"][0].get("bytesBase64Encoded"):
                    image_base64 = result["predictions"][0]["bytesBase64Encoded"]
                    image_url = f"data:image/png;base64,{image_base64}"
                    return image_url
                else:
                    return f"Error: Could not generate image for topic '{topic}'. Unexpected API response structure."
    except aiohttp.ClientError as e:
        return f"Error connecting to image generation API: {e}. Please check your network and API key."
    except Exception as e:
        return f"An unexpected error occurred during image generation: {e}"

# --- Callback to Intercept Image Generation Requests ---
async def check_and_call_image_tool(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Checks the user's latest message for image generation keywords.
    If found, it constructs and returns an LlmResponse with a FunctionCall,
    bypassing the LLM's text generation for that turn.
    """
    print("\n--- Running before_model_callback ---") # Debugging print

    ctx: InvocationContext = callback_context._invocation_context
    user_message_content = ctx.user_content

    user_message_text = ""
    if user_message_content and user_message_content.parts:
        for part in user_message_content.parts:
            if part.text:
                user_message_text += part.text

    print(f"User Message captured by callback: '{user_message_text}'") # Debugging print

    if not user_message_text:
        print("Callback: No user message text found. Returning None.") # Debugging print
        return None

    user_message_lower = user_message_text.lower()

    # CORRECTED: More flexible image patterns
    image_patterns = [
        r"(?:create|generate|draw|show me a|make a)\s+(?:image|picture|drawing)\s+of\s+(.*)", # e.g., "create image of X"
        r"(?:create|generate|draw|make)\s+(.*)\s+(?:image|picture|drawing)", # e.g., "generate X image"
        r"(?:image|picture|drawing)\s+of\s+(.*)", # e.g., "image of X"
        r"show me (.*)\s+(?:image|picture|drawing)", # e.g., "show me X image"
        r"generate\s+(.*)", # Broad catch for "generate X"
        r"create\s+(.*)", # Broad catch for "create X"
    ]

    topic = None
    for pattern in image_patterns:
        match = re.search(pattern, user_message_lower)
        if match and match.group(1): # Ensure group 1 (the topic) exists
            topic = match.group(1).strip()
            break

    if topic:
        print(f"Callback: Keyword matched. Extracted topic: '{topic}'. Triggering tool.") # Debugging print

        function_call = types.FunctionCall(
            name="generate_image_tool",
            args={"topic": topic}
        )

        return LlmResponse(
            content=types.Content(
                parts=[types.Part(function_call=function_call)],
                role="model" # Role is needed for a valid Content object
            )
        )
    else:
        print("Callback: No image generation keyword found. Returning None.") # Debugging print
        return None

# --- Define the LlmAgent for Image Generation ---
image_generator_agent = LlmAgent(
    name="image_generator_agent",
    model=Gemini(model="gemini-1.5-flash-latest"),
    instruction=(
        "You are an image generation service. "
        "Your primary role is to facilitate image creation. "
        "If the user asks for something that cannot be visualized or is inappropriate, politely decline "
        "by saying 'I cannot generate an image for that request.' and explain why. "
        "Otherwise, your behavior is guided by the 'before_model_callback' to generate images."
    ),
    tools=[
        FunctionTool(func=generate_image_tool)
    ],
    before_model_callback=check_and_call_image_tool
)
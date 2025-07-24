from google.genai import types
from google.adk.sessions import BaseSessionService

async def call_agent_async(runner, user_id, session_id, query):
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print("\n--- Running Query ---")
    final_response_text = None

    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(f"AI: {part.text.strip()}")
                    final_response_text = part.text.strip()

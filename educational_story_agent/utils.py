from google.genai import types

async def call_agent_async(runner, user_id, session_id, query):
    print(f"\n--- Running Query: {query} ---")
    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response = None

    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        final_response = part.text.strip()
                        print(f"\n📘 Story Generated:\n{final_response}\n")
    except Exception as e:
        print(f"Error during agent execution: {e}")

    return final_response
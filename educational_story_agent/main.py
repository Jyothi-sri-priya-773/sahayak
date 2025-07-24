import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

from story_agent import story_teacher_agent
from utils import call_agent_async

load_dotenv()

# Create in-memory session store (not persistent)
session_service = InMemorySessionService()

# Define initial session state
initial_state = {
    "user_name": "Educator",
    "topic": "",
    "lesson": ""
}

async def main_async():
    app_name = "StoryTeachingApp"
    user_id = "educator001"

    # Create session
    session = await session_service.create_session(app_name=app_name, user_id=user_id, state=initial_state)
    session_id = session.id
    print(f"Session started with ID: {session_id}")

    # Setup runner
    runner = Runner(agent=story_teacher_agent, app_name=app_name, session_service=session_service)

    # Chat loop
    print("\nWelcome to the Story Teaching Agent!")
    print("Type 'exit' at any point to quit.\n")

    while True:
        topic = input("Enter a topic for the story: ")
        if topic.lower() == "exit":
            break

        lesson = input("Enter the lesson to teach: ")
        if lesson.lower() == "exit":
            break

        # Build input prompt
        user_input = f"Create a story about '{topic}' that teaches: '{lesson}'"

        await call_agent_async(runner, user_id, session_id, user_input)

if __name__ == "__main__":
    asyncio.run(main_async())
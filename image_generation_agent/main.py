# main.py
import asyncio
import os
from dotenv import load_dotenv
from image_agent.agent import image_generator_agent # Correct import for the image agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async # Assuming utils.py is available

load_dotenv()

APP_NAME = "ImageGeneratorApp" # A unique name for your image generation app
USER_ID = "image_user_001"
DB_URL = os.getenv("DB_URL")

# Setup persistent session
session_service = DatabaseSessionService(db_url=DB_URL)

initial_state = {
    "user_name": "Image User",
    "interaction_history": [],
}

async def main_async():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    session_id = session.id
    print(f"Created session: {session_id}")
    print("Ask me to generate an image (e.g., 'create an image of a flying car', type 'exit' to quit):")

    while True:
        query = input("You: ")
        if query.strip().lower() in ["exit", "quit"]:
            break
        await call_agent_async(runner, USER_ID, session_id, query)

runner = Runner(
    agent=image_generator_agent, # This points to your image generation agent
    app_name=APP_NAME,
    session_service=session_service,
)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from image_agent import image_teacher_agent
from utils import call_agent_async
from dotenv import load_dotenv

load_dotenv()

session_service = InMemorySessionService()
APP_NAME = "ImageAssignmentBot"
USER_ID = "student_01"

initial_state = {
    "assignments": []
}

async def main_async():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state
    )
    SESSION_ID = session.id
    print(f"Created session: {SESSION_ID}")

    runner = Runner(agent=image_teacher_agent, app_name=APP_NAME, session_service=session_service)

    print("Upload an image for your assignment. Type 'exit' to quit.")
    while True:
        img_path = input("Image path: ").strip()
        if img_path.lower() in ["exit", "quit"]:
            break

        await call_agent_async(runner, USER_ID, SESSION_ID, img_path, is_image=True)

if __name__ == "__main__":
    asyncio.run(main_async())
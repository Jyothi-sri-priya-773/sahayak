


import asyncio
import os
from dotenv import load_dotenv
from memory_agent.agent import memory_agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async
import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

load_dotenv()

APP_NAME = "TextbookQA"
USER_ID = "student_001"
DB_URL = os.getenv("DB_URL")

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Extract text from PDF (OCR fallback)
def extract_text_from_pdf(file_path):
    text = ""

    # Try text extraction
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print("PyPDF2 failed:", e)

    # Fallback to OCR if above failed or gave low content
    if len(text.strip()) < 100:
        print("Using OCR fallback...")
        images = convert_from_path(file_path)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text.strip()

# Load textbook content
pdf_path = os.path.join(os.getcwd(), "textbook.pdf")
textbook_content = extract_text_from_pdf(pdf_path)
print("✅ Extracted textbook length:", len(textbook_content))
print("📄 Sample content:\n", textbook_content[:300])


# Setup persistent session
session_service = DatabaseSessionService(db_url=DB_URL)

initial_state = {
    "user_name": "Student",
    "interaction_history": [],
    "textbook": textbook_content,
}

async def main_async():
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state=initial_state,
    )
    session_id = session.id
    print(f"Created session: {session_id}")
    print("Ask a question about the textbook (type 'exit' to quit):")

    while True:
        query = input("You: ")
        if query.strip().lower() in ["exit", "quit"]:
            break
        await call_agent_async(runner, USER_ID, session_id, query)

runner = Runner(
    agent=memory_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()

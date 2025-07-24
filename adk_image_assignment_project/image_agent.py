# image_agent.py
from google.adk.agents import Agent
from PIL import Image
import io
import base64

def analyze_image_base64(image_base64: str) -> str:
    """Analyzes a base64 encoded image and generates a short assignment."""
    try:
        image_bytes = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(image_bytes))
        width, height = img.size
        mode = img.mode
        format = img.format

        return (
            f"Assignment based on uploaded image:\n"
            f"- Image Format: {format}\n"
            f"- Dimensions: {width} x {height}\n"
            f"- Color Mode: {mode}\n\n"
            f"Write a paragraph describing what the image might represent."
        )
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

image_teacher_agent = Agent(
    name="image_teacher_agent",
    model="gemini-1.5-flash-latest",
    instruction="When a base64-encoded image is received, analyze it and prepare a relevant assignment for students.",
    tools=[analyze_image_base64],
)
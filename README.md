# Sahayak - Educational Assistant

## Installation

### Prerequisites
- Python 3.12
- Git
- Tesseract OCR

### 1. Clone the repository
```bash
git clone https://github.com/Jyothi-sri-priya-773/sahayak.git
cd sahayak
```

### 2. Install Python dependencies
```bash
pip install google-adk==1.7.0 python-dotenv aiohttp Pillow
```

### 3. Install Tesseract OCR

**Windows (using Chocolatey):**
```bash
choco install tesseract
```

**macOS (using Homebrew):**
```bash
brew install tesseract
```

### 4. Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey) and sign in with your Google account
2. Click on "Create API key"
3. Copy the generated API key
4. Create a `.env` file in the project root and add:
```
GEMINI_API_KEY=your_api_key_here
```

## Running the Applications

### Image Generation Agent
```bash
cd image_generation_agent
python main.py
```

### Educational Story Agent
```bash
cd educational_story_agent
python main.py
```

### Educational QA Agent
```bash
cd educational_qa_agent
python main.py
```

### ADK Image Assignment Project
```bash
cd adk_image_assignment_project
python main.py
```


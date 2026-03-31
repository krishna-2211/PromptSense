# PromptSense

PromptSense is a context-aware LLM instruction optimizer that helps users turn vague intent into structured, high-quality prompts for better LLM outputs.

## Tech Stack
- React + Vite + Tailwind CSS
- Python + FastAPI
- MCP-based architecture

## Current Features
- Prompt type classification
- Missing context detection
- Intelligent prompt optimization
- Confidence scoring
- Expected output preview
- Variants generation

## Run Locally

### Frontend
```bash
cd frontend
npm install
npm run dev
```
### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

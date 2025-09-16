# Voice Compare API

This is a FastAPI service to compare two voice samples using Resemblyzer and SpeechBrain.

## Local Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

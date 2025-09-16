# Voice Compare API

This is a simple FastAPI app to test deployment on Render.

## Local Run
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Deploy on Render
1. Push this code to GitHub.
2. Create a new **Web Service** on Render.
3. Use `uvicorn main:app --host 0.0.0.0 --port 10000` as the Start Command.
4. Done!
```


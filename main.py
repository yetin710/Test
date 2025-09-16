from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CompareRequest(BaseModel):
    text1: str
    text2: str

@app.get("/")
def root():
    return {"message": "Voice Compare API is running on Render!"}

@app.post("/compare")
def compare(req: CompareRequest):
    # Dummy similarity logic
    similarity1 = len(req.text1) / (len(req.text2) + 1)
    similarity2 = len(req.text2) / (len(req.text1) + 1)
    result = similarity1 >= 0.6 and similarity2 >= 0.7
    return {
        "similarity1": similarity1,
        "similarity2": similarity2,
        "same_speaker": result
    }

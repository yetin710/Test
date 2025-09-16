import os
import base64
import uuid
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from resemblyzer import VoiceEncoder, preprocess_wav
from speechbrain.inference import SpeakerRecognition
from speechbrain.utils.fetching import LocalStrategy
from numpy import dot
from numpy.linalg import norm

app = FastAPI()

encoder = VoiceEncoder()
verification = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="pretrained_models/spkrec-ecapa-voxceleb",
    local_strategy=LocalStrategy.COPY
)

API_KEY = "7aP9Kx!kmtuQ2mL8vN0tB6fJ1yh22230pri"  # <-- replace with your own key

class VoiceCompareRequest(BaseModel):
    voice1_base64: str
    voice2_base64: str

def decode_to_wav(base64_str):
    # Use /tmp folder for cloud compatibility instead of C:/voice
    temp_path = os.path.join("/tmp", f"temp_{uuid.uuid4().hex}.wav")
    with open(temp_path, "wb") as f:
        f.write(base64.b64decode(base64_str))
    return temp_path

@app.post("/compare")
async def compare_voices(
    request: VoiceCompareRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized: Invalid API key")

    try:
        file1 = decode_to_wav(request.voice1_base64)
        file2 = decode_to_wav(request.voice2_base64)

        wav1 = preprocess_wav(file1)
        wav2 = preprocess_wav(file2)
        embed1, embed2 = encoder.embed_utterance(wav1), encoder.embed_utterance(wav2)
        similarity1 = float(dot(embed1, embed2) / (norm(embed1) * norm(embed2)))

        score, _ = verification.verify_files(file1, file2)
        similarity2 = float(score)

        result = similarity1 >= 0.6 and similarity2 >= 0.7

        os.remove(file1)
        os.remove(file2)

        return {
            "similarity_resemblyzer": round(similarity1, 4),
            "similarity_speechbrain": round(similarity2, 4),
            "same_speaker": result
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

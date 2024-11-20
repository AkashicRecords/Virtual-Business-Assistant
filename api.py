from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel

app = FastAPI()

@app.post("/process-voice/")
async def process_voice(audio_file: UploadFile):
    # Process voice command
    return {"status": "success"} 
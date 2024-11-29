"""Voice Processing API"""
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Dict, Any, Optional
import io
import speech_recognition as sr
from .service import VoiceProcessor

app = FastAPI()
processor = VoiceProcessor()

class ProcessingResponse(BaseModel):
    text: str
    intent: str
    confidence: float
    entities: Dict[str, Any]
    context: Dict[str, Any]

@app.post("/process_voice", response_model=ProcessingResponse)
async def process_voice(audio_file: UploadFile = File(...)):
    """Process voice audio file"""
    # Read audio file
    audio_data = await audio_file.read()
    
    # Convert to audio format recognizer can use
    recognizer = sr.Recognizer()
    with io.BytesIO(audio_data) as audio_file:
        audio = recognizer.record(audio_file)
    
    # Process audio
    result = processor.process_audio(audio)
    
    if result:
        return ProcessingResponse(
            text=result.text,
            intent=result.intent,
            confidence=result.confidence,
            entities=result.entities,
            context=result.context
        )
    else:
        return ProcessingResponse(
            text="",
            intent="error",
            confidence=0.0,
            entities={},
            context={}
        )

@app.post("/update_context")
async def update_context(context: Dict[str, Any]):
    """Update conversation context"""
    processor.update_context(context)
    return {"status": "success"} 
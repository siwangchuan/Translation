from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(title="AI Translation Assistant")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "auto"
    target_lang: str = "zh"

class TranslationResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str

@app.get("/")
async def root():
    return {"message": "AI Translation Assistant API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text from source language to target language
    """
    # Placeholder for actual translation logic
    # In production, this would call Aliyun API or other translation service
    api_key = os.getenv("ALIYUN_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ALIYUN_API_KEY not configured")
    
    # Mock translation for demonstration
    translated = f"[Translated from {request.source_lang} to {request.target_lang}]: {request.text}"
    
    return TranslationResponse(
        translated_text=translated,
        source_lang=request.source_lang,
        target_lang=request.target_lang
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

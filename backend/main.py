from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from config import config
from agents.hr_assistant import HRAssistant

app = FastAPI(title="CoreMind AI Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for now to avoid issues, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Agents
hr_agent = HRAssistant()

class ChatRequest(BaseModel):
    question: str
    overrideConfig: Optional[dict] = None

@app.get("/")
async def root():
    return {"status": "running", "service": "CoreMind AI Backend"}

@app.post("/api/v1/prediction/{chatflow_id}")
async def chat(
    chatflow_id: str,
    question: str = Form(None),
    files: UploadFile = File(None),
    # Flowise compatible fields
    overrideConfig: str = Form(None) 
    # Note: In a real Flowise replacement, we'd parse the JSON string in overrideConfig
):
    """
    Endpoint compatible with Flowise API structure.
    """
    try:
        # Parse session_id from overrideConfig if possible, or use default
        session_id = "default"
        # Simple parsing logic (in real app, use json.loads)
        if overrideConfig and "sessionId" in overrideConfig:
            import json
            try:
                config_dict = json.loads(overrideConfig)
                session_id = config_dict.get("sessionId", "default")
            except:
                pass

        # Handle file
        file_content = None
        filename = None
        if files:
            file_content = await files.read()
            filename = files.filename

        # Route to appropriate agent based on chatflow_id or default to HR
        # For now, we only have HR Agent
        response = await hr_agent.process_message(
            message=question or "",
            session_id=session_id,
            file=file_content,
            filename=filename
        )
        
        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# JSON body handler for text-only requests (Flowise compatibility)
@app.post("/api/v1/prediction/{chatflow_id}/json")
async def chat_json(chatflow_id: str, request: ChatRequest):
    try:
        session_id = "default"
        if request.overrideConfig:
            session_id = request.overrideConfig.get("sessionId", "default")
            
        response = await hr_agent.process_message(
            message=request.question,
            session_id=session_id
        )
        return response
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)

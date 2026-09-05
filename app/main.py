import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.schemas.chat_schema import CultureRequest, CultureResponse
from app.services.rag_service import RAGService
from app.services.groq_service import GroqService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Bharat Sanskriti API",
    description="Clean, modular API for Indian Cultural Heritage powered by Groq Llama 3.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize reusable services once on startup
rag_service = RAGService(json_file_path="data/culture_knowledge.json")
groq_service = GroqService(model_name="openai/gpt-oss-120b")
# groq_service = GroqService(model_name="llama-3.3-70b-versatile")


@app.post("/api/chat", response_model=CultureResponse)
async def chat_endpoint(payload: CultureRequest):
    try:
        # 1. Fetch context using RAG Service
        state_data = rag_service.get_state_culture_data(payload.state_name)
        found_data = bool(state_data)

        # 2. Pass context and query to Groq Service
        ai_response = groq_service.generate_cultural_response(
            state_name=payload.state_name,
            user_query=payload.user_query,
            context_data=state_data
        )

        return CultureResponse(
            state_name=payload.state_name,
            user_query=payload.user_query,
            found_in_json=found_data,
            ai_response=ai_response
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"API Error: {str(e)}")


@app.get("/health")
def health_check():
    return {"status": "online", "model": "llama-3.1-8b-instant", "provider": "Groq"}
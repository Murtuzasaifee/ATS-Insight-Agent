from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from functools import lru_cache
from src.ats_insight_agent.LLMS.groqllm import GroqLLM
from src.ats_insight_agent.LLMS.geminillm import GeminiLLM
from src.ats_insight_agent.LLMS.openai_llm import OpenAILLM
from src.ats_insight_agent.graph.graph_builder import GraphBuilder
from src.ats_insight_agent.graph.graph_executor import GraphExecutor
from src.ats_insight_agent.dto.ats_request import ATSRequest
from src.ats_insight_agent.dto.ats_response import ATSResponse
from contextlib import asynccontextmanager
from src.ats_insight_agent.utils.logging_config import setup_logging
from loguru import logger
import uvicorn

## Setup logging level
setup_logging(log_level="DEBUG")

gemini_models = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite", 
    "gemini-2.5-pro-exp-03-25"
]

groq_models = [
    "gemma2-9b-it",
    "llama3-8b-8192",
    "llama3-70b-8192"
]

openai_models = [
    "gpt-4o", 
    "gpt-4", 
    "gpt-3.5-turbo"
]

def load_app():
     uvicorn.run(app, host="0.0.0.0", port=8000)

class Settings:
    def __init__(self):
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")        
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")        

@lru_cache()
def get_settings():
    return Settings()

def validate_api_keys(settings: Settings = Depends(get_settings)):
    required_keys = {
        'GEMINI_API_KEY': settings.GEMINI_API_KEY,
        'GROQ_API_KEY': settings.GROQ_API_KEY,
        'OPENAI_API_KEY': settings.OPENAI_API_KEY
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    if missing_keys:
        raise HTTPException(
            status_code=500,
            detail=f"Missing required API keys: {', '.join(missing_keys)}"
        )
    return settings


# Initialize the LLM and GraphBuilder instances once and store them in the app state
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    
    gemini_llm = GeminiLLM(model=gemini_models[0], api_key=settings.GEMINI_API_KEY).get_llm_model()
    groq_llm = GroqLLM(model=groq_models[0], api_key=settings.GROQ_API_KEY).get_llm_model()
    openai_llm = OpenAILLM(model=openai_models[0], api_key=settings.OPENAI_API_KEY).get_llm_model()
    
    graph_builder = GraphBuilder()
    graph_builder.set_groq_llm(groq_llm)
    graph_builder.set_gemini_llm(gemini_llm)
    graph_builder.set_openai_llm(openai_llm)
    
    graph = graph_builder.setup_graph()
    graph_executor = GraphExecutor(graph)
    
    app.state.graph = graph
    app.state.graph_executor = graph_executor
    yield
    
    # Clean up resources if needed
    app.state.graph = None
    app.state.graph_executor = None

app = FastAPI(
    title="ATS Insight Agent API",
    description="AI-powered ATS Insight Agent",
    version="1.0.0",
    lifespan=lifespan
)

logger.info("Application starting up...")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to ATS Insight Agent API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }


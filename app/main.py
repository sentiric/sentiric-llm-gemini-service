# sentiric-llm-gemini-service/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager
from app.core.logging import setup_logging
from app.core.config import settings
import structlog
# import google.generativeai as genai # İleride eklenecek

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("LLM Gemini Service başlatılıyor", 
                version=settings.SERVICE_VERSION, 
                env=settings.ENV,
                model_endpoint=settings.GEMINI_MODEL_ENDPOINT)
    
    # TODO: Gemini istemcisini API key ile başlat
    # genai.configure(api_key=settings.GEMINI_API_KEY)
    
    yield
    
    logger.info("LLM Gemini Service kapatılıyor")

app = FastAPI(
    title="Sentiric LLM Gemini Service",
    description="Google Gemini API adaptör servisi",
    version=settings.SERVICE_VERSION,
    lifespan=lifespan
)

# LLM Gateway'in çağıracağı placeholder endpoint
@app.post(settings.API_V1_STR + "/generate", status_code=status.HTTP_200_OK)
async def generate_text(prompt: str, model_name: str):
    logger.info("Metin üretme isteği alındı", prompt_len=len(prompt), model=model_name)
    
    if settings.GEMINI_API_KEY == "MOCK_KEY":
        return {"generated_text": f"MOCK: {model_name} tarafından {len(prompt)} uzunluğunda metin üretildi."}

    # Gerçek API çağrısı burada yer alacak
    # client = genai.Client()
    # response = client.models.generate_content(...)
    
    return {"generated_text": "API call simulated."}

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    # API key kontrolü veya basit ping eklenebilir
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "MOCK_KEY":
        return {"status": "degraded", "detail": "Using MOCK API key."}, status.HTTP_200_OK
        
    return {"status": "ok", "service": "llm-gemini"}
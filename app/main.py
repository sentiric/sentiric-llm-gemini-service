# sentiric-llm-gemini-service/app/main.py
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from app.core.logging import setup_logging
from app.core.config import settings
import structlog
import httpx # Yeni eklenen bağımlılık
import json

# Hata yönetimi için kullanılabilecek özel istisnalar
class GeminiAPIError(HTTPException):
    pass

logger = structlog.get_logger(__name__)

# HTTPX istemcisini FastAPI lifespan içinde yönetmek
# Global olarak tanımlıyoruz, böylece her istekte yeniden oluşturulmaz
http_client: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global http_client
    setup_logging()
    
    logger.info("LLM Gemini Service başlatılıyor", 
                version=settings.SERVICE_VERSION, 
                env=settings.ENV,
                model_endpoint=settings.GEMINI_MODEL_ENDPOINT)
    
    # HTTPX istemcisini başlat
    http_client = httpx.AsyncClient(base_url=settings.GEMINI_MODEL_ENDPOINT, timeout=30.0)
    
    yield
    
    # HTTPX istemcisini kapat
    await http_client.aclose()
    logger.info("LLM Gemini Service kapatılıyor")

app = FastAPI(
    title="Sentiric LLM Gemini Service",
    description="Google Gemini API adaptör servisi",
    version=settings.SERVICE_VERSION,
    lifespan=lifespan
)

# LLM Gateway'in çağıracağı endpoint
@app.post(settings.API_V1_STR + "/generate", status_code=status.HTTP_200_OK)
async def generate_text(prompt: str, model_name: str):
    logger.info("Metin üretme isteği alındı", prompt_len=len(prompt), model=model_name)
    
    if settings.GEMINI_API_KEY == "MOCK_KEY":
        return {"generated_text": f"MOCK: {model_name} tarafından {len(prompt)} uzunluğunda metin üretildi."}

    # 1. Gemini API İstek Formatı
    gemini_endpoint = f"/v1/models/{model_name}:generateContent"
    request_data = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}]
    }

    # 2. API Çağrısı
    try:
        response = await http_client.post(
            gemini_endpoint,
            json=request_data,
            headers={"x-goog-api-key": settings.GEMINI_API_KEY},
        )
        
        response.raise_for_status() # HTTP 4xx/5xx hatalarını yakala

        # 3. Yanıtı Çözümleme ve Normalize Etme
        result = response.json()
        
        # Basit yanıt analizi (Gerçek projede daha detaylı parsing gerekir)
        if 'candidates' in result and result['candidates']:
            generated_text = result['candidates'][0]['content']['parts'][0]['text']
            # TODO: Maliyet takibi (token kullanımı) burada yapılmalıdır
            
            return {"generated_text": generated_text}
        
        # Eğer yanıt formatı beklenmedikse
        logger.error("Gemini API'den boş veya hatalı yanıt", response_data=result)
        raise GeminiAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Gemini API'den sonuç alınamadı."
        )

    except httpx.HTTPStatusError as e:
        # Harici API'den gelen HTTP hatalarını Sentiric standardına çevir
        logger.error("Harici Gemini API hatası", status_code=e.response.status_code, error_detail=e.response.text)
        raise GeminiAPIError(
            status_code=status.HTTP_502_BAD_GATEWAY, 
            detail=f"Gemini API hatası: {e.response.status_code}. Detay: {e.response.text[:100]}"
        )
    except httpx.RequestError as e:
        # Ağ veya zaman aşımı hataları
        logger.error("Gemini API bağlantı hatası", error=str(e))
        raise GeminiAPIError(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"Gemini API bağlantı hatası: {str(e)}"
        )
    except Exception as e:
        logger.exception("Metin üretme sırasında beklenmedik hata")
        raise GeminiAPIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Beklenmedik bir sunucu hatası oluştu."
        )

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    # API key kontrolü veya basit ping eklenebilir
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "MOCK_KEY":
        return {"status": "degraded", "detail": "Using MOCK API key."}, status.HTTP_200_OK
        
    return {"status": "ok", "service": "llm-gemini"}
# ✨ Sentiric LLM Gemini Service - Mantık ve Akış Mimarisi

**Stratejik Rol:** Google Gemini API'si ile doğrudan entegrasyonu yönetir. LLM Gateway'den gelen istekleri alır, Gemini formatına çevirir ve Gemini'dan gelen yanıtları normalize ederek Gateway'e döndürür.

---

## 1. Temel Akış: Metin Üretme (Generate)

```mermaid
sequenceDiagram
    participant Gateway as LLM Gateway
    participant GeminiService as Gemini Service
    participant GeminiAPI as Google Gemini API
    
    Gateway->>GeminiService: Generate(prompt, model_name)
    
    Note over GeminiService: 1. API Anahtarı ve Modeli Hazırla
    GeminiService->>GeminiAPI: POST /generateContent
    
    GeminiAPI-->>GeminiService: JSON Response (Raw)
    
    Note over GeminiService: 2. Sonucu Normalize Et
    GeminiService-->>Gateway: GenerateResponse(text)
```

## 2. API Adaptasyonu
* Bu servis, model adını (gemini-2.0-flash, gemini-2.5-pro) config'den veya doğrudan isteğin model_name alanından alabilir.
* Akış (Streaming): GenerateStream istekleri için kalıcı HTTP bağlantılarını veya sunucu tarafından itilen olayları (SSE) yönetir.
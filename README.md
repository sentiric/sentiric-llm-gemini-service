### 📄 File: `README.md` | 🏷️ Markdown

```markdown
# ✨ Sentiric LLM Gemini Service

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Language](https://img.shields.io/badge/language-Python-blue.svg)]()
[![Engine](https://img.shields.io/badge/engine-GoogleGemini-orange.svg)]()

**Sentiric LLM Gemini Service**, Google'ın üretken yapay zeka modelleriyle konuşmak için bir adaptör katmanıdır. Yüksek ölçeklenebilirlik ve bulut güvenilirliği gerektiren görevler için kullanılır.

## 🎯 Temel Sorumluluklar

*   **API Entegrasyonu:** Gemini API'sine (Generate, Stream) güvenli ve optimize edilmiş çağrılar yapar.
*   **Hata Dönüşümü:** Harici API hatalarını (Rate Limit, Invalid API Key) dahili gRPC durum kodlarına çevirir.
*   **Maliyet Takibi (Gelecek):** Kullanılan token miktarını izleyerek `sentiric-billing-service`'e raporlar.

## 🛠️ Teknoloji Yığını

*   **Dil:** Python 3.11
*   **Web Çerçevesi:** FastAPI / Uvicorn
*   **SDK:** `google-genai`
*   **Bağımlılıklar:** `sentiric-contracts` v1.9.0

## 🔌 API Etkileşimleri

*   **Gelen (Sunucu):**
    *   `sentiric-llm-gateway-service` (HTTP POST / gRPC): `Generate` RPC'si.
*   **Giden (İstemci):**
    *   Google Gemini API (REST over HTTPS).

---
## 🏛️ Anayasal Konum

Bu servis, [Sentiric Anayasası'nın](https://github.com/sentiric/sentiric-governance) **AI Engine Layer**'ında yer alan uzman bir bileşendir.
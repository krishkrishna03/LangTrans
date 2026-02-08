# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. POST /detect-language

Detect the language of input text.

**Request:**
```json
{
  "text": "Bonjour, comment allez-vous?"
}
```

**Response (200 OK):**
```json
{
  "detected_language": "fr",
  "language_name": "French",
  "confidence": 0.98
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Text must be at least 3 characters long",
  "detail": null
}
```

---

### 2. POST /translate

Translate text from source language to target language.

**Request:**
```json
{
  "text": "The quick brown fox jumps over the lazy dog",
  "source_language": "en",
  "target_language": "es"
}
```

**Response (200 OK):**
```json
{
  "original_text": "The quick brown fox jumps over the lazy dog",
  "translated_text": "El rápido zorro marrón salta sobre el perro perezoso",
  "source_language": "en",
  "source_language_name": "English",
  "target_language": "es",
  "target_language_name": "Spanish",
  "confidence": 0.87
}
```

**With Auto-Detection (source_language omitted):**
```json
{
  "text": "Hola, ¿cómo estás?",
  "target_language": "en"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Source and target languages cannot be the same",
  "detail": null
}
```

---

### 3. GET /supported-languages

Get list of all supported languages.

**Response (200 OK):**
```json
{
  "count": 100,
  "languages": [
    {
      "code": "en",
      "name": "English"
    },
    {
      "code": "es",
      "name": "Spanish"
    },
    {
      "code": "fr",
      "name": "French"
    },
    ...
  ]
}
```

---

### 4. GET /health

Health check endpoint.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-08T10:30:45.123456"
}
```

---

### 5. GET / (Root)

Root endpoint.

**Response (200 OK):**
```json
{
  "status": "online",
  "service": "Universal Language Translator",
  "version": "1.0.0"
}
```

---

## Request Validation

### Text Field Constraints
- **Minimum Length:** 1 character
- **Maximum Length:** 5000 characters
- **Required:** Yes
- **Type:** String (UTF-8)

### Language Code Format
- **Format:** ISO 639-1 codes (e.g., "en", "es", "fr")
- **Case:** Lowercase
- **Required:** Yes for target, optional for source

---

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 400 | Bad Request | Invalid input parameters |
| 500 | Internal Server Error | Server or model processing error |
| 503 | Service Unavailable | ML models not loaded |

---

## Response Headers

```
Content-Type: application/json
Access-Control-Allow-Origin: *
```

---

## Rate Limiting

Currently no rate limiting. Future versions will implement:
- 100 requests/minute per IP
- 10000 requests/day per API key

---

## Authentication

Currently no authentication required. Future versions will support:
- API Key authentication
- JWT tokens
- OAuth 2.0

---

## Examples

### Python with Requests
```python
import requests

api_url = "http://localhost:8000/api"

# Detect language
response = requests.post(
    f"{api_url}/detect-language",
    json={"text": "Hello world"}
)
print(response.json())

# Translate
response = requests.post(
    f"{api_url}/translate",
    json={
        "text": "Hello world",
        "source_language": "en",
        "target_language": "es"
    }
)
print(response.json())
```

### JavaScript with Fetch
```javascript
const API_URL = "http://localhost:8000/api";

// Detect language
fetch(`${API_URL}/detect-language`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ text: "Hello world" })
})
.then(res => res.json())
.then(data => console.log(data));

// Translate
fetch(`${API_URL}/translate`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    text: "Hello world",
    source_language: "en",
    target_language: "es"
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
# Detect language
curl -X POST http://localhost:8000/api/detect-language \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world"}'

# Translate
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","source_language":"en","target_language":"es"}'

# Get supported languages
curl http://localhost:8000/api/supported-languages

# Health check
curl http://localhost:8000/api/health
```

---

## Interactive API Testing

Visit Swagger UI at: `http://localhost:8000/docs`

This provides interactive testing for all endpoints with auto-generated documentation.

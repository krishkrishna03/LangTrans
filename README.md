# 🌐 Universal Language Translator

A production-ready web application for real-time translation between 100+ world languages using advanced transformer-based neural machine translation models.

## 📋 Features

✨ **Core Features:**
- 🎯 Auto-detection of source language
- 🌍 Support for 100+ world languages  
- ⚡ Real-time translation with confidence scores
- 🔤 Full Unicode support
- 💾 Clean, modern UI with Vite + React
- 🚀 Fast async backend with FastAPI
- 🤖 State-of-the-art M2M-100 Transformer model
- 🐳 Docker containerized for easy deployment

**Advanced Features:**
- ✅ CORS-enabled for cross-origin requests
- ✅ Comprehensive error handling and logging
- ✅ Language detection with confidence metrics
- ✅ Translation confidence scoring
- ✅ GPU acceleration support (auto-detected)
- ✅ Production-grade error handling
- ✅ Health check endpoints
- ✅ Optimized model loading

## 🚀 Quick Start

### Docker Compose (Recommended)

```bash
git clone <your-repo-url>
cd LangTrans
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend Setup:**
```bash
cd frontend
npm install
npm run dev
```

## 📡 API Documentation

### Base URL: `http://localhost:8000/api`

### 1. Detect Language
```bash
POST /detect-language
Content-Type: application/json

{
  "text": "Hello, how are you?"
}
```
**Response:**
```json
{
  "detected_language": "en",
  "language_name": "English",
  "confidence": 0.95
}
```

### 2. Translate Text
```bash
POST /translate
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "source_language": "en",
  "target_language": "es"
}
```
**Response:**
```json
{
  "original_text": "Hello, how are you?",
  "translated_text": "Hola, ¿cómo estás?",
  "source_language": "en",
  "source_language_name": "English",
  "target_language": "es",
  "target_language_name": "Spanish",
  "confidence": 0.89
}
```

### 3. Get Supported Languages
```bash
GET /supported-languages
```

### 4. Health Check
```bash
GET /health
```

## 🏗️ Project Structure

```
LangTrans/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI app + lifespan
│   │   ├── routes/
│   │   │   └── translator_routes.py  # API endpoints
│   │   ├── services/
│   │   │   ├── language_detection.py # Language detection
│   │   │   └── translation_service.py # M2M-100 translation
│   │   ├── models/
│   │   │   └── schemas.py            # Pydantic schemas
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── .gitignore
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Translator.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── styles/
│   │   │   ├── global.css
│   │   │   └── translator.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── Dockerfile
│   ├── .env.example
│   └── .gitignore
│
├── docker-compose.yml
└── README.md
```

## 🛠️ Configuration

### Backend (.env)
```env
PORT=8000
DEBUG=false
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
TRANSFORMERS_CACHE=/tmp/huggingface_cache
TORCH_HOME=/tmp/torch_cache
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000/api
```

## 🤖 Machine Learning Model

**Model:** Facebook's M2M-100 (418M parameters)
- **Type:** Sequence-to-Sequence Transformer
- **Languages:** 100+
- **Architecture:** Beam search decoding for translation
- **GPU Support:** Automatic detection and usage

### Model Loading Strategy
- Models loaded once at application startup via lifespan context manager
- Single instance reused across all requests for optimal performance
- Automatic GPU/CPU detection with memory optimization

## 🧪 API Testing

With cURL:
```bash
# Detect language
curl -X POST http://localhost:8000/api/detect-language \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'

# Translate text
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "source_language": "en", "target_language": "es"}'

# Get supported languages
curl http://localhost:8000/api/supported-languages
```

**Interactive Testing:** http://localhost:8000/docs (Swagger UI)

## 🐳 Docker Deployment

```bash
# Using Docker Compose
docker-compose up --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Individual Containers:**
```bash
# Backend
cd backend
docker build -t langtrans-backend:1.0 .
docker run -p 8000:8000 langtrans-backend:1.0

# Frontend
cd frontend
docker build -t langtrans-frontend:1.0 .
docker run -p 3000:3000 langtrans-frontend:1.0
```

## ☁️ Cloud Deployment

### AWS Deployment
```bash
# Push to ECR
aws ecr-public get-login-password | docker login --username AWS --password-stdin public.ecr.aws/YOUR_ID

docker build -t langtrans-backend:latest backend/
docker tag langtrans-backend:latest public.ecr.aws/YOUR_ID/langtrans-backend:latest
docker push public.ecr.aws/YOUR_ID/langtrans-backend:latest
```

### Google Cloud Deployment
```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT/langtrans-backend backend/
gcloud run deploy langtrans-backend --image gcr.io/YOUR_PROJECT/langtrans-backend
```

## 📚 Technology Stack

**Backend:** 
- FastAPI 0.104+
- PyTorch 2.1+
- Transformers 4.35+
- langdetect 1.0+
- Pydantic 2.5+

**Frontend:**
- React 18.2+
- Vite 5.0+
- Axios 1.6+
- CSS3 with custom properties

**DevOps:**
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

## 📊 Supported Languages

100+ languages including:
Arabic, Afrikaans, Albanian, Assamese, Bengali, Bulgarian, Catalan, Chinese, Czech, Danish, Dutch, English, Estonian, Finnish, French, German, Greek, Gujarati, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Kannada, Korean, Latvian, Lithuanian, Malayalam, Marathi, Nepali, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Slovenian, Spanish, Swedish, Tamil, Telugu, Thai, Turkish, Ukrainian, Urdu, Vietnamese... and more!

See `/api/supported-languages` for complete list.

## 🔍 Troubleshooting

### Issue: Model Download Fails
```bash
# Pre-download model
python -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; AutoTokenizer.from_pretrained('facebook/m2m100_418M')"
```

### Issue: Out of Memory
- Use CPU instead: Set `CUDA_VISIBLE_DEVICES=""`
- Or switch to smaller model variant

### Issue: CORS Errors
Update `CORS_ORIGINS` in `.env` to include your domain.

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with clear description

---

Made with ❤️ for breaking language barriers
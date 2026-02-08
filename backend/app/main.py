import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routes
from app.routes import translator_routes

# Global state for ML models
class MLModels:
    language_detector = None
    translator_model = None
    translator_tokenizer = None
    
ml_models = MLModels()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for loading/unloading models
    Models are loaded once at startup and reused across requests
    """
    logger.info("Loading ML models on startup...")
    
    try:
        from app.services.language_detection import LanguageDetector
        ml_models.language_detector = LanguageDetector()
        logger.info("Language detector loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load language detector: {e}")
    
    try:
        from app.services.translation_service import TranslationService
        ml_models.translator_model, ml_models.translator_tokenizer = TranslationService.load_model()
        logger.info("Translation model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load translation model: {e}")
    
    yield
    
    logger.info("Shutting down - cleaning up resources")

# Initialize FastAPI app
app = FastAPI(
    title="Universal Language Translator API",
    description="Translate text from any language to any language",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(translator_routes.router, prefix="/api", tags=["translator"])

# Root endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Universal Language Translator",
        "version": "1.0.0"
    }

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "false").lower() == "true" else "An error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )

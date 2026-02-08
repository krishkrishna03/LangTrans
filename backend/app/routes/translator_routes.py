import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from app.models import (
    DetectLanguageRequest,
    DetectLanguageResponse,
    TranslateRequest,
    TranslateResponse,
    ErrorResponse
)
from app.services.language_detection import LanguageDetector
from app.services.translation_service import TranslationService
import app.main as main_module

logger = logging.getLogger(__name__)

router = APIRouter()

def get_ml_models():
    """Dependency to get ML models from global state"""
    return main_module.ml_models

@router.post(
    "/detect-language",
    response_model=DetectLanguageResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def detect_language(
    request: DetectLanguageRequest,
    ml_models = Depends(get_ml_models)
):
    """
    Detect the language of input text
    
    - **text**: Input text to detect language for (1-5000 characters)
    
    Returns language code, name, and confidence score
    """
    try:
        if not ml_models.language_detector:
            raise HTTPException(
                status_code=503,
                detail="Language detection model not loaded"
            )
        
        lang_code, lang_name, confidence = ml_models.language_detector.detect(request.text)
        
        return DetectLanguageResponse(
            detected_language=lang_code,
            language_name=lang_name,
            confidence=confidence
        )
        
    except ValueError as e:
        logger.error(f"Validation error in detect_language: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in detect_language: {str(e)}")
        raise HTTPException(status_code=500, detail="Language detection failed")

@router.post(
    "/translate",
    response_model=TranslateResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def translate(
    request: TranslateRequest,
    ml_models = Depends(get_ml_models)
):
    """
    Translate text from source to target language
    
    - **text**: Text to translate (1-5000 characters)
    - **source_language**: Source language code (optional, auto-detected if not provided)
    - **target_language**: Target language code (required)
    
    Returns original text, translated text, language codes, names, and confidence
    """
    try:
        if not ml_models.language_detector or not ml_models.translator_model:
            raise HTTPException(
                status_code=503,
                detail="ML models not loaded"
            )
        
        # Detect source language if not provided
        if request.source_language:
            source_lang = request.source_language
            source_lang_name = TranslationService.get_language_name(source_lang)
        else:
            source_lang, source_lang_name, _ = ml_models.language_detector.detect(request.text)
        
        # Validate target language
        try:
            target_lang_name = TranslationService.get_language_name(request.target_language)
        except:
            target_lang_name = request.target_language.upper()
        
        # Perform translation
        translated_text, confidence = TranslationService.translate(
            text=request.text,
            source_language=source_lang,
            target_language=request.target_language,
            model=ml_models.translator_model,
            tokenizer=ml_models.translator_tokenizer
        )
        
        logger.info(f"Translation successful: {source_lang} -> {request.target_language}")
        
        return TranslateResponse(
            original_text=request.text,
            translated_text=translated_text,
            source_language=source_lang,
            source_language_name=source_lang_name,
            target_language=request.target_language,
            target_language_name=target_lang_name,
            confidence=confidence
        )
        
    except ValueError as e:
        logger.error(f"Validation error in translate: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in translate: {str(e)}")
        raise HTTPException(status_code=500, detail="Translation failed")

@router.get("/supported-languages")
async def get_supported_languages():
    """Get list of all supported languages"""
    try:
        languages = TranslationService.get_supported_languages()
        language_list = [
            {
                "code": code,
                "name": TranslationService.get_language_name(code)
            }
            for code in sorted(languages)
        ]
        
        return {
            "count": len(language_list),
            "languages": language_list
        }
    except Exception as e:
        logger.error(f"Error fetching supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch language list")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }

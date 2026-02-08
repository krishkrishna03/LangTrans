import logging
from langdetect import detect, detect_langs, LangDetectException
from typing import Tuple

logger = logging.getLogger(__name__)

# Mapping from language code to full language name
LANGUAGE_NAMES = {
    'af': 'Afrikaans', 'ar': 'Arabic', 'bg': 'Bulgarian', 'bn': 'Bengali',
    'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish',
    'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish',
    'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French',
    'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian',
    'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese',
    'ja': 'Japanese', 'kn': 'Kannada', 'ko': 'Korean', 'lt': 'Lithuanian',
    'lv': 'Latvian', 'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi',
    'ne': 'Nepali', 'nl': 'Dutch', 'no': 'Norwegian', 'pa': 'Punjabi',
    'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian', 'ru': 'Russian',
    'sk': 'Slovak', 'sl': 'Slovenian', 'so': 'Somali', 'sq': 'Albanian',
    'sv': 'Swedish', 'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai',
    'tl': 'Tagalog', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
    'vi': 'Vietnamese', 'zh-cn': 'Chinese (Simplified)', 'zh-tw': 'Chinese (Traditional)',
    'zh': 'Chinese', 'as': 'Assamese', 'or': 'Odia'
}

class LanguageDetector:
    """Language detection service using langdetect"""
    
    def __init__(self):
        """Initialize language detector"""
        logger.info("Initializing LanguageDetector")
    
    def detect(self, text: str) -> Tuple[str, str, float]:
        """
        Detect language from text
        
        Args:
            text: Input text to detect language from
            
        Returns:
            Tuple of (language_code, language_name, confidence)
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        if len(text.strip()) < 3:
            raise ValueError("Text must be at least 3 characters long")
        
        try:
            # Get all potential language matches with probabilities
            detected_langs = detect_langs(text)
            
            if detected_langs:
                top_result = detected_langs[0]
                lang_code = top_result.lang
                confidence = top_result.prob
                
                # Get language name
                lang_name = LANGUAGE_NAMES.get(lang_code, lang_code.upper())
                
                logger.info(f"Detected language: {lang_code} ({lang_name}) with confidence {confidence:.2f}")
                return lang_code, lang_name, float(confidence)
            else:
                raise ValueError("Unable to detect language")
                
        except LangDetectException as e:
            logger.error(f"Language detection error: {str(e)}")
            raise ValueError(f"Language detection failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {str(e)}")
            raise ValueError(f"Language detection failed: {str(e)}")
    
    @staticmethod
    def get_supported_languages():
        """Get list of supported languages"""
        return list(LANGUAGE_NAMES.items())
    
    @staticmethod
    def get_language_name(code: str) -> str:
        """Get language name from code"""
        return LANGUAGE_NAMES.get(code, code.upper())

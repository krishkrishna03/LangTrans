import logging
import torch
from typing import Tuple, Optional
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

logger = logging.getLogger(__name__)

# Language code mappings for M2M-100
M2M_LANGUAGE_CODES = {
    'en': 'en_XX',      # English
    'es': 'es_XX',      # Spanish
    'fr': 'fr_XX',      # French
    'de': 'de_DE',      # German
    'it': 'it_IT',      # Italian
    'pt': 'pt_XX',      # Portuguese
    'nl': 'nl_XX',      # Dutch
    'ru': 'ru_RU',      # Russian
    'zh': 'zh_CN',      # Chinese (Simplified)
    'ja': 'ja_XX',      # Japanese
    'ko': 'ko_KR',      # Korean
    'ar': 'ar_AR',      # Arabic
    'hi': 'hi_IN',      # Hindi
    'tr': 'tr_TR',      # Turkish
    'pl': 'pl_PL',      # Polish
    'uk': 'uk_UA',      # Ukrainian
    'ro': 'ro_RO',      # Romanian
    'hu': 'hu_HU',      # Hungarian
    'cs': 'cs_CZ',      # Czech
    'sv': 'sv_SE',      # Swedish
    'da': 'da_DK',      # Danish
    'fi': 'fi_FI',      # Finnish
    'el': 'el_GR',      # Greek
    'he': 'he_IL',      # Hebrew
    'th': 'th_TH',      # Thai
    'vi': 'vi_VN',      # Vietnamese
    'id': 'id_ID',      # Indonesian
    'ms': 'ms_MY',      # Malay
    'tl': 'tl_XX',      # Tagalog
    'bn': 'bn_IN',      # Bengali
    'ta': 'ta_IN',      # Tamil
    'te': 'te_IN',      # Telugu
    'mr': 'mr_IN',      # Marathi
    'gu': 'gu_IN',      # Gujarati
    'kn': 'kn_IN',      # Kannada
    'ml': 'ml_IN',      # Malayalam
    'af': 'af_ZA',      # Afrikaans
    'bg': 'bg_BG',      # Bulgarian
    'et': 'et_EE',      # Estonian
    'fa': 'fa_IR',      # Persian
    'hr': 'hr_HR',      # Croatian
    'lt': 'lt_LT',      # Lithuanian
    'lv': 'lv_LV',      # Latvian
    'mk': 'mk_MK',      # Macedonian
    'ne': 'ne_NP',      # Nepali
    'pa': 'pa_IN',      # Punjabi
    'sk': 'sk_SK',      # Slovak
    'sl': 'sl_SI',      # Slovenian
    'so': 'so_SO',      # Somali
    'sq': 'sq_AL',      # Albanian
    'sr': 'sr_RS',      # Serbian
    'sw': 'sw_KE',      # Swahili
    'ur': 'ur_PK',      # Urdu
}

LANGUAGE_NAMES = {
    'ar': 'Arabic', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish',
    'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish',
    'et': 'Estonian', 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French',
    'gu': 'Gujarati', 'he': 'Hebrew', 'hi': 'Hindi', 'hr': 'Croatian',
    'hu': 'Hungarian', 'id': 'Indonesian', 'it': 'Italian', 'ja': 'Japanese',
    'kn': 'Kannada', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian',
    'mk': 'Macedonian', 'ml': 'Malayalam', 'mr': 'Marathi', 'ne': 'Nepali',
    'nl': 'Dutch', 'pa': 'Punjabi', 'pl': 'Polish', 'pt': 'Portuguese',
    'ro': 'Romanian', 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian',
    'so': 'Somali', 'sq': 'Albanian', 'sv': 'Swedish', 'sw': 'Swahili',
    'ta': 'Tamil', 'te': 'Telugu', 'th': 'Thai', 'tr': 'Turkish',
    'uk': 'Ukrainian', 'ur': 'Urdu', 'vi': 'Vietnamese', 'zh': 'Chinese',
    'ms': 'Malay', 'sr': 'Serbian', 'bg': 'Bulgarian', 'af': 'Afrikaans',
    'tl': 'Tagalog', 'bn': 'Bengali'
}

class TranslationService:
    """Translation service using Facebook's M2M-100 model"""
    
    # Use smaller model for demo (1.2B instead of 418M)
    MODEL_NAME = "facebook/m2m100_418M"
    
    @staticmethod
    def load_model():
        """
        Load the translation model and tokenizer
        
        Returns:
            Tuple of (model, tokenizer)
        """
        logger.info(f"Loading translation model: {TranslationService.MODEL_NAME}")
        
        try:
            # Check if GPU is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device}")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(TranslationService.MODEL_NAME)
            model = AutoModelForSeq2SeqLM.from_pretrained(TranslationService.MODEL_NAME)
            
            # Move model to device
            model = model.to(device)
            model.eval()  # Set to evaluation mode
            
            logger.info("Translation model loaded successfully")
            return model, tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load translation model: {str(e)}")
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    @staticmethod
    def translate(
        text: str,
        source_language: str,
        target_language: str,
        model,
        tokenizer
    ) -> Tuple[str, float]:
        """
        Translate text from source to target language
        
        Args:
            text: Text to translate
            source_language: Source language code (e.g., 'en')
            target_language: Target language code (e.g., 'es')
            model: Loaded translation model
            tokenizer: Loaded tokenizer
            
        Returns:
            Tuple of (translated_text, confidence_score)
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        if len(text.strip()) > 5000:
            raise ValueError("Text exceeds maximum length of 5000 characters")
        
        # Validate language codes
        if source_language not in M2M_LANGUAGE_CODES:
            raise ValueError(f"Unsupported source language: {source_language}")
        
        if target_language not in M2M_LANGUAGE_CODES:
            raise ValueError(f"Unsupported target language: {target_language}")
        
        if source_language == target_language:
            logger.warning("Source and target languages are the same")
            return text, 1.0
        
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Set the source language for the tokenizer
            tokenizer.src_lang = M2M_LANGUAGE_CODES[source_language]
            
            # Encode the input text
            encoded = tokenizer(text, return_tensors="pt").to(device)
            
            # Generate translation
            with torch.no_grad():
                generated_tokens = model.generate(
                    **encoded,
                    forced_bos_token_id=tokenizer.get_lang_id(M2M_LANGUAGE_CODES[target_language]),
                    max_length=200,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode the generated tokens
            translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
            
            # Confidence score is estimated based on translation length and model output
            # For simplicity, we use a heuristic confidence
            confidence = min(0.95, 0.7 + (len(translated_text) / len(text) * 0.25))
            
            logger.info(f"Translated from {source_language} to {target_language}")
            return translated_text, float(confidence)
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            raise RuntimeError(f"Translation failed: {str(e)}")
    
    @staticmethod
    def get_supported_languages():
        """Get list of supported language codes"""
        return list(M2M_LANGUAGE_CODES.keys())
    
    @staticmethod
    def get_language_name(code: str) -> str:
        """Get language name from code"""
        return LANGUAGE_NAMES.get(code, code.upper())

import { useState, useEffect } from 'react';
import translationAPI from '../services/api';
import '../styles/translator.css';

const Translator = () => {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [detectedLanguage, setDetectedLanguage] = useState(null);
  const [targetLanguage, setTargetLanguage] = useState('es');
  const [languages, setLanguages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [translationConfidence, setTranslationConfidence] = useState(null);

  // Load supported languages on component mount
  useEffect(() => {
    const loadLanguages = async () => {
      try {
        const response = await translationAPI.getSupportedLanguages();
        setLanguages(response.languages);
      } catch (err) {
        console.error('Failed to load languages:', err);
        setError('Failed to load supported languages');
      }
    };
    loadLanguages();
  }, []);

  // Auto-detect language when input changes
  const handleDetectLanguage = async (text) => {
    if (!text.trim()) {
      setDetectedLanguage(null);
      return;
    }

    if (text.length < 3) return;

    try {
      setError(null);
      const response = await translationAPI.detectLanguage(text);
      setDetectedLanguage(response);
    } catch (err) {
      console.error('Language detection failed:', err);
      setDetectedLanguage(null);
    }
  };

  // Handle input change with debouncing
  useEffect(() => {
    const timer = setTimeout(() => {
      handleDetectLanguage(inputText);
    }, 500);

    return () => clearTimeout(timer);
  }, [inputText]);

  // Handle translation
  const handleTranslate = async (e) => {
    e.preventDefault();

    if (!inputText.trim()) {
      setError('Please enter text to translate');
      return;
    }

    if (!detectedLanguage) {
      setError('Unable to detect language. Please try again.');
      return;
    }

    if (detectedLanguage.detected_language === targetLanguage) {
      setError('Source and target languages cannot be the same');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await translationAPI.translate(
        inputText,
        detectedLanguage.detected_language,
        targetLanguage
      );

      setOutputText(response.translated_text);
      setTranslationConfidence(response.confidence);
    } catch (err) {
      console.error('Translation failed:', err);
      setError(
        err.response?.data?.detail ||
        'Translation failed. Please try again.'
      );
      setOutputText('');
      setTranslationConfidence(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle clear
  const handleClear = () => {
    setInputText('');
    setOutputText('');
    setDetectedLanguage(null);
    setTargetLanguage('es');
    setError(null);
    setTranslationConfidence(null);
  };

  // Handle copy to clipboard
  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="translator-container">
      <div className="translator-card">
        <h1 className="title">🌐 Universal Language Translator</h1>
        <p className="subtitle">Translate text between any languages instantly</p>

        <form onSubmit={handleTranslate}>
          {/* Input Section */}
          <div className="input-section">
            <div className="section-header">
              <label>Source Text</label>
              {detectedLanguage && (
                <span className="detected-lang">
                  Detected: <strong>{detectedLanguage.language_name}</strong> ({detectedLanguage.confidence.toFixed(2)} confidence)
                </span>
              )}
            </div>
            <textarea
              className="textarea"
              placeholder="Enter text to translate..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              disabled={loading}
              maxLength={5000}
            />
            <div className="char-count">
              {inputText.length}/5000 characters
            </div>
          </div>

          {/* Language Selection Section */}
          <div className="language-selection">
            <div className="language-item">
              <label htmlFor="source-lang">Source Language</label>
              <select
                id="source-lang"
                disabled
                value={detectedLanguage?.detected_language || ''}
                className="language-select"
              >
                <option value="">Auto-detected</option>
              </select>
            </div>

            <div className="swap-button-container">
              {/* Swap button could be added here for future enhancement */}
            </div>

            <div className="language-item">
              <label htmlFor="target-lang">Target Language</label>
              <select
                id="target-lang"
                value={targetLanguage}
                onChange={(e) => setTargetLanguage(e.target.value)}
                disabled={loading}
                className="language-select"
              >
                <option value="">Select language</option>
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Error Message */}
          {error && <div className="error-message">{error}</div>}

          {/* Buttons */}
          <div className="button-group">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !inputText.trim() || !detectedLanguage}
            >
              {loading ? 'Translating...' : 'Translate'}
            </button>
            <button
              type="button"
              onClick={handleClear}
              className="btn btn-secondary"
              disabled={loading}
            >
              Clear
            </button>
          </div>
        </form>

        {/* Output Section */}
        {outputText && (
          <div className="output-section">
            <div className="section-header">
              <label>Translation Result</label>
              {translationConfidence && (
                <span className="confidence-badge">
                  Confidence: {(translationConfidence * 100).toFixed(1)}%
                </span>
              )}
            </div>
            <textarea
              className="textarea output"
              value={outputText}
              readOnly
              disabled
            />
            <div className="output-actions">
              <button
                type="button"
                className="btn btn-small"
                onClick={() => handleCopy(outputText)}
              >
                📋 Copy Translation
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="translator-footer">
        <p>Powered by Facebook's M2M-100 Transformer Model</p>
        <p className="version">LangTrans v1.0</p>
      </div>
    </div>
  );
};

export default Translator;

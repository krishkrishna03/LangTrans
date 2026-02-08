import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.url);
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error.response || error.message);
    throw error;
  }
);

export const translationAPI = {
  /**
   * Detect language from text
   * @param {string} text - Text to detect language
   * @returns {Promise<{detected_language: string, language_name: string, confidence: number}>}
   */
  detectLanguage: (text) =>
    apiClient.post('/detect-language', { text }),

  /**
   * Translate text
   * @param {string} text - Text to translate
   * @param {string} sourceLanguage - Source language code
   * @param {string} targetLanguage - Target language code
   * @returns {Promise<TranslateResponse>}
   */
  translate: (text, sourceLanguage, targetLanguage) =>
    apiClient.post('/translate', {
      text,
      source_language: sourceLanguage,
      target_language: targetLanguage
    }),

  /**
   * Get list of supported languages
   * @returns {Promise<{count: number, languages: Array}>}
   */
  getSupportedLanguages: () =>
    apiClient.get('/supported-languages'),

  /**
   * Health check
   * @returns {Promise}
   */
  healthCheck: () =>
    apiClient.get('/health')
};

export default translationAPI;

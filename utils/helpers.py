"""Helper functions"""
from flask import session

def get_language():
    """Get current language from session, default to English"""
    return session.get('language', 'en')

def set_language(lang):
    """Set language in session"""
    if lang in ['en', 'km']:
        session['language'] = lang

def translate_symptom(symptom_name, lang):
    """
    Translate symptom name based on selected language.
    Falls back to the original name if no translation is found.
    """
    from translations import SYMPTOM_TRANSLATIONS
    if not symptom_name:
        return ''
    if lang == 'km':
        return SYMPTOM_TRANSLATIONS.get('km', {}).get(symptom_name, symptom_name)
    return symptom_name


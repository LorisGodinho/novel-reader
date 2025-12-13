"""
Configuração do ElevenLabs para narração de alta qualidade
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do ElevenLabs
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', '')

# Vozes recomendadas (mulheres, português/multilíngue)
VOZES_DISPONIVEIS = {
    'Rachel': {
        'id': '21m00Tcm4TlvDq8ikWAM',
        'idioma': 'Multilíngue',
        'descricao': 'Voz feminina calma e profissional',
        'estilo': 'narração'
    },
    'Domi': {
        'id': 'AZnzlk1XvdvUeBnXmlld',
        'idioma': 'Multilíngue',
        'descricao': 'Voz feminina forte e confiante',
        'estilo': 'narração'
    },
    'Bella': {
        'id': 'EXAVITQu4vr4xnSDxMaL',
        'idioma': 'Multilíngue',
        'descricao': 'Voz feminina jovem e expressiva',
        'estilo': 'narrativa dinâmica'
    },
    'Elli': {
        'id': 'MF3mGyEYCl7XYWbV9V6O',
        'idioma': 'Multilíngue',
        'descricao': 'Voz feminina emocional',
        'estilo': 'muito expressiva'
    },
    'Grace': {
        'id': 'oWAxZDx7w5VEj9dCyTzz',
        'idioma': 'Multilíngue',
        'descricao': 'Voz feminina sulista americana',
        'estilo': 'narrativa rica'
    }
}

# Voz padrão
VOZ_PADRAO = 'Rachel'

# Tags de emoção suportadas pelo ElevenLabs
TAGS_EMOCAO = {
    'sarcastically': 'sarcástico',
    'giggles': 'risada',
    'whispers': 'sussurro',
    'shouting': 'gritando',
    'sadly': 'tristeza',
    'angrily': 'raiva',
    'laughs': 'rindo',
    'sighs': 'suspiro',
    'excited': 'animado',
    'scared': 'assustado',
    'mysterious': 'misterioso',
    'cheerful': 'alegre'
}

# Configurações de qualidade
MODELO_ELEVENLABS = 'eleven_multilingual_v2'  # Suporta português
STABILITY = 0.5  # 0-1, quanto maior mais estável
SIMILARITY_BOOST = 0.75  # 0-1, similaridade com voz original
STYLE = 0.5  # 0-1, quanto de estilo aplicar
SPEAKER_BOOST = True  # Melhora clareza

def obter_config():
    """Retorna configuração completa."""
    return {
        'api_key': ELEVENLABS_API_KEY,
        'voz_padrao': VOZ_PADRAO,
        'vozes': VOZES_DISPONIVEIS,
        'modelo': MODELO_ELEVENLABS,
        'stability': STABILITY,
        'similarity_boost': SIMILARITY_BOOST,
        'style': STYLE,
        'speaker_boost': SPEAKER_BOOST
    }

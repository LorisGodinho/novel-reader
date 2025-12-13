"""
Teste rápido - Narrar capítulo 961 com ElevenLabs
"""

import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))

from leitor import LeitorNovel
from elevenlabs.client import ElevenLabs
from elevenlabs_config import obter_config
import tempfile
import time
import pygame
import re

config = obter_config()

# Configurar cliente
from elevenlabs import VoiceSettings
cliente = ElevenLabs(api_key=config['api_key'])

def processar_tags_emocao(texto: str) -> str:
    """Adiciona tags automáticas."""
    if 'gritou' in texto.lower() or 'berrou' in texto.lower():
        texto = texto.replace('gritou', '[shouting] gritou').replace('berrou', '[shouting] berrou')
    
    if 'sussurrou' in texto.lower() or 'murmurou' in texto.lower():
        texto = texto.replace('sussurrou', '[whispers] sussurrou').replace('murmurou', '[whispers] murmurou')
    
    if 'riu' in texto.lower() or 'risada' in texto.lower():
        texto = texto.replace('riu', '[giggles] riu').replace('risada', '[giggles] risada')
    
    return texto

print("\n" + "="*60)
print(" TESTE - MARTIAL WORLD CAPÍTULO 961")
print(" 🎤 Narração: ElevenLabs Ultra HD")
print(" 🎭 Voz: Rachel (calma e profissional)")
print("="*60 + "\n")

# Carregar capítulo
leitor = LeitorNovel('./novels/martial_world')
capitulo = leitor.carregar_capitulo(961)

if not capitulo:
    print("❌ Capítulo 961 não encontrado.")
    sys.exit(1)

print(f"📖 {capitulo['titulo']}")
print(f"📄 {len(capitulo['conteudo'])} parágrafos\n")
print("="*60 + "\n")
print("🎬 Iniciando narração...\n")

# Voz Rachel
voz_id = config['vozes']['Rachel']['id']

# Inicializar pygame
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
temp_dir = tempfile.gettempdir()

try:
    for i, paragrafo in enumerate(capitulo['conteudo'], 1):
        print(f"[{i}/{len(capitulo['conteudo'])}] {paragrafo[:70]}...")
        
        # Adicionar tags automáticas
        paragrafo_processado = processar_tags_emocao(paragrafo)
        
        try:
            # Gerar áudio
            audio = cliente.text_to_speech.convert(
                voice_id=voz_id,
                text=paragrafo_processado,
                model_id=config['modelo'],
                voice_settings=VoiceSettings(
                    stability=config['stability'],
                    similarity_boost=config['similarity_boost'],
                    style=config['style'],
                    use_speaker_boost=config['speaker_boost']
                )
            )
            
            # Salvar temporariamente
            temp_file = os.path.join(temp_dir, f"eleven_test_{i}.mp3")
            with open(temp_file, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            
            # Reproduzir
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Pausa entre parágrafos
            time.sleep(0.15)
            
            # Limpar
            try:
                os.remove(temp_file)
            except:
                pass
        
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            continue
        
        print()
    
    print("\n" + "="*60)
    print(" ✓ FIM DO CAPÍTULO 961")
    print("="*60 + "\n")

except KeyboardInterrupt:
    print("\n\n⏸️ Narração interrompida.")
    pygame.mixer.music.stop()

finally:
    pygame.mixer.quit()

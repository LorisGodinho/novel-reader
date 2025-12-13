"""
Teste rápido de velocidade de narração
"""

import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gtts import gTTS
import pygame
import tempfile
import time

def testar_velocidade():
    """Testa diferentes velocidades de narração."""
    
    texto_teste = "Este é um teste de velocidade de narração. Estou testando como o áudio soa em diferentes velocidades."
    
    velocidades = [1.0, 1.25, 1.5, 1.75, 2.0]
    
    print("\n" + "="*60)
    print(" TESTE DE VELOCIDADE - NARRAÇÃO")
    print("="*60 + "\n")
    
    temp_dir = tempfile.gettempdir()
    
    for vel in velocidades:
        print(f"\n🔊 Testando velocidade {vel}x...")
        print(f"Texto: {texto_teste}\n")
        
        try:
            # Gerar áudio
            temp_file = os.path.join(temp_dir, "teste_velocidade.mp3")
            tts = gTTS(text=texto_teste, lang='pt-br', slow=False, tld='com.br')
            tts.save(temp_file)
            
            # Reiniciar mixer com frequência ajustada
            pygame.mixer.quit()
            freq_ajustada = int(24000 * vel)
            pygame.mixer.init(frequency=freq_ajustada, size=-16, channels=2, buffer=512)
            
            # Reproduzir
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Limpar
            try:
                os.remove(temp_file)
            except:
                pass
            
            print(f"✓ Concluído ({vel}x)\n")
            time.sleep(0.5)
        
        except Exception as e:
            print(f"❌ Erro: {e}\n")
    
    pygame.mixer.quit()
    
    print("\n" + "="*60)
    print(" TESTE CONCLUÍDO")
    print("="*60)
    print("\nAgora você pode:")
    print("1. Executar: python narrar_martial_world.py")
    print("2. Escolher opção 4 para configurar sua velocidade preferida")
    print("3. Escolher opção 1 para narrar um capítulo")

if __name__ == "__main__":
    testar_velocidade()

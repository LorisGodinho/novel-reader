"""
Teste rápido de narração com Google TTS
"""

import os
import sys
import io

# Configura encoding para UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gtts import gTTS
import pygame
from pydub import AudioSegment
import tempfile
import time
from leitor import LeitorNovel

def testar_narracao():
    """Testa narração dos primeiros 3 parágrafos do capítulo 961."""
    
    print("\n" + "="*60)
    print(" TESTE DE NARRAÇÃO - CAPÍTULO 961")
    print(" Google TTS PT-BR - Velocidade 1.5x")
    print("="*60 + "\n")
    
    # Carregar capítulo
    leitor = LeitorNovel('./novels/martial_world')
    capitulo = leitor.carregar_capitulo(961)
    
    if not capitulo:
        print("❌ Capítulo 961 não encontrado!")
        return
    
    print(f"📖 {capitulo['titulo']}")
    print(f"📄 Narrando os primeiros 3 parágrafos de {len(capitulo['conteudo'])}\n")
    print("="*60 + "\n")
    
    # Inicializar pygame
    pygame.mixer.init(frequency=22050)
    
    temp_dir = tempfile.gettempdir()
    velocidade = 1.5
    
    try:
        # Narrar apenas os 3 primeiros parágrafos
        for i, paragrafo in enumerate(capitulo['conteudo'][:3], 1):
            print(f"[{i}/3] {paragrafo[:80]}...")
            
            temp_file = os.path.join(temp_dir, f"teste_mw_{i}.mp3")
            
            try:
                # Gerar TTS
                print("   🎤 Gerando áudio...")
                tts = gTTS(text=paragrafo, lang='pt-br', slow=False)
                tts.save(temp_file)
                
                # Ajustar velocidade
                print(f"   ⚡ Ajustando velocidade para {velocidade}x...")
                audio = AudioSegment.from_mp3(temp_file)
                
                # Acelerar
                audio_acelerado = audio._spawn(audio.raw_data, overrides={
                    "frame_rate": int(audio.frame_rate * velocidade)
                })
                audio_acelerado = audio_acelerado.set_frame_rate(audio.frame_rate)
                
                # Salvar versão ajustada
                temp_file_adj = os.path.join(temp_dir, f"teste_mw_adj_{i}.mp3")
                audio_acelerado.export(temp_file_adj, format="mp3")
                
                # Reproduzir
                print("   🔊 Reproduzindo...")
                pygame.mixer.music.load(temp_file_adj)
                pygame.mixer.music.play()
                
                # Aguardar fim
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                print("   ✓ Concluído\n")
                
                # Limpar
                try:
                    os.remove(temp_file)
                    os.remove(temp_file_adj)
                except:
                    pass
                
                time.sleep(0.5)  # Pausa entre parágrafos
            
            except Exception as e:
                print(f"   ❌ Erro: {e}\n")
        
        print("="*60)
        print(" TESTE CONCLUÍDO!")
        print("="*60)
        print("\nSe funcionou corretamente, execute:")
        print("python narrar_martial_world.py")
        print("E escolha a opção 1 para narrar o capítulo completo.")
        
    except KeyboardInterrupt:
        print("\n\n⏸️ Teste interrompido.")
    
    finally:
        pygame.mixer.quit()

if __name__ == "__main__":
    testar_narracao()

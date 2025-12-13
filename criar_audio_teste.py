"""
Script para criar arquivos de áudio de teste
Gera tons simples para testar o sistema de música
"""

import numpy as np
from scipy.io import wavfile
import os

def criar_tom_teste(frequencia, duracao, nome_arquivo, volume=0.3):
    """Cria um arquivo WAV com um tom simples."""
    sample_rate = 22050
    t = np.linspace(0, duracao, int(sample_rate * duracao))
    
    # Tom simples
    onda = np.sin(2 * np.pi * frequencia * t) * volume
    
    # Converter para int16
    audio = (onda * 32767).astype(np.int16)
    
    # Salvar
    wavfile.write(nome_arquivo, sample_rate, audio)
    print(f"✓ Criado: {nome_arquivo}")

# Criar pasta se não existir
os.makedirs('./assets/audio/background', exist_ok=True)

# Criar arquivos de teste
print("Criando arquivos de teste...")
criar_tom_teste(440, 5, './assets/audio/background/ambient_test.wav', 0.2)  # Lá (440Hz)
criar_tom_teste(880, 5, './assets/audio/background/combat_test.wav', 0.2)   # Lá (oitava acima)
print("\nArquivos criados! Use-os para testar o sistema.")

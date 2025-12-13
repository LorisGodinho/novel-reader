"""
Script de teste para verificar vozes TTS disponíveis no sistema
"""

import pyttsx3

def listar_vozes_sistema():
    """Lista todas as vozes disponíveis no sistema."""
    print("=== Vozes TTS Disponíveis no Sistema ===\n")
    
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"Total de vozes encontradas: {len(voices)}\n")
    
    for i, voice in enumerate(voices, 1):
        print(f"{i}. ID: {voice.id}")
        print(f"   Nome: {voice.name}")
        print(f"   Idioma: {voice.languages}")
        print(f"   Gênero: {voice.gender if hasattr(voice, 'gender') else 'N/A'}")
        print(f"   Idade: {voice.age if hasattr(voice, 'age') else 'N/A'}")
        print()
    
    return voices

def testar_voz(texto="Olá, eu sou uma voz de teste para o projeto Novel Reader.", voz_index=0):
    """
    Testa uma voz específica.
    
    Args:
        texto: Texto para sintetizar
        voz_index: Índice da voz (0 = primeira voz)
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    if voz_index >= len(voices):
        print(f"Erro: Índice {voz_index} inválido. Há apenas {len(voices)} vozes disponíveis.")
        return
    
    engine.setProperty('voice', voices[voz_index].id)
    
    print(f"\n🔊 Testando voz: {voices[voz_index].name}")
    print(f"📝 Texto: {texto}\n")
    
    engine.say(texto)
    engine.runAndWait()

def testar_todas_vozes(texto="Teste de voz"):
    """Testa todas as vozes disponíveis."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    
    print(f"\n=== Testando {len(voices)} vozes ===\n")
    
    for i, voice in enumerate(voices):
        print(f"\n{i+1}. Testando: {voice.name}")
        engine.setProperty('voice', voice.id)
        engine.say(f"Voz número {i+1}. {texto}")
        engine.runAndWait()

if __name__ == "__main__":
    # Lista todas as vozes
    vozes = listar_vozes_sistema()
    
    # Recomendações
    print("\n" + "="*50)
    print("RECOMENDAÇÕES PARA PORTUGUÊS:")
    print("="*50)
    
    vozes_pt = []
    for i, voice in enumerate(vozes):
        # Procura por vozes em português
        if any('pt' in str(lang).lower() or 'portuguese' in voice.name.lower() 
               or 'brazil' in voice.name.lower() or 'maria' in voice.name.lower() 
               or 'daniel' in voice.name.lower() for lang in voice.languages):
            vozes_pt.append((i, voice.name))
            print(f"✓ Índice {i}: {voice.name}")
    
    if not vozes_pt:
        print("⚠️ Nenhuma voz em português encontrada.")
        print("Você pode:")
        print("1. Baixar vozes em PT-BR das configurações do Windows")
        print("2. Usar gTTS (Google TTS) que suporta PT-BR online")
    
    print("\n" + "="*50)
    print("Para testar uma voz específica, execute:")
    print('python test_vozes.py --test <indice>')
    print("\nPara testar TODAS as vozes (pode demorar):")
    print('python test_vozes.py --test-all')
    print("="*50)

"""
Script para narrar capítulos usando TTS
Demonstra o sistema de narração com vozes diferenciadas
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from leitor import LeitorNovel
import pyttsx3


def narrar_com_tts(caminho_novel: str, numero_capitulo: int):
    """
    Narra um capítulo usando síntese de voz real.
    
    Args:
        caminho_novel: Caminho da pasta da novel
        numero_capitulo: Número do capítulo a narrar
    """
    print("\n" + "="*60)
    print(f" NARRANDO CAPÍTULO {numero_capitulo}")
    print("="*60 + "\n")
    
    leitor = LeitorNovel(caminho_novel)
    
    # Processar capítulo
    segmentos = leitor.processar_capitulo(numero_capitulo)
    
    if not segmentos:
        print("❌ Capítulo não encontrado ou vazio.")
        return
    
    # Inicializar engine TTS
    engine = pyttsx3.init()
    
    print(f"📖 Novel: {leitor.metadata.get('titulo', 'Sem título')}")
    print(f"📄 Total de segmentos: {len(segmentos)}\n")
    print("🔊 Iniciando narração...\n")
    print("-"*60 + "\n")
    
    for i, segmento in enumerate(segmentos, 1):
        tipo = segmento['tipo']
        texto = segmento['texto']
        voz_config = segmento.get('voz_config', {})
        
        # Mostrar informação do segmento
        if tipo == 'narracao':
            print(f"[NARRADOR]")
        else:
            personagem = segmento.get('personagem', 'Desconhecido')
            print(f"[{personagem.upper()}]")
        
        print(f"{texto}\n")
        
        # Configurar voz
        modelo_voz = voz_config.get('modelo', '')
        if modelo_voz:
            try:
                engine.setProperty('voice', modelo_voz)
                engine.setProperty('rate', int(150 * voz_config.get('velocidade', 1.0)))
            except:
                pass  # Usa voz padrão se houver erro
        
        # Narrar
        engine.say(texto)
        engine.runAndWait()
        
        print("-"*60 + "\n")
    
    print("="*60)
    print(f" FIM DO CAPÍTULO {numero_capitulo}")
    print("="*60 + "\n")


def narrar_silencioso(caminho_novel: str, numero_capitulo: int):
    """
    Processa e mostra o capítulo sem narrar (modo texto).
    
    Args:
        caminho_novel: Caminho da pasta da novel
        numero_capitulo: Número do capítulo
    """
    print("\n" + "="*60)
    print(f" VISUALIZANDO CAPÍTULO {numero_capitulo} (Modo Texto)")
    print("="*60 + "\n")
    
    leitor = LeitorNovel(caminho_novel)
    segmentos = leitor.processar_capitulo(numero_capitulo)
    
    if not segmentos:
        print("❌ Capítulo não encontrado ou vazio.")
        return
    
    print(f"📖 Novel: {leitor.metadata.get('titulo', 'Sem título')}")
    print(f"📄 Total de segmentos: {len(segmentos)}\n")
    print("-"*60 + "\n")
    
    for segmento in segmentos:
        tipo = segmento['tipo']
        texto = segmento['texto']
        voz_config = segmento.get('voz_config', {})
        
        if tipo == 'narracao':
            print(f"[NARRADOR] (Voz: {voz_config.get('modelo', 'padrão')[:40]}...)")
        else:
            personagem = segmento.get('personagem', 'Desconhecido')
            voz_id = voz_config.get('modelo', 'padrão')
            print(f"[{personagem.upper()}] (Voz: {voz_id[:40]}...)")
        
        print(f"{texto}\n")
        print("-"*60 + "\n")
    
    print("="*60)
    print(f" FIM DO CAPÍTULO {numero_capitulo}")
    print("="*60 + "\n")


def menu_principal():
    """Menu interativo para narração."""
    caminho_novel = './novels/exemplo_novel'
    
    while True:
        print("\n" + "="*60)
        print(" NOVEL READER - SISTEMA DE NARRAÇÃO")
        print("="*60)
        print("\n1. Narrar capítulo com voz (TTS)")
        print("2. Visualizar capítulo (apenas texto)")
        print("3. Listar capítulos disponíveis")
        print("4. Alterar novel")
        print("5. Sair")
        print("\n" + "-"*60)
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            cap = input("Número do capítulo: ").strip()
            try:
                narrar_com_tts(caminho_novel, int(cap))
            except ValueError:
                print("❌ Número inválido.")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif escolha == '2':
            cap = input("Número do capítulo: ").strip()
            try:
                narrar_silencioso(caminho_novel, int(cap))
            except ValueError:
                print("❌ Número inválido.")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif escolha == '3':
            leitor = LeitorNovel(caminho_novel)
            caps = leitor.listar_capitulos_disponiveis()
            print(f"\n📚 Capítulos disponíveis: {caps}")
        
        elif escolha == '4':
            novo_caminho = input("Caminho da novel: ").strip()
            if os.path.exists(novo_caminho):
                caminho_novel = novo_caminho
                print(f"✓ Novel alterada para: {caminho_novel}")
            else:
                print("❌ Caminho não existe.")
        
        elif escolha == '5':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Modo linha de comando
        if sys.argv[1] == '--silencioso':
            narrar_silencioso('./novels/exemplo_novel', 1)
        else:
            narrar_com_tts('./novels/exemplo_novel', int(sys.argv[1]))
    else:
        # Narração rápida do exemplo
        print("\n🎤 DEMONSTRAÇÃO RÁPIDA - Narrando capítulo de exemplo")
        print("(Use: python exemplo_narrar.py --silencioso para modo texto)\n")
        
        input("Pressione ENTER para começar a narração com voz...")
        narrar_com_tts('./novels/exemplo_novel', 1)
        
        print("\n" + "="*60)
        print(" Para modo interativo, execute: menu_principal()")
        print("="*60)

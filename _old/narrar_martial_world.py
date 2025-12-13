"""
Script para narrar Martial World com vozes configuradas
"""

import os
import sys
import io

# Configura encoding para UTF-8
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from leitor import LeitorNovel
from gerenciador_vozes import GerenciadorVozes
from wiki_personagens import WikiPersonagens
import pyttsx3
from gtts import gTTS
import tempfile
import time
import pygame


def configurar_martial_world():
    """Configura vozes e personagens para Martial World."""
    print("\n" + "="*60)
    print(" CONFIGURANDO MARTIAL WORLD")
    print("="*60 + "\n")
    
    caminho_novel = './novels/martial_world'
    
    # Gerenciador de Vozes
    gv = GerenciadorVozes()
    
    # Voz do narrador (Maria - PT-BR)
    print("Configurando voz do narrador...")
    gv.definir_voz_narrador(
        modelo='HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_PT-BR_MARIA_11.0',
        idioma='pt-BR',
        velocidade=1.0
    )
    
    # Wiki de personagens
    wiki = WikiPersonagens(caminho_novel)
    
    # Adicionar personagem principal
    print("Adicionando personagens...")
    
    wiki.adicionar_personagem(
        nome='Lin Ming',
        descricao='Protagonista de Martial World, guerreiro talentoso',
        primeiro_aparecimento='Capítulo 961'
    )
    
    # Voz para Lin Ming (usando Zira com ajustes)
    voz_lin_ming = gv.adicionar_voz(
        nome='Lin Ming',
        tipo='personagem',
        modelo='HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0',
        velocidade=0.95,
        pitch=0.9
    )
    
    wiki.associar_voz('Lin Ming', voz_lin_ming)
    gv.associar_voz_personagem('Lin Ming', voz_lin_ming)
    
    print(f"\n✅ Configuração completa!")
    print(f"   Narrador: Microsoft Maria Desktop")
    print(f"   Lin Ming: {voz_lin_ming}")
    print("="*60 + "\n")


def narrar_capitulo_gtts(numero: int, velocidade: float = 1.5):
    """
    Narra um capítulo usando Google TTS (melhor qualidade).
    Velocidade controlada via frequência do pygame mixer.
    
    Args:
        numero: Número do capítulo
        velocidade: Velocidade de reprodução (1.0 = normal, 1.5 = recomendado, 2.0 = rápido)
    """
    caminho_novel = './novels/martial_world'
    leitor = LeitorNovel(caminho_novel)
    
    print(f"\n{'='*60}")
    print(f" MARTIAL WORLD - CAPÍTULO {numero}")
    print(f" Narração: Google TTS PT-BR (Alta Qualidade)")
    print(f" ⚡ Velocidade: {velocidade}x")
    print(f"{'='*60}\n")
    
    # Carregar capítulo
    capitulo = leitor.carregar_capitulo(numero)
    
    if not capitulo:
        print(f"❌ Capítulo {numero} não encontrado.")
        print(f"   Execute: python extrair_martial_world.py {numero}")
        return
    
    print(f"📖 {capitulo['titulo']}")
    print(f"📄 {len(capitulo['conteudo'])} parágrafos\n")
    print(f"{'='*60}\n")
    
    print("🎤 Narrando com Google TTS...")
    print(f"💡 Velocidade configurada: {velocidade}x\n")
    print("⏯️  Pressione Ctrl+C para interromper\n")
    
    # Inicializar pygame mixer com frequência ajustada para velocidade
    # Aumentar a frequência acelera o áudio
    freq_base = 24000
    freq_ajustada = int(freq_base * velocidade)
    pygame.mixer.init(frequency=freq_ajustada, size=-16, channels=2, buffer=512)
    
    # Criar diretório temporário
    temp_dir = tempfile.gettempdir()
    
    try:
        for i, paragrafo in enumerate(capitulo['conteudo'], 1):
            print(f"[{i}/{len(capitulo['conteudo'])}] {paragrafo[:75]}...")
            
            temp_file = os.path.join(temp_dir, f"mw_audio_{i}.mp3")
            
            try:
                # Gerar TTS com Google (já é rápido e claro)
                # slow=False deixa a voz mais dinâmica
                tts = gTTS(text=paragrafo, lang='pt-br', slow=False, tld='com.br')
                tts.save(temp_file)
                
                # Reproduzir com pygame
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                # Aguardar término da reprodução
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Pausa entre parágrafos (menor = mais dinâmico)
                pausa = 0.3 / velocidade  # Ajusta pausa pela velocidade
                time.sleep(pausa)
                
                # Limpar arquivo temporário
                try:
                    os.remove(temp_file)
                except:
                    pass
            
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                continue
        
        print(f"\n{'='*60}")
        print(f" ✓ FIM DO CAPÍTULO {numero}")
        print(f"{'='*60}\n")
    
    except KeyboardInterrupt:
        print("\n\n⏸️ Narração interrompida.")
        pygame.mixer.music.stop()
    
    finally:
        pygame.mixer.quit()


def narrar_capitulo(numero: int, modo_texto: bool = False, usar_gtts: bool = True, velocidade: float = 1.5):
    """
    Narra um capítulo de Martial World.
    
    Args:
        numero: Número do capítulo
        modo_texto: Se True, apenas mostra texto sem narrar
        usar_gtts: Se True, usa Google TTS (melhor qualidade)
        velocidade: Velocidade de reprodução
    """
    if modo_texto:
        # Modo texto apenas
        caminho_novel = './novels/martial_world'
        leitor = LeitorNovel(caminho_novel)
        
        print(f"\n{'='*60}")
        print(f" MARTIAL WORLD - CAPÍTULO {numero}")
        print(f"{'='*60}\n")
        
        capitulo = leitor.carregar_capitulo(numero)
        
        if not capitulo:
            print(f"❌ Capítulo {numero} não encontrado.")
            return
        
        print(f"📖 {capitulo['titulo']}")
        print(f"📄 {len(capitulo['conteudo'])} parágrafos\n")
        print(f"{'='*60}\n")
        
        for i, paragrafo in enumerate(capitulo['conteudo'], 1):
            print(f"[{i}] {paragrafo}\n")
        
        print(f"\n{'='*60}")
        print(f" FIM DO CAPÍTULO {numero}")
        print(f"{'='*60}\n")
    
    elif usar_gtts:
        narrar_capitulo_gtts(numero, velocidade)
    
    else:
        # Modo pyttsx3 (voz local)
        caminho_novel = './novels/martial_world'
        leitor = LeitorNovel(caminho_novel)
        
        print(f"\n{'='*60}")
        print(f" MARTIAL WORLD - CAPÍTULO {numero}")
        print(f"{'='*60}\n")
        
        capitulo = leitor.carregar_capitulo(numero)
        
        if not capitulo:
            print(f"❌ Capítulo {numero} não encontrado.")
            return
        
        print(f"📖 {capitulo['titulo']}")
        print(f"📄 {len(capitulo['conteudo'])} parágrafos")
        print(f"\n{'='*60}\n")
        
        engine = pyttsx3.init()
        
        # Configurar voz do narrador
        gv = GerenciadorVozes()
        voz_narrador = gv.obter_voz_narrador()
        
        if voz_narrador.get('modelo'):
            try:
                engine.setProperty('voice', voz_narrador['modelo'])
                engine.setProperty('rate', int(150 * velocidade))
            except:
                pass
        
        print("🔊 Iniciando narração...\n")
        input("Pressione ENTER para começar...")
        print()
        
        for i, paragrafo in enumerate(capitulo['conteudo'], 1):
            print(f"[{i}/{len(capitulo['conteudo'])}] {paragrafo[:80]}...")
            
            engine.say(paragrafo)
            engine.runAndWait()
            
            if i < len(capitulo['conteudo']):
                time.sleep(0.3)
        
        print(f"\n{'='*60}")
        print(f" FIM DO CAPÍTULO {numero}")
        print(f"{'='*60}\n")


def menu_principal():
    """Menu principal para Martial World."""
    velocidade = 1.5  # Velocidade padrão
    
    while True:
        print("\n" + "="*60)
        print(" MARTIAL WORLD - NARRADOR")
        print(f" Velocidade atual: {velocidade}x")
        print("="*60)
        print("\n1. Narrar capítulo com voz (Google TTS - Alta Qualidade)")
        print("2. Narrar com voz local (pyttsx3)")
        print("3. Ler capítulo (apenas texto)")
        print("4. Configurar velocidade de narração")
        print("5. Listar capítulos disponíveis")
        print("6. Sair")
        print("\n" + "-"*60)
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            try:
                cap = int(input("Número do capítulo: ").strip())
                narrar_capitulo(cap, modo_texto=False, usar_gtts=True, velocidade=velocidade)
            except ValueError:
                print("❌ Número inválido.")
            except KeyboardInterrupt:
                print("\n\n⏸️ Narração interrompida.")
        
        elif escolha == '2':
            try:
                cap = int(input("Número do capítulo: ").strip())
                narrar_capitulo(cap, modo_texto=False, usar_gtts=False, velocidade=velocidade)
            except ValueError:
                print("❌ Número inválido.")
            except KeyboardInterrupt:
                print("\n\n⏸️ Narração interrompida.")
        
        elif escolha == '3':
            try:
                cap = int(input("Número do capítulo: ").strip())
                narrar_capitulo(cap, modo_texto=True)
            except ValueError:
                print("❌ Número inválido.")
        
        elif escolha == '4':
            try:
                nova_vel = float(input("Nova velocidade (1.0 = normal, 1.5 = recomendado, 2.0 = rápido): ").strip())
                if 0.5 <= nova_vel <= 3.0:
                    velocidade = nova_vel
                    print(f"✓ Velocidade ajustada para {velocidade}x")
                else:
                    print("❌ Velocidade deve estar entre 0.5 e 3.0")
            except ValueError:
                print("❌ Valor inválido.")
        
        elif escolha == '5':
            leitor = LeitorNovel('./novels/martial_world')
            caps = leitor.listar_capitulos_disponiveis()
            
            if caps:
                print(f"\n📚 Capítulos disponíveis: {min(caps)} a {max(caps)}")
                print(f"   Total: {len(caps)} capítulos")
                
                # Mostra primeiros e últimos
                if len(caps) > 10:
                    print(f"   Primeiros: {caps[:5]}")
                    print(f"   Últimos: {caps[-5:]}")
                else:
                    print(f"   Capítulos: {caps}")
            else:
                print("\n❌ Nenhum capítulo disponível.")
                print("   Execute: python extrair_martial_world.py 961")
        
        elif escolha == '6':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    # Verifica se a configuração já foi feita
    import os
    if not os.path.exists('./novels/martial_world/capitulos'):
        print("\n⚠️ Martial World ainda não foi extraído!")
        print("Execute primeiro: python extrair_martial_world.py 961")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        # Linha de comando
        try:
            numero = int(sys.argv[1])
            modo = '--texto' in sys.argv
            usar_local = '--local' in sys.argv
            velocidade = 1.5
            
            # Verifica se há argumento de velocidade
            for arg in sys.argv:
                if arg.startswith('--vel='):
                    velocidade = float(arg.split('=')[1])
            
            narrar_capitulo(numero, modo_texto=modo, usar_gtts=(not usar_local), velocidade=velocidade)
        except ValueError:
            print("❌ Uso: python narrar_martial_world.py [numero] [--texto] [--local] [--vel=1.5]")
    else:
        # Menu interativo
        menu_principal()

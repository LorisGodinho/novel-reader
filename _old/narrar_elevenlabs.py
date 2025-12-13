"""
Narrador com ElevenLabs - Alta Qualidade com Tags de Emoção
"""

import os
import sys
import io
import re

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from leitor import LeitorNovel
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import tempfile
import time
import pygame

# Configurar API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'config'))
from elevenlabs_config import obter_config

config = obter_config()
cliente_elevenlabs = None


def configurar_api_key():
    """Configura a API key do ElevenLabs."""
    global cliente_elevenlabs
    
    api_key = config['api_key']
    
    if not api_key or api_key == '':
        print("\n⚠️ API Key do ElevenLabs não configurada!")
        print("\n📝 Para obter uma chave gratuita:")
        print("1. Acesse: https://elevenlabs.io/")
        print("2. Crie uma conta (10.000 caracteres grátis/mês)")
        print("3. Vá em Profile → API Key")
        print("4. Copie sua chave\n")
        
        api_key = input("Cole sua API Key aqui (ou ENTER para sair): ").strip()
        
        if not api_key:
            return False
        
        # Salvar no .env
        env_path = '.env'
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(f"ELEVENLABS_API_KEY={api_key}\n")
        
        print("✓ API Key salva!\n")
    
    try:
        cliente_elevenlabs = ElevenLabs(api_key=api_key)
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar API: {e}")
        return False


def processar_tags_emocao(texto: str) -> list:
    """
    Processa o texto e identifica tags de emoção.
    
    Args:
        texto: Texto com possíveis tags como [whispers], [giggles]
    
    Returns:
        Lista de segmentos: [{'tipo': 'normal'/'emocao', 'tag': str, 'texto': str}]
    """
    # Padrão para encontrar tags: [palavra]
    padrao = r'\[([^\]]+)\]'
    
    segmentos = []
    ultima_pos = 0
    tag_atual = None
    
    for match in re.finditer(padrao, texto):
        tag = match.group(1).lower()
        pos_inicio = match.start()
        pos_fim = match.end()
        
        # Adiciona texto antes da tag (se houver)
        if pos_inicio > ultima_pos:
            texto_antes = texto[ultima_pos:pos_inicio].strip()
            if texto_antes:
                segmentos.append({
                    'tipo': 'normal' if not tag_atual else 'emocao',
                    'tag': tag_atual,
                    'texto': texto_antes
                })
        
        # Atualiza tag atual para próximo segmento
        tag_atual = tag
        ultima_pos = pos_fim
    
    # Adiciona texto final (se houver)
    if ultima_pos < len(texto):
        texto_final = texto[ultima_pos:].strip()
        if texto_final:
            segmentos.append({
                'tipo': 'emocao' if tag_atual else 'normal',
                'tag': tag_atual,
                'texto': texto_final
            })
    
    # Se não houver segmentos, retorna texto completo
    if not segmentos:
        segmentos.append({
            'tipo': 'normal',
            'tag': None,
            'texto': texto
        })
    
    return segmentos


def adicionar_tags_automaticas(paragrafo: str) -> str:
    """
    Adiciona tags de emoção automaticamente baseado no contexto.
    
    Args:
        paragrafo: Texto do parágrafo
    
    Returns:
        Texto com tags inseridas
    """
    # Detectar diálogos com aspas
    if '"' in paragrafo:
        # Adicionar ênfase antes de diálogos importantes
        paragrafo = re.sub(r'(gritou|berrou)', r'[shouting] \1', paragrafo, flags=re.IGNORECASE)
        paragrafo = re.sub(r'(sussurrou|murmurou)', r'[whispers] \1', paragrafo, flags=re.IGNORECASE)
        paragrafo = re.sub(r'(riu|risos|risadas)', r'[giggles] \1', paragrafo, flags=re.IGNORECASE)
    
    # Frases de suspense
    if any(palavra in paragrafo.lower() for palavra in ['mistério', 'sombra', 'silêncio', 'escuro']):
        if not paragrafo.startswith('['):
            paragrafo = '[mysterious] ' + paragrafo
    
    # Exclamações
    if '!' in paragrafo and 'gritou' not in paragrafo.lower():
        paragrafo = re.sub(r'!', r'! [excited]', paragrafo, count=1)
    
    return paragrafo


def narrar_com_elevenlabs(numero: int, voz_id: str = None, adicionar_tags: bool = True, velocidade: float = 1.3):
    """
    Narra um capítulo usando ElevenLabs com tags de emoção.
    
    Args:
        numero: Número do capítulo
        voz_id: ID da voz (None = usar padrão)
        adicionar_tags: Se True, adiciona tags automaticamente
        velocidade: Não aplicado (ElevenLabs tem velocidade natural ótima)
    """
    if not configurar_api_key():
        print("\n❌ Não é possível narrar sem API Key.")
        return
    
    caminho_novel = './novels/martial_world'
    leitor = LeitorNovel(caminho_novel)
    
    # Selecionar voz
    if not voz_id:
        voz_nome = config['voz_padrao']
        voz_id = config['vozes'][voz_nome]['id']
    else:
        voz_nome = 'Customizada'
    
    print(f"\n{'='*60}")
    print(f" MARTIAL WORLD - CAPÍTULO {numero}")
    print(f" 🎤 Narração: ElevenLabs (Ultra HD)")
    print(f" 🎭 Voz: {voz_nome}")
    print(f" ✨ Tags de emoção: {'Ativadas' if adicionar_tags else 'Desativadas'}")
    print(f"{'='*60}\n")
    
    # Carregar capítulo
    capitulo = leitor.carregar_capitulo(numero)
    
    if not capitulo:
        print(f"❌ Capítulo {numero} não encontrado.")
        return
    
    print(f"📖 {capitulo['titulo']}")
    print(f"📄 {len(capitulo['conteudo'])} parágrafos\n")
    print(f"{'='*60}\n")
    
    print("🎬 Iniciando narração...\n")
    
    # Inicializar pygame para reprodução
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    temp_dir = tempfile.gettempdir()
    
    try:
        for i, paragrafo in enumerate(capitulo['conteudo'], 1):
            print(f"[{i}/{len(capitulo['conteudo'])}] {paragrafo[:70]}...")
            
            # Adicionar tags automáticas se ativado
            if adicionar_tags:
                paragrafo = adicionar_tags_automaticas(paragrafo)
            
            try:
                # Gerar áudio com ElevenLabs
                audio = cliente_elevenlabs.generate(
                    text=paragrafo,
                    voice=voz_id,
                    model=config['modelo']
                )
                
                # Salvar temporariamente
                temp_file = os.path.join(temp_dir, f"eleven_mw_{i}.mp3")
                with open(temp_file, 'wb') as f:
                    f.write(audio)
                
                # Reproduzir
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                # Pausa curta entre parágrafos
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
        
        print(f"\n{'='*60}")
        print(f" ✓ FIM DO CAPÍTULO {numero}")
        print(f"{'='*60}\n")
    
    except KeyboardInterrupt:
        print("\n\n⏸️ Narração interrompida.")
        pygame.mixer.music.stop()
    
    finally:
        pygame.mixer.quit()


def listar_vozes_disponiveis():
    """Lista todas as vozes disponíveis."""
    if not configurar_api_key():
        return
    
    print("\n" + "="*60)
    print(" VOZES DISPONÍVEIS - ELEVENLABS")
    print("="*60 + "\n")
    
    print("Vozes recomendadas para português:\n")
    
    for nome, info in config['vozes'].items():
        print(f"🎤 {nome}")
        print(f"   ID: {info['id']}")
        print(f"   Idioma: {info['idioma']}")
        print(f"   Descrição: {info['descricao']}")
        print(f"   Estilo: {info['estilo']}\n")
    
    print("="*60)
    print("\nPara usar uma voz específica, copie o nome.")


def menu_principal():
    """Menu interativo com ElevenLabs."""
    voz_nome = config['voz_padrao']
    adicionar_tags = True
    
    while True:
        print("\n" + "="*60)
        print(" MARTIAL WORLD - NARRADOR ELEVENLABS")
        print(f" 🎤 Voz: {voz_nome}")
        print(f" ✨ Tags automáticas: {'Sim' if adicionar_tags else 'Não'}")
        print("="*60)
        print("\n1. Narrar capítulo (ElevenLabs Ultra HD)")
        print("2. Escolher voz da narradora")
        print("3. Alternar tags de emoção automáticas")
        print("4. Listar vozes disponíveis")
        print("5. Listar capítulos disponíveis")
        print("6. Testar voz atual")
        print("7. Sair")
        print("\n" + "-"*60)
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            try:
                cap = int(input("Número do capítulo: ").strip())
                voz_id = config['vozes'][voz_nome]['id']
                narrar_com_elevenlabs(cap, voz_id, adicionar_tags)
            except ValueError:
                print("❌ Número inválido.")
            except KeyboardInterrupt:
                print("\n\n⏸️ Narração interrompida.")
        
        elif escolha == '2':
            print("\nVozes disponíveis:")
            for i, nome in enumerate(config['vozes'].keys(), 1):
                print(f"{i}. {nome} - {config['vozes'][nome]['descricao']}")
            
            try:
                idx = int(input("\nEscolha o número: ").strip()) - 1
                vozes_lista = list(config['vozes'].keys())
                if 0 <= idx < len(vozes_lista):
                    voz_nome = vozes_lista[idx]
                    print(f"✓ Voz alterada para: {voz_nome}")
            except:
                print("❌ Opção inválida.")
        
        elif escolha == '3':
            adicionar_tags = not adicionar_tags
            print(f"✓ Tags automáticas: {'Ativadas' if adicionar_tags else 'Desativadas'}")
        
        elif escolha == '4':
            listar_vozes_disponiveis()
        
        elif escolha == '5':
            leitor = LeitorNovel('./novels/martial_world')
            caps = leitor.listar_capitulos_disponiveis()
            
            if caps:
                print(f"\n📚 Capítulos disponíveis: {min(caps)} a {max(caps)}")
                print(f"   Total: {len(caps)} capítulos")
            else:
                print("\n❌ Nenhum capítulo disponível.")
        
        elif escolha == '6':
            print("\n🎤 Testando voz atual...")
            texto_teste = "Olá! Eu sou a narradora de Martial World. [excited] Vamos começar essa aventura épica! [giggles]"
            
            try:
                if not configurar_api_key():
                    continue
                
                voz_id = config['vozes'][voz_nome]['id']
                audio = cliente_elevenlabs.generate(text=texto_teste, voice=voz_id, model=config['modelo'])
                
                pygame.mixer.init()
                temp_file = os.path.join(tempfile.gettempdir(), "teste_voz.mp3")
                with open(temp_file, 'wb') as f:
                    f.write(audio)
                
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                
                pygame.mixer.quit()
                os.remove(temp_file)
                print("✓ Teste concluído!")
            except Exception as e:
                print(f"❌ Erro: {e}")
        
        elif escolha == '7':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    if not os.path.exists('./novels/martial_world/capitulos'):
        print("\n⚠️ Martial World ainda não foi extraído!")
        print("Execute: python extrair_martial_world.py 961")
        sys.exit(1)
    
    menu_principal()

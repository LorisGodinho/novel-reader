"""
Narrador Principal - Sistema Completo com Emoções Customizadas
100% Gratuito usando gTTS + manipulação de áudio
Com controles interativos: Pausar, Avançar, Retroceder
"""

import os
import sys
import io
import threading
from pynput import keyboard

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'engines'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from leitor import LeitorNovel
from emocoes import ProcessadorEmocoes
from narracao import EngineNarracao


class ControladorNarracao:
    """Controla a narração com comandos de teclado."""
    
    def __init__(self):
        self.pausado = False
        self.parar = False
        self.pular_paragrafo = 0  # -1 = anterior, +1 = próximo, 0 = nada
        self.paragrafo_atual = 0
        self.total_paragrafos = 0
        self.capitulo_atual = 0
        self.lock = threading.Lock()
        self.audio_interrompido = False
    
    def pausar_retomar(self):
        """Alterna entre pausado e reproduzindo."""
        with self.lock:
            self.pausado = not self.pausado
            self.audio_interrompido = False
    
    def mostrar_status(self):
        """Mostra status visual no terminal."""
        with self.lock:
            if self.pausado:
                print(f"\n{'='*70}", flush=True)
                print(f"⏸️  PAUSADO", flush=True)
                print(f"📖 Capítulo: {self.capitulo_atual}", flush=True)
                print(f"📄 Parágrafo: {self.paragrafo_atual}/{self.total_paragrafos}", flush=True)
                print(f"{'='*70}\n", flush=True)
            else:
                print(f"\n▶️  REPRODUZINDO\n", flush=True)
    
    def proximo_paragrafo(self):
        """Pula para próximo parágrafo."""
        with self.lock:
            # Só aceitar se não houver comando pendente
            if self.pular_paragrafo == 0:
                self.pular_paragrafo = 1
                self.audio_interrompido = True
                print(f"\n⏭️  Próximo parágrafo\n", flush=True)
    
    def paragrafo_anterior(self):
        """Volta para parágrafo anterior."""
        with self.lock:
            # Só aceitar se não houver comando pendente
            if self.pular_paragrafo == 0:
                self.pular_paragrafo = -1
                self.audio_interrompido = True
                if self.paragrafo_atual > 1:
                    print(f"\n⏮️  Parágrafo anterior\n", flush=True)
    
    def parar_narracao(self):
        """Para a narração completamente."""
        with self.lock:
            self.parar = True
            self.audio_interrompido = True
            print("\n⏹️  PARANDO...\n", flush=True)
    
    def deve_pausar(self):
        with self.lock:
            return self.pausado
    
    def deve_parar(self):
        with self.lock:
            return self.parar
    
    def verificar_pulo(self):
        """Verifica e reseta comando de pulo."""
        with self.lock:
            pulo = self.pular_paragrafo
            if pulo != 0:
                self.pular_paragrafo = 0
            return pulo
    
    def foi_interrompido(self):
        """Verifica se o áudio foi interrompido."""
        with self.lock:
            return self.audio_interrompido
    
    def limpar_interrupcao(self):
        """Limpa flag de interrupção."""
        with self.lock:
            self.audio_interrompido = False


def narrar_capitulo(numero: int, detectar_auto: bool = True, voz: str = 'Francisca', controlador_externo=None):
    """
    Narra um capítulo com sistema de emoções customizado e controles interativos.
    
    Args:
        numero: Número do capítulo
        detectar_auto: Detecta emoções automaticamente do contexto
        voz: Nome da voz a usar
        controlador_externo: Controlador compartilhado (para narração contínua)
    
    Returns:
        True se concluído, False se interrompido
    """
    print("\n" + "="*70)
    print(f" MARTIAL WORLD - CAPÍTULO {numero}")
    print(f" 🎭 Voz: {voz}")
    print(" 🎤 Motor: Microsoft Edge TTS (Gratuito)")
    print("="*70 + "\n")
    
    # Inicializar sistemas
    leitor = LeitorNovel('./novels/martial_world')
    processador = ProcessadorEmocoes()
    engine = EngineNarracao(voz_padrao=voz)
    controlador = controlador_externo if controlador_externo else ControladorNarracao()
    controlador.capitulo_atual = numero
    
    # Carregar capítulo
    capitulo = leitor.carregar_capitulo(numero)
    
    if not capitulo:
        print(f"❌ Capítulo {numero} não encontrado.")
        if not controlador_externo:
            engine.finalizar()
        return False
    
    # Configurar controlador
    controlador.total_paragrafos = len(capitulo['conteudo'])
    
    print(f"📖 {capitulo['titulo']}")
    print(f"📄 {len(capitulo['conteudo'])} parágrafos")
    print(f"✨ Detecção automática: {'Ativada' if detectar_auto else 'Desativada'}")
    print("\n" + "="*70)
    print("\n⌨️  CONTROLES:")
    print("   ESPAÇO  - Pausar/Retomar (mostra posição)")
    print("   →       - Próximo parágrafo")
    print("   ←       - Parágrafo anterior")
    print("   Q       - Parar narração")
    print("\n" + "="*70 + "\n")
    print("🎬 Iniciando narração...\n")
    
    # Configurar listener de teclado apenas se não for controlador externo
    listener = None
    if not controlador_externo:
        def on_press(key):
            try:
                if key == keyboard.Key.space:
                    controlador.pausar_retomar()
                    controlador.mostrar_status()
                elif key == keyboard.Key.right:
                    controlador.proximo_paragrafo()
                elif key == keyboard.Key.left:
                    controlador.paragrafo_anterior()
                elif hasattr(key, 'char') and key.char and key.char.lower() == 'q':
                    controlador.parar_narracao()
                    return False  # Para o listener
            except:
                pass
        
        # Iniciar listener em thread separada
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    
    try:
        i = 0
        while i < len(capitulo['conteudo']):
            # Verificar se deve parar
            if controlador.deve_parar():
                break
            
            # Verificar comando de pulo
            pulo = controlador.verificar_pulo()
            if pulo == 1:  # Próximo
                i = min(i + 1, len(capitulo['conteudo']) - 1)
                controlador.limpar_interrupcao()
                continue
            elif pulo == -1:  # Anterior
                i = max(i - 1, 0)
                controlador.limpar_interrupcao()
                continue
            
            # Atualizar posição
            controlador.paragrafo_atual = i + 1
            
            # Aguardar se pausado
            if controlador.deve_pausar():
                import time
                while controlador.deve_pausar():
                    time.sleep(0.1)
                    if controlador.deve_parar():
                        break
                    # Verificar pulo durante pausa
                    pulo = controlador.verificar_pulo()
                    if pulo != 0:
                        break
            
            if controlador.deve_parar():
                break
            
            # Se pulou durante pausa, processar
            pulo = controlador.verificar_pulo()
            if pulo == 1:
                i = min(i + 1, len(capitulo['conteudo']) - 1)
                controlador.limpar_interrupcao()
                continue
            elif pulo == -1:
                i = max(i - 1, 0)
                controlador.limpar_interrupcao()
                continue
            
            paragrafo = capitulo['conteudo'][i]
            print(f"[{i+1}/{len(capitulo['conteudo'])}] {paragrafo[:65]}...")
            
            # Detectar se é momento de clímax
            is_climax = processador.detectar_climax(paragrafo)
            
            # Extrair segmentos com emoções
            segmentos = processador.extrair_segmentos(paragrafo)
            
            # Se não tem tags e detecção automática está ativa
            if len(segmentos) == 1 and segmentos[0]['emocao'] == 'normal' and detectar_auto:
                emocao_detectada = processador.detectar_emocao_contextual(paragrafo)
                segmentos[0]['emocao'] = emocao_detectada
            
            # Narrar cada segmento
            paragrafo_interrompido = False
            for segmento in segmentos:
                # Processar texto (remover tags, aplicar transformações)
                texto_limpo = processador.processar_texto(
                    segmento['texto'],
                    segmento['emocao']
                )
                
                if not texto_limpo:
                    continue
                
                # Obter configuração da emoção
                config = processador.obter_config_emocao(segmento['emocao'])
                
                # Narrar
                try:
                    engine.narrar_segmento(texto_limpo, config, controlador=controlador)
                    
                    # Verificar se foi interrompido
                    if controlador.foi_interrompido():
                        paragrafo_interrompido = True
                        break
                        
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    continue
            
            # Se não foi interrompido, avançar para próximo parágrafo
            if not paragrafo_interrompido and not controlador.deve_parar():
                print()
                i += 1
                controlador.limpar_interrupcao()
            else:
                # Foi interrompido - aguardar pequeno delay para processar comando
                import time
                time.sleep(0.2)
                print()
        
        print("\n" + "="*70)
        print(f" ✅ CAPÍTULO {numero} CONCLUÍDO")
        print("="*70 + "\n")
        return True
    
    except KeyboardInterrupt:
        print("\n\n⏸️ Narração interrompida.")
        return False
    
    finally:
        if listener:
            listener.stop()
        if not controlador_externo:
            engine.finalizar()


def narrar_continuo(capitulo_inicial: int, detectar_auto: bool = True, voz: str = 'Francisca'):
    """
    Narra capítulos consecutivos automaticamente a partir de um capítulo inicial.
    
    Args:
        capitulo_inicial: Número do capítulo inicial
        detectar_auto: Detecta emoções automaticamente do contexto
        voz: Nome da voz a usar
    """
    print("\n" + "="*70)
    print(f" NARRAÇÃO CONTÍNUA - Iniciando do capítulo {capitulo_inicial}")
    print(f" 🎭 Voz: {voz}")
    print("="*70)
    print("\n⌨️  CONTROLES:")
    print("   ESPAÇO  - Pausar/Retomar")
    print("   →       - Próximo parágrafo")
    print("   ←       - Parágrafo anterior")
    print("   Q       - Parar narração contínua")
    print("\n" + "="*70 + "\n")
    
    # Inicializar sistemas compartilhados
    leitor = LeitorNovel('./novels/martial_world')
    engine = EngineNarracao(voz_padrao=voz)
    controlador = ControladorNarracao()
    
    # Configurar listener de teclado global
    def on_press(key):
        try:
            if key == keyboard.Key.space:
                controlador.pausar_retomar()
                controlador.mostrar_status()
            elif key == keyboard.Key.right:
                controlador.proximo_paragrafo()
            elif key == keyboard.Key.left:
                controlador.paragrafo_anterior()
            elif hasattr(key, 'char') and key.char and key.char.lower() == 'q':
                controlador.parar_narracao()
                return False
        except:
            pass
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    try:
        capitulo_atual = capitulo_inicial
        
        while True:
            # Verificar se deve parar completamente
            if controlador.deve_parar():
                print("\n⏹️  Narração contínua encerrada.")
                break
            
            # Narrar capítulo
            concluido = narrar_capitulo(capitulo_atual, detectar_auto, voz, controlador_externo=controlador)
            
            if not concluido or controlador.deve_parar():
                break
            
            # Perguntar se quer continuar para o próximo
            if not controlador.deve_parar():
                print(f"\n{'─'*70}")
                print(f"Pressione ENTER para o capítulo {capitulo_atual + 1} ou 'Q' para sair...")
                print(f"{'─'*70}\n")
                
                import msvcrt
                import time
                
                # Aguardar 5 segundos ou input do usuário
                timeout = 5
                start = time.time()
                escolha = None
                
                while (time.time() - start) < timeout:
                    if msvcrt.kbhit():
                        char = msvcrt.getch().decode('utf-8', errors='ignore').lower()
                        if char == 'q':
                            escolha = 'q'
                            break
                        elif char == '\r':  # Enter
                            escolha = 'continuar'
                            break
                    time.sleep(0.1)
                    
                    # Verificar se apertou Q via controlador
                    if controlador.deve_parar():
                        escolha = 'q'
                        break
                
                if escolha == 'q' or controlador.deve_parar():
                    print("\n⏹️  Narração contínua encerrada.")
                    break
                
                # Continuar automaticamente se não escolheu sair
                capitulo_atual += 1
                print(f"\n▶️  Continuando para capítulo {capitulo_atual}...\n")
                
    except KeyboardInterrupt:
        print("\n\n⏸️  Narração contínua interrompida.")
    finally:
        listener.stop()
        engine.finalizar()


def menu_principal():
    """Menu interativo."""
    detectar_auto = True
    voz_atual = 'Francisca'
    
    while True:
        print("\n" + "="*70)
        print(" MARTIAL WORLD - NARRADOR MULTI-VOZES")
        print(f" 🎭 Voz atual: {voz_atual}")
        print(f" ✨ Detecção automática: {'Ativada' if detectar_auto else 'Desativada'}")
        print("="*70)
        print("\n1. Narrar capítulo único")
        print("2. Narração contínua (múltiplos capítulos)")
        print("3. Trocar voz da narradora")
        print("4. Alternar detecção automática de emoções")
        print("5. Listar capítulos disponíveis")
        print("6. Sair")
        print("\n" + "-"*70)
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            try:
                cap = int(input("Número do capítulo: ").strip())
                narrar_capitulo(cap, detectar_auto, voz_atual)
            except ValueError:
                print("❌ Número inválido.")
            except KeyboardInterrupt:
                print("\n\n⏸️ Cancelado.")
        
        elif escolha == '2':
            try:
                cap = int(input("Capítulo inicial: ").strip())
                narrar_continuo(cap, detectar_auto, voz_atual)
            except ValueError:
                print("❌ Número inválido.")
            except KeyboardInterrupt:
                print("\n\n⏸️ Cancelado.")
        
        elif escolha == '3':
            print("\n🎤 Vozes disponíveis:")
            vozes = ['Francisca', 'Thalita', 'Antonio', 'Raquel', 'Duarte']
            descricoes = {
                'Francisca': 'Feminino BR - Calma',
                'Thalita': 'Feminino BR - Multilíngue',
                'Antonio': 'Masculino BR',
                'Raquel': 'Feminino PT',
                'Duarte': 'Masculino PT'
            }
            
            for i, v in enumerate(vozes, 1):
                print(f"  {i}. {v:<12} - {descricoes[v]}")
            
            try:
                idx = int(input("\nEscolha (1-5): ").strip()) - 1
                if 0 <= idx < len(vozes):
                    voz_atual = vozes[idx]
                    print(f"✓ Voz alterada para: {voz_atual}")
                else:
                    print("❌ Opção inválida.")
            except:
                print("❌ Entrada inválida.")
        
        elif escolha == '4':
            detectar_auto = not detectar_auto
            print(f"\n✓ Detecção automática: {'Ativada' if detectar_auto else 'Desativada'}")
        
        elif escolha == '5':
            leitor = LeitorNovel('./novels/martial_world')
            caps = leitor.listar_capitulos_disponiveis()
            
            if caps:
                print(f"\n📚 Capítulos disponíveis: {min(caps)} a {max(caps)}")
                print(f"   Total: {len(caps)} capítulos")
            else:
                print("\n❌ Nenhum capítulo disponível.")
        
        elif escolha == '6':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    if not os.path.exists('./novels/martial_world/capitulos'):
        print("\n⚠️ Martial World ainda não foi extraído!")
        print("Execute: python extrair_martial_world.py")
        sys.exit(1)
    
    menu_principal()

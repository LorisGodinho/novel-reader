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
        self.avancar = False
        self.retroceder = False
        self.paragrafo_atual = 0
        self.lock = threading.Lock()
    
    def pausar_retomar(self):
        """Alterna entre pausado e reproduzindo."""
        with self.lock:
            self.pausado = not self.pausado
            status = "⏸️  PAUSADO" if self.pausado else "▶️  REPRODUZINDO"
            print(f"\n{status}\n")
    
    def proximo_paragrafo(self):
        """Pula para próximo parágrafo."""
        with self.lock:
            self.avancar = True
            print("\n⏭️  AVANÇANDO...\n")
    
    def paragrafo_anterior(self):
        """Volta para parágrafo anterior."""
        with self.lock:
            self.retroceder = True
            print("\n⏮️  RETROCEDENDO...\n")
    
    def parar_narracao(self):
        """Para a narração completamente."""
        with self.lock:
            self.parar = True
            print("\n⏹️  PARANDO...\n")
    
    def deve_pausar(self):
        with self.lock:
            return self.pausado
    
    def deve_parar(self):
        with self.lock:
            return self.parar
    
    def deve_avancar(self):
        with self.lock:
            if self.avancar:
                self.avancar = False
                return True
            return False
    
    def deve_retroceder(self):
        with self.lock:
            if self.retroceder:
                self.retroceder = False
                return True
            return False


def narrar_capitulo(numero: int, detectar_auto: bool = True, voz: str = 'Francisca'):
    """
    Narra um capítulo com sistema de emoções customizado e controles interativos.
    
    Args:
        numero: Número do capítulo
        detectar_auto: Detecta emoções automaticamente do contexto
        voz: Nome da voz a usar
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
    controlador = ControladorNarracao()
    
    # Carregar capítulo
    capitulo = leitor.carregar_capitulo(numero)
    
    if not capitulo:
        print(f"❌ Capítulo {numero} não encontrado.")
        return
    
    print(f"📖 {capitulo['titulo']}")
    print(f"📄 {len(capitulo['conteudo'])} parágrafos")
    print(f"✨ Detecção automática: {'Ativada' if detectar_auto else 'Desativada'}")
    print("\n" + "="*70)
    print("\n⌨️  CONTROLES:")
    print("   ESPAÇO  - Pausar/Retomar")
    print("   →       - Próximo parágrafo")
    print("   ←       - Parágrafo anterior")
    print("   Q       - Parar narração")
    print("\n" + "="*70 + "\n")
    print("🎬 Iniciando narração...\n")
    
    # Configurar listener de teclado
    def on_press(key):
        try:
            if key == keyboard.Key.space:
                controlador.pausar_retomar()
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
            
            # Verificar se deve retroceder
            if controlador.deve_retroceder() and i > 0:
                i -= 1
                continue
            
            # Verificar se deve avançar
            if controlador.deve_avancar():
                i += 1
                continue
            
            # Aguardar se pausado
            while controlador.deve_pausar():
                import time
                time.sleep(0.1)
                if controlador.deve_parar():
                    break
            
            if controlador.deve_parar():
                break
            
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
            for segmento in segmentos:
                # Verificar novamente se deve pular
                if controlador.deve_avancar() or controlador.deve_retroceder() or controlador.deve_parar():
                    break
                
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
                except Exception as e:
                    print(f"   ❌ Erro: {e}")
                    continue
            
            print()
            i += 1
        
        print("\n" + "="*70)
        print(f" ✅ CAPÍTULO {numero} CONCLUÍDO")
        print("="*70 + "\n")
    
    except KeyboardInterrupt:
        print("\n\n⏸️ Narração interrompida.")
    
    finally:
        listener.stop()
        engine.finalizar()


def testar_emocoes(voz: str = 'Francisca'):
    """Testa todas as emoções disponíveis."""
    print("\n" + "="*70)
    print(f" TESTE DE EMOÇÕES - Voz: {voz}")
    print("="*70 + "\n")
    
    processador = ProcessadorEmocoes()
    engine = EngineNarracao(voz_padrao=voz)
    
    testes = [
        "[normal] Este é um texto normal de narração.",
        "[sussurro] Ele sussurrou algo importante.",
        "[grito] Lin Ming gritou com toda sua força!",
        "[riso] Ela riu da situação absurda.",
        "[brincalhao] Não se atreva a fazer isso novamente!",
        "[misterioso] Uma sombra surgiu no escuro.",
        "[animado] Incrível! Isso é fantástico!",
        "[triste] Lágrimas correram por seu rosto.",
        "[raiva] A raiva explodiu em seu peito!",
        "[suspiro] Ele suspirou profundamente."
    ]
    
    for i, texto in enumerate(testes, 1):
        print(f"[{i}/{len(testes)}] Testando: {texto}")
        
        segmentos = processador.extrair_segmentos(texto)
        
        for segmento in segmentos:
            texto_limpo = processador.processar_texto(
                segmento['texto'],
                segmento['emocao']
            )
            
            config = processador.obter_config_emocao(segmento['emocao'])
            
            print(f"   Emoção: {segmento['emocao']}")
            print(f"   Velocidade: {config['velocidade']}x")
            print(f"   Volume: {config['volume']:+d}dB\n")
            
            try:
                engine.narrar_segmento(texto_limpo, config)
            except Exception as e:
                print(f"   ❌ Erro: {e}\n")
                continue
    
    engine.finalizar()
    print("\n✅ Teste concluído!\n")


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
        print("\n1. Narrar capítulo")
        print("2. Trocar voz da narradora")
        print("3. Alternar detecção automática de emoções")
        print("4. Testar sistema de emoções")
        print("5. Listar capítulos disponíveis")
        print("6. Ajuda - Como usar tags de emoção")
        print("7. Sair")
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
        
        elif escolha == '3':
            detectar_auto = not detectar_auto
            print(f"\n✓ Detecção automática: {'Ativada' if detectar_auto else 'Desativada'}")
        
        elif escolha == '4':
            testar_emocoes(voz_atual)
        
        elif escolha == '5':
            leitor = LeitorNovel('./novels/martial_world')
            caps = leitor.listar_capitulos_disponiveis()
            
            if caps:
                print(f"\n📚 Capítulos disponíveis: {min(caps)} a {max(caps)}")
                print(f"   Total: {len(caps)} capítulos")
            else:
                print("\n❌ Nenhum capítulo disponível.")
        
        elif escolha == '6':
            mostrar_ajuda()
        
        elif escolha == '7':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


def mostrar_ajuda():
    """Mostra ajuda sobre tags de emoção."""
    print("\n" + "="*70)
    print(" COMO USAR TAGS DE EMOÇÃO")
    print("="*70)
    print("\nVocê pode adicionar tags nos capítulos para controlar a narração:")
    print("\n📝 TAGS DISPONÍVEIS:")
    print("   [sussurro] ou [whispers] - Voz baixa e lenta")
    print("   [grito] ou [shouting] - Voz alta e rápida")
    print("   [riso] ou [giggles] - Insere risada + tom alegre")
    print("   [brincalhao] ou [provocador] - Separa sílabas: 'nã-ão'")
    print("   [misterioso] ou [mysterious] - Voz lenta e grave")
    print("   [animado] ou [excited] - Voz rápida e energética")
    print("   [triste] ou [sadly] - Voz lenta e baixa")
    print("   [raiva] ou [angrily] - Voz alta e intensa")
    print("   [suspiro] ou [sighs] - Insere suspiro")
    print("\n💡 EXEMPLOS:")
    print('   "Não faça isso!", [grito] ele berrou.')
    print('   [sussurro] "Venha aqui", ela murmurou.')
    print('   [brincalhao] "Fa-ça vo-cê mes-mo!"')
    print("\n✨ DETECÇÃO AUTOMÁTICA:")
    print("   O sistema detecta automaticamente palavras como:")
    print("   - 'sussurrou', 'murmurou' → sussurro")
    print("   - 'gritou', 'berrou' → grito")
    print("   - 'riu', 'sorriu' → riso")
    print("   - 'explodiu', '!!!' → clímax (+ velocidade/volume)")
    print("\n" + "="*70)


if __name__ == "__main__":
    if not os.path.exists('./novels/martial_world/capitulos'):
        print("\n⚠️ Martial World ainda não foi extraído!")
        print("Execute: python extrair_martial_world.py")
        sys.exit(1)
    
    menu_principal()

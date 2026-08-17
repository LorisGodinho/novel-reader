"""
Novel Reader - Interface Gráfica Moderna
Sistema de narração com controles visuais avançados e tema escuro
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import asyncio
import pygame
import edge_tts
import tempfile
import time
import json
import shutil
import subprocess
from queue import Queue
from collections import OrderedDict

# Função para obter caminho base (funciona com PyInstaller)
def obter_caminho_base():
    """Retorna o caminho base, considerando se está executando como executável."""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Adicionar paths
base_path = obter_caminho_base()
sys.path.insert(0, os.path.join(base_path, 'src'))
from leitor import LeitorNovel


# ===== TEMA ESCURO MODERNO =====
class TemaEscuro:
    """Configurações de tema escuro moderno com contraste otimizado para UX."""
    
    # Cores principais (contraste adequado WCAG 2.1)
    BG_PRINCIPAL = "#1a1b26"        # Fundo principal mais escuro
    BG_SECUNDARIO = "#24283b"       # Fundo secundário com melhor contraste
    BG_TERCIARIO = "#2f3549"        # Fundo terciário destacado
    BG_HOVER = "#3b4261"            # Hover state mais visível
    BG_CARD = "#1f2335"             # Cards e painéis
    
    # Acentos (saturação reduzida para conforto visual)
    ACCENT_PRIMARY = "#7aa2f7"      # Azul suave
    ACCENT_SECONDARY = "#bb9af7"    # Roxo suave
    ACCENT_SUCCESS = "#9ece6a"      # Verde suave
    ACCENT_WARNING = "#e0af68"      # Amarelo suave
    ACCENT_DANGER = "#f7768e"       # Vermelho suave
    ACCENT_INFO = "#7dcfff"         # Ciano suave
    
    # Textos (contraste otimizado)
    TEXT_PRIMARY = "#e2e8f0"        # Texto principal (contraste 13.5:1)
    TEXT_SECONDARY = "#a9b1d6"      # Texto secundário (contraste 7.5:1)
    TEXT_MUTED = "#565f89"          # Texto menos importante (contraste 4.5:1)
    TEXT_DISABLED = "#414868"       # Texto desabilitado
    
    # Bordas e sombras
    BORDER = "#45475a"
    SHADOW = "#11111b"
    
    # Highlight (mais sutil)
    HIGHLIGHT_BG = "#3d3d52"  # Cinza azulado sutil
    
    @staticmethod
    def aplicar_tema(root):
        """Aplica tema escuro ao ttk."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurações gerais
        style.configure('.', 
            background=TemaEscuro.BG_PRINCIPAL,
            foreground=TemaEscuro.TEXT_PRIMARY,
            bordercolor=TemaEscuro.BORDER,
            fieldbackground=TemaEscuro.BG_SECUNDARIO,
            troughcolor=TemaEscuro.BG_SECUNDARIO,
            selectbackground=TemaEscuro.ACCENT_PRIMARY,
            selectforeground=TemaEscuro.BG_PRINCIPAL,
            font=('Segoe UI', 10))
        
        # Labels
        style.configure('TLabel',
            background=TemaEscuro.BG_PRINCIPAL,
            foreground=TemaEscuro.TEXT_PRIMARY)
        
        # LabelFrames
        style.configure('TLabelframe',
            background=TemaEscuro.BG_PRINCIPAL,
            foreground=TemaEscuro.TEXT_PRIMARY,
            bordercolor=TemaEscuro.BORDER,
            borderwidth=1,
            relief='solid')
        
        style.configure('TLabelframe.Label',
            background=TemaEscuro.BG_PRINCIPAL,
            foreground=TemaEscuro.ACCENT_PRIMARY,
            font=('Segoe UI', 10, 'bold'))
        
        # Buttons
        style.configure('TButton',
            background=TemaEscuro.BG_TERCIARIO,
            foreground=TemaEscuro.TEXT_PRIMARY,
            bordercolor=TemaEscuro.BORDER,
            focuscolor=TemaEscuro.ACCENT_PRIMARY,
            lightcolor=TemaEscuro.BG_HOVER,
            darkcolor=TemaEscuro.BG_SECUNDARIO,
            borderwidth=1,
            relief='flat',
            padding=(10, 5))
        
        style.map('TButton',
            background=[('active', TemaEscuro.BG_HOVER), ('pressed', TemaEscuro.ACCENT_PRIMARY)],
            foreground=[('active', TemaEscuro.TEXT_PRIMARY)])
        
        # Accent Button
        style.configure('Accent.TButton',
            background=TemaEscuro.ACCENT_PRIMARY,
            foreground=TemaEscuro.BG_PRINCIPAL,
            font=('Segoe UI', 10, 'bold'),
            borderwidth=0,
            padding=(15, 8))
        
        style.map('Accent.TButton',
            background=[('active', TemaEscuro.ACCENT_SECONDARY), ('pressed', TemaEscuro.ACCENT_PRIMARY)])
        
        # Success Button
        style.configure('Success.TButton',
            background=TemaEscuro.ACCENT_SUCCESS,
            foreground=TemaEscuro.BG_PRINCIPAL,
            font=('Segoe UI', 9, 'bold'),
            borderwidth=0,
            padding=(10, 5))
        
        # Danger Button
        style.configure('Danger.TButton',
            background=TemaEscuro.ACCENT_DANGER,
            foreground=TemaEscuro.BG_PRINCIPAL,
            font=('Segoe UI', 9, 'bold'),
            borderwidth=0,
            padding=(10, 5))
        
        # Combobox - Estilo moderno e responsivo
        style.map('TCombobox', 
            fieldbackground=[('readonly', TemaEscuro.BG_TERCIARIO)],
            selectbackground=[('readonly', TemaEscuro.BG_TERCIARIO)],
            foreground=[('readonly', TemaEscuro.TEXT_PRIMARY)])
        
        style.configure('TCombobox',
            background=TemaEscuro.BG_TERCIARIO,
            foreground=TemaEscuro.TEXT_PRIMARY,
            bordercolor=TemaEscuro.BORDER,
            arrowcolor=TemaEscuro.ACCENT_PRIMARY,
            relief='flat',
            borderwidth=2,
            padding=8)
        
        # Notebook - Abas com cores corretas
        style.configure('TNotebook',
            background=TemaEscuro.BG_PRINCIPAL,
            borderwidth=0,
            tabmargins=[2, 5, 2, 0])
        
        style.configure('TNotebook.Tab',
            background=TemaEscuro.BG_SECUNDARIO,
            foreground=TemaEscuro.TEXT_PRIMARY,
            padding=[20, 10],
            borderwidth=1,
            font=('Segoe UI', 10))
        
        style.map('TNotebook.Tab',
            background=[('selected', TemaEscuro.BG_TERCIARIO), ('active', TemaEscuro.BG_HOVER)],
            foreground=[('selected', TemaEscuro.TEXT_PRIMARY), ('active', TemaEscuro.TEXT_PRIMARY)],
            expand=[('selected', [1, 1, 1, 0])])
        
        # Combobox grande e moderna - para seleção de BGMs
        style.configure('BGM.TCombobox',
            background=TemaEscuro.BG_TERCIARIO,
            foreground=TemaEscuro.TEXT_PRIMARY,
            fieldbackground=TemaEscuro.BG_TERCIARIO,
            bordercolor=TemaEscuro.ACCENT_PRIMARY,
            arrowcolor=TemaEscuro.ACCENT_PRIMARY,
            relief='flat',
            borderwidth=2,
            padding=10,
            font=('Segoe UI', 10, 'bold'))
        
        style.map('BGM.TCombobox',
            fieldbackground=[('readonly', TemaEscuro.BG_TERCIARIO), ('hover', TemaEscuro.BG_HOVER)],
            bordercolor=[('focus', TemaEscuro.ACCENT_PRIMARY), ('hover', TemaEscuro.ACCENT_SECONDARY)],
            foreground=[('readonly', TemaEscuro.TEXT_PRIMARY)])
        
        # Spinbox
        style.configure('TSpinbox',
            background=TemaEscuro.BG_SECUNDARIO,
            foreground=TemaEscuro.TEXT_PRIMARY,
            fieldbackground=TemaEscuro.BG_SECUNDARIO,
            selectbackground=TemaEscuro.ACCENT_PRIMARY,
            bordercolor=TemaEscuro.BORDER,
            arrowcolor=TemaEscuro.TEXT_PRIMARY)
        
        # Scale
        style.configure('TScale',
            background=TemaEscuro.BG_PRINCIPAL,
            troughcolor=TemaEscuro.BG_SECUNDARIO,
            bordercolor=TemaEscuro.BORDER,
            lightcolor=TemaEscuro.ACCENT_PRIMARY,
            darkcolor=TemaEscuro.ACCENT_PRIMARY)
        
        # Frames
        style.configure('TFrame',
            background=TemaEscuro.BG_PRINCIPAL)
        
        style.configure('Card.TFrame',
            background=TemaEscuro.BG_SECUNDARIO,
            borderwidth=1,
            relief='solid')


class MusicaFundo:
    """Gerenciador de música de fundo."""
    
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=256)
        pygame.mixer.set_num_channels(8)
        self.canal_musica = pygame.mixer.Channel(0)
        self.canal_narrador = pygame.mixer.Channel(1)
        
        # Dicionário para armazenar todas as músicas
        self.musicas = {}  # {nome_arquivo: pygame.Sound}
        
        # Música selecionada atualmente
        self.musica_atual = None
        
        self.som_atual = None
        self.modo_atual = None
        self.volume_musica = 0.3
        self.mutado = False
        
    def carregar_musicas(self):
        """Carrega todas as músicas de fundo disponíveis."""
        base_path = os.path.join(obter_caminho_base(), 'assets', 'audio', 'background')
        
        try:
            if os.path.exists(base_path):
                arquivos = os.listdir(base_path)
                
                # Carregar TODOS os arquivos MP3
                mp3_files = [f for f in arquivos if f.endswith('.mp3')]
                
                if mp3_files:
                    for bgm in mp3_files:
                        try:
                            path = os.path.join(base_path, bgm)
                            self.musicas[bgm] = pygame.mixer.Sound(path)
                            print(f"✓ Música carregada: {bgm}")
                        except Exception as e:
                            print(f"❌ Erro ao carregar {bgm}: {e}")
                    
                    # Selecionar primeira como padrão
                    if self.musicas:
                        self.musica_atual = list(self.musicas.keys())[0]
                        print(f"🎵 {len(self.musicas)} músicas carregadas")
                else:
                    print(f"⚠️ Nenhum arquivo MP3 encontrado em {base_path}")
            else:
                print(f"⚠️ Pasta de músicas não encontrada: {base_path}")
        except Exception as e:
            print(f"❌ Erro ao carregar músicas: {e}")
    
    def obter_lista_musicas(self):
        """Retorna lista de nomes das músicas para o combobox."""
        return list(self.musicas.keys())
    
    def selecionar_musica(self, nome_arquivo):
        """Seleciona uma música específica."""
        if nome_arquivo in self.musicas:
            self.musica_atual = nome_arquivo
            print(f"🎵 Música selecionada: {nome_arquivo}")
            return True
        return False
    
    def tocar_normal(self):
        """Toca música de fundo."""
        if self.musica_atual and self.musica_atual in self.musicas:
            self.canal_musica.stop()
            self.som_atual = self.musicas[self.musica_atual]
            self.som_atual.set_volume(0 if self.mutado else self.volume_musica)
            self.canal_musica.play(self.som_atual, loops=-1)
            self.modo_atual = 'normal'
            print(f"▶️ Tocando: {self.musica_atual} (volume: {self.volume_musica:.2f})")
        else:
            print("❌ Música não disponível")
    
    def mutar(self, mutar=True):
        """Muta/desmuta música."""
        self.mutado = mutar
        if self.som_atual:
            self.som_atual.set_volume(0 if self.mutado else self.volume_musica)
        print(f"🔇 Música {'mutada' if mutar else 'desmutada'}")
    
    def set_volume(self, volume):
        """Define volume da música (0.0 a 1.0)."""
        self.volume_musica = volume
        if self.som_atual and not self.mutado:
            self.som_atual.set_volume(volume)
        print(f"🎚️ Volume música: {int(volume * 100)}%")
    
    def parar(self):
        """Para a música."""
        self.canal_musica.stop()
        self.som_atual = None


class EngineNarracaoSimples:
    """Engine simplificado sem emoções com sistema de pré-carregamento otimizado."""
    
    VOZES = {
        'Francisca': 'pt-BR-FranciscaNeural',
        'Thalita': 'pt-BR-ThalitaMultilingualNeural',
        'Antonio': 'pt-BR-AntonioNeural',
        'Raquel': 'pt-PT-RaquelNeural',
        'Duarte': 'pt-PT-DuarteNeural'
    }
    
    # Edge TTS soa natural até ~1.5×; acima disso usamos ffmpeg (atempo)
    # para acelerar de verdade preservando o tom da voz.
    RATE_NATIVO_MAX = 1.5

    def __init__(self, voz='Francisca', canal=None):
        self.voz_atual = self.VOZES.get(voz, self.VOZES['Francisca'])
        self.temp_dir = tempfile.gettempdir()
        self.canal = canal if canal else pygame.mixer.Channel(1)
        self.volume = 1.0
        self.multiplicador = 1.0  # 0.5× a 3.0×
        self.pausado = False
        self.som_atual = None
        self.ffmpeg = self._localizar_ffmpeg()

        # Sistema de cache otimizado com OrderedDict para LRU
        self.cache_sounds = OrderedDict()  # {chave: pygame.Sound}
        self.max_cache_size = 16  # Janela de pré-carregamento maior

        # Sistema de pré-carregamento com thread dedicada
        self.fila_precarregamento = Queue()
        self.desejados = set()       # chaves já enfileiradas/em cache (evita duplicar)
        self._lock = threading.Lock()
        self.thread_precarregamento = None
        self.precarregamento_ativo = False
        self._iniciar_thread_precarregamento()

    # ----- Helpers de velocidade / ffmpeg -----
    def _localizar_ffmpeg(self):
        """Retorna o caminho do ffmpeg.exe empacotado, ou 'ffmpeg' do PATH."""
        candidato = os.path.join(obter_caminho_base(), 'ffmpeg.exe')
        if os.path.exists(candidato):
            return candidato
        return shutil.which('ffmpeg') or 'ffmpeg'

    def _chave(self, texto: str) -> str:
        """Chave de cache única por texto + velocidade + voz."""
        return f"{hash(texto)}_{self.multiplicador:.2f}_{self.voz_atual}"

    def _decompor_velocidade(self):
        """Divide o multiplicador entre rate nativo (Edge) e residual (ffmpeg)."""
        mult = max(0.5, min(3.0, self.multiplicador))
        nativo = min(mult, self.RATE_NATIVO_MAX)
        edge_rate_pct = int(round((nativo - 1.0) * 100))
        residual = mult / nativo  # 1.0 .. 2.0
        return edge_rate_pct, residual

    def _aplicar_ffmpeg(self, entrada: str, residual: float, chave: str) -> str:
        """Acelera o áudio via ffmpeg atempo (tom preservado). Fallback: retorna entrada."""
        if residual <= 1.001:
            return entrada
        saida = os.path.join(self.temp_dir, f'tts_x_{abs(hash(chave))}.mp3')
        if os.path.exists(saida):
            return saida
        try:
            flags = 0
            if os.name == 'nt':
                flags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            subprocess.run(
                [self.ffmpeg, '-y', '-i', entrada,
                 '-filter:a', f'atempo={residual:.4f}',
                 '-vn', saida],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                creationflags=flags, timeout=30
            )
            if os.path.exists(saida) and os.path.getsize(saida) > 0:
                return saida
        except Exception as e:
            print(f"⚠️ ffmpeg indisponível ({e}); usando velocidade nativa (teto ~2×)")
        return entrada

    def _iniciar_thread_precarregamento(self):
        """Inicia thread dedicada para pré-carregamento."""
        self.precarregamento_ativo = True
        self.thread_precarregamento = threading.Thread(
            target=self._worker_precarregamento,
            daemon=True
        )
        self.thread_precarregamento.start()

    def _worker_precarregamento(self):
        """Worker thread que processa fila de pré-carregamento."""
        while self.precarregamento_ativo:
            try:
                texto = self.fila_precarregamento.get(timeout=1.0)
                if not texto or not texto.strip():
                    continue

                chave = self._chave(texto)
                if chave in self.cache_sounds:
                    self.desejados.discard(chave)
                    continue

                arquivo = asyncio.run(self._gerar_audio_async(texto))
                som = pygame.mixer.Sound(arquivo)

                with self._lock:
                    self.cache_sounds[chave] = som
                    if len(self.cache_sounds) > self.max_cache_size:
                        self.cache_sounds.popitem(last=False)
                    self.desejados.discard(chave)

                print(f"✓ Pré-carregado em background (buffer: {len(self.cache_sounds)})")
            except Exception as e:
                if not isinstance(e, TimeoutError):
                    pass  # Timeout é normal quando não há nada na fila

    async def _gerar_audio_async(self, texto: str):
        """Gera áudio via Edge TTS e aplica ffmpeg quando > 1.5×."""
        chave = self._chave(texto)
        edge_rate_pct, residual = self._decompor_velocidade()
        rate = f"{edge_rate_pct:+d}%"
        base = os.path.join(self.temp_dir, f'tts_{abs(hash(chave))}_r{edge_rate_pct}.mp3')

        if not os.path.exists(base):
            communicate = edge_tts.Communicate(texto, self.voz_atual, rate=rate)
            await communicate.save(base)

        return self._aplicar_ffmpeg(base, residual, chave)

    def set_velocidade(self, multiplicador):
        """Define a velocidade como multiplicador (0.5× a 3.0×)."""
        self.multiplicador = max(0.5, min(3.0, float(multiplicador)))
        print(f"⚡ Velocidade narração: {self.multiplicador:.2f}×")

    def set_volume(self, volume):
        """Define volume (0.0 a 1.0)."""
        self.volume = volume
        if self.som_atual:
            self.som_atual.set_volume(volume)
        print(f"🎙️ Volume narração: {int(volume * 100)}%")

    def pausar(self):
        """Pausa a narração."""
        if self.canal.get_busy():
            self.canal.pause()
            self.pausado = True

    def despausar(self):
        """Continua a narração."""
        if self.pausado:
            self.canal.unpause()
            self.pausado = False

    def parar(self):
        """Para a narração completamente."""
        self.canal.stop()
        self.pausado = False

    def solicitar_precarregamento(self, texto: str):
        """Compat: pré-carrega um único parágrafo."""
        self.solicitar_precarregamento_lote([texto])

    def solicitar_precarregamento_lote(self, textos):
        """Enfileira uma janela de parágrafos, sem limpar o cache existente."""
        for texto in textos:
            if not texto or not texto.strip():
                continue
            chave = self._chave(texto)
            with self._lock:
                if chave in self.cache_sounds or chave in self.desejados:
                    continue
                self.desejados.add(chave)
            self.fila_precarregamento.put(texto)

    def narrar(self, texto: str, callback_pausado=None):
        """Narra texto simples com suporte a pausa e cache."""
        if not texto.strip():
            return

        try:
            chave = self._chave(texto)

            if chave in self.cache_sounds:
                self.som_atual = self.cache_sounds[chave]
                print(f"⚡ Usando áudio do cache (transição instantânea)")
            else:
                print(f"⚠️ Áudio não estava em cache, gerando...")
                arquivo = asyncio.run(self._gerar_audio_async(texto))
                self.som_atual = pygame.mixer.Sound(arquivo)
                with self._lock:
                    self.cache_sounds[chave] = self.som_atual

            self.som_atual.set_volume(self.volume)
            self.canal.play(self.som_atual)

            while self.canal.get_busy() or self.pausado:
                if callback_pausado and callback_pausado():
                    if not self.pausado:
                        self.pausar()
                elif self.pausado:
                    self.despausar()
                time.sleep(0.01)  # Reduzir sleep para melhor responsividade
        except Exception as e:
            print(f"Erro ao narrar: {e}")

    def limpar_cache(self):
        """Limpa o cache de áudios."""
        with self._lock:
            self.cache_sounds.clear()
            self.desejados.clear()
        print("🗑️ Cache de áudio limpo")

    def trocar_voz(self, nova_voz):
        """Troca a voz e limpa o cache."""
        voz_id = self.VOZES.get(nova_voz, self.VOZES['Francisca'])
        if voz_id != self.voz_atual:
            self.voz_atual = voz_id
            self.limpar_cache()
            print(f"🎙️ Voz alterada para: {nova_voz}")

    def parar_precarregamento(self):
        """Para a thread de pré-carregamento."""
        self.precarregamento_ativo = False
        if self.thread_precarregamento:
            self.thread_precarregamento.join(timeout=2.0)


class NovelReaderGUI:
    """Interface gráfica moderna do Novel Reader."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Novel Reader - Martial World")
        self.root.geometry("1100x800")
        self.root.minsize(1000, 700)  # Tamanho mínimo otimizado para todos os elementos
        self.root.resizable(True, True)  # ✓ Interface redimensionável
        
        # Aplicar tema escuro
        self.root.configure(bg=TemaEscuro.BG_PRINCIPAL)
        TemaEscuro.aplicar_tema(self.root)
        
        # Configurar grid weights para redimensionamento
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Estado
        self.narrando = False
        self.pausado = False
        self.capitulo_atual = 961
        self.paragrafo_atual = 1
        self.capitulos_disponiveis = []
        self.conteudo_capitulo = []
        self.arquivo_progresso = os.path.join(obter_caminho_base(), 'config', 'progresso.json')
        self.palavras_narradas = 0  # Para tracking de highlight
        self.tempo_inicio_narracao = None
        self.tempo_total_narracao = 0
        self.modo_compacto = False  # Controla layout adaptativo
        self.modo_leitura = True   # Modo de leitura imersivo ativo por padrão
        self.velocidade_mult = 1.0  # Multiplicador de velocidade (0.5×–3.0×)
        self.pular_para = None      # Sinal de "pular para parágrafo" para o loop
        self.imersivo_total = False # Tela cheia sem cabeçalho
        self.drawer_aberto = False  # Painel lateral de configurações
        self._cache_prox_capitulo = {}  # {numero: conteudo} prefetch de capítulos
        self._barra_timer = None    # Timer de auto-hide da barra flutuante

        # Configurações de estilização de texto
        self.config_texto = {
            'paleta': 'padrao',
            'tamanho_fonte': 13
        }
        self.carregar_config_texto()
        
        # Sistemas
        self.leitor = LeitorNovel(os.path.join(obter_caminho_base(), 'novels', 'martial_world'))
        self.musica = MusicaFundo()
        self.engine = None
        self.thread_narracao = None
        
        # Criar interface
        self.criar_interface()
        self.carregar_capitulos()
        self.carregar_progresso()
        self.musica.carregar_musicas()
        self.inicializar_comboboxes_bgm()

        # Renderizar o capítulo no modo leitura já na abertura
        if self.conteudo_capitulo:
            self.atualizar_display_modo_leitura()
        self.atualizar_status()

        # Bind de foco e redimensionamento
        self.root.bind('<FocusIn>', self.on_focus)
        self.root.bind('<FocusOut>', self.on_unfocus)
        self.root.bind('<Configure>', self.on_resize)
        self.tem_foco = True

        # Atalhos de teclado (comandos dinâmicos)
        self._registrar_atalhos()

        # Auto-hide da barra flutuante ao mover o mouse
        self.root.bind('<Motion>', self._on_mouse_activity)
        self._agendar_esconder_barra()

        # Protocolo para fechar janela
        self.root.protocol("WM_DELETE_WINDOW", self.on_fechar_janela)
    
    def criar_interface(self):
        """Monta a interface imersiva: cabeçalho fino, texto em tela cheia,
        barra de player flutuante auto-oculta e drawer lateral de ajustes."""
        # Cores das listbox dos comboboxes (aplicar uma vez)
        self.root.option_add('*TCombobox*Listbox.background', TemaEscuro.BG_SECUNDARIO)
        self.root.option_add('*TCombobox*Listbox.foreground', TemaEscuro.TEXT_PRIMARY)
        self.root.option_add('*TCombobox*Listbox.selectBackground', TemaEscuro.ACCENT_PRIMARY)
        self.root.option_add('*TCombobox*Listbox.selectForeground', TemaEscuro.BG_PRINCIPAL)

        # Container principal
        main_container = ttk.Frame(self.root)
        main_container.grid(row=0, column=0, sticky='nsew')
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)  # texto expande

        # Cabeçalho fino
        self.criar_cabecalho(main_container)

        # Área de texto (ocupa a tela)
        self.frame_texto = ttk.Frame(main_container)
        self.frame_texto.grid(row=1, column=0, sticky='nsew')
        self.frame_texto.grid_rowconfigure(0, weight=1)
        self.frame_texto.grid_columnconfigure(0, weight=1)
        self.criar_area_visualizacao(self.frame_texto)

        # Overlays flutuantes
        self.criar_barra_player()
        self.criar_drawer()

    def criar_cabecalho(self, parent):
        """Cabeçalho fino com título, posição, status e engrenagem."""
        self.header_frame = ttk.Frame(parent, padding=(14, 8))
        self.header_frame.grid(row=0, column=0, sticky='ew')
        self.header_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(self.header_frame, text="📚 Novel Reader",
                  font=('Segoe UI', 14, 'bold'),
                  foreground=TemaEscuro.ACCENT_PRIMARY).grid(row=0, column=0, sticky='w')

        info = ttk.Frame(self.header_frame)
        info.grid(row=0, column=1, sticky='w', padx=16)
        self.lbl_posicao = ttk.Label(info, text="Capítulo: - | Parágrafo: -/-",
                                     font=('Segoe UI', 10))
        self.lbl_posicao.pack(side='left', padx=(0, 14))
        self.lbl_cap_info = ttk.Label(info, text="", font=('Segoe UI', 9),
                                      foreground=TemaEscuro.ACCENT_SUCCESS)
        self.lbl_cap_info.pack(side='left', padx=(0, 14))
        self.lbl_progresso_total = ttk.Label(info, text="", font=('Segoe UI', 9),
                                             foreground=TemaEscuro.TEXT_SECONDARY)
        self.lbl_progresso_total.pack(side='left')

        self.status_badge = tk.Label(self.header_frame, text="⏹️ PARADO",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg=TemaEscuro.BG_TERCIARIO,
                                     fg=TemaEscuro.TEXT_SECONDARY,
                                     padx=12, pady=4, relief='flat', borderwidth=0)
        self.status_badge.grid(row=0, column=2, sticky='e', padx=(0, 8))

        ttk.Button(self.header_frame, text="⚙️", width=3,
                   command=self.toggle_drawer).grid(row=0, column=3, sticky='e')

    def criar_area_visualizacao(self, parent):
        """Área de leitura em tela cheia."""
        text_container = ttk.Frame(parent)
        text_container.grid(row=0, column=0, sticky='nsew')
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)

        self.text_paragrafo = tk.Text(
            text_container, wrap='word',
            font=('Segoe UI', self.config_texto.get('tamanho_fonte', 13)),
            bg=TemaEscuro.BG_SECUNDARIO, fg=TemaEscuro.TEXT_PRIMARY,
            insertbackground=TemaEscuro.ACCENT_PRIMARY,
            selectbackground=TemaEscuro.ACCENT_PRIMARY,
            selectforeground=TemaEscuro.BG_PRINCIPAL,
            relief='flat', borderwidth=0,
            padx=60, pady=30, spacing1=6, spacing3=10,
            cursor='hand2', state='disabled')
        self.text_paragrafo.grid(row=0, column=0, sticky='nsew')
        self.text_paragrafo.bind('<Button-1>', self.on_texto_clicado)

        scrollbar = ttk.Scrollbar(text_container, command=self.text_paragrafo.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.text_paragrafo.config(yscrollcommand=scrollbar.set)

    # ===== Barra de player flutuante =====
    def criar_barra_player(self):
        """Barra minimalista flutuante com navegação, play e velocidade."""
        bar = tk.Frame(self.root, bg=TemaEscuro.BG_CARD,
                       highlightbackground=TemaEscuro.BORDER, highlightthickness=1)
        self.barra_player = bar
        pad = {'padx': 3, 'pady': 6}

        def separador():
            tk.Frame(bar, bg=TemaEscuro.BORDER, width=1).pack(side='left', fill='y', padx=6, pady=8)

        self.btn_cap_anterior = ttk.Button(bar, text="⏮", width=3, command=self.capitulo_anterior)
        self.btn_cap_anterior.pack(side='left', **pad)
        self.criar_tooltip(self.btn_cap_anterior, "Capítulo anterior (Shift+←)")

        self.spin_capitulo = ttk.Spinbox(bar, from_=1, to=2266, width=6,
                                         command=self.on_capitulo_mudado)
        self.spin_capitulo.set('961')
        self.spin_capitulo.pack(side='left', **pad)
        self.spin_capitulo.bind('<Return>', lambda e: self.on_capitulo_mudado())
        self.spin_capitulo.bind('<FocusOut>', lambda e: self.on_capitulo_mudado())

        self.btn_cap_proximo = ttk.Button(bar, text="⏭", width=3, command=self.capitulo_proximo)
        self.btn_cap_proximo.pack(side='left', **pad)
        self.criar_tooltip(self.btn_cap_proximo, "Próximo capítulo (Shift+→)")

        separador()

        self.btn_par_anterior = ttk.Button(bar, text="◄", width=3, command=self.paragrafo_anterior)
        self.btn_par_anterior.pack(side='left', **pad)

        self.btn_play_pause = ttk.Button(bar, text="▶️", width=4, style='Accent.TButton',
                                         command=self.toggle_narracao)
        self.btn_play_pause.pack(side='left', **pad)
        self.criar_tooltip(self.btn_play_pause, "Reproduzir / Pausar (Espaço)")

        self.btn_par_proximo = ttk.Button(bar, text="►", width=3, command=self.paragrafo_proximo)
        self.btn_par_proximo.pack(side='left', **pad)

        self.btn_stop = ttk.Button(bar, text="⏹", width=3, style='Danger.TButton',
                                   command=self.parar_narracao_completa)
        self.btn_stop.pack(side='left', **pad)

        # Spinbox de parágrafo (compacto)
        self.spin_paragrafo = ttk.Spinbox(bar, from_=1, to=999, width=5,
                                          command=self.on_paragrafo_mudado)
        self.spin_paragrafo.set('1')
        self.spin_paragrafo.pack(side='left', **pad)
        self.spin_paragrafo.bind('<Return>', lambda e: self.on_paragrafo_mudado())
        self.spin_paragrafo.bind('<FocusOut>', lambda e: self.on_paragrafo_mudado())

        separador()

        # Chips de velocidade
        self.botoes_velocidade = {}
        for texto, val in [("0.5×", 0.5), ("1×", 1.0), ("1.5×", 1.5),
                           ("2×", 2.0), ("2.5×", 2.5), ("3×", 3.0)]:
            b = ttk.Button(bar, text=texto, width=4,
                           command=lambda v=val: self.definir_velocidade_fixa(v))
            b.pack(side='left', padx=1, pady=6)
            self.botoes_velocidade[val] = b

        separador()

        # Progresso do capítulo
        self.progress_capitulo = ttk.Progressbar(bar, length=120, mode='determinate')
        self.progress_capitulo.pack(side='left', padx=(4, 2), pady=6)
        self.lbl_progress = tk.Label(bar, text="0%", width=4, bg=TemaEscuro.BG_CARD,
                                     fg=TemaEscuro.ACCENT_PRIMARY, font=('Segoe UI', 9, 'bold'))
        self.lbl_progress.pack(side='left', padx=(0, 4))

        separador()

        btn_imersivo = ttk.Button(bar, text="⛶", width=3, command=self.toggle_imersivo)
        btn_imersivo.pack(side='left', **pad)
        self.criar_tooltip(btn_imersivo, "Modo imersivo total (F)")
        ttk.Button(bar, text="⚙️", width=3, command=self.toggle_drawer).pack(side='left', **pad)

        bar.bind('<Enter>', lambda e: self._cancelar_esconder())
        bar.bind('<Leave>', lambda e: self._agendar_esconder_barra())

        self._barra_visivel = True
        self._posicionar_barra()

    # ===== Drawer lateral de ajustes rápidos =====
    def criar_drawer(self):
        """Painel lateral deslizante com voz, velocidade, volumes, música e aparência."""
        self.drawer = tk.Frame(self.root, bg=TemaEscuro.BG_CARD,
                               highlightbackground=TemaEscuro.BORDER, highlightthickness=1)
        cont = ttk.Frame(self.drawer, padding=16)
        cont.pack(fill='both', expand=True)

        def secao(txt):
            ttk.Label(cont, text=txt, font=('Segoe UI', 10, 'bold'),
                      foreground=TemaEscuro.ACCENT_PRIMARY).pack(anchor='w', pady=(12, 4))

        top = ttk.Frame(cont)
        top.pack(fill='x')
        ttk.Label(top, text="⚙️ Ajustes rápidos", font=('Segoe UI', 12, 'bold'),
                  foreground=TemaEscuro.ACCENT_SECONDARY).pack(side='left')
        ttk.Button(top, text="✕", width=3, command=self._fechar_drawer).pack(side='right')

        # Voz
        secao("🎙️ Voz")
        self.combo_voz = ttk.Combobox(cont, values=list(EngineNarracaoSimples.VOZES.keys()),
                                      state='readonly')
        self.combo_voz.set('Francisca')
        self.combo_voz.pack(fill='x')
        self.combo_voz.bind('<<ComboboxSelected>>', self.on_voz_alterada)

        # Velocidade
        secao("⚡ Velocidade (0.5×–3×)")
        velf = ttk.Frame(cont)
        velf.pack(fill='x')
        self.velocidade_narracao = ttk.Scale(velf, from_=0.5, to=3.0, orient='horizontal',
                                             command=self.ajustar_velocidade_narracao)
        self.velocidade_narracao.set(1.0)
        self.velocidade_narracao.pack(side='left', fill='x', expand=True)
        self.lbl_velocidade = ttk.Label(velf, text="1.00×", width=6,
                                        foreground=TemaEscuro.ACCENT_WARNING,
                                        font=('Segoe UI', 9, 'bold'))
        self.lbl_velocidade.pack(side='left', padx=(6, 0))

        # Volume da narração
        secao("🔊 Volume da narração")
        vnf = ttk.Frame(cont)
        vnf.pack(fill='x')
        self.lbl_icone_vol_nar = ttk.Label(vnf, text="🔊", font=('Segoe UI', 12))
        self.lbl_icone_vol_nar.pack(side='left', padx=(0, 4))
        self.volume_narracao = ttk.Scale(vnf, from_=0, to=100, orient='horizontal',
                                         command=self.ajustar_volume_narracao)
        self.volume_narracao.set(100)
        self.volume_narracao.pack(side='left', fill='x', expand=True)
        self.lbl_vol_narracao = ttk.Label(vnf, text="100%", width=5,
                                          foreground=TemaEscuro.ACCENT_PRIMARY,
                                          font=('Segoe UI', 9, 'bold'))
        self.lbl_vol_narracao.pack(side='left', padx=(6, 0))

        # Música de fundo
        secao("🎼 Música de fundo")
        vmf = ttk.Frame(cont)
        vmf.pack(fill='x')
        self.lbl_icone_vol_mus = ttk.Label(vmf, text="🔊", font=('Segoe UI', 12))
        self.lbl_icone_vol_mus.pack(side='left', padx=(0, 4))
        self.volume_musica = ttk.Scale(vmf, from_=0, to=100, orient='horizontal',
                                       command=self.ajustar_volume_musica)
        self.volume_musica.set(30)
        self.volume_musica.pack(side='left', fill='x', expand=True)
        self.lbl_vol_musica = ttk.Label(vmf, text="30%", width=5,
                                        foreground=TemaEscuro.ACCENT_SECONDARY,
                                        font=('Segoe UI', 9, 'bold'))
        self.lbl_vol_musica.pack(side='left', padx=(6, 0))

        bgmf = ttk.Frame(cont)
        bgmf.pack(fill='x', pady=(6, 0))
        ttk.Button(bgmf, text="🎵", width=3, style='Accent.TButton',
                   command=self.musica_normal).pack(side='left', padx=(0, 4))
        self.combo_bgm = ttk.Combobox(bgmf, values=[], state='readonly', style='BGM.TCombobox')
        self.combo_bgm.pack(side='left', fill='x', expand=True)
        self.combo_bgm.bind('<<ComboboxSelected>>', self.on_bgm_selecionada)
        self.btn_mutar = ttk.Button(bgmf, text="🔇", width=3, command=self.toggle_mutar)
        self.btn_mutar.pack(side='left', padx=(4, 0))

        # Aparência
        secao("🎨 Aparência")
        palf = ttk.Frame(cont)
        palf.pack(fill='x')
        for nome, key in [("Padrão", "padrao"), ("Sépia", "sepia"),
                          ("Noite", "noite"), ("Papel", "papel")]:
            ttk.Button(palf, text=nome, width=7,
                       command=lambda k=key: self._aplicar_paleta(k)).pack(side='left', padx=2)
        fontf = ttk.Frame(cont)
        fontf.pack(fill='x', pady=(6, 0))
        ttk.Label(fontf, text="Fonte", font=('Segoe UI', 9)).pack(side='left', padx=(0, 6))
        self.slider_fonte = ttk.Scale(fontf, from_=10, to=26, orient='horizontal',
                                      command=self._ajustar_fonte)
        self.slider_fonte.set(self.config_texto.get('tamanho_fonte', 13))
        self.slider_fonte.pack(side='left', fill='x', expand=True)

        # Leitura
        secao("📖 Leitura")
        self.btn_modo_leitura = ttk.Button(cont, text="Ver só o parágrafo atual",
                                           command=self.toggle_modo_leitura)
        self.btn_modo_leitura.pack(fill='x')

        # Tempo
        secao("⏱️ Tempo")
        self.lbl_tempo_narracao = ttk.Label(cont, text="⏱️ Tempo de narração: 00:00:00",
                                            font=('Segoe UI', 9),
                                            foreground=TemaEscuro.TEXT_SECONDARY)
        self.lbl_tempo_narracao.pack(anchor='w')
        self.lbl_tempo_estimado = ttk.Label(cont, text="⏳ Tempo estimado: --:--",
                                            font=('Segoe UI', 9),
                                            foreground=TemaEscuro.TEXT_SECONDARY)
        self.lbl_tempo_estimado.pack(anchor='w')

        ttk.Separator(cont, orient='horizontal').pack(fill='x', pady=10)
        ttk.Button(cont, text="Mais configurações…",
                   command=self.abrir_configuracoes).pack(fill='x')
        ttk.Button(cont, text="💾 Salvar e sair", style='Success.TButton',
                   command=self.sair).pack(fill='x', pady=(6, 0))

    # ===== Posicionamento / auto-hide dos overlays =====
    def _posicionar_barra(self):
        if hasattr(self, 'barra_player'):
            self.barra_player.place(relx=0.5, rely=1.0, y=-14, anchor='s')
            self.barra_player.lift()

    def _mostrar_barra(self):
        self._barra_visivel = True
        self._posicionar_barra()

    def _esconder_barra(self):
        self._barra_timer = None
        # Nunca esconder com o drawer aberto
        if getattr(self, 'drawer_aberto', False):
            return
        if hasattr(self, 'barra_player'):
            self.barra_player.place_forget()
        self._barra_visivel = False

    def _cancelar_esconder(self):
        if getattr(self, '_barra_timer', None):
            self.root.after_cancel(self._barra_timer)
            self._barra_timer = None

    def _agendar_esconder_barra(self):
        self._cancelar_esconder()
        self._barra_timer = self.root.after(2800, self._esconder_barra)

    def _on_mouse_activity(self, event=None):
        if not getattr(self, '_barra_visivel', False):
            self._mostrar_barra()
        self._agendar_esconder_barra()

    def toggle_drawer(self):
        if getattr(self, 'drawer_aberto', False):
            self._fechar_drawer()
        else:
            self.drawer.place(relx=1.0, rely=0, anchor='ne', relheight=1.0, width=340)
            self.drawer.lift()
            self.drawer_aberto = True
            self._mostrar_barra()
            self._cancelar_esconder()

    def _fechar_drawer(self):
        self.drawer.place_forget()
        self.drawer_aberto = False
        self._agendar_esconder_barra()

    def toggle_imersivo(self):
        self.imersivo_total = not self.imersivo_total
        if self.imersivo_total:
            self.header_frame.grid_remove()
        else:
            self.header_frame.grid()
        self._posicionar_barra()

    # ===== Atalhos de teclado =====
    def _foco_em_campo(self):
        w = self.root.focus_get()
        return isinstance(w, (tk.Entry, ttk.Entry, ttk.Spinbox, ttk.Combobox, tk.Spinbox))

    def _registrar_atalhos(self):
        r = self.root
        r.bind('<space>', self._atalho_play)
        r.bind('<Left>', lambda e: None if self._foco_em_campo() else self.paragrafo_anterior())
        r.bind('<Right>', lambda e: None if self._foco_em_campo() else self.paragrafo_proximo())
        r.bind('<Shift-Left>', lambda e: self.capitulo_anterior())
        r.bind('<Shift-Right>', lambda e: self.capitulo_proximo())
        r.bind('<Up>', lambda e: self._passo_velocidade(0.25))
        r.bind('<Down>', lambda e: self._passo_velocidade(-0.25))
        for k in ('<r>', '<R>'):
            r.bind(k, lambda e: self.reiniciar_capitulo())
        for k in ('<c>', '<C>'):
            r.bind(k, lambda e: None if self._foco_em_campo() else self.toggle_drawer())
        for k in ('<f>', '<F>'):
            r.bind(k, lambda e: None if self._foco_em_campo() else self.toggle_imersivo())
        r.bind('<Escape>', self._atalho_escape)
        r.bind('<Home>', lambda e: self.reiniciar_capitulo())

    def _atalho_play(self, event=None):
        if self._foco_em_campo():
            return
        self.toggle_narracao()
        return 'break'

    def _atalho_escape(self, event=None):
        if getattr(self, 'drawer_aberto', False):
            self._fechar_drawer()
        elif self.imersivo_total:
            self.toggle_imersivo()

    def _passo_velocidade(self, delta):
        novo = max(0.5, min(3.0, round((self.velocidade_mult + delta) * 100) / 100))
        self.definir_velocidade_fixa(novo)

    # ===== Aparência via drawer =====
    def _aplicar_paleta(self, key):
        self.config_texto['paleta'] = key
        self.salvar_config_texto()
        self.aplicar_estilo_texto()
        if self.modo_leitura and self.conteudo_capitulo:
            self.atualizar_display_modo_leitura()

    def _ajustar_fonte(self, valor):
        try:
            tam = int(float(valor))
            self.config_texto['tamanho_fonte'] = tam
            self.aplicar_estilo_texto()
        except (ValueError, TypeError):
            pass

    def ajustar_layout_responsivo(self):
        """Ajusta layout baseado no tamanho da janela."""
        if self.modo_compacto:
            # Modo compacto: labels menores, ícones simplificados
            if hasattr(self, 'lbl_icone_vol_nar'):
                self.lbl_icone_vol_nar.config(font=('Segoe UI', 10))
            if hasattr(self, 'lbl_icone_vol_mus'):
                self.lbl_icone_vol_mus.config(font=('Segoe UI', 10))
        else:
            # Modo normal: ícones maiores
            if hasattr(self, 'lbl_icone_vol_nar'):
                self.lbl_icone_vol_nar.config(font=('Segoe UI', 12))
            if hasattr(self, 'lbl_icone_vol_mus'):
                self.lbl_icone_vol_mus.config(font=('Segoe UI', 12))
    
    def criar_tooltip(self, widget, texto):
        """Cria tooltip para um widget."""
        def mostrar_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=texto,
                           background=TemaEscuro.BG_TERCIARIO,
                           foreground=TemaEscuro.TEXT_PRIMARY,
                           relief='solid',
                           borderwidth=1,
                           font=('Segoe UI', 9),
                           padx=8, pady=4)
            label.pack()
            widget.tooltip = tooltip
        
        def esconder_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind('<Enter>', mostrar_tooltip)
        widget.bind('<Leave>', esconder_tooltip)
    
    def on_resize(self, event):
        """Callback para redimensionamento da janela."""
        if event.widget == self.root:
            largura = event.width
            altura = event.height
            
            # Detectar tela cheia (ou quase cheia)
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            is_fullscreen = (largura >= screen_width - 10 and altura >= screen_height - 50)
            
            # Ativar modo leitura automaticamente em tela cheia
            if is_fullscreen and not self.modo_leitura:
                self.toggle_modo_leitura()
            
            # Modo compacto para janelas menores que 1100px
            novo_modo = largura < 1100
            
            if novo_modo != self.modo_compacto:
                self.modo_compacto = novo_modo
                self.ajustar_layout_responsivo()
    
    def on_focus(self, event):
        """Callback quando janela ganha foco."""
        self.tem_foco = True
    
    def on_unfocus(self, event):
        """Callback quando janela perde foco."""
        self.tem_foco = False
    
    def on_capitulo_mudado(self):
        """Callback quando capítulo é mudado manualmente."""
        try:
            novo_cap = int(self.spin_capitulo.get())
            if novo_cap != self.capitulo_atual:
                self.parar_narracao_completa()
                if self.carregar_capitulo(novo_cap):
                    self.paragrafo_atual = 1
                    self.spin_paragrafo.set('1')
                    if self.modo_leitura:
                        self.atualizar_display_modo_leitura()
                    elif self.conteudo_capitulo:
                        self.atualizar_display(self.conteudo_capitulo[0])
                    self.atualizar_status()
        except ValueError:
            pass
    
    def on_paragrafo_mudado(self):
        """Callback quando parágrafo é mudado manualmente."""
        try:
            novo_par = int(self.spin_paragrafo.get())
            if novo_par != self.paragrafo_atual and self.conteudo_capitulo:
                if 1 <= novo_par <= len(self.conteudo_capitulo):
                    self.parar_narracao_completa()
                    self.paragrafo_atual = novo_par
                    self.atualizar_display(self.conteudo_capitulo[self.paragrafo_atual - 1])
                    self.atualizar_status()
        except ValueError:
            pass
    
    def on_voz_alterada(self, event=None):
        """Callback quando a voz é alterada."""
        if hasattr(self, 'engine') and self.engine:
            nova_voz = self.combo_voz.get()
            self.engine.trocar_voz(nova_voz)
            print(f"🎙️ Voz alterada para: {nova_voz}")
    
    def carregar_capitulos(self):
        """Carrega lista de capítulos disponíveis."""
        self.capitulos_disponiveis = self.leitor.listar_capitulos_disponiveis()
        if self.capitulos_disponiveis:
            self.spin_capitulo.config(from_=min(self.capitulos_disponiveis),
                                     to=max(self.capitulos_disponiveis))
    
    def _cor_highlight(self):
        """Cor de destaque do parágrafo atual conforme a paleta."""
        return {
            'padrao': '#3d3d52',
            'sepia': '#e6d3a3',
            'noite': '#1f3350',
            'papel': '#dfe7c8',
        }.get(self.config_texto.get('paleta', 'padrao'), '#3d3d52')

    def atualizar_display(self, texto):
        """Atualiza o texto do parágrafo atual."""
        if self.modo_leitura:
            # Re-renderiza se o capítulo mudou; senão só move o highlight (barato)
            self.atualizar_display_modo_leitura()
        else:
            # Modo normal: mostrar apenas o parágrafo atual
            self.text_paragrafo.config(state='normal')
            self.text_paragrafo.delete('1.0', 'end')
            self.text_paragrafo.insert('1.0', texto)
            self.text_paragrafo.config(state='disabled')
            self.aplicar_estilo_texto()

    def atualizar_display_modo_leitura(self, force=False):
        """Renderiza o capítulo inteiro (só reconstrói quando o capítulo muda)."""
        if not self.conteudo_capitulo:
            return

        # Se o capítulo já está renderizado, apenas mover o highlight (barato)
        if not force and getattr(self, '_cap_renderizado', None) == self.capitulo_atual:
            self._mover_highlight(self.paragrafo_atual)
            return

        self.text_paragrafo.config(state='normal')
        self.text_paragrafo.delete('1.0', tk.END)
        self._par_starts = {}

        for i, paragrafo in enumerate(self.conteudo_capitulo, 1):
            self.text_paragrafo.insert(tk.END, f"[{i}] ", 'paragrafo_num')
            inicio = self.text_paragrafo.index(tk.END + '-1c')
            self.text_paragrafo.insert(tk.END, paragrafo + "\n\n")
            fim = self.text_paragrafo.index(tk.END + '-1c')
            self.text_paragrafo.tag_add(f'paragrafo_{i}', inicio, fim)
            self._par_starts[i] = inicio

        self.text_paragrafo.tag_config('paragrafo_num',
                                       foreground=TemaEscuro.ACCENT_SECONDARY,
                                       font=('Segoe UI', 9, 'bold'))
        self.text_paragrafo.config(state='disabled')
        self._cap_renderizado = self.capitulo_atual
        self.aplicar_estilo_texto()
        self._mover_highlight(self.paragrafo_atual)

    def _mover_highlight(self, novo_par):
        """Move o destaque para o parágrafo dado sem reconstruir o texto."""
        if not getattr(self, '_par_starts', None):
            return
        cor = self._cor_highlight()
        for tag in self.text_paragrafo.tag_names():
            if tag.startswith('paragrafo_') and tag != 'paragrafo_num':
                self.text_paragrafo.tag_config(tag, background='')
        tag_atual = f'paragrafo_{novo_par}'
        if novo_par in self._par_starts:
            self.text_paragrafo.tag_config(tag_atual, background=cor)
            self.text_paragrafo.see(self._par_starts[novo_par])
    
    def atualizar_status(self):
        """Atualiza labels de status."""
        total = len(self.conteudo_capitulo) if self.conteudo_capitulo else 0
        self.lbl_posicao.config(
            text=f"📑 Capítulo: {self.capitulo_atual} | 📄 Parágrafo: {self.paragrafo_atual}/{total}"
        )
        
        # Atualizar info de capítulo carregado
        if self.conteudo_capitulo:
            self.lbl_cap_info.config(text=f"✓ Capítulo {self.capitulo_atual} carregado ({total} parágrafos)")
        
        # Atualizar progresso total
        progresso_pct = (self.capitulo_atual / 2266) * 100
        self.lbl_progresso_total.config(text=f"📚 Progresso total: Capítulo {self.capitulo_atual}/2266 ({progresso_pct:.1f}%)")
        
        # Atualizar barra de progresso do capítulo
        if total > 0:
            progresso_cap = (self.paragrafo_atual / total) * 100
            self.progress_capitulo['value'] = progresso_cap
            self.lbl_progress.config(text=f"{progresso_cap:.0f}%")
        
        # Atualizar tempo estimado (considerando a velocidade atual)
        if self.narrando and total > 0:
            palavras_por_min = 150 * max(0.5, self.velocidade_mult)
            texto_restante = ' '.join(self.conteudo_capitulo[self.paragrafo_atual-1:])
            palavras_restantes = len(texto_restante.split())
            minutos_estimados = palavras_restantes / palavras_por_min
            horas = int(minutos_estimados // 60)
            mins = int(minutos_estimados % 60)
            self.lbl_tempo_estimado.config(text=f"⏳ Tempo estimado: {horas:02d}:{mins:02d}")
        
        if self.narrando:
            if self.pausado:
                self.status_badge.config(text="⏸️ PAUSADO",
                                        bg=TemaEscuro.ACCENT_WARNING,
                                        fg=TemaEscuro.BG_PRINCIPAL)
            else:
                self.status_badge.config(text="▶️ NARRANDO",
                                        bg=TemaEscuro.ACCENT_SUCCESS,
                                        fg=TemaEscuro.BG_PRINCIPAL)
        else:
            self.status_badge.config(text="⏹️ PARADO",
                                    bg=TemaEscuro.BG_TERCIARIO,
                                    fg=TemaEscuro.TEXT_SECONDARY)
    
    JANELA_PREFETCH = 4  # quantos parágrafos à frente manter em buffer

    def _conteudo_de(self, numero):
        """Retorna o conteúdo de um capítulo, usando o cache de prefetch."""
        if numero in self._cache_prox_capitulo:
            return self._cache_prox_capitulo[numero]
        cap = self.leitor.carregar_capitulo(numero)
        conteudo = cap['conteudo'] if cap else None
        if conteudo is not None:
            self._cache_prox_capitulo[numero] = conteudo
            # manter o cache pequeno
            if len(self._cache_prox_capitulo) > 3:
                for k in list(self._cache_prox_capitulo)[:-3]:
                    self._cache_prox_capitulo.pop(k, None)
        return conteudo

    def _prefetch_janela(self):
        """Pré-carrega uma janela de parágrafos à frente (e o início do próximo
        capítulo quando o fim se aproxima), sem limpar o cache."""
        if not self.engine or not self.conteudo_capitulo:
            return
        total = len(self.conteudo_capitulo)
        janela = []
        # próximos N parágrafos do capítulo atual (paragrafo_atual é 1-based)
        for idx in range(self.paragrafo_atual - 1, min(total, self.paragrafo_atual - 1 + self.JANELA_PREFETCH)):
            if 0 <= idx < total:
                janela.append(self.conteudo_capitulo[idx])

        # se restam poucos parágrafos, buscar o próximo capítulo em background
        restantes = total - self.paragrafo_atual
        if restantes <= 2:
            prox = self.capitulo_atual + 1
            if self.capitulos_disponiveis and prox <= max(self.capitulos_disponiveis):
                threading.Thread(target=self._prefetch_capitulo, args=(prox,), daemon=True).start()
                conteudo_prox = self._cache_prox_capitulo.get(prox)
                if conteudo_prox:
                    janela.extend(conteudo_prox[:2])

        self.engine.solicitar_precarregamento_lote(janela)

    def _prefetch_capitulo(self, numero):
        """Carrega o conteúdo de um capítulo em background (sem trocar o atual)."""
        try:
            self._conteudo_de(numero)
        except Exception as e:
            print(f"⚠️ Falha ao pré-carregar capítulo {numero}: {e}")

    def carregar_capitulo(self, numero):
        """Carrega um capítulo (reaproveitando o prefetch quando disponível)."""
        conteudo = self._conteudo_de(numero)
        if conteudo is not None:
            mudou = (numero != getattr(self, 'capitulo_atual', None))
            self.conteudo_capitulo = conteudo
            self.capitulo_atual = numero
            if mudou:
                self._cap_renderizado = None  # forçar re-render no modo leitura
            self.spin_capitulo.set(str(numero))
            self.spin_paragrafo.config(to=len(self.conteudo_capitulo))
            return True
        return False
    
    def toggle_narracao(self):
        """Inicia ou pausa narração."""
        if not self.narrando:
            # Iniciar narração
            cap = int(self.spin_capitulo.get())
            par = int(self.spin_paragrafo.get())
            
            if self.carregar_capitulo(cap):
                self.paragrafo_atual = par
                self.narrando = True
                self.pausado = False
                self.tempo_inicio_narracao = time.time()
                self.btn_play_pause.config(text="⏸️")

                # Iniciar thread de narração
                self.thread_narracao = threading.Thread(target=self.loop_narracao, daemon=True)
                self.thread_narracao.start()

                # Iniciar thread de atualização de tempo
                threading.Thread(target=self.atualizar_tempo, daemon=True).start()
            else:
                messagebox.showerror("Erro", f"Capítulo {cap} não encontrado")
        else:
            # Pausar/despausar
            self.pausado = not self.pausado
            if self.pausado:
                self.btn_play_pause.config(text="▶️")
            else:
                self.btn_play_pause.config(text="⏸️")
            self.atualizar_status()
    
    def atualizar_tempo(self):
        """Atualiza contador de tempo de narração."""
        while self.narrando:
            if not self.pausado and self.tempo_inicio_narracao:
                tempo_decorrido = time.time() - self.tempo_inicio_narracao + self.tempo_total_narracao
                horas = int(tempo_decorrido // 3600)
                minutos = int((tempo_decorrido % 3600) // 60)
                segundos = int(tempo_decorrido % 60)
                self.root.after(0, lambda: self.lbl_tempo_narracao.config(
                    text=f"⏱️ Tempo de narração: {horas:02d}:{minutos:02d}:{segundos:02d}"
                ))
            time.sleep(1)
    
    def loop_narracao(self):
        """Loop principal de narração com highlight progressivo."""
        voz = self.combo_voz.get()
        
        # Se já existe engine, trocar voz e limpar cache
        if self.engine:
            self.engine.trocar_voz(voz)
        else:
            self.engine = EngineNarracaoSimples(voz, self.musica.canal_narrador)
        
        self.engine.set_volume(self.volume_narracao.get() / 100)
        self.engine.set_velocidade(self.velocidade_mult)

        # Pré-carregar a janela inicial de parágrafos
        print("🔄 Pré-carregando buffer inicial...")
        self._prefetch_janela()
        time.sleep(0.4)  # dar um head start ao buffer
        print("✓ Pronto para narrar")

        while self.narrando:
            # Sinal de "pular para parágrafo" vindo do clique no texto
            if self.pular_para is not None:
                alvo = self.pular_para
                self.pular_para = None
                if 1 <= alvo <= len(self.conteudo_capitulo):
                    self.paragrafo_atual = alvo

            # Verificar se terminou o capítulo
            if self.paragrafo_atual > len(self.conteudo_capitulo):
                proximo_cap = self.capitulo_atual + 1
                if self.capitulos_disponiveis and proximo_cap <= max(self.capitulos_disponiveis):
                    print(f"📖 Capítulo {self.capitulo_atual} concluído! Indo para {proximo_cap}...")
                    if self.carregar_capitulo(proximo_cap):
                        self.paragrafo_atual = 1
                        self.root.after(0, lambda: self.spin_capitulo.set(str(self.capitulo_atual)))
                        self.root.after(0, lambda: self.spin_paragrafo.set(str(self.paragrafo_atual)))
                        self.root.after(0, self.atualizar_display_modo_leitura)
                        continue
                    else:
                        print("❌ Erro ao carregar próximo capítulo")
                        break
                else:
                    print("✅ Última página da novel! Narração concluída.")
                    break

            if not self.narrando:
                break

            paragrafo = self.conteudo_capitulo[self.paragrafo_atual - 1]

            # Atualizar UI
            self.root.after(0, self.atualizar_display, paragrafo)
            self.root.after(0, self.atualizar_status)

            # Manter o buffer cheio à frente
            self._prefetch_janela()

            # Narrar com callback para verificar pausa (instantâneo com cache)
            self.engine.narrar(paragrafo, callback_pausado=lambda: self.pausado)

            # Avançar (só se não pausou nem pediu para pular)
            if not self.pausado and self.narrando and self.pular_para is None:
                self.paragrafo_atual += 1
                self.root.after(0, lambda p=self.paragrafo_atual: self.spin_paragrafo.set(str(p)))

        # Atualizar UI ao finalizar
        self.narrando = False
        self.pausado = False
        self.root.after(0, lambda: self.btn_play_pause.config(text="▶️"))
        self.root.after(0, self.atualizar_status)
    
    def parar_narracao_completa(self):
        """Para a narração completamente."""
        if self.narrando or self.pausado:
            if self.tempo_inicio_narracao:
                self.tempo_total_narracao += time.time() - self.tempo_inicio_narracao
                self.tempo_inicio_narracao = None
            self.narrando = False
            self.pausado = False
            if self.engine:
                self.engine.parar()
            self.btn_play_pause.config(text="▶️")
            self.atualizar_status()
    
    def reiniciar_capitulo(self):
        """Reinicia o capítulo atual do início."""
        self.parar_narracao_completa()
        self.paragrafo_atual = 1
        self.spin_paragrafo.set('1')
        if self.conteudo_capitulo:
            self.atualizar_display(self.conteudo_capitulo[0])
        self.atualizar_status()
    
    def capitulo_anterior(self):
        """Vai para capítulo anterior."""
        self.parar_narracao_completa()
        if self.capitulo_atual > 1:
            self.carregar_capitulo(self.capitulo_atual - 1)
            self.paragrafo_atual = 1
            self.spin_paragrafo.set('1')
            if self.conteudo_capitulo:
                self.atualizar_display(self.conteudo_capitulo[0])
            self.atualizar_status()
    
    def capitulo_proximo(self):
        """Vai para próximo capítulo."""
        self.parar_narracao_completa()
        if self.capitulo_atual < 2266:
            self.carregar_capitulo(self.capitulo_atual + 1)
            self.paragrafo_atual = 1
            self.spin_paragrafo.set('1')
            if self.conteudo_capitulo:
                self.atualizar_display(self.conteudo_capitulo[0])
            self.atualizar_status()
    
    def paragrafo_anterior(self):
        """Vai para parágrafo anterior."""
        if self.paragrafo_atual > 1:
            self.paragrafo_atual -= 1
            self.spin_paragrafo.set(str(self.paragrafo_atual))
            if self.conteudo_capitulo:
                self.atualizar_display(self.conteudo_capitulo[self.paragrafo_atual - 1])
            self.atualizar_status()
    
    def paragrafo_proximo(self):
        """Vai para próximo parágrafo."""
        if self.conteudo_capitulo and self.paragrafo_atual < len(self.conteudo_capitulo):
            self.paragrafo_atual += 1
            self.spin_paragrafo.set(str(self.paragrafo_atual))
            self.atualizar_display(self.conteudo_capitulo[self.paragrafo_atual - 1])
            self.atualizar_status()
    
    def ajustar_volume_narracao(self, valor):
        """Ajusta volume da narração."""
        try:
            vol = float(valor) / 100
            vol_int = int(float(valor))
            if hasattr(self, 'lbl_vol_narracao'):
                self.lbl_vol_narracao.config(text=f"{vol_int}%")
            if hasattr(self, 'lbl_icone_vol_nar'):
                if vol_int == 0:
                    self.lbl_icone_vol_nar.config(text="🔇")
                elif vol_int <= 50:
                    self.lbl_icone_vol_nar.config(text="🔉")
                else:
                    self.lbl_icone_vol_nar.config(text="🔊")
            if self.engine:
                self.engine.set_volume(vol)
        except Exception as e:
            print(f"Erro ao ajustar volume narração: {e}")
    
    def ajustar_volume_musica(self, valor):
        """Ajusta volume da música."""
        try:
            vol = float(valor) / 100
            vol_int = int(float(valor))
            if hasattr(self, 'lbl_vol_musica'):
                self.lbl_vol_musica.config(text=f"{vol_int}%")
            if hasattr(self, 'lbl_icone_vol_mus'):
                if vol_int == 0:
                    self.lbl_icone_vol_mus.config(text="🔇")
                elif vol_int <= 50:
                    self.lbl_icone_vol_mus.config(text="🔉")
                else:
                    self.lbl_icone_vol_mus.config(text="🔊")
            self.musica.set_volume(vol)
        except Exception as e:
            print(f"Erro ao ajustar volume música: {e}")
    
    def ajustar_velocidade_narracao(self, valor):
        """Ajusta a velocidade (multiplicador direto de 0.5× a 3.0×)."""
        try:
            mult = max(0.5, min(3.0, float(valor)))
            self.velocidade_mult = mult
            if hasattr(self, 'lbl_velocidade'):
                self.lbl_velocidade.config(text=f"{mult:.2f}×")
            self._destacar_chip_velocidade(mult)
            if self.engine:
                self.engine.set_velocidade(mult)
        except Exception as e:
            print(f"Erro ao ajustar velocidade narração: {e}")

    def definir_velocidade_fixa(self, valor):
        """Define uma velocidade fixa a partir dos chips."""
        try:
            self.velocidade_narracao.set(valor)  # dispara ajustar_velocidade_narracao
            self.ajustar_velocidade_narracao(valor)
        except Exception as e:
            print(f"Erro ao definir velocidade fixa: {e}")

    def _destacar_chip_velocidade(self, mult):
        """Realça o chip de velocidade correspondente ao valor atual."""
        botoes = getattr(self, 'botoes_velocidade', None)
        if not botoes:
            return
        for val, btn in botoes.items():
            btn.configure(style='Accent.TButton' if abs(val - mult) < 0.01 else 'TButton')
    
    def musica_normal(self):
        """Ativa música de fundo."""
        self.musica.tocar_normal()
    
    def toggle_mutar(self):
        """Muta/desmuta música."""
        self.musica.mutar(not self.musica.mutado)
        if self.musica.mutado:
            self.btn_mutar.config(text="🔊 Desmutar")
        else:
            self.btn_mutar.config(text="🔇 Mutar")
    
    def carregar_progresso(self):
        """Carrega progresso salvo."""
        try:
            if os.path.exists(self.arquivo_progresso):
                with open(self.arquivo_progresso, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    cap = dados.get('capitulo', 961)
                    par = dados.get('paragrafo', 1)

                    # Carregar preferências
                    if 'voz' in dados:
                        self.combo_voz.set(dados['voz'])
                    if 'volume_narracao' in dados:
                        self.volume_narracao.set(dados['volume_narracao'])
                    if 'volume_musica' in dados:
                        self.volume_musica.set(dados['volume_musica'])
                    # Velocidade: aceitar apenas o novo formato (multiplicador 0.5–3.0)
                    vel = dados.get('velocidade')
                    if isinstance(vel, (int, float)) and 0.5 <= vel <= 3.0:
                        self.definir_velocidade_fixa(float(vel))

                    # Carregar o capítulo salvo para exibir de imediato
                    if self.carregar_capitulo(cap):
                        self.paragrafo_atual = min(max(1, par), len(self.conteudo_capitulo))
                    else:
                        self.capitulo_atual = cap
                        self.paragrafo_atual = par
                    self.spin_capitulo.set(str(self.capitulo_atual))
                    self.spin_paragrafo.set(str(self.paragrafo_atual))

                    print(f"✓ Progresso carregado: Cap {self.capitulo_atual}, Par {self.paragrafo_atual}")
        except Exception as e:
            print(f"Erro ao carregar progresso: {e}")
    
    def salvar_progresso(self):
        """Salva progresso atual."""
        try:
            os.makedirs(os.path.dirname(self.arquivo_progresso), exist_ok=True)
            dados = {
                'capitulo': self.capitulo_atual,
                'paragrafo': self.paragrafo_atual,
                'voz': self.combo_voz.get(),
                'volume_narracao': self.volume_narracao.get(),
                'volume_musica': self.volume_musica.get(),
                'velocidade': self.velocidade_narracao.get()
            }
            with open(self.arquivo_progresso, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print(f"💾 Progresso salvo: Cap {self.capitulo_atual}, Par {self.paragrafo_atual}")
            return True
        except Exception as e:
            print(f"Erro ao salvar progresso: {e}")
            return False
    
    def inicializar_comboboxes_bgm(self):
        """Inicializa o combobox com todas as músicas disponíveis."""
        try:
            musicas = self.musica.obter_lista_musicas()
            
            if musicas:
                self.combo_bgm['values'] = musicas
                if self.musica.musica_atual:
                    self.combo_bgm.set(self.musica.musica_atual)
                else:
                    self.combo_bgm.set(musicas[0])
        except Exception as e:
            print(f"Erro ao inicializar músicas: {e}")
    
    def on_bgm_selecionada(self, event=None):
        """Callback quando usuário seleciona uma música."""
        musica_selecionada = self.combo_bgm.get()
        if self.musica.selecionar_musica(musica_selecionada):
            # Se estiver tocando, atualizar música
            if self.musica.modo_atual:
                self.musica.tocar_normal()
    
    def abrir_configuracoes(self):
        """Abre a janela de configurações."""
        ConfiguracoesWindow(self.root, self)
    
    def recarregar_lista_musicas(self):
        """Recarrega a lista de músicas nos comboboxes."""
        try:
            # Recarregar músicas
            self.musica.carregar_musicas()
            
            # Atualizar combobox
            musicas = self.musica.obter_lista_musicas()
            if musicas:
                self.combo_bgm['values'] = musicas
                
                # Manter seleção atual se ainda existir
                if self.combo_bgm.get() not in musicas and musicas:
                    self.combo_bgm.set(musicas[0])
        except Exception as e:
            print(f"Erro ao recarregar músicas: {e}")
    
    def carregar_config_texto(self):
        """Carrega configurações de estilização de texto."""
        try:
            arquivo_config = os.path.join('config', 'config_texto.json')
            if os.path.exists(arquivo_config):
                with open(arquivo_config, 'r', encoding='utf-8') as f:
                    self.config_texto = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar config texto: {e}")
    
    def salvar_config_texto(self):
        """Salva configurações de estilização de texto."""
        try:
            os.makedirs('config', exist_ok=True)
            arquivo_config = os.path.join('config', 'config_texto.json')
            with open(arquivo_config, 'w', encoding='utf-8') as f:
                json.dump(self.config_texto, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar config texto: {e}")
    
    def aplicar_estilo_texto(self):
        """Aplica estilização ao widget de texto."""
        paletas = {
            'padrao': {
                'bg': TemaEscuro.BG_SECUNDARIO,
                'fg': TemaEscuro.TEXT_PRIMARY,
                'select_bg': TemaEscuro.ACCENT_PRIMARY
            },
            'sepia': {
                'bg': '#f4ecd8',
                'fg': '#5b4636',
                'select_bg': '#d4a574'
            },
            'noite': {
                'bg': '#0d1117',
                'fg': '#c9d1d9',
                'select_bg': '#58a6ff'
            },
            'papel': {
                'bg': '#fefcf3',
                'fg': '#2e2e2e',
                'select_bg': '#ffa94d'
            }
        }
        
        paleta = paletas.get(self.config_texto.get('paleta', 'padrao'), paletas['padrao'])
        tamanho = self.config_texto.get('tamanho_fonte', 11)
        
        self.text_paragrafo.config(
            bg=paleta['bg'],
            fg=paleta['fg'],
            selectbackground=paleta['select_bg'],
            font=('Segoe UI', tamanho)
        )
    
    def toggle_modo_leitura(self):
        """Alterna entre ler o capítulo inteiro e focar só no parágrafo atual."""
        self.modo_leitura = not self.modo_leitura

        if self.modo_leitura:
            self.btn_modo_leitura.config(text="Ver só o parágrafo atual")
            self._cap_renderizado = None
            self.atualizar_display_modo_leitura()
        else:
            self.btn_modo_leitura.config(text="Ver capítulo inteiro")
            if self.conteudo_capitulo and self.paragrafo_atual <= len(self.conteudo_capitulo):
                texto = self.conteudo_capitulo[self.paragrafo_atual - 1]
                self.text_paragrafo.config(state='normal')
                self.text_paragrafo.delete('1.0', 'end')
                self.text_paragrafo.insert('1.0', texto)
                self.text_paragrafo.config(state='disabled')
                self.aplicar_estilo_texto()

    def _paragrafo_do_clique(self, index):
        """Descobre o número do parágrafo a partir do índice clicado no texto."""
        tags = self.text_paragrafo.tag_names(index)
        # Clique no texto do parágrafo
        for tag in tags:
            if tag.startswith('paragrafo_') and tag != 'paragrafo_num':
                try:
                    return int(tag.split('_')[1])
                except (IndexError, ValueError):
                    pass
        # Clique no número "[N]"
        linha = int(index.split('.')[0])
        conteudo_linha = self.text_paragrafo.get(f"{linha}.0", f"{linha}.end")
        import re
        match = re.match(r'\s*\[(\d+)\]', conteudo_linha)
        if match:
            return int(match.group(1))
        return None

    def on_texto_clicado(self, event):
        """Clique no texto: pula para o parágrafo e narra a partir dali (sem jank)."""
        try:
            index = self.text_paragrafo.index(f"@{event.x},{event.y}")

            if self.modo_leitura:
                paragrafo_clicado = self._paragrafo_do_clique(index)
                if not paragrafo_clicado or not (1 <= paragrafo_clicado <= len(self.conteudo_capitulo)):
                    return

                self.spin_paragrafo.set(str(paragrafo_clicado))

                if self.narrando:
                    # Sinaliza o loop para saltar e corta o clipe atual (sem parar tudo)
                    self.pular_para = paragrafo_clicado
                    self._mover_highlight(paragrafo_clicado)
                    if self.engine:
                        self.engine.parar()
                else:
                    # Parado: começa a narrar a partir do parágrafo clicado
                    self.paragrafo_atual = paragrafo_clicado
                    self._mover_highlight(paragrafo_clicado)
                    self.toggle_narracao()
            else:
                # Modo parágrafo único: clique alterna play/pause
                self.toggle_narracao()
        except Exception as e:
            print(f"Erro ao clicar no texto: {e}")
    
    def on_fechar_janela(self):
        """Confirmação ao fechar a janela."""
        resposta = messagebox.askyesnocancel(
            "Fechar Novel Reader",
            "💾 Deseja salvar o progresso antes de sair?\n\n"
            f"📑 Capítulo atual: {self.capitulo_atual}\n"
            f"📄 Parágrafo atual: {self.paragrafo_atual}",
            icon='question'
        )
        
        if resposta is None:  # Cancelar
            return
        elif resposta:  # Sim (salvar)
            self.sair()
        else:  # Não (sair sem salvar)
            self.parar_narracao_completa()
            self.musica.parar()
            self.root.destroy()
    
    def sair(self):
        """Salva progresso e fecha aplicação."""
        self.parar_narracao_completa()
        self.musica.parar()
        
        if self.salvar_progresso():
            messagebox.showinfo("Novel Reader",
                              f"✓ Progresso salvo com sucesso!\n\n"
                              f"📑 Capítulo: {self.capitulo_atual}\n"
                              f"📄 Parágrafo: {self.paragrafo_atual}")
        
        self.root.destroy()


class ConfiguracoesWindow:
    """Janela de configurações do aplicativo."""
    
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        
        # Criar janela modal responsiva
        self.window = tk.Toplevel(parent)
        self.window.title("⚙️ Configurações")
        self.window.configure(bg=TemaEscuro.BG_PRINCIPAL)
        self.window.transient(parent)
        self.window.grab_set()
        
        # Tamanho inicial e mínimo
        largura_inicial = 900
        altura_inicial = 700
        self.window.minsize(750, 600)
        
        # Centralizar
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (largura_inicial // 2)
        y = (self.window.winfo_screenheight() // 2) - (altura_inicial // 2)
        self.window.geometry(f"{largura_inicial}x{altura_inicial}+{x}+{y}")
        
        # Container principal com scroll
        main_container = ttk.Frame(self.window)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Criar notebook com abas (sem padding extra)
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Criar abas
        self.criar_aba_musicas()
        self.criar_aba_texto()
        self.criar_aba_aparencia()
        self.criar_aba_perfil()
        self.criar_aba_novels()
        
        # Botão fechar
        btn_frame = ttk.Frame(main_container)
        btn_frame.pack(fill='x', pady=(10, 0))
        ttk.Button(btn_frame, text="✓ Fechar", command=self.fechar_janela,
                  style='Accent.TButton').pack(side='right', padx=5)
        
        # Protocolo para fechar janela (parar música de teste)
        self.window.protocol("WM_DELETE_WINDOW", self.fechar_janela)
    
    def criar_aba_musicas(self):
        """Cria aba de gerenciamento de músicas."""
        # Frame com scrollbar
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎵 Músicas")
        
        # Canvas e scrollbar para scroll vertical
        canvas = tk.Canvas(frame, bg=TemaEscuro.BG_PRINCIPAL, highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Frame principal com padding (dentro do scrollable)
        main_frame = ttk.Frame(scrollable_frame, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título com descrição
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(title_frame, text="Gerenciar Músicas de Fundo", 
                 font=('Segoe UI', 14, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(anchor='w')
        ttk.Label(title_frame, text="Adicione, teste e organize suas músicas de leitura e combate",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_SECONDARY).pack(anchor='w', pady=(3, 0))
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=(0, 15))
        
        # Música Atual
        musica_card = ttk.LabelFrame(main_frame, text="🎵 Música de Fundo", padding=12)
        musica_card.pack(fill='x', pady=(0, 15))
        
        musica_entry_frame = ttk.Frame(musica_card)
        musica_entry_frame.pack(fill='x', pady=(0, 8))
        
        self.entry_musica = ttk.Entry(musica_entry_frame, state='readonly',
                                      font=('Segoe UI', 10))
        self.entry_musica.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        btn_frame_musica = ttk.Frame(musica_card)
        btn_frame_musica.pack(fill='x')
        ttk.Button(btn_frame_musica, text="📁 Selecionar", 
                  command=self.selecionar_musica,
                  width=15).pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame_musica, text="▶ Testar", 
                  command=self.testar_musica,
                  width=12).pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame_musica, text="⏹ Parar", 
                  command=self.parar_teste,
                  width=12).pack(side='left')
        
        # Lista de músicas disponíveis
        list_card = ttk.LabelFrame(main_frame, text="📁 Biblioteca de Músicas", padding=12)
        list_card.pack(fill='both', expand=True)
        
        list_container = ttk.Frame(list_card)
        list_container.pack(fill='both', expand=True, pady=(0, 8))
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox_musicas = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                          bg=TemaEscuro.BG_CARD,
                                          fg=TemaEscuro.TEXT_PRIMARY,
                                          selectbackground=TemaEscuro.ACCENT_PRIMARY,
                                          selectforeground=TemaEscuro.BG_PRINCIPAL,
                                          font=('Segoe UI', 10),
                                          relief='flat',
                                          highlightthickness=1,
                                          highlightbackground=TemaEscuro.BORDER,
                                          activestyle='none')
        self.listbox_musicas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox_musicas.yview)
        
        # Botões de ação
        action_frame = ttk.Frame(list_card)
        action_frame.pack(fill='x')
        
        ttk.Button(action_frame, text="🗑️ Excluir Selecionada",
                  command=self.excluir_musica_selecionada,
                  width=20).pack(side='left', padx=(0, 5))
        ttk.Button(action_frame, text="🔄 Atualizar Lista",
                  command=self.atualizar_lista_musicas,
                  width=18).pack(side='left')
        
        # NÃO carregar automaticamente - apenas ao clicar no botão
    
    def criar_aba_texto(self):
        """Cria aba de estilização de texto."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Texto")
        
        # Dividir em área de conteúdo (scroll) e botões (fixo)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_columnconfigure(0, weight=1)
        
        # === ÁREA DE CONTEÚDO COM SCROLLBAR ===
        scroll_container = ttk.Frame(frame)
        scroll_container.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10, 5))
        scroll_container.grid_rowconfigure(0, weight=1)
        scroll_container.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(scroll_container, bg=TemaEscuro.BG_PRINCIPAL, highlightthickness=0)
        canvas.grid(row=0, column=0, sticky='nsew')
        
        scrollbar = ttk.Scrollbar(scroll_container, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        main_frame = ttk.Frame(canvas)
        canvas_window = canvas.create_window((0, 0), window=main_frame, anchor='nw')
        
        def on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
        
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        main_frame.bind('<Configure>', on_frame_configure)
        canvas.bind('<Configure>', on_canvas_configure)
        
        # Conteúdo dentro do main_frame com padding
        content_frame = ttk.Frame(main_frame, padding=20)
        content_frame.pack(fill='both', expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(title_frame, text="Estilização do Texto", 
                 font=('Segoe UI', 14, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(anchor='w')
        ttk.Label(title_frame, text="Personalize a aparência do texto para leitura confortável",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_SECONDARY).pack(anchor='w', pady=(3, 0))
        
        ttk.Separator(content_frame, orient='horizontal').pack(fill='x', pady=(0, 15))
        
        # Paleta de Cores
        paleta_card = ttk.LabelFrame(content_frame, text="🎨 Paleta de Cores", padding=15)
        paleta_card.pack(fill='x', pady=(0, 15))
        
        self.paleta_var = tk.StringVar(value=self.app.config_texto.get('paleta', 'padrao'))
        
        paletas_info = [
            ('padrao', '🌙 Padrão (Tokyo Night)', 'Tema escuro padrão do aplicativo'),
            ('sepia', '📜 Sépia', 'Tom quente ideal para leitura prolongada'),
            ('noite', '🌃 Noite', 'Preto profundo para ambientes escuros'),
            ('papel', '📄 Papel', 'Fundo claro como papel para leitura diurna')
        ]
        
        for valor, nome, desc in paletas_info:
            paleta_frame = ttk.Frame(paleta_card)
            paleta_frame.pack(fill='x', pady=5)
            
            ttk.Radiobutton(paleta_frame, text=nome, 
                           variable=self.paleta_var, 
                           value=valor,
                           command=self.aplicar_paleta_preview).pack(side='left')
            ttk.Label(paleta_frame, text=f"- {desc}",
                     font=('Segoe UI', 9),
                     foreground=TemaEscuro.TEXT_MUTED).pack(side='left', padx=(10, 0))
        
        # Tamanho da Fonte
        fonte_card = ttk.LabelFrame(content_frame, text="📏 Tamanho da Fonte", padding=15)
        fonte_card.pack(fill='x', pady=(0, 15))
        
        fonte_frame = ttk.Frame(fonte_card)
        fonte_frame.pack(fill='x', pady=5)
        
        ttk.Label(fonte_frame, text="Tamanho:",
                 font=('Segoe UI', 10, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(side='left', padx=(0, 10))
        
        self.tamanho_fonte_var = tk.IntVar(value=self.app.config_texto.get('tamanho_fonte', 11))
        self.slider_fonte = ttk.Scale(fonte_frame, from_=9, to=20, 
                                      variable=self.tamanho_fonte_var,
                                      orient='horizontal', length=300,
                                      command=self.atualizar_preview_fonte)
        self.slider_fonte.pack(side='left', padx=(0, 10))
        
        self.lbl_tamanho = ttk.Label(fonte_frame, text=f"{self.tamanho_fonte_var.get()}pt",
                                     font=('Segoe UI', 10, 'bold'),
                                     foreground=TemaEscuro.ACCENT_PRIMARY,
                                     width=5)
        self.lbl_tamanho.pack(side='left')
        
        # Preview (reduzido para caber na tela)
        preview_card = ttk.LabelFrame(content_frame, text="👁️ Pré-visualização", padding=12)
        preview_card.pack(fill='both', expand=True)
        
        preview_container = ttk.Frame(preview_card)
        preview_container.pack(fill='both', expand=True)
        
        self.text_preview = tk.Text(preview_container, height=6, wrap='word',
                                    font=('Segoe UI', self.tamanho_fonte_var.get()),
                                    relief='flat',
                                    borderwidth=2,
                                    padx=15,
                                    pady=10)
        self.text_preview.pack(fill='both', expand=True)
        
        texto_exemplo = (
            "Era uma vez, em uma terra distante, um jovem cultivador que sonhava em alcançar o ápice das artes marciais. "
            "Através de inúmeras provações e tribulações, ele forjou seu caminho através do Mundo Marcial.\n\n"
            "Este é um exemplo de como o texto aparecerá durante a narração. "
            "Ajuste a paleta de cores e o tamanho da fonte ao seu gosto para uma experiência de leitura confortável."
        )
        self.text_preview.insert('1.0', texto_exemplo)
        self.text_preview.config(state='disabled')
        
        # Aplicar preview inicial
        self.aplicar_paleta_preview()
        
        # === BOTÕES FIXOS NO RODAPÉ (FORA DO SCROLL) ===
        btn_frame = ttk.Frame(frame, padding=(15, 10))
        btn_frame.grid(row=1, column=0, sticky='ew')
        
        # Separador visual
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=(0, 10))
        
        btn_container = ttk.Frame(btn_frame)
        btn_container.pack(fill='x')
        
        ttk.Button(btn_container, text="✓ Aplicar e Salvar",
                  command=self.salvar_estilo_texto,
                  style='Accent.TButton',
                  width=20).pack(side='right', padx=(5, 0))
        ttk.Button(btn_container, text="↺ Restaurar Padrão",
                  command=self.restaurar_padrao_texto,
                  width=20).pack(side='right')
    
    def aplicar_paleta_preview(self):
        """Aplica paleta selecionada no preview."""
        paletas = {
            'padrao': {'bg': '#24283b', 'fg': '#e2e8f0'},
            'sepia': {'bg': '#f4ecd8', 'fg': '#5b4636'},
            'noite': {'bg': '#0d1117', 'fg': '#c9d1d9'},
            'papel': {'bg': '#fefcf3', 'fg': '#2e2e2e'}
        }
        paleta = paletas.get(self.paleta_var.get(), paletas['padrao'])
        self.text_preview.config(bg=paleta['bg'], fg=paleta['fg'])
    
    def atualizar_preview_fonte(self, valor):
        """Atualiza tamanho da fonte no preview."""
        tamanho = int(float(valor))
        self.lbl_tamanho.config(text=f"{tamanho}pt")
        self.text_preview.config(font=('Segoe UI', tamanho))
    
    def salvar_estilo_texto(self):
        """Salva e aplica estilo de texto."""
        self.app.config_texto['paleta'] = self.paleta_var.get()
        self.app.config_texto['tamanho_fonte'] = int(self.tamanho_fonte_var.get())
        self.app.salvar_config_texto()
        self.app.aplicar_estilo_texto()
        
        # Atualizar display se estiver em modo leitura
        if self.app.modo_leitura:
            self.app.atualizar_display_modo_leitura()
        else:
            # Atualizar texto atual
            if self.app.conteudo_capitulo and self.app.paragrafo_atual <= len(self.app.conteudo_capitulo):
                texto = self.app.conteudo_capitulo[self.app.paragrafo_atual - 1]
                self.app.atualizar_display(texto)
        
        messagebox.showinfo("✓ Sucesso", "Estilo de texto aplicado!")
    
    def restaurar_padrao_texto(self):
        """Restaura estilo padrão de texto."""
        self.paleta_var.set('padrao')
        self.tamanho_fonte_var.set(11)
        self.aplicar_paleta_preview()
        self.atualizar_preview_fonte(11)
    
    def criar_aba_aparencia(self):
        """Cria aba de personalização de aparência."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎨 Aparência")
        
        main_frame = ttk.Frame(frame, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(title_frame, text="Personalização Visual", 
                 font=('Segoe UI', 14, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(anchor='w')
        ttk.Label(title_frame, text="Ajuste a aparência do aplicativo ao seu gosto",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_SECONDARY).pack(anchor='w', pady=(3, 0))
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=(0, 15))
        
        # Tema
        tema_card = ttk.LabelFrame(main_frame, text="🌙 Tema de Cores", padding=15)
        tema_card.pack(fill='x', pady=(0, 15))
        
        self.tema_var = tk.StringVar(value="Escuro (Tokyo Night)")
        
        # Opção de tema escuro
        tema_escuro_frame = ttk.Frame(tema_card)
        tema_escuro_frame.pack(fill='x', pady=5)
        
        ttk.Radiobutton(tema_escuro_frame, text="🌙 Escuro (Tokyo Night)", 
                       variable=self.tema_var, 
                       value="Escuro (Tokyo Night)").pack(side='left')
        ttk.Label(tema_escuro_frame, text="- Tema escuro otimizado para conforto visual",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED).pack(side='left', padx=(10, 0))
        
        # Opção de tema claro (em desenvolvimento)
        tema_claro_frame = ttk.Frame(tema_card)
        tema_claro_frame.pack(fill='x', pady=5)
        
        ttk.Radiobutton(tema_claro_frame, text="☀️ Claro (em desenvolvimento)", 
                       variable=self.tema_var, 
                       value="Claro",
                       state='disabled').pack(side='left')
        ttk.Label(tema_claro_frame, text="- Em breve!",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED).pack(side='left', padx=(10, 0))
        
        # Paleta de cores atual
        paleta_card = ttk.LabelFrame(main_frame, text="🎨 Paleta Atual", padding=15)
        paleta_card.pack(fill='x', pady=(0, 15))
        
        ttk.Label(paleta_card, text="Esquema de cores Tokyo Night Storm",
                 font=('Segoe UI', 10, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(anchor='w', pady=(0, 10))
        
        # Mostrar cores
        cores_info = [
            ("🔵 Primária", TemaEscuro.ACCENT_PRIMARY, "Destaques e botões principais"),
            ("🟣 Secundária", TemaEscuro.ACCENT_SECONDARY, "Acentos secundários"),
            ("🟢 Sucesso", TemaEscuro.ACCENT_SUCCESS, "Indicações de sucesso"),
            ("🟡 Aviso", TemaEscuro.ACCENT_WARNING, "Avisos e alertas"),
            ("🔴 Perigo", TemaEscuro.ACCENT_DANGER, "Erros e ações destrutivas")
        ]
        
        for label, cor, desc in cores_info:
            cor_frame = ttk.Frame(paleta_card)
            cor_frame.pack(fill='x', pady=3)
            
            # Amostra de cor
            canvas = tk.Canvas(cor_frame, width=30, height=20, 
                             bg=cor, highlightthickness=1,
                             highlightbackground=TemaEscuro.BORDER)
            canvas.pack(side='left', padx=(0, 10))
            
            ttk.Label(cor_frame, text=label,
                     font=('Segoe UI', 9, 'bold'),
                     foreground=TemaEscuro.TEXT_PRIMARY,
                     width=15).pack(side='left')
            ttk.Label(cor_frame, text=desc,
                     font=('Segoe UI', 9),
                     foreground=TemaEscuro.TEXT_SECONDARY).pack(side='left')
        
        # Informações sobre UX
        ux_card = ttk.LabelFrame(main_frame, text="ℹ️ Sobre o Design", padding=15)
        ux_card.pack(fill='x')
        
        ux_text = (
            "• Contraste otimizado seguindo WCAG 2.1 (mínimo 4.5:1)\n"
            "• Cores com saturação reduzida para conforto visual prolongado\n"
            "• Espaçamento adequado para facilitar a leitura\n"
            "• Hierarquia visual clara com diferentes pesos de fonte"
        )
        ttk.Label(ux_card, text=ux_text,
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED,
                 justify='left').pack(anchor='w')
    
    def criar_aba_perfil(self):
        """Cria aba de gerenciamento de perfil."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👤 Perfil")
        
        main_frame = ttk.Frame(frame, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(title_frame, text="Gerenciar Progresso de Leitura", 
                 font=('Segoe UI', 14, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(anchor='w')
        ttk.Label(title_frame, text="Visualize e gerencie seu progresso de leitura",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_SECONDARY).pack(anchor='w', pady=(3, 0))
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=(0, 15))
        
        # Informações atuais
        info_card = ttk.LabelFrame(main_frame, text="📊 Progresso Atual", padding=15)
        info_card.pack(fill='x', pady=(0, 15))
        
        # Obter nome da novel dos metadados ou usar padrão
        novel_nome = self.app.leitor.metadata.get('titulo', 'Martial World')
        
        # Grid para informações organizadas
        info_labels = [
            ("📖 Novel:", novel_nome),
            ("📑 Capítulo:", str(self.app.capitulo_atual)),
            ("📄 Parágrafo:", str(self.app.paragrafo_atual)),
        ]
        
        for i, (label, value) in enumerate(info_labels):
            row_frame = ttk.Frame(info_card)
            row_frame.pack(fill='x', pady=3)
            ttk.Label(row_frame, text=label, 
                     font=('Segoe UI', 10, 'bold'),
                     foreground=TemaEscuro.TEXT_SECONDARY,
                     width=15).pack(side='left')
            ttk.Label(row_frame, text=value, 
                     font=('Segoe UI', 10),
                     foreground=TemaEscuro.TEXT_PRIMARY).pack(side='left')
        
        # Gerenciamento de Arquivos
        files_card = ttk.LabelFrame(main_frame, text="📁 Gerenciar Arquivos", padding=15)
        files_card.pack(fill='x', pady=(0, 15))
        
        ttk.Button(files_card, text="📂 Abrir Pasta de Configurações",
                  command=self.abrir_pasta_config,
                  width=35).pack(fill='x', pady=(0, 8))
        
        ttk.Label(files_card, text="Acesse os arquivos de progresso e configurações",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED).pack(anchor='w')
        
        # Ações de Progresso
        acoes_card = ttk.LabelFrame(main_frame, text="🔧 Ações de Progresso", padding=15)
        acoes_card.pack(fill='x', pady=(0, 15))
        
        # Exportar
        export_frame = ttk.Frame(acoes_card)
        export_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(export_frame, text="📤 Exportar Progresso", 
                  command=self.exportar_progresso,
                  width=25).pack(side='left', padx=(0, 8))
        ttk.Label(export_frame, text="Salve seu progresso em um arquivo",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED).pack(side='left')
        
        # Importar
        import_frame = ttk.Frame(acoes_card)
        import_frame.pack(fill='x', pady=(0, 10))
        ttk.Button(import_frame, text="📥 Importar Progresso", 
                  command=self.importar_progresso,
                  width=25).pack(side='left', padx=(0, 8))
        ttk.Label(import_frame, text="Carregue progresso de um arquivo",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED).pack(side='left')
        
        # Resetar novel específica
        reset_novel_frame = ttk.Frame(acoes_card)
        reset_novel_frame.pack(fill='x', pady=(0, 10))
        
        # Obter nome da novel
        novel_nome = self.app.leitor.metadata.get('titulo', 'Martial World')
        
        ttk.Button(reset_novel_frame, text="🔄 Resetar Novel Atual", 
                  command=self.resetar_novel_atual,
                  width=25).pack(side='left', padx=(0, 8))
        ttk.Label(reset_novel_frame, text=f"Reinicia o progresso de {novel_nome}",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_MUTED).pack(side='left')
        
        # Resetar tudo
        reset_frame = ttk.Frame(acoes_card)
        reset_frame.pack(fill='x')
        ttk.Button(reset_frame, text="⚠️ Resetar Tudo", 
                  command=self.resetar_progresso,
                  width=25).pack(side='left', padx=(0, 8))
        ttk.Label(reset_frame, text="Remove todo o progresso (irreversível)",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.ACCENT_DANGER).pack(side='left')
    
    # Métodos de música
    def selecionar_musica(self):
        """Abre diálogo para selecionar arquivo de música."""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Música de Fundo",
            filetypes=[
                ("Arquivos de Áudio", "*.mp3 *.wav *.ogg"),
                ("MP3", "*.mp3"),
                ("WAV", "*.wav"),
                ("OGG", "*.ogg"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        if arquivo:
            try:
                # Copiar para pasta de assets
                destino = os.path.join('assets', 'audio', 'background', os.path.basename(arquivo))
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                shutil.copy2(arquivo, destino)
                
                # Atualizar entry
                self.entry_musica.config(state='normal')
                self.entry_musica.delete(0, tk.END)
                self.entry_musica.insert(0, os.path.basename(arquivo))
                self.entry_musica.config(state='readonly')
                
                self.atualizar_lista_musicas()
                # Recarregar comboboxes da tela principal
                self.app.recarregar_lista_musicas()
                messagebox.showinfo("✓ Sucesso", "Música adicionada com sucesso!")
                
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao adicionar música:\n{str(e)}")
    
    def testar_musica(self):
        """Testa a música selecionada usando canal temporário."""
        try:
            # SEMPRE verificar primeiro a seleção da listbox
            selecao = self.listbox_musicas.curselection()
            if selecao:
                musica = self.listbox_musicas.get(selecao[0])
            else:
                # Se não há seleção na listbox, usar o entry
                musica = self.entry_musica.get()
            
            if not musica:
                messagebox.showwarning("⚠️ Aviso", "Selecione uma música na lista ou no campo")
                return
            
            # Criar canal temporário para teste
            if not hasattr(self, 'canal_teste'):
                self.canal_teste = pygame.mixer.Channel(2)  # Canal 2 para testes
            
            # Parar teste anterior
            self.canal_teste.stop()
            
            # Construir caminho completo
            arquivo_musica = os.path.abspath(os.path.join('assets', 'audio', 'background', musica))
            
            if os.path.exists(arquivo_musica):
                som = pygame.mixer.Sound(arquivo_musica)
                self.canal_teste.play(som, loops=-1)
                self.canal_teste.set_volume(0.3)  # Volume reduzido para teste
                
                # Atualizar entry com a música testada
                self.entry_musica.config(state='normal')
                self.entry_musica.delete(0, tk.END)
                self.entry_musica.insert(0, musica)
                self.entry_musica.config(state='readonly')
                
                print(f"🎵 Testando: {musica}")
            else:
                messagebox.showerror("❌ Erro", f"Arquivo não encontrado:\n{arquivo_musica}")
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao testar música:\n{str(e)}")
    
    def parar_teste(self):
        """Para o teste de música."""
        try:
            if hasattr(self, 'canal_teste'):
                self.canal_teste.stop()
                print("⏹ Teste de música parado")
        except Exception as e:
            print(f"Erro ao parar música: {e}")
    
    def fechar_janela(self):
        """Fecha a janela parando qualquer música de teste."""
        self.parar_teste()
        self.window.destroy()
    
    def atualizar_lista_musicas(self):
        """Atualiza a lista de músicas disponíveis."""
        self.listbox_musicas.delete(0, tk.END)
        try:
            pasta_musicas = os.path.join('assets', 'audio', 'background')
            if os.path.exists(pasta_musicas):
                musicas = [f for f in os.listdir(pasta_musicas) 
                          if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
                for musica in sorted(musicas):
                    self.listbox_musicas.insert(tk.END, musica)
                
                # Recarregar comboboxes na tela principal
                self.app.recarregar_lista_musicas()
        except Exception as e:
            print(f"Erro ao listar músicas: {e}")
    
    def excluir_musica_selecionada(self):
        """Exclui a música selecionada da lista."""
        selecao = self.listbox_musicas.curselection()
        if not selecao:
            messagebox.showwarning("⚠️ Aviso", "Selecione uma música para excluir")
            return
        
        musica = self.listbox_musicas.get(selecao[0])
        resposta = messagebox.askyesno(
            "⚠️ Confirmar Exclusão",
            f"Tem certeza que deseja excluir a música:\n\n{musica}\n\nEsta ação não pode ser desfeita!"
        )
        
        if resposta:
            try:
                arquivo = os.path.join('assets', 'audio', 'background', musica)
                if os.path.exists(arquivo):
                    os.remove(arquivo)
                    self.atualizar_lista_musicas()
                    messagebox.showinfo("✓ Sucesso", f"Música '{musica}' excluída com sucesso!")
                else:
                    messagebox.showerror("❌ Erro", "Arquivo não encontrado")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao excluir música:\n{str(e)}")
    
    # Métodos de voz
    # Métodos de perfil
    def exportar_progresso(self):
        """Exporta o progresso atual para um arquivo JSON."""
        arquivo = filedialog.asksaveasfilename(
            title="Exportar Progresso",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                # Obter nome da novel
                novel_nome = self.app.leitor.metadata.get('titulo', 'Martial World')
                
                progresso = {
                    'novel_id': novel_nome,
                    'capitulo_atual': self.app.capitulo_atual,
                    'paragrafo_atual': self.app.paragrafo_atual,
                    'tempo_total': self.app.tempo_total_narracao
                }
                
                with open(arquivo, 'w', encoding='utf-8') as f:
                    json.dump(progresso, f, indent=4, ensure_ascii=False)
                
                messagebox.showinfo("✓ Sucesso", "Progresso exportado com sucesso!")
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao exportar:\n{str(e)}")
    
    def importar_progresso(self):
        """Importa progresso de um arquivo JSON."""
        arquivo = filedialog.askopenfilename(
            title="Importar Progresso",
            filetypes=[("JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    progresso = json.load(f)
                
                # Validar dados
                required_keys = ['novel_id', 'capitulo_atual', 'paragrafo_atual']
                if not all(k in progresso for k in required_keys):
                    raise ValueError("Arquivo de progresso inválido")
                
                # Aplicar progresso
                self.app.capitulo_atual = progresso['capitulo_atual']
                self.app.paragrafo_atual = progresso['paragrafo_atual']
                self.app.carregar_capitulo()
                
                messagebox.showinfo("✓ Sucesso", "Progresso importado com sucesso!")
                self.window.destroy()
                
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao importar:\n{str(e)}")
    
    def abrir_pasta_config(self):
        """Abre a pasta de configurações no explorador."""
        try:
            pasta_config = os.path.abspath('config')
            if not os.path.exists(pasta_config):
                os.makedirs(pasta_config)
            
            # Abrir no explorador do Windows
            os.startfile(pasta_config)
        except Exception as e:
            messagebox.showerror("❌ Erro", f"Erro ao abrir pasta:\n{str(e)}")
    
    def resetar_novel_atual(self):
        """Reseta o progresso apenas da novel atual."""
        # Obter nome da novel
        novel_atual = self.app.leitor.metadata.get('titulo', 'Martial World')
        
        resposta = messagebox.askyesno(
            "⚠️ Confirmar Reset",
            f"Tem certeza que deseja resetar o progresso da novel:\n\n"
            f"📖 {novel_atual}\n\n"
            f"Esta ação não pode ser desfeita!"
        )
        
        if resposta:
            self.app.capitulo_atual = 1
            self.app.paragrafo_atual = 1
            self.app.tempo_total_narracao = 0
            self.app.carregar_capitulo()
            self.app.salvar_progresso()
            messagebox.showinfo("✓ Sucesso", f"Progresso de '{novel_atual}' resetado!")
            self.window.destroy()
    
    def resetar_progresso(self):
        """Reseta TODO o progresso de leitura."""
        resposta = messagebox.askyesno(
            "⚠️ AVISO: Ação Irreversível",
            "Tem certeza que deseja resetar TODO o progresso?\n\n"
            "⚠️ Isso irá apagar o progresso de TODAS as novels!\n\n"
            "Esta ação não pode ser desfeita!",
            icon='warning'
        )
        
        if resposta:
            # Confirmação dupla para ação crítica
            confirma = messagebox.askyesno(
                "⚠️ Última Confirmação",
                "Você tem ABSOLUTA certeza?\n\n"
                "Todo o progresso será PERDIDO permanentemente!"
            )
            
            if confirma:
                try:
                    # Apagar arquivo de progresso
                    arquivo_progresso = os.path.join('config', 'progresso.json')
                    if os.path.exists(arquivo_progresso):
                        os.remove(arquivo_progresso)
                    
                    # Resetar valores
                    self.app.capitulo_atual = 1
                    self.app.paragrafo_atual = 1
                    self.app.tempo_total_narracao = 0
                    self.app.carregar_capitulo()
                    self.app.salvar_progresso()
                    
                    messagebox.showinfo("✓ Sucesso", "Todo o progresso foi resetado!")
                    self.window.destroy()
                except Exception as e:
                    messagebox.showerror("❌ Erro", f"Erro ao resetar:\n{str(e)}")
    
    # Métodos de novels
    def atualizar_lista_novels(self):
        """Atualiza a lista de novels disponíveis."""
        self.listbox_novels.delete(0, tk.END)
        try:
            pasta_novels = 'novels'
            if os.path.exists(pasta_novels):
                novels = [d for d in os.listdir(pasta_novels) 
                         if os.path.isdir(os.path.join(pasta_novels, d))]
                for novel in sorted(novels):
                    self.listbox_novels.insert(tk.END, novel)
        except Exception as e:
            print(f"Erro ao listar novels: {e}")
    
    def criar_aba_novels(self):
        """Cria aba de gerenciamento de novels."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📚 Novels")
        
        main_frame = ttk.Frame(frame, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Título
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 15))
        ttk.Label(title_frame, text="Gerenciar Novels", 
                 font=('Segoe UI', 14, 'bold'),
                 foreground=TemaEscuro.TEXT_PRIMARY).pack(anchor='w')
        ttk.Label(title_frame, text="Adicione e gerencie suas novels para narração",
                 font=('Segoe UI', 9),
                 foreground=TemaEscuro.TEXT_SECONDARY).pack(anchor='w', pady=(3, 0))
        
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=(0, 15))
        
        # Novels disponíveis
        list_card = ttk.LabelFrame(main_frame, text="📖 Biblioteca de Novels", padding=12)
        list_card.pack(fill='both', expand=True, pady=(0, 12))
        
        list_container = ttk.Frame(list_card)
        list_container.pack(fill='both', expand=True, pady=(0, 10))
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox_novels = tk.Listbox(list_container, yscrollcommand=scrollbar.set,
                                         bg=TemaEscuro.BG_CARD,
                                         fg=TemaEscuro.TEXT_PRIMARY,
                                         selectbackground=TemaEscuro.ACCENT_PRIMARY,
                                         selectforeground=TemaEscuro.BG_PRINCIPAL,
                                         font=('Segoe UI', 10),
                                         relief='flat',
                                         highlightthickness=1,
                                         highlightbackground=TemaEscuro.BORDER,
                                         activestyle='none')
        self.listbox_novels.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox_novels.yview)
        
        # Botões de ação
        btn_frame = ttk.Frame(list_card)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame, text="➕ Adicionar Novel", 
                  command=self.adicionar_novel,
                  width=20).pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame, text="🔄 Atualizar Lista",
                  command=self.atualizar_lista_novels,
                  width=18).pack(side='left')
        
        # Requisitos de estrutura
        req_card = ttk.LabelFrame(main_frame, text="ℹ️ Estrutura Necessária", padding=12)
        req_card.pack(fill='x')
        
        estrutura_text = (
            "Para adicionar uma novel, a pasta deve conter:\n\n"
            "├─ metadata.json     (informações da novel)\n"
            "└─ capitulos/         (pasta com os capítulos)\n"
            "    ├─ cap_0001.json\n"
            "    ├─ cap_0002.json\n"
            "    └─ ..."
        )
        
        ttk.Label(req_card, text=estrutura_text,
                 font=('Consolas', 9),
                 foreground=TemaEscuro.TEXT_SECONDARY,
                 justify='left').pack(anchor='w')
        
        # Carregar lista de novels
        self.atualizar_lista_novels()
    
    def adicionar_novel(self):
        """Adiciona uma nova novel ao sistema."""
        pasta = filedialog.askdirectory(
            title="Selecionar Pasta da Novel"
        )
        
        if pasta:
            # Validar estrutura
            erros = []
            
            metadata_path = os.path.join(pasta, 'metadata.json')
            if not os.path.exists(metadata_path):
                erros.append("❌ metadata.json não encontrado")
            
            capitulos_path = os.path.join(pasta, 'capitulos')
            if not os.path.exists(capitulos_path):
                erros.append("❌ Pasta 'capitulos/' não encontrada")
            elif not os.listdir(capitulos_path):
                erros.append("❌ Pasta 'capitulos/' está vazia")
            
            if erros:
                messagebox.showerror("❌ Estrutura Inválida", 
                                   "A pasta selecionada não possui a estrutura correta:\n\n" + 
                                   "\n".join(erros) +
                                   "\n\nEstrutura esperada:\n" +
                                   "pasta_novel/\n" +
                                   "  ├─ metadata.json\n" +
                                   "  └─ capitulos/\n" +
                                   "      ├─ cap_0001.json\n" +
                                   "      ├─ cap_0002.json\n" +
                                   "      └─ ...")
                return
            
            try:
                # Copiar para pasta novels
                nome_novel = os.path.basename(pasta)
                destino = os.path.join('novels', nome_novel)
                
                if os.path.exists(destino):
                    resposta = messagebox.askyesno(
                        "⚠️ Novel Existente",
                        f"A novel '{nome_novel}' já existe.\n\nDeseja substituir?"
                    )
                    if not resposta:
                        return
                    shutil.rmtree(destino)
                
                shutil.copytree(pasta, destino)
                self.atualizar_lista_novels()
                messagebox.showinfo("✓ Sucesso", 
                                  f"Novel '{nome_novel}' adicionada com sucesso!")
                
            except Exception as e:
                messagebox.showerror("❌ Erro", f"Erro ao adicionar novel:\n{str(e)}")


def main():
    root = tk.Tk()
    app = NovelReaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
Novel Reader - Interface Gráfica Moderna
Sistema de narração com controles visuais avançados e tema escuro
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import asyncio
import pygame
import edge_tts
import tempfile
import time
import json
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
    """Configurações de tema escuro moderno."""
    
    # Cores principais
    BG_PRINCIPAL = "#1e1e2e"
    BG_SECUNDARIO = "#2a2a3e"
    BG_TERCIARIO = "#313244"
    BG_HOVER = "#3a3a52"
    
    # Acentos
    ACCENT_PRIMARY = "#89b4fa"
    ACCENT_SECONDARY = "#cba6f7"
    ACCENT_SUCCESS = "#a6e3a1"
    ACCENT_WARNING = "#fab387"
    ACCENT_DANGER = "#f38ba8"
    
    # Textos
    TEXT_PRIMARY = "#cdd6f4"
    TEXT_SECONDARY = "#a6adc8"
    TEXT_MUTED = "#6c7086"
    
    # Bordas e sombras
    BORDER = "#45475a"
    SHADOW = "#11111b"
    
    # Highlight
    HIGHLIGHT_BG = "#f9e2af"
    HIGHLIGHT_FG = "#1e1e2e"
    
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
        
        # Dicionários para armazenar todas as BGMs
        self.bgms_leitura = {}  # {nome_arquivo: pygame.Sound}
        self.bgms_combate = {}  # {nome_arquivo: pygame.Sound}
        
        # BGMs selecionadas atualmente
        self.bgm_leitura_atual = None
        self.bgm_combate_atual = None
        
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
                
                # Carregar TODAS as BGMs de leitura (bgm_u_*)
                bgms_leitura = [f for f in arquivos if f.startswith('bgm_u_') and f.endswith('.mp3')]
                for bgm in bgms_leitura:
                    path = os.path.join(base_path, bgm)
                    self.bgms_leitura[bgm] = pygame.mixer.Sound(path)
                    print(f"✓ BGM Leitura carregada: {bgm}")
                
                # Selecionar primeira como padrão
                if self.bgms_leitura:
                    self.bgm_leitura_atual = list(self.bgms_leitura.keys())[0]
                else:
                    print(f"⚠️ Nenhuma BGM de leitura encontrada (bgm_u_*.mp3)")
                
                # Carregar TODAS as BGMs de combate
                bgms_combate = [f for f in arquivos if f.startswith('combat_') and f.endswith('.mp3')]
                for bgm in bgms_combate:
                    path = os.path.join(base_path, bgm)
                    self.bgms_combate[bgm] = pygame.mixer.Sound(path)
                    print(f"✓ BGM Combate carregada: {bgm}")
                
                # Selecionar primeira como padrão
                if self.bgms_combate:
                    self.bgm_combate_atual = list(self.bgms_combate.keys())[0]
                else:
                    print(f"⚠️ Nenhuma BGM de combate encontrada (combat_*.mp3)")
            else:
                print(f"⚠️ Pasta de BGMs não encontrada: {base_path}")
        except Exception as e:
            print(f"❌ Erro ao carregar músicas: {e}")
    
    def obter_listas_bgms(self):
        """Retorna listas de nomes de BGMs para os comboboxes."""
        return list(self.bgms_leitura.keys()), list(self.bgms_combate.keys())
    
    def selecionar_bgm_leitura(self, nome_arquivo):
        """Seleciona uma BGM de leitura específica."""
        if nome_arquivo in self.bgms_leitura:
            self.bgm_leitura_atual = nome_arquivo
            print(f"🎵 BGM Leitura selecionada: {nome_arquivo}")
            # Se estiver tocando música normal, troca automaticamente
            if self.modo_atual == 'normal':
                self.tocar_normal()
        else:
            print(f"❌ BGM não encontrada: {nome_arquivo}")
    
    def selecionar_bgm_combate(self, nome_arquivo):
        """Seleciona uma BGM de combate específica."""
        if nome_arquivo in self.bgms_combate:
            self.bgm_combate_atual = nome_arquivo
            print(f"⚔️ BGM Combate selecionada: {nome_arquivo}")
            # Se estiver tocando música de combate, troca automaticamente
            if self.modo_atual == 'combate':
                self.tocar_combate()
        else:
            print(f"❌ BGM não encontrada: {nome_arquivo}")
    
    def tocar_normal(self):
        """Toca música ambiente normal (leitura)."""
        if self.bgm_leitura_atual and self.bgm_leitura_atual in self.bgms_leitura:
            self.canal_musica.stop()
            self.som_atual = self.bgms_leitura[self.bgm_leitura_atual]
            self.som_atual.set_volume(0 if self.mutado else self.volume_musica)
            self.canal_musica.play(self.som_atual, loops=-1)
            self.modo_atual = 'normal'
            print(f"▶️ Tocando: {self.bgm_leitura_atual} (volume: {self.volume_musica:.2f})")
        else:
            print("❌ Música de leitura não disponível")
    
    def tocar_combate(self):
        """Toca música de combate."""
        if self.bgm_combate_atual and self.bgm_combate_atual in self.bgms_combate:
            self.canal_musica.stop()
            self.som_atual = self.bgms_combate[self.bgm_combate_atual]
            self.som_atual.set_volume(0 if self.mutado else self.volume_musica)
            self.canal_musica.play(self.som_atual, loops=-1)
            self.modo_atual = 'combate'
            print(f"▶️ Tocando: {self.bgm_combate_atual} (volume: {self.volume_musica:.2f})")
        else:
            print("❌ Música de combate não disponível")
    
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
    
    def __init__(self, voz='Francisca', canal=None):
        self.voz_atual = self.VOZES.get(voz, self.VOZES['Francisca'])
        self.temp_dir = tempfile.gettempdir()
        self.canal = canal if canal else pygame.mixer.Channel(1)
        self.volume = 1.0
        self.velocidade = 0
        self.pausado = False
        self.som_atual = None
        
        # Sistema de cache otimizado com OrderedDict para LRU
        self.cache_sounds = OrderedDict()  # {hash_texto: pygame.Sound}
        self.max_cache_size = 10  # Manter últimos 10 parágrafos em cache
        
        # Sistema de pré-carregamento com thread dedicada
        self.fila_precarregamento = Queue()
        self.thread_precarregamento = None
        self.precarregamento_ativo = False
        self._iniciar_thread_precarregamento()
        
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
                # Pegar próximo texto da fila (timeout de 1s)
                texto = self.fila_precarregamento.get(timeout=1.0)
                
                if not texto or not texto.strip():
                    continue
                
                texto_hash = f"{hash(texto)}_{self.velocidade}"
                
                # Se já está em cache, pular
                if texto_hash in self.cache_sounds:
                    continue
                
                # Gerar áudio
                arquivo = asyncio.run(self._gerar_audio_async(texto))
                som = pygame.mixer.Sound(arquivo)
                
                # Adicionar ao cache (LRU)
                self.cache_sounds[texto_hash] = som
                
                # Limitar tamanho do cache
                if len(self.cache_sounds) > self.max_cache_size:
                    # Remover o mais antigo (primeiro item)
                    self.cache_sounds.popitem(last=False)
                
                print(f"✓ Pré-carregado em background")
                
            except Exception as e:
                if not isinstance(e, TimeoutError):
                    pass  # Timeout é normal quando não há nada na fila
    
    async def _gerar_audio_async(self, texto: str):
        """Gera áudio usando Edge TTS."""
        texto_hash = f"{hash(texto)}_{self.velocidade}"
        rate = f"{self.velocidade:+d}%"
        temp_file = os.path.join(self.temp_dir, f'tts_{texto_hash}.mp3')
        
        if not os.path.exists(temp_file):
            communicate = edge_tts.Communicate(texto, self.voz_atual, rate=rate)
            await communicate.save(temp_file)
        
        return temp_file
    
    def set_velocidade(self, velocidade):
        """Define velocidade (-50 a +50)."""
        self.velocidade = int(velocidade)
        print(f"⚡ Velocidade narração: {self.velocidade:+d}%")
    
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
        """Adiciona texto à fila de pré-carregamento."""
        if texto and texto.strip():
            # Limpar fila antiga e adicionar novo
            while not self.fila_precarregamento.empty():
                try:
                    self.fila_precarregamento.get_nowait()
                except:
                    break
            self.fila_precarregamento.put(texto)
    
    def narrar(self, texto: str, callback_pausado=None):
        """Narra texto simples com suporte a pausa e cache."""
        if not texto.strip():
            return
        
        try:
            texto_hash = f"{hash(texto)}_{self.velocidade}"
            
            # Tentar obter do cache primeiro
            if texto_hash in self.cache_sounds:
                self.som_atual = self.cache_sounds[texto_hash]
                print(f"⚡ Usando áudio do cache (transição instantânea)")
            else:
                # Se não está em cache, gerar agora (fallback)
                print(f"⚠️ Áudio não estava em cache, gerando...")
                arquivo = asyncio.run(self._gerar_audio_async(texto))
                self.som_atual = pygame.mixer.Sound(arquivo)
                self.cache_sounds[texto_hash] = self.som_atual
            
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
        
        # Bind de foco e redimensionamento
        self.root.bind('<FocusIn>', self.on_focus)
        self.root.bind('<FocusOut>', self.on_unfocus)
        self.root.bind('<Configure>', self.on_resize)
        self.tem_foco = True
    
    def criar_interface(self):
        """Cria todos os elementos da interface moderna."""
        
        # Container principal com padding
        main_container = ttk.Frame(self.root, padding=15)
        main_container.grid(row=0, column=0, sticky='nsew')
        main_container.grid_columnconfigure(0, weight=1)
        
        # ===== CABEÇALHO =====
        self.criar_cabecalho(main_container)
        
        # ===== SEÇÃO DE CONTROLES =====
        self.criar_secao_controles(main_container)
        
        # ===== ÁREA DE VISUALIZAÇÃO =====
        self.criar_area_visualizacao(main_container)
        
        # ===== CONTROLES DE PLAYBACK =====
        self.criar_controles_playback(main_container)
        
        # ===== RODAPÉ =====
        self.criar_rodape(main_container)
    
    def criar_cabecalho(self, parent):
        """Cria cabeçalho com título e status."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(header_frame, 
                          text="📚 Novel Reader",
                          font=('Segoe UI', 22, 'bold'),
                          foreground=TemaEscuro.ACCENT_PRIMARY)
        titulo.grid(row=0, column=0, sticky='w')
        
        # Subtítulo
        subtitulo = ttk.Label(header_frame,
                             text="Sistema de Narração Inteligente",
                             font=('Segoe UI', 9),
                             foreground=TemaEscuro.TEXT_MUTED)
        subtitulo.grid(row=1, column=0, sticky='w')
        
        # Status badge
        self.status_badge = tk.Label(header_frame,
                                     text="⏹️ PARADO",
                                     font=('Segoe UI', 10, 'bold'),
                                     bg=TemaEscuro.BG_TERCIARIO,
                                     fg=TemaEscuro.TEXT_SECONDARY,
                                     padx=15,
                                     pady=5,
                                     relief='flat',
                                     borderwidth=0)
        self.status_badge.grid(row=0, column=2, sticky='e')
        
        # Posição info
        self.lbl_posicao = ttk.Label(header_frame,
                                     text="Capítulo: - | Parágrafo: -/-",
                                     font=('Segoe UI', 10))
        self.lbl_posicao.grid(row=2, column=0, columnspan=3, sticky='w', pady=(5, 0))
        
        # Info de capítulo carregado
        self.lbl_cap_info = ttk.Label(header_frame,
                                      text="",
                                      font=('Segoe UI', 9),
                                      foreground=TemaEscuro.ACCENT_SUCCESS)
        self.lbl_cap_info.grid(row=3, column=0, columnspan=3, sticky='w', pady=(2, 0))
        
        # Progresso total da novel
        self.lbl_progresso_total = ttk.Label(header_frame,
                                             text="",
                                             font=('Segoe UI', 9),
                                             foreground=TemaEscuro.TEXT_SECONDARY)
        self.lbl_progresso_total.grid(row=4, column=0, columnspan=3, sticky='w', pady=(2, 5))
        
        # Separador
        ttk.Separator(header_frame, orient='horizontal').grid(row=5, column=0, columnspan=3, sticky='ew', pady=(5, 0))
    
    def criar_secao_controles(self, parent):
        """Cria seção de controles expandida."""
        # Frame principal dos controles
        controls_frame = ttk.LabelFrame(parent, text="⚙️ Controles", padding=15)
        controls_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        # Grid simples e flexível
        for i in range(7):
            controls_frame.grid_columnconfigure(i, weight=1, minsize=80)
        
        # === LINHA 1: Seleção ===
        # Novel
        ttk.Label(controls_frame, text="📖 Novel:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.combo_novel = ttk.Combobox(controls_frame, values=['Martial World'], 
                                        state='readonly', width=20)
        self.combo_novel.set('Martial World')
        self.combo_novel.grid(row=0, column=1, columnspan=2, sticky='ew', padx=(0, 15))
        # Configurar cores após criar
        self.combo_novel.configure(foreground=TemaEscuro.TEXT_PRIMARY)
        self.root.option_add('*TCombobox*Listbox.background', TemaEscuro.BG_SECUNDARIO)
        self.root.option_add('*TCombobox*Listbox.foreground', TemaEscuro.TEXT_PRIMARY)
        self.root.option_add('*TCombobox*Listbox.selectBackground', TemaEscuro.ACCENT_PRIMARY)
        self.root.option_add('*TCombobox*Listbox.selectForeground', TemaEscuro.BG_PRINCIPAL)
        
        # Voz
        ttk.Label(controls_frame, text="🎙️ Voz:").grid(row=0, column=3, sticky='w', padx=(0, 5))
        self.combo_voz = ttk.Combobox(controls_frame, 
                                      values=list(EngineNarracaoSimples.VOZES.keys()),
                                      state='readonly', width=15)
        self.combo_voz.set('Francisca')
        self.combo_voz.grid(row=0, column=4, columnspan=3, sticky='ew')
        # Configurar cores após criar
        self.combo_voz.configure(foreground=TemaEscuro.TEXT_PRIMARY)
        
        # === LINHA 2: Navegação ===
        # Capítulo
        ttk.Label(controls_frame, text="📑 Capítulo:").grid(row=1, column=0, sticky='w', 
                                                           padx=(0, 5), pady=(10, 0))
        cap_frame = ttk.Frame(controls_frame)
        cap_frame.grid(row=1, column=1, columnspan=2, sticky='ew', pady=(10, 0), padx=(0, 15))
        
        self.btn_cap_anterior = ttk.Button(cap_frame, text="◄◄", width=4,
                                          command=self.capitulo_anterior)
        self.btn_cap_anterior.pack(side='left', padx=(0, 5))
        
        self.spin_capitulo = ttk.Spinbox(cap_frame, from_=1, to=2266, width=10,
                                        command=self.on_capitulo_mudado)
        self.spin_capitulo.set('961')
        self.spin_capitulo.pack(side='left', padx=(0, 5))
        self.spin_capitulo.bind('<Return>', lambda e: self.on_capitulo_mudado())
        self.spin_capitulo.bind('<FocusOut>', lambda e: self.on_capitulo_mudado())
        
        self.btn_cap_proximo = ttk.Button(cap_frame, text="►►", width=4,
                                         command=self.capitulo_proximo)
        self.btn_cap_proximo.pack(side='left')
        
        # Parágrafo
        ttk.Label(controls_frame, text="📄 Parágrafo:").grid(row=1, column=3, sticky='w',
                                                            padx=(0, 5), pady=(10, 0))
        par_frame = ttk.Frame(controls_frame)
        par_frame.grid(row=1, column=4, columnspan=2, sticky='ew', pady=(10, 0), padx=(0, 5))
        
        self.btn_par_anterior = ttk.Button(par_frame, text="◄", width=4,
                                          command=self.paragrafo_anterior)
        self.btn_par_anterior.pack(side='left', padx=(0, 5))
        
        self.spin_paragrafo = ttk.Spinbox(par_frame, from_=1, to=999, width=10,
                                         command=self.on_paragrafo_mudado)
        self.spin_paragrafo.set('1')
        self.spin_paragrafo.pack(side='left', padx=(0, 5))
        self.spin_paragrafo.bind('<Return>', lambda e: self.on_paragrafo_mudado())
        self.spin_paragrafo.bind('<FocusOut>', lambda e: self.on_paragrafo_mudado())
        
        self.btn_par_proximo = ttk.Button(par_frame, text="►", width=4,
                                         command=self.paragrafo_proximo)
        self.btn_par_proximo.pack(side='left')
        
        # Barra de progresso do capítulo (linha própria)
        prog_frame = ttk.Frame(controls_frame)
        prog_frame.grid(row=1, column=6, sticky='ew', pady=(10, 0))
        
        ttk.Label(prog_frame, text="📊", font=('Segoe UI', 10)).pack(side='left', padx=(5, 2))
        self.progress_capitulo = ttk.Progressbar(prog_frame, length=100, mode='determinate')
        self.progress_capitulo.pack(side='left', fill='x', expand=True, padx=2)
        self.lbl_progress = ttk.Label(prog_frame, text="0%", width=4,
                                     foreground=TemaEscuro.ACCENT_PRIMARY,
                                     font=('Segoe UI', 9, 'bold'))
        self.lbl_progress.pack(side='left', padx=(2, 0))
        
        # === LINHA 3: Volumes ===
        # Volume Narração
        vol_nar_container = ttk.Frame(controls_frame)
        vol_nar_container.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(10, 0))
        
        self.lbl_icone_vol_nar = ttk.Label(vol_nar_container, text="🔊", font=('Segoe UI', 12))
        self.lbl_icone_vol_nar.pack(side='left', padx=(0, 3))
        
        ttk.Label(vol_nar_container, text="Narração:", font=('Segoe UI', 9)).pack(side='left', padx=(0, 3))
        
        vol_nar_frame = ttk.Frame(vol_nar_container)
        vol_nar_frame.pack(side='left', fill='x', expand=True)
        
        self.volume_narracao = ttk.Scale(vol_nar_frame, from_=0, to=100, orient='horizontal',
                                        command=self.ajustar_volume_narracao)
        self.volume_narracao.set(100)
        self.volume_narracao.pack(side='left', fill='x', expand=True)
        
        self.lbl_vol_narracao = ttk.Label(vol_nar_frame, text="100%", width=6,
                                         foreground=TemaEscuro.ACCENT_PRIMARY,
                                         font=('Segoe UI', 9, 'bold'))
        self.lbl_vol_narracao.pack(side='left', padx=(5, 0))
        
        # Volume Música
        vol_mus_container = ttk.Frame(controls_frame)
        vol_mus_container.grid(row=2, column=3, columnspan=4, sticky='ew', pady=(10, 0))
        
        self.lbl_icone_vol_mus = ttk.Label(vol_mus_container, text="🔊", font=('Segoe UI', 12))
        self.lbl_icone_vol_mus.pack(side='left', padx=(0, 3))
        
        ttk.Label(vol_mus_container, text="Música:", font=('Segoe UI', 9)).pack(side='left', padx=(0, 3))
        
        vol_mus_frame = ttk.Frame(vol_mus_container)
        vol_mus_frame.pack(side='left', fill='x', expand=True)
        
        self.volume_musica = ttk.Scale(vol_mus_frame, from_=0, to=100, orient='horizontal',
                                      command=self.ajustar_volume_musica)
        self.volume_musica.set(30)
        self.volume_musica.pack(side='left', fill='x', expand=True)
        
        self.lbl_vol_musica = ttk.Label(vol_mus_frame, text="30%", width=6,
                                       foreground=TemaEscuro.ACCENT_SECONDARY,
                                       font=('Segoe UI', 9, 'bold'))
        self.lbl_vol_musica.pack(side='left', padx=(5, 0))
        
        # === LINHA 4: Velocidade ===
        # Botões de velocidade fixa
        vel_btns_container = ttk.Frame(controls_frame)
        vel_btns_container.grid(row=3, column=0, columnspan=7, sticky='ew', pady=(10, 0))
        
        ttk.Label(vel_btns_container, text="⚡ Velocidade:", font=('Segoe UI', 9)).pack(side='left', padx=(0, 8))
        
        # Botões de velocidade pré-definidas
        velocidades = [
            ("0.5×", -50),
            ("1×", 0),
            ("1.25×", 12.5),
            ("1.5×", 25),
            ("2×", 50),
            ("3×", 100)
        ]
        
        for texto, valor in velocidades:
            btn = ttk.Button(vel_btns_container, text=texto, width=5,
                           command=lambda v=valor: self.definir_velocidade_fixa(v))
            btn.pack(side='left', padx=2)
        
        ttk.Separator(vel_btns_container, orient='vertical').pack(side='left', fill='y', padx=8)
        
        ttk.Label(vel_btns_container, text="Ajuste fino:", font=('Segoe UI', 8)).pack(side='left', padx=(0, 3))
        
        # Barra de ajuste fino
        vel_frame = ttk.Frame(vel_btns_container)
        vel_frame.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.velocidade_narracao = ttk.Scale(vel_frame, from_=-50, to=100, orient='horizontal',
                                            command=self.ajustar_velocidade_narracao)
        self.velocidade_narracao.set(0)
        self.velocidade_narracao.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        self.lbl_velocidade = ttk.Label(vel_frame, text="1.00×", width=6,
                                       foreground=TemaEscuro.ACCENT_WARNING,
                                       font=('Segoe UI', 9, 'bold'))
        self.lbl_velocidade.pack(side='left', padx=(5, 0))
        
        # === LINHA 5: Música ===
        musica_frame = ttk.Frame(controls_frame)
        musica_frame.grid(row=4, column=0, columnspan=7, sticky='ew', pady=(10, 0))
        
        ttk.Label(musica_frame, text="🎼", font=('Segoe UI', 10)).pack(side='left', padx=(0, 5))
        
        # Botão música normal
        ttk.Button(musica_frame, text="🎵", command=self.musica_normal,
                  width=4, style='Accent.TButton').pack(side='left', padx=(0, 8))
        ttk.Label(musica_frame, text="Leitura:", 
                 font=('Segoe UI', 10, 'bold'),
                 foreground=TemaEscuro.ACCENT_PRIMARY).pack(side='left', padx=(0, 5))
        
        # Combobox BGM Leitura - Maior e mais moderna
        self.combo_bgm_leitura = ttk.Combobox(musica_frame, values=[], 
                                              state='readonly', width=28,
                                              style='BGM.TCombobox')
        self.combo_bgm_leitura.pack(side='left', padx=(0, 15))
        self.combo_bgm_leitura.bind('<<ComboboxSelected>>', self.on_bgm_leitura_selecionada)
        
        # Botão música combate
        ttk.Button(musica_frame, text="⚔️", command=self.musica_combate,
                  width=4, style='Accent.TButton').pack(side='left', padx=(0, 8))
        ttk.Label(musica_frame, text="Combate:", 
                 font=('Segoe UI', 10, 'bold'),
                 foreground=TemaEscuro.ACCENT_DANGER).pack(side='left', padx=(0, 5))
        
        # Combobox BGM Combate - Maior e mais moderna
        self.combo_bgm_combate = ttk.Combobox(musica_frame, values=[], 
                                              state='readonly', width=28,
                                              style='BGM.TCombobox')
        self.combo_bgm_combate.pack(side='left', padx=(0, 15))
        self.combo_bgm_combate.bind('<<ComboboxSelected>>', self.on_bgm_combate_selecionada)
        
        # Botão mutar
        self.btn_mutar = ttk.Button(musica_frame, text="🔇",
                                    command=self.toggle_mutar, width=4)
        self.btn_mutar.pack(side='left', padx=(0, 5))
        ttk.Label(musica_frame, text="Mutar", 
                 font=('Segoe UI', 9)).pack(side='left', padx=0)
    
    def criar_area_visualizacao(self, parent):
        """Cria área de visualização do texto com highlight."""
        viz_frame = ttk.LabelFrame(parent, text="📖 Texto", padding=15)
        viz_frame.grid(row=2, column=0, sticky='nsew', pady=(0, 10))
        viz_frame.grid_rowconfigure(0, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)
        
        # Frame interno para texto e scrollbar
        text_container = ttk.Frame(viz_frame)
        text_container.grid(row=0, column=0, sticky='nsew')
        text_container.grid_rowconfigure(0, weight=1)
        text_container.grid_columnconfigure(0, weight=1)
        
        # Text widget com tema escuro
        self.text_paragrafo = tk.Text(text_container,
                                      wrap='word',
                                      font=('Segoe UI', 11),
                                      bg=TemaEscuro.BG_SECUNDARIO,
                                      fg=TemaEscuro.TEXT_PRIMARY,
                                      insertbackground=TemaEscuro.ACCENT_PRIMARY,
                                      selectbackground=TemaEscuro.ACCENT_PRIMARY,
                                      selectforeground=TemaEscuro.BG_PRINCIPAL,
                                      relief='flat',
                                      borderwidth=0,
                                      padx=15,
                                      pady=15,
                                      spacing1=5,
                                      spacing3=5,
                                      state='disabled')
        self.text_paragrafo.grid(row=0, column=0, sticky='nsew')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_container, command=self.text_paragrafo.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.text_paragrafo.config(yscrollcommand=scrollbar.set)
        
        # Permitir redimensionamento
        parent.grid_rowconfigure(2, weight=1)
        
        # Contador de tempo
        time_frame = ttk.Frame(viz_frame)
        time_frame.grid(row=1, column=0, sticky='ew', pady=(10, 0))
        
        self.lbl_tempo_narracao = ttk.Label(time_frame,
                                            text="⏱️ Tempo de narração: 00:00:00",
                                            font=('Segoe UI', 9),
                                            foreground=TemaEscuro.TEXT_SECONDARY)
        self.lbl_tempo_narracao.pack(side='left', padx=(0, 20))
        
        self.lbl_tempo_estimado = ttk.Label(time_frame,
                                            text="⏳ Tempo estimado: --:--",
                                            font=('Segoe UI', 9),
                                            foreground=TemaEscuro.TEXT_SECONDARY)
        self.lbl_tempo_estimado.pack(side='left')
    
    def criar_controles_playback(self, parent):
        """Cria controles de playback principais."""
        playback_frame = ttk.Frame(parent, padding=10)
        playback_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        
        # Centralizar botões
        btn_container = ttk.Frame(playback_frame)
        btn_container.pack(expand=True)
        
        # Botão Play/Pause (destaque maior)
        self.btn_play_pause = ttk.Button(btn_container,
                                        text="▶️  INICIAR NARRAÇÃO",
                                        command=self.toggle_narracao,
                                        style='Accent.TButton',
                                        width=30)
        self.btn_play_pause.pack(side='left', padx=5)
        
        # Botão Parar
        self.btn_stop = ttk.Button(btn_container,
                                   text="⏹️  Parar",
                                   command=self.parar_narracao_completa,
                                   style='Danger.TButton',
                                   width=15)
        self.btn_stop.pack(side='left', padx=5)
        self.criar_tooltip(self.btn_stop, "Para completamente a narração")
        
        # Botão Reiniciar Capítulo
        btn_reiniciar = ttk.Button(btn_container,
                                   text="🔄 Reiniciar Cap.",
                                   command=self.reiniciar_capitulo,
                                   width=15)
        btn_reiniciar.pack(side='left', padx=5)
        self.criar_tooltip(btn_reiniciar, "Volta ao início do capítulo atual")
    
    def criar_rodape(self, parent):
        """Cria rodapé com ações e informações."""
        footer_frame = ttk.Frame(parent)
        footer_frame.grid(row=4, column=0, sticky='ew')
        footer_frame.grid_columnconfigure(1, weight=1)
        
        # Botão Sair
        ttk.Button(footer_frame,
                  text="💾 Salvar e Sair",
                  command=self.sair,
                  style='Success.TButton',
                  width=20).grid(row=0, column=0, sticky='w')
        
        # Info de versão
        ttk.Label(footer_frame,
                 text="Novel Reader v2.0 - Tema Escuro Moderno",
                 font=('Segoe UI', 8),
                 foreground=TemaEscuro.TEXT_MUTED).grid(row=0, column=1, sticky='e')
    
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
                self.carregar_capitulo(novo_cap)
                self.paragrafo_atual = 1
                self.spin_paragrafo.set('1')
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
    
    def carregar_capitulos(self):
        """Carrega lista de capítulos disponíveis."""
        self.capitulos_disponiveis = self.leitor.listar_capitulos_disponiveis()
        if self.capitulos_disponiveis:
            self.spin_capitulo.config(from_=min(self.capitulos_disponiveis),
                                     to=max(self.capitulos_disponiveis))
    
    def atualizar_display(self, texto):
        """Atualiza o texto do parágrafo atual."""
        self.text_paragrafo.config(state='normal')
        self.text_paragrafo.delete('1.0', 'end')
        self.text_paragrafo.insert('1.0', texto)
        self.text_paragrafo.config(state='disabled')
    
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
        
        # Atualizar tempo estimado
        if self.narrando and total > 0:
            palavras_por_min = 150
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
    
    def precarregar_proximo_paragrafo(self):
        """Solicita pré-carregamento do próximo parágrafo."""
        if not self.engine or not self.conteudo_capitulo:
            return
        
        # Próximo parágrafo
        proximo_idx = self.paragrafo_atual  # paragrafo_atual é 1-based
        if 0 <= proximo_idx < len(self.conteudo_capitulo):
            texto_proximo = self.conteudo_capitulo[proximo_idx]
            self.engine.solicitar_precarregamento(texto_proximo)
    
    def carregar_capitulo(self, numero):
        """Carrega um capítulo."""
        capitulo = self.leitor.carregar_capitulo(numero)
        if capitulo:
            self.conteudo_capitulo = capitulo['conteudo']
            self.capitulo_atual = numero
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
                self.btn_play_pause.config(text="⏸️  PAUSAR")
                
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
                self.btn_play_pause.config(text="▶️  CONTINUAR")
            else:
                self.btn_play_pause.config(text="⏸️  PAUSAR")
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
        self.engine = EngineNarracaoSimples(voz, self.musica.canal_narrador)
        self.engine.set_volume(self.volume_narracao.get() / 100)
        self.engine.set_velocidade(int(self.velocidade_narracao.get()))
        
        # Pré-carregar apenas o primeiro parágrafo
        print("🔄 Pré-carregando parágrafo inicial...")
        if 1 <= self.paragrafo_atual <= len(self.conteudo_capitulo):
            self.engine.solicitar_precarregamento(self.conteudo_capitulo[self.paragrafo_atual - 1])
        time.sleep(0.5)  # Aguardar pré-carregamento do primeiro
        print("✓ Pronto para narrar")
        
        while self.narrando:
            # Verificar se terminou o capítulo
            if self.paragrafo_atual > len(self.conteudo_capitulo):
                # Ir para próximo capítulo automaticamente
                proximo_cap = self.capitulo_atual + 1
                if proximo_cap <= max(self.capitulos_disponiveis):
                    print(f"📖 Capítulo {self.capitulo_atual} concluído! Indo para capítulo {proximo_cap}...")
                    if self.carregar_capitulo(proximo_cap):
                        self.paragrafo_atual = 1
                        self.root.after(0, lambda: self.spin_capitulo.set(str(self.capitulo_atual)))
                        self.root.after(0, lambda: self.spin_paragrafo.set(str(self.paragrafo_atual)))
                        continue
                    else:
                        print("❌ Erro ao carregar próximo capítulo")
                        break
                else:
                    print("✅ Última página da novel! Narração concluída.")
                    break
            
            if not self.narrando:
                break
            
            # Parágrafo atual
            paragrafo = self.conteudo_capitulo[self.paragrafo_atual - 1]
            
            # Atualizar UI
            self.root.after(0, self.atualizar_display, paragrafo)
            self.root.after(0, self.atualizar_status)
            
            # ANTES de narrar, solicitar pré-carregamento do próximo
            self.precarregar_proximo_paragrafo()
            
            # Narrar com callback para verificar pausa (instantâneo com cache)
            self.engine.narrar(paragrafo, callback_pausado=lambda: self.pausado)
            
            # Próximo parágrafo (só se não pausou)
            if not self.pausado and self.narrando:
                self.paragrafo_atual += 1
                self.root.after(0, lambda p=self.paragrafo_atual: self.spin_paragrafo.set(str(p)))
        
        # Atualizar UI ao finalizar
        self.narrando = False
        self.pausado = False
        self.root.after(0, lambda: self.btn_play_pause.config(text="▶️ Iniciar Narração"))
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
            self.btn_play_pause.config(text="▶️ Iniciar Narração")
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
        """Ajusta velocidade da narração."""
        try:
            vel = float(valor)
            # Converter de porcentagem para multiplicador
            # -50 = 0.5x, 0 = 1.0x, 50 = 1.5x, 100 = 2.0x
            multiplicador = 1.0 + (vel / 100.0)
            if hasattr(self, 'lbl_velocidade'):
                self.lbl_velocidade.config(text=f"{multiplicador:.2f}×")
            if self.engine:
                self.engine.set_velocidade(int(vel))
        except Exception as e:
            print(f"Erro ao ajustar velocidade narração: {e}")
    
    def definir_velocidade_fixa(self, valor):
        """Define uma velocidade fixa pré-determinada."""
        try:
            self.velocidade_narracao.set(valor)
            self.ajustar_velocidade_narracao(valor)
        except Exception as e:
            print(f"Erro ao definir velocidade fixa: {e}")
    
    def musica_normal(self):
        """Ativa música normal."""
        self.musica.tocar_normal()
    
    def musica_combate(self):
        """Ativa música de combate."""
        self.musica.tocar_combate()
    
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
                    self.capitulo_atual = dados.get('capitulo', 961)
                    self.paragrafo_atual = dados.get('paragrafo', 1)
                    self.spin_capitulo.set(str(self.capitulo_atual))
                    self.spin_paragrafo.set(str(self.paragrafo_atual))
                    
                    # Carregar preferências
                    if 'voz' in dados:
                        self.combo_voz.set(dados['voz'])
                    if 'volume_narracao' in dados:
                        self.volume_narracao.set(dados['volume_narracao'])
                    if 'volume_musica' in dados:
                        self.volume_musica.set(dados['volume_musica'])
                    
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
        """Inicializa os comboboxes com as BGMs disponíveis."""
        leitura, combate = self.musica.obter_listas_bgms()
        
        # Configurar combobox de leitura
        if leitura:
            self.combo_bgm_leitura['values'] = leitura
            self.combo_bgm_leitura.set(leitura[0])
        
        # Configurar combobox de combate
        if combate:
            self.combo_bgm_combate['values'] = combate
            self.combo_bgm_combate.set(combate[0])
    
    def on_bgm_leitura_selecionada(self, event=None):
        """Callback quando usuário seleciona uma BGM de leitura."""
        bgm_selecionada = self.combo_bgm_leitura.get()
        self.musica.selecionar_bgm_leitura(bgm_selecionada)
    
    def on_bgm_combate_selecionada(self, event=None):
        """Callback quando usuário seleciona uma BGM de combate."""
        bgm_selecionada = self.combo_bgm_combate.get()
        self.musica.selecionar_bgm_combate(bgm_selecionada)
    
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


def main():
    root = tk.Tk()
    app = NovelReaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

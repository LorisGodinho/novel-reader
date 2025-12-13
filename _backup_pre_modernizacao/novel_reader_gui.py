"""
Novel Reader - Interface Gráfica
Sistema de narração com controles visuais e música de fundo
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

# Função para obter caminho base (funciona com PyInstaller)
def obter_caminho_base():
    """Retorna o caminho base, considerando se está executando como executável."""
    if getattr(sys, 'frozen', False):
        # Executando como executável PyInstaller
        return sys._MEIPASS
    else:
        # Executando como script Python
        return os.path.dirname(os.path.abspath(__file__))

# Adicionar paths
base_path = obter_caminho_base()
sys.path.insert(0, os.path.join(base_path, 'src'))
from leitor import LeitorNovel


class MusicaFundo:
    """Gerenciador de música de fundo."""
    
    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(8)
        self.canal_musica = pygame.mixer.Channel(0)
        self.canal_narrador = pygame.mixer.Channel(1)
        
        self.musica_normal = None
        self.musica_combate = None
        self.som_atual = None
        self.modo_atual = None
        self.volume_musica = 0.3
        self.mutado = False
        
    def carregar_musicas(self):
        """Carrega as músicas de fundo."""
        base_path = os.path.join(obter_caminho_base(), 'assets', 'audio', 'background')
        
        # Tentar MP3 primeiro, depois WAV de teste
        normal_paths = [
            os.path.join(base_path, 'ambient.mp3'),
            os.path.join(base_path, 'ambient_test.wav')
        ]
        combate_paths = [
            os.path.join(base_path, 'combat.mp3'),
            os.path.join(base_path, 'combat_test.wav')
        ]
        
        try:
            # Carregar música normal
            for path in normal_paths:
                if os.path.exists(path):
                    self.musica_normal = pygame.mixer.Sound(path)
                    print(f"✓ Música normal carregada: {os.path.basename(path)}")
                    break
            else:
                print(f"⚠️ Música normal não encontrada")
        
            # Carregar música combate
            for path in combate_paths:
                if os.path.exists(path):
                    self.musica_combate = pygame.mixer.Sound(path)
                    print(f"✓ Música combate carregada: {os.path.basename(path)}")
                    break
            else:
                print(f"⚠️ Música combate não encontrada")
        except Exception as e:
            print(f"❌ Erro ao carregar músicas: {e}")
    
    def tocar_normal(self):
        """Toca música ambiente normal."""
        if self.musica_normal:
            self.canal_musica.stop()
            self.som_atual = self.musica_normal
            self.som_atual.set_volume(0 if self.mutado else self.volume_musica)
            self.canal_musica.play(self.som_atual, loops=-1)
            self.modo_atual = 'normal'
            print(f"▶️ Tocando música normal (volume: {self.volume_musica:.2f})")
        else:
            print("❌ Música normal não disponível")
    
    def tocar_combate(self):
        """Toca música de combate."""
        if self.musica_combate:
            self.canal_musica.stop()
            self.som_atual = self.musica_combate
            self.som_atual.set_volume(0 if self.mutado else self.volume_musica)
            self.canal_musica.play(self.som_atual, loops=-1)
            self.modo_atual = 'combate'
            print(f"▶️ Tocando música combate (volume: {self.volume_musica:.2f})")
        else:
            print("❌ Música combate não disponível")
    
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
    """Engine simplificado sem emoções."""
    
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
        self.velocidade = 0  # -50% a +50% (Edge TTS rate)
        self.pausado = False
        self.som_atual = None
        
    async def _gerar_audio_async(self, texto: str):
        """Gera áudio usando Edge TTS."""
        # Rate: -50% a +50% (aceita de -100% a +100%, mas -50 a +50 é mais natural)
        rate = f"{self.velocidade:+d}%"
        temp_file = os.path.join(self.temp_dir, f'tts_{hash(texto)}_{self.velocidade}.mp3')
        
        # Evitar gerar novamente se já existe
        if os.path.exists(temp_file):
            return temp_file
            
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
    
    def narrar(self, texto: str, callback_pausado=None):
        """Narra texto simples com suporte a pausa."""
        if not texto.strip():
            return
        
        try:
            arquivo = asyncio.run(self._gerar_audio_async(texto))
            self.som_atual = pygame.mixer.Sound(arquivo)
            self.som_atual.set_volume(self.volume)
            self.canal.play(self.som_atual)
            
            while self.canal.get_busy() or self.pausado:
                if callback_pausado and callback_pausado():
                    if not self.pausado:
                        self.pausar()
                elif self.pausado:
                    self.despausar()
                time.sleep(0.05)
            
            try:
                os.remove(arquivo)
            except:
                pass
        except Exception as e:
            print(f"Erro ao narrar: {e}")


class NovelReaderGUI:
    """Interface gráfica do Novel Reader."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Novel Reader - Martial World")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Estado
        self.narrando = False
        self.pausado = False
        self.capitulo_atual = 961
        self.paragrafo_atual = 1
        self.capitulos_disponiveis = []
        self.conteudo_capitulo = []
        self.arquivo_progresso = os.path.join(obter_caminho_base(), 'config', 'progresso.json')
        self.mudanca_manual = False  # Flag para detectar mudança manual
        
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
        
        # Bind de foco
        self.root.bind('<FocusIn>', self.on_focus)
        self.root.bind('<FocusOut>', self.on_unfocus)
        self.tem_foco = True
    
    def criar_interface(self):
        """Cria todos os elementos da interface."""
        
        # Frame superior - Seleção
        frame_selecao = ttk.LabelFrame(self.root, text="Seleção", padding=10)
        frame_selecao.pack(fill='x', padx=10, pady=5)
        
        # Novel
        ttk.Label(frame_selecao, text="Novel:").grid(row=0, column=0, sticky='w')
        self.combo_novel = ttk.Combobox(frame_selecao, values=['Martial World'], state='readonly', width=30)
        self.combo_novel.set('Martial World')
        self.combo_novel.grid(row=0, column=1, padx=5)
        
        # Voz
        ttk.Label(frame_selecao, text="Voz:").grid(row=0, column=2, sticky='w', padx=(20,0))
        self.combo_voz = ttk.Combobox(frame_selecao, values=list(EngineNarracaoSimples.VOZES.keys()), 
                                       state='readonly', width=15)
        self.combo_voz.set('Francisca')
        self.combo_voz.grid(row=0, column=3, padx=5)
        
        # Capítulo
        ttk.Label(frame_selecao, text="Capítulo:").grid(row=1, column=0, sticky='w', pady=(10,0))
        self.spin_capitulo = ttk.Spinbox(frame_selecao, from_=1, to=2266, width=10, command=self.on_capitulo_mudado)
        self.spin_capitulo.set('961')
        self.spin_capitulo.grid(row=1, column=1, sticky='w', padx=5, pady=(10,0))
        self.spin_capitulo.bind('<Return>', lambda e: self.on_capitulo_mudado())
        self.spin_capitulo.bind('<FocusOut>', lambda e: self.on_capitulo_mudado())
        
        # Parágrafo
        ttk.Label(frame_selecao, text="Parágrafo:").grid(row=1, column=2, sticky='w', padx=(20,0), pady=(10,0))
        self.spin_paragrafo = ttk.Spinbox(frame_selecao, from_=1, to=999, width=10, command=self.on_paragrafo_mudado)
        self.spin_paragrafo.set('1')
        self.spin_paragrafo.grid(row=1, column=3, sticky='w', padx=5, pady=(10,0))
        self.spin_paragrafo.bind('<Return>', lambda e: self.on_paragrafo_mudado())
        self.spin_paragrafo.bind('<FocusOut>', lambda e: self.on_paragrafo_mudado())
        
        # Frame Volume
        frame_volume = ttk.LabelFrame(self.root, text="Volume", padding=10)
        frame_volume.pack(fill='x', padx=10, pady=5)
        
        # Volume Narração
        ttk.Label(frame_volume, text="🎙️ Narração:").grid(row=0, column=0, sticky='w', padx=5)
        self.volume_narracao = ttk.Scale(frame_volume, from_=0, to=100, orient='horizontal', length=200,
                                         command=self.ajustar_volume_narracao)
        self.volume_narracao.set(100)
        self.volume_narracao.grid(row=0, column=1, padx=5)
        self.lbl_vol_narracao = ttk.Label(frame_volume, text="100%", width=5)
        self.lbl_vol_narracao.grid(row=0, column=2, padx=5)
        
        # Volume Música
        ttk.Label(frame_volume, text="🎵 Música:").grid(row=1, column=0, sticky='w', padx=5, pady=(5,0))
        self.volume_musica = ttk.Scale(frame_volume, from_=0, to=100, orient='horizontal', length=200,
                                       command=self.ajustar_volume_musica)
        self.volume_musica.set(30)
        self.volume_musica.grid(row=1, column=1, padx=5, pady=(5,0))
        self.lbl_vol_musica = ttk.Label(frame_volume, text="30%", width=5)
        self.lbl_vol_musica.grid(row=1, column=2, padx=5, pady=(5,0))
        
        # Velocidade Narração
        ttk.Label(frame_volume, text="⚡ Velocidade:").grid(row=2, column=0, sticky='w', padx=5, pady=(5,0))
        self.velocidade_narracao = ttk.Scale(frame_volume, from_=-50, to=50, orient='horizontal', length=200,
                                             command=self.ajustar_velocidade_narracao)
        self.velocidade_narracao.set(0)
        self.velocidade_narracao.grid(row=2, column=1, padx=5, pady=(5,0))
        self.lbl_velocidade = ttk.Label(frame_volume, text="±0%", width=5)
        self.lbl_velocidade.grid(row=2, column=2, padx=5, pady=(5,0))
        
        # Frame controles de navegação
        frame_nav = ttk.LabelFrame(self.root, text="Navegação", padding=10)
        frame_nav.pack(fill='x', padx=10, pady=5)
        
        # Botões de capítulo
        ttk.Label(frame_nav, text="Capítulo:").grid(row=0, column=0, sticky='w')
        self.btn_cap_anterior = ttk.Button(frame_nav, text="◄◄ Anterior", command=self.capitulo_anterior, width=12)
        self.btn_cap_anterior.grid(row=0, column=1, padx=2)
        self.btn_cap_proximo = ttk.Button(frame_nav, text="Próximo ►►", command=self.capitulo_proximo, width=12)
        self.btn_cap_proximo.grid(row=0, column=2, padx=2)
        
        # Botões de parágrafo
        ttk.Label(frame_nav, text="Parágrafo:").grid(row=0, column=3, sticky='w', padx=(20,0))
        self.btn_par_anterior = ttk.Button(frame_nav, text="◄ Anterior", command=self.paragrafo_anterior, width=12)
        self.btn_par_anterior.grid(row=0, column=4, padx=2)
        self.btn_par_proximo = ttk.Button(frame_nav, text="Próximo ►", command=self.paragrafo_proximo, width=12)
        self.btn_par_proximo.grid(row=0, column=5, padx=2)
        
        # Frame controles principais
        frame_controles = ttk.Frame(self.root, padding=10)
        frame_controles.pack(fill='x', padx=10, pady=5)
        
        # Botões principais
        btn_frame = ttk.Frame(frame_controles)
        btn_frame.pack(pady=10)
        
        self.btn_play_pause = ttk.Button(btn_frame, text="▶ Iniciar Narração", 
                                         command=self.toggle_narracao, width=20)
        self.btn_play_pause.pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="💾 Sair", command=self.sair, width=10).pack(side='left', padx=5)
        
        # Frame música
        frame_musica = ttk.LabelFrame(self.root, text="Música de Fundo", padding=10)
        frame_musica.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_musica, text="🎵 Normal", command=self.musica_normal, width=12).pack(side='left', padx=2)
        ttk.Button(frame_musica, text="⚔️ Combate", command=self.musica_combate, width=12).pack(side='left', padx=2)
        self.btn_mutar = ttk.Button(frame_musica, text="🔇 Mutar Música", command=self.toggle_mutar, width=15)
        self.btn_mutar.pack(side='left', padx=2)
        
        # Frame status
        frame_status = ttk.LabelFrame(self.root, text="Status", padding=10)
        frame_status.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Labels de status
        self.lbl_status = ttk.Label(frame_status, text="Pronto para narrar", font=('Arial', 12, 'bold'))
        self.lbl_status.pack(pady=5)
        
        self.lbl_posicao = ttk.Label(frame_status, text="Capítulo: - | Parágrafo: -/-", font=('Arial', 10))
        self.lbl_posicao.pack(pady=5)
        
        # Text widget para mostrar parágrafo atual
        self.text_paragrafo = tk.Text(frame_status, height=10, width=90, wrap='word', 
                                       font=('Arial', 10), state='disabled')
        self.text_paragrafo.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.text_paragrafo)
        scrollbar.pack(side='right', fill='y')
        self.text_paragrafo.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_paragrafo.yview)
    
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
        self.lbl_posicao.config(text=f"Capítulo: {self.capitulo_atual} | Parágrafo: {self.paragrafo_atual}/{total}")
        
        if self.narrando:
            if self.pausado:
                self.lbl_status.config(text="⏸️ PAUSADO")
            else:
                self.lbl_status.config(text="▶️ NARRANDO")
        else:
            self.lbl_status.config(text="⏹️ Parado")
    
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
                self.btn_play_pause.config(text="⏸ Pausar")
                
                # Iniciar thread de narração
                self.thread_narracao = threading.Thread(target=self.loop_narracao, daemon=True)
                self.thread_narracao.start()
            else:
                messagebox.showerror("Erro", f"Capítulo {cap} não encontrado")
        else:
            # Pausar/despausar
            self.pausado = not self.pausado
            if self.pausado:
                self.btn_play_pause.config(text="▶ Continuar")
            else:
                self.btn_play_pause.config(text="⏸ Pausar")
            self.atualizar_status()
    
    def loop_narracao(self):
        """Loop principal de narração."""
        voz = self.combo_voz.get()
        self.engine = EngineNarracaoSimples(voz, self.musica.canal_narrador)
        self.engine.set_volume(self.volume_narracao.get() / 100)
        self.engine.set_velocidade(int(self.velocidade_narracao.get()))
        
        while self.narrando and self.paragrafo_atual <= len(self.conteudo_capitulo):
            if not self.narrando:
                break
            
            # Narrar parágrafo atual
            paragrafo = self.conteudo_capitulo[self.paragrafo_atual - 1]
            
            # Atualizar UI
            self.root.after(0, self.atualizar_display, paragrafo)
            self.root.after(0, self.atualizar_status)
            
            # Narrar com callback para verificar pausa
            self.engine.narrar(paragrafo, callback_pausado=lambda: self.pausado)
            
            # Próximo parágrafo (só se não pausou)
            if not self.pausado and self.narrando:
                self.paragrafo_atual += 1
                self.root.after(0, lambda: self.spin_paragrafo.set(str(self.paragrafo_atual)))
                # Pequena pausa entre parágrafos (reduzida de implícito para explícito)
                time.sleep(0.1)
        
        # Fim da narração
        self.narrando = False
        self.pausado = False
        self.root.after(0, lambda: self.btn_play_pause.config(text="▶ Iniciar Narração"))
        self.root.after(0, self.atualizar_status)
    
    def parar_narracao_completa(self):
        """Para a narração completamente."""
        if self.narrando:
            self.narrando = False
            self.pausado = False
            if self.engine:
                self.engine.parar()
            self.btn_play_pause.config(text="▶ Iniciar Narração")
            self.atualizar_status()
    
    def capitulo_anterior(self):
        """Vai para capítulo anterior."""
        self.parar_narracao_completa()
        if self.capitulo_atual > 1:
            self.carregar_capitulo(self.capitulo_atual - 1)
            self.paragrafo_atual = 1
            self.spin_paragrafo.set('1')
            self.atualizar_status()
    
    def capitulo_proximo(self):
        """Vai para próximo capítulo."""
        self.parar_narracao_completa()
        if self.capitulo_atual < 2266:
            self.carregar_capitulo(self.capitulo_atual + 1)
            self.paragrafo_atual = 1
            self.spin_paragrafo.set('1')
            self.atualizar_status()
    
    def paragrafo_anterior(self):
        """Vai para parágrafo anterior."""
        self.parar_narracao_completa()
        if self.paragrafo_atual > 1:
            self.paragrafo_atual -= 1
            self.spin_paragrafo.set(str(self.paragrafo_atual))
            if self.conteudo_capitulo:
                self.atualizar_display(self.conteudo_capitulo[self.paragrafo_atual - 1])
            self.atualizar_status()
    
    def paragrafo_proximo(self):
        """Vai para próximo parágrafo."""
        self.parar_narracao_completa()
        if self.conteudo_capitulo and self.paragrafo_atual < len(self.conteudo_capitulo):
            self.paragrafo_atual += 1
            self.spin_paragrafo.set(str(self.paragrafo_atual))
            self.atualizar_display(self.conteudo_capitulo[self.paragrafo_atual - 1])
            self.atualizar_status()
    
    def ajustar_volume_narracao(self, valor):
        """Ajusta volume da narração."""
        try:
            vol = float(valor) / 100
            self.lbl_vol_narracao.config(text=f"{int(float(valor))}%")
            if self.engine:
                self.engine.set_volume(vol)
        except Exception as e:
            print(f"Erro ao ajustar volume narração: {e}")
    
    def ajustar_volume_musica(self, valor):
        """Ajusta volume da música."""
        try:
            vol = float(valor) / 100
            self.lbl_vol_musica.config(text=f"{int(float(valor))}%")
            self.musica.set_volume(vol)
        except Exception as e:
            print(f"Erro ao ajustar volume música: {e}")
    
    def ajustar_velocidade_narracao(self, valor):
        """Ajusta velocidade da narração."""
        try:
            vel = int(float(valor))
            self.lbl_velocidade.config(text=f"{vel:+d}%")
            if self.engine:
                self.engine.set_velocidade(vel)
        except Exception as e:
            print(f"Erro ao ajustar velocidade narração: {e}")
    
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
            self.btn_mutar.config(text="🔊 Desmutar Música")
        else:
            self.btn_mutar.config(text="🔇 Mutar Música")
    
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
                'volume_musica': self.volume_musica.get()
            }
            with open(self.arquivo_progresso, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print(f"💾 Progresso salvo: Cap {self.capitulo_atual}, Par {self.paragrafo_atual}")
            return True
        except Exception as e:
            print(f"Erro ao salvar progresso: {e}")
            return False
    
    def sair(self):
        """Salva progresso e fecha aplicação."""
        self.parar_narracao_completa()
        self.musica.parar()
        
        if self.salvar_progresso():
            messagebox.showinfo("Novel Reader", 
                              f"Progresso salvo!\n\nCapítulo: {self.capitulo_atual}\nParágrafo: {self.paragrafo_atual}")
        
        self.root.destroy()


def main():
    root = tk.Tk()
    app = NovelReaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

"""
Motores de TTS do Novel Reader.

Cada voz do catálogo pertence a um motor:
- edge:       Microsoft Edge TTS (online, gratuito)
- piper:      Piper (offline, CPU, muito rápido)
- kokoro:     Kokoro-82M via ONNX (offline, CPU)
- chatterbox: Chatterbox Multilingual (offline, GPU) rodando num processo
              separado (.venv-chatterbox), clonando uma voz de referência

Todos os motores entregam um arquivo de áudio; a velocidade acima do que o
motor suporta nativamente é completada com ffmpeg (atempo).
"""

import os
import re
import sys
import json
import time
import wave
import atexit
import asyncio
import threading
import subprocess
import urllib.request
from dataclasses import dataclass
from collections import OrderedDict


# ===== Caminhos =====
def pasta_projeto() -> str:
    """Raiz do projeto (ou pasta do executável quando empacotado)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def pasta_modelos() -> str:
    return os.environ.get('NOVEL_READER_MODELOS') or os.path.join(pasta_projeto(), 'modelos_tts')


def pasta_referencias() -> str:
    """Áudios de referência (clonagem). Qualquer .wav colocado aqui vira uma voz GPU."""
    return os.path.join(pasta_modelos(), 'chatterbox', 'referencias')


def python_chatterbox() -> str:
    return os.environ.get('NOVEL_READER_CHATTERBOX_PYTHON') or os.path.join(
        pasta_projeto(), '.venv-chatterbox', 'Scripts', 'python.exe')


def _flags_sem_janela():
    return getattr(subprocess, 'CREATE_NO_WINDOW', 0) if os.name == 'nt' else 0


# ===== Catálogo de vozes =====
@dataclass(frozen=True)
class Voz:
    nome: str       # rótulo exibido na interface
    motor: str      # edge | piper | kokoro | chatterbox
    id: str         # id da voz no motor (para chatterbox: nome da referência)
    genero: str     # 'F' ou 'M'

    @property
    def offline(self) -> bool:
        return self.motor != 'edge'


# Vozes Edge usadas para gerar as referências automáticas do Chatterbox
REFERENCIAS_AUTOMATICAS = OrderedDict([
    ('Antonio', 'M'), ('Francisca', 'F'), ('Thalita', 'F'),
    ('Remy', 'M'), ('Vivienne', 'F'), ('Cadu · offline', 'M'), ('Dora · offline', 'F'),
])

TEXTO_REFERENCIA = (
    "Naquela noite, o vento soprava forte sobre as montanhas. "
    "Ele respirou fundo, olhou para o céu estrelado e sorriu. "
    "Você realmente acha que pode me deter? Então venha, estou esperando! "
    "A jornada ainda estava longe de terminar."
)


def _vozes_base():
    return [
        # Edge (online)
        Voz('Francisca', 'edge', 'pt-BR-FranciscaNeural', 'F'),
        Voz('Thalita', 'edge', 'pt-BR-ThalitaMultilingualNeural', 'F'),
        Voz('Antonio', 'edge', 'pt-BR-AntonioNeural', 'M'),
        Voz('Vivienne', 'edge', 'fr-FR-VivienneMultilingualNeural', 'F'),
        Voz('Remy', 'edge', 'fr-FR-RemyMultilingualNeural', 'M'),
        Voz('Raquel', 'edge', 'pt-PT-RaquelNeural', 'F'),
        Voz('Duarte', 'edge', 'pt-PT-DuarteNeural', 'M'),
        # Piper (offline). edresson-low ficou de fora: o modelo perde as nasais.
        Voz('Faber · offline', 'piper', 'pt_BR-faber-medium', 'M'),
        Voz('Cadu · offline', 'piper', 'pt_BR-cadu-medium', 'M'),
        Voz('Jeff · offline', 'piper', 'pt_BR-jeff-medium', 'M'),
        # Kokoro (offline)
        Voz('Dora · offline', 'kokoro', 'pf_dora', 'F'),
        Voz('Alex · offline', 'kokoro', 'pm_alex', 'M'),
        Voz('Santa · offline', 'kokoro', 'pm_santa', 'M'),
    ]


def _nome_clone(ref: str) -> str:
    return f"{ref.replace(' · offline', '')} · clone GPU"


def catalogo_vozes() -> 'OrderedDict[str, Voz]':
    """Todas as vozes disponíveis, na ordem de exibição."""
    vozes = OrderedDict((v.nome, v) for v in _vozes_base())
    if os.path.exists(python_chatterbox()):
        refs = OrderedDict(REFERENCIAS_AUTOMATICAS)
        # Referências extras colocadas pelo usuário na pasta
        if os.path.isdir(pasta_referencias()):
            for arq in sorted(os.listdir(pasta_referencias())):
                nome = os.path.splitext(arq)[0]
                if arq.lower().endswith('.wav') and nome not in refs:
                    refs[nome] = 'F' if nome.lower().endswith(('a', 'f')) else 'M'
        for ref, genero in refs.items():
            v = Voz(_nome_clone(ref), 'chatterbox', ref, genero)
            vozes[v.nome] = v
    return vozes


# ===== Downloads de modelos =====
_URL_PIPER = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/{n}/{q}/{arq}'
_URL_KOKORO = 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/{arq}'
_lock_download = threading.Lock()


def _baixar(url: str, destino: str):
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return destino
    with _lock_download:
        if os.path.exists(destino) and os.path.getsize(destino) > 0:
            return destino
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        print(f"⬇️ Baixando modelo de voz: {os.path.basename(destino)} ...")
        tmp = destino + '.part'
        urllib.request.urlretrieve(url, tmp)
        os.replace(tmp, destino)
        print(f"✓ Modelo baixado: {os.path.basename(destino)}")
    return destino


# ===== Motores =====
def _temporario(saida: str) -> str:
    """Arquivo temporário único por thread (prefetch e narração podem gerar o mesmo trecho)."""
    return f'{saida}.{threading.get_ident()}.part'


class MotorEdge:
    RATE_MAX = 1.5  # soa natural até ~1.5×

    def sintetizar(self, texto, voz, velocidade, saida):
        import edge_tts
        rate = f"{int(round((velocidade - 1.0) * 100)):+d}%"
        saida += '.mp3'
        if not os.path.exists(saida):
            tmp = _temporario(saida)
            asyncio.run(edge_tts.Communicate(texto, voz.id, rate=rate).save(tmp))
            os.replace(tmp, saida)
        return saida


class MotorPiper:
    RATE_MAX = 1.5

    def __init__(self):
        self._vozes = {}
        self._lock = threading.Lock()

    def _carregar(self, voz_id):
        if voz_id not in self._vozes:
            from piper import PiperVoice
            nome, qualidade = voz_id.split('-')[1], voz_id.split('-')[2]
            pasta = os.path.join(pasta_modelos(), 'piper')
            for ext in ('.onnx', '.onnx.json'):
                arq = voz_id + ext
                _baixar(_URL_PIPER.format(n=nome, q=qualidade, arq=arq), os.path.join(pasta, arq))
            self._vozes[voz_id] = PiperVoice.load(os.path.join(pasta, voz_id + '.onnx'))
        return self._vozes[voz_id]

    def sintetizar(self, texto, voz, velocidade, saida):
        from piper import SynthesisConfig
        saida += '.wav'
        if os.path.exists(saida):
            return saida
        tmp = _temporario(saida)
        with self._lock:
            pv = self._carregar(voz.id)
            with wave.open(tmp, 'wb') as wf:
                pv.synthesize_wav(texto, wf, syn_config=SynthesisConfig(length_scale=1.0 / velocidade))
        os.replace(tmp, saida)
        return saida


class MotorKokoro:
    RATE_MAX = 1.5
    MODELO = 'kokoro-v1.0.onnx'  # fp32: ~3× tempo real em CPU (o int8 é mais lento)
    VOZES = 'voices-v1.0.bin'

    def __init__(self):
        self._kokoro = None
        self._lock = threading.Lock()

    def sintetizar(self, texto, voz, velocidade, saida):
        import numpy as np
        saida += '.wav'
        if os.path.exists(saida):
            return saida
        with self._lock:
            if self._kokoro is None:
                from kokoro_onnx import Kokoro
                pasta = os.path.join(pasta_modelos(), 'kokoro')
                for arq in (self.MODELO, self.VOZES):
                    _baixar(_URL_KOKORO.format(arq=arq), os.path.join(pasta, arq))
                self._kokoro = Kokoro(os.path.join(pasta, self.MODELO), os.path.join(pasta, self.VOZES))
            amostras, sr = self._kokoro.create(texto, voice=voz.id, speed=velocidade, lang='pt-br')
        pcm = (np.clip(amostras, -1, 1) * 32767).astype('<i2')
        tmp = _temporario(saida)
        with wave.open(tmp, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(pcm.tobytes())
        os.replace(tmp, saida)
        return saida


class MotorChatterbox:
    """Cliente do worker Chatterbox (processo separado no .venv-chatterbox)."""
    RATE_MIN = RATE_MAX = 1.0  # sem controle nativo de velocidade: tudo via ffmpeg
    PORTA = 50931

    def __init__(self):
        self._proc = None
        self._lock = threading.Lock()
        self._lock_ref = threading.Lock()
        atexit.register(self.encerrar)

    def _url(self, rota):
        return f'http://127.0.0.1:{self.PORTA}{rota}'

    def _vivo(self):
        try:
            with urllib.request.urlopen(self._url('/saude'), timeout=2) as r:
                return r.status == 200
        except Exception:
            return False

    def _garantir_worker(self):
        if self._vivo():
            return
        py = python_chatterbox()
        if not os.path.exists(py):
            raise RuntimeError(f"Chatterbox não instalado ({py})")
        if self._proc is None or self._proc.poll() is not None:
            print("🚀 Iniciando Chatterbox na GPU (a primeira vez demora ~30s)...")
            script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chatterbox_worker.py')
            os.makedirs(os.path.join(pasta_modelos(), 'chatterbox'), exist_ok=True)
            log = open(os.path.join(pasta_modelos(), 'chatterbox', 'worker.log'), 'w', encoding='utf-8')
            env = dict(os.environ, TQDM_DISABLE='1', PYTHONIOENCODING='utf-8')
            self._proc = subprocess.Popen([py, script, '--porta', str(self.PORTA)],
                                          stdout=log, stderr=subprocess.STDOUT, env=env,
                                          creationflags=_flags_sem_janela())
        limite = time.time() + 300
        while time.time() < limite:
            if self._proc.poll() is not None:
                raise RuntimeError("Worker do Chatterbox encerrou; veja modelos_tts/chatterbox/worker.log")
            if self._vivo():
                print("✓ Chatterbox pronto")
                return
            time.sleep(1)
        raise RuntimeError("Chatterbox não respondeu a tempo")

    def _referencia(self, voz):
        ref = os.path.join(pasta_referencias(), voz.id + '.wav')
        with self._lock_ref:
            if not os.path.exists(ref):
                gerar_referencia(voz.id, ref)
        return ref

    def sintetizar(self, texto, voz, velocidade, saida, expressividade=0.5):
        saida += '.wav'
        if os.path.exists(saida):
            return saida
        os.makedirs(pasta_referencias(), exist_ok=True)
        ref = self._referencia(voz)
        with self._lock:
            self._garantir_worker()
            corpo = json.dumps({'texto': texto, 'referencia': ref, 'saida': saida,
                                'expressividade': expressividade}).encode('utf-8')
            req = urllib.request.Request(self._url('/tts'), data=corpo,
                                         headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=600) as r:
                resp = json.loads(r.read().decode('utf-8'))
        if not resp.get('ok'):
            raise RuntimeError(f"Chatterbox: {resp.get('erro')}")
        return saida

    def encerrar(self):
        if self._proc and self._proc.poll() is None:
            self._proc.terminate()


MOTORES = {
    'edge': MotorEdge(),
    'piper': MotorPiper(),
    'kokoro': MotorKokoro(),
    'chatterbox': MotorChatterbox(),
}


def gerar_referencia(nome_voz_origem: str, destino: str):
    """Gera um áudio de referência (~12s) com uma voz do catálogo, para clonagem."""
    origem = OrderedDict((v.nome, v) for v in _vozes_base()).get(nome_voz_origem)
    if origem is None:
        raise RuntimeError(f"Referência '{nome_voz_origem}' não existe (coloque um .wav em {pasta_referencias()})")
    print(f"🎤 Gerando referência de voz para clonagem: {nome_voz_origem}")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    base = os.path.splitext(destino)[0] + '_origem'
    arq = MOTORES[origem.motor].sintetizar(TEXTO_REFERENCIA, origem, 1.0, base)
    converter(arq, destino, extra=['-ar', '24000', '-ac', '1'])
    os.remove(arq)


# ===== Diálogos =====
_RE_DIALOGO = re.compile(r'(“[^”]*(?:”|$)|"[^"]*(?:"|$)|«[^»]*(?:»|$))')


def dividir_dialogos(texto: str):
    """Divide o parágrafo em [(eh_dialogo, trecho), ...] pelas aspas."""
    partes = []
    for i, trecho in enumerate(_RE_DIALOGO.split(texto)):
        if trecho and re.search(r'\w', trecho):
            partes.append((i % 2 == 1, trecho.strip()))
    return partes


# ===== ffmpeg =====
_ffmpeg = None


def ffmpeg() -> str:
    global _ffmpeg
    if _ffmpeg is None:
        candidatos = [os.path.join(getattr(sys, '_MEIPASS', pasta_projeto()), 'ffmpeg.exe'),
                      os.path.join(pasta_projeto(), 'ffmpeg.exe')]
        _ffmpeg = next((c for c in candidatos if os.path.exists(c)), None)
        if _ffmpeg is None:
            import shutil
            _ffmpeg = shutil.which('ffmpeg') or 'ffmpeg'
    return _ffmpeg


def cadeia_atempo(fator: float) -> str:
    """atempo aceita 0.5–2.0 por filtro; encadeia para fatores maiores."""
    filtros = []
    while fator > 2.0:
        filtros.append('atempo=2.0')
        fator /= 2.0
    filtros.append(f'atempo={fator:.4f}')
    return ','.join(filtros)


def converter(entrada: str, saida: str, extra=None):
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', '-i', entrada, *(extra or []), saida],
                   check=True, creationflags=_flags_sem_janela(), timeout=60)


def juntar_e_acelerar(segmentos, saida: str) -> str:
    """Concatena [(arquivo, fator_residual), ...] aplicando atempo em cada um."""
    if len(segmentos) == 1 and abs(segmentos[0][1] - 1.0) <= 0.001:
        return segmentos[0][0]
    entradas, rotulos = [], []
    for i, (arq, fator) in enumerate(segmentos):
        entradas += ['-i', arq]
        f = f'[{i}:a]aresample=24000,aformat=sample_fmts=s16:channel_layouts=mono'
        if abs(fator - 1.0) > 0.001:
            f += ',' + cadeia_atempo(fator)
        rotulos.append(f + f'[a{i}]')
    filtro = ';'.join(rotulos) + ';' + ''.join(f'[a{i}]' for i in range(len(segmentos)))
    filtro += f'concat=n={len(segmentos)}:v=0:a=1[out]'
    subprocess.run([ffmpeg(), '-y', '-loglevel', 'error', *entradas, '-filter_complex', filtro,
                    '-map', '[out]', saida],
                   check=True, creationflags=_flags_sem_janela(), timeout=120)
    return saida


# ===== Síntese de um parágrafo =====
FALLBACK_OFFLINE = {'F': 'Dora · offline', 'M': 'Faber · offline'}


class Sintetizador:
    """Gera o áudio de um parágrafo: separa narração/diálogo, escolhe o motor de
    cada trecho, ajusta velocidade e cai para uma voz offline se o motor falhar."""

    PAUSA_EDGE_FALHOU = 60  # s sem tentar o Edge depois de uma falha de rede

    def __init__(self, temp_dir: str):
        self.temp_dir = os.path.join(temp_dir, 'novel_reader_tts')
        os.makedirs(self.temp_dir, exist_ok=True)
        self.vozes = catalogo_vozes()
        self._edge_off_ate = 0.0

    def _arquivo(self, *partes) -> str:
        import hashlib
        h = hashlib.md5('|'.join(map(str, partes)).encode('utf-8')).hexdigest()
        return os.path.join(self.temp_dir, h)

    def _sintetizar_trecho(self, texto, voz: Voz, mult: float, dialogo: bool):
        """Retorna (arquivo, fator_residual). Tenta a voz pedida e depois o fallback."""
        tentativas = [voz]
        reserva = self.vozes.get(FALLBACK_OFFLINE[voz.genero])
        if reserva and reserva != voz:
            tentativas.append(reserva)
        erro = None
        for v in tentativas:
            if v.motor == 'edge' and time.time() < self._edge_off_ate:
                continue
            motor = MOTORES[v.motor]
            rate_min = getattr(motor, 'RATE_MIN', 0.5)
            nativo = max(rate_min, min(mult, motor.RATE_MAX))
            base = self._arquivo(v.nome, f'{nativo:.2f}', dialogo, texto)
            try:
                if v.motor == 'chatterbox':
                    arq = motor.sintetizar(texto, v, nativo, base, expressividade=0.65 if dialogo else 0.5)
                else:
                    arq = motor.sintetizar(texto, v, nativo, base)
                if v is not voz:
                    print(f"⚠️ {voz.nome} indisponível ({erro or 'sem conexão'}); usando {v.nome}")
                return arq, mult / nativo
            except Exception as e:
                erro = e
                if v.motor == 'edge' and type(e).__name__ != 'NoAudioReceived':
                    self._edge_off_ate = time.time() + self.PAUSA_EDGE_FALHOU
        raise RuntimeError(f"Falha ao sintetizar com {voz.nome}: {erro}")

    def gerar(self, texto: str, voz: str, voz_dialogo: str, mult: float) -> str:
        v_narr = self.vozes.get(voz) or self.vozes['Francisca']
        v_dial = self.vozes.get(voz_dialogo) if voz_dialogo else None
        if v_dial and v_dial != v_narr:
            trechos = [(d, t, v_dial if d else v_narr) for d, t in dividir_dialogos(texto)]
        else:
            trechos = []
        if not trechos:
            trechos = [(False, texto, v_narr)]
        if len(trechos) == 1:
            segmentos = [self._sintetizar_trecho(trechos[0][1], trechos[0][2], mult, trechos[0][0])]
        else:
            # Trechos em paralelo (Edge é limitado pela rede; motores locais têm lock próprio)
            from concurrent.futures import ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=4) as pool:
                segmentos = list(pool.map(lambda x: self._sintetizar_trecho(x[1], x[2], mult, x[0]), trechos))
        saida = self._arquivo('final', v_narr.nome, v_dial.nome if v_dial else '', f'{mult:.2f}', texto) + '.wav'
        if os.path.exists(saida):
            return saida
        return juntar_e_acelerar(segmentos, saida)

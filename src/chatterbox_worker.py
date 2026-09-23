"""
Worker do Chatterbox Multilingual (roda no .venv-chatterbox, com PyTorch CUDA).

O app principal inicia este processo sob demanda e conversa com ele via HTTP
local (127.0.0.1). Mantê-lo separado evita conflito de dependências
(chatterbox exige numpy<2; o app usa numpy 2).

POST /tts  {texto, referencia, saida, expressividade} -> {ok, caminho}
GET  /saude
"""

import os
import re
import sys
import json
import argparse
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import torch
import numpy as np
import soundfile as sf
from chatterbox.mtl_tts import ChatterboxMultilingualTTS

MAX_CHARS = 280  # o modelo gera no máximo ~40s por chamada; frases longas são divididas
PAUSA_ENTRE_FRASES = 0.12  # s

modelo = None
lock = threading.Lock()
conds_cache = {}  # {(referencia, expressividade): Conditionals}


def dividir_frases(texto: str):
    frases = re.split(r'(?<=[.!?…])\s+', texto.strip())
    blocos, atual = [], ''
    for f in frases:
        if len(atual) + len(f) + 1 <= MAX_CHARS:
            atual = f'{atual} {f}'.strip()
        else:
            if atual:
                blocos.append(atual)
            # frase isolada maior que o limite: quebra em vírgulas/espaços
            while len(f) > MAX_CHARS:
                corte = max(f.rfind(',', 0, MAX_CHARS), f.rfind(' ', 0, MAX_CHARS))
                corte = corte if corte > 0 else MAX_CHARS
                blocos.append(f[:corte + 1].strip())
                f = f[corte + 1:].strip()
            atual = f
    if atual:
        blocos.append(atual)
    return [b for b in blocos if re.search(r'\w', b)]


def sintetizar(texto, referencia, saida, expressividade):
    chave = (referencia, round(float(expressividade), 2))
    with lock:
        if chave not in conds_cache:
            modelo.prepare_conditionals(referencia, exaggeration=expressividade)
            conds_cache[chave] = modelo.conds
        modelo.conds = conds_cache[chave]
        partes = []
        silencio = np.zeros(int(modelo.sr * PAUSA_ENTRE_FRASES), dtype=np.float32)
        for bloco in dividir_frases(texto) or [texto]:
            wav = modelo.generate(bloco, language_id='pt', exaggeration=expressividade)
            partes += [wav.squeeze(0).numpy().astype(np.float32), silencio]
    audio = np.concatenate(partes[:-1]) if partes else silencio
    sf.write(saida + '.part.wav', audio, modelo.sr)
    os.replace(saida + '.part.wav', saida)
    return saida


class Handler(BaseHTTPRequestHandler):
    def _responder(self, codigo, dados):
        corpo = json.dumps(dados).encode('utf-8')
        self.send_response(codigo)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        if self.path == '/saude':
            self._responder(200, {'ok': True, 'gpu': torch.cuda.get_device_name(0) if torch.cuda.is_available() else None})
        else:
            self._responder(404, {'ok': False})

    def do_POST(self):
        if self.path != '/tts':
            return self._responder(404, {'ok': False})
        try:
            req = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
            caminho = sintetizar(req['texto'], req['referencia'], req['saida'],
                                 float(req.get('expressividade', 0.5)))
            self._responder(200, {'ok': True, 'caminho': caminho})
        except Exception as e:
            print(f"Erro: {e!r}", flush=True)
            self._responder(500, {'ok': False, 'erro': repr(e)})

    def log_message(self, *args):
        pass


def main():
    global modelo
    ap = argparse.ArgumentParser()
    ap.add_argument('--porta', type=int, default=50931)
    args = ap.parse_args()
    dispositivo = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Carregando Chatterbox Multilingual em {dispositivo}...", flush=True)
    modelo = ChatterboxMultilingualTTS.from_pretrained(device=dispositivo)
    print("Pronto.", flush=True)
    ThreadingHTTPServer(('127.0.0.1', args.porta), Handler).serve_forever()


if __name__ == '__main__':
    sys.exit(main())

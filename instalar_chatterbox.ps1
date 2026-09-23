# Instala o Chatterbox Multilingual (vozes clonadas na GPU) num ambiente separado.
# Uso: powershell -ExecutionPolicy Bypass -File instalar_chatterbox.ps1
#
# Por que separado: o chatterbox-tts exige numpy<2 e torch==2.6, e o app usa
# numpy 2. Além disso, placas RTX 50xx precisam do PyTorch com CUDA 12.8 (2.7+).
# Download total: ~3 GB (PyTorch) + ~3 GB (modelo, baixado no primeiro uso).

$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
$venv = Join-Path $raiz '.venv-chatterbox'
$py = Join-Path $venv 'Scripts\python.exe'

if (-not (Test-Path $py)) {
    Write-Host 'Criando .venv-chatterbox...'
    py -3.12 -m venv $venv
}

& $py -m pip install -U pip
& $py -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
# --no-deps: evita que o pip troque o torch CUDA pelo torch 2.6 fixado no pacote
& $py -m pip install chatterbox-tts --no-deps
& $py -m pip install 'numpy<2' librosa==0.11.0 s3tokenizer transformers==5.2.0 diffusers==0.29.0 `
    'resemble-perth>=1.0.0' conformer==0.3.2 safetensors==0.5.3 spacy-pkuseg pykakasi==2.3.0 `
    pyloudnorm omegaconf soundfile

& $py -c "import torch; print('CUDA:', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')"
Write-Host 'Pronto. Reabra o Novel Reader: as vozes "clone GPU" aparecem no seletor.'

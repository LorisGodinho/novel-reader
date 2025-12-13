# Instruções para Download Manual

O script automático pode ter problemas com ffmpeg. Aqui está como baixar manualmente:

## Opção 1: Usar Site Online

### 1. Ir para um conversor YouTube to MP3:
- https://ytmp3.nu/
- https://notube.io/
- https://y2mate.com/

### 2. Colar os URLs e baixar:

**Música Ambiente (Normal):**
- URL: https://www.youtube.com/watch?v=1xhK_zVZvBU
- Salvar como: `ambient.mp3`

**Música Combate:**
- URL: https://youtu.be/xDuCccDiQQM
- Salvar como: `combat.mp3`

### 3. Mover arquivos para:
```
C:\Users\loris\Desktop\novel_reader\assets\audio\background\
```

## Opção 2: Continuar Script Automático

Se o script estava funcionando, apenas aguarde. Ele pode demorar alguns minutos para:
1. Baixar o áudio
2. Converter com ffmpeg
3. Salvar como MP3

Execute novamente se necessário:
```bash
.venv\Scripts\python baixar_musicas.py
```

## Verificar se Funcionou

```bash
cd C:\Users\loris\Desktop\novel_reader
dir assets\audio\background\*.mp3
```

Deve mostrar:
- `ambient.mp3`
- `combat.mp3`

## Testar

Depois que os arquivos estiverem no lugar:
```bash
.venv\Scripts\python novel_reader_gui.py
```

Clique nos botões "🎵 Normal" e "⚔️ Combate" para testar!

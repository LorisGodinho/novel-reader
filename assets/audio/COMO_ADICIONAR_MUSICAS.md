# Como Adicionar Músicas de Background

## Opções para BGMs de Qualidade

### 1. Fontes de Música Livre de Copyright

**Sites Recomendados:**
- **YouTube Audio Library** - https://studio.youtube.com/channel/UCg-vlUFxfAKc1JJuNJfK1oA/music
- **Free Music Archive** - https://freemusicarchive.org/
- **Incompetech** - https://incompetech.com/
- **Purple Planet** - https://www.purple-planet.com/
- **Bensound** - https://www.bensound.com/

### 2. Requisitos para BGM em Loop Perfeito

Para que a música faça loop sem interrupções:

1. **Equalização Constante**: Volume consistente do início ao fim
2. **Fade In/Out**: Transição suave no início (2s) e fim (2s)
3. **Normalização**: Volume normalizado para -16 LUFS
4. **Duração**: 3-4 minutos para variedade sem repetição excessiva

### 3. Estrutura de Pastas

```
assets/audio/background/
├── combat_*.mp3      # BGMs para cenas de combate
├── reading_*.mp3     # BGMs para leitura tranquila
└── ambient_*.mp3     # BGMs ambiente genéricas
```

### 4. Processamento Manual com FFmpeg

Se você baixou uma música e quer processar manualmente:

```powershell
# Cortar trecho, normalizar e adicionar fades
.\ffmpeg.exe -i "musica_original.mp3" ^
  -ss 30 -t 180 ^
  -af "volume=1.5,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=in:st=0:d=2,afade=t=out:st=178:d=2" ^
  -b:a 192k ^
  "assets/audio/background/combat_epic.mp3"
```

**Parâmetros:**
- `-ss 30`: Começa em 30 segundos
- `-t 180`: Duração de 3 minutos
- `volume=1.5`: Aumenta volume em 50%
- `loudnorm`: Normaliza para -16 LUFS
- `afade`: Fade in de 2s no início e fade out de 2s no fim
- `-b:a 192k`: Qualidade de áudio 192kbps

### 5. Músicas Recomendadas para Xianxia/Cultivation

**Buscar por:**
- "chinese traditional music instrumental"
- "wuxia background music"
- "meditation ambient music"
- "epic battle music no copyright"
- "martial arts soundtrack"

**Características ideais:**
- **Combate**: Ritmo acelerado, percussão forte, cordas dramáticas
- **Leitura**: Instrumentos tradicionais chineses (guzheng, erhu), ritmo calmo

### 6. Script Automático

Use o script `baixar_musicas.py` que já processa automaticamente:
```powershell
python baixar_musicas.py
```

O script:
- ✅ Baixa do YouTube
- ✅ Corta o melhor trecho
- ✅ Normaliza o volume
- ✅ Adiciona fade in/out
- ✅ Converte para MP3 192kbps

### 7. Teste a Qualidade do Loop

Depois de adicionar uma música, teste no aplicativo:
1. Abra o Novel Reader
2. Vá para Configurações > Áudio
3. Selecione a BGM
4. Ative "Loop" e teste por alguns minutos
5. Verifique se não há picos/quedas de volume na transição

## Dicas Importantes

⚠️ **Sempre use música sem copyright** para distribuição pública
✅ **Verifique a licença** antes de usar qualquer música
🎵 **Teste o loop** várias vezes antes de finalizar
📊 **Mantenha volume consistente** entre diferentes BGMs

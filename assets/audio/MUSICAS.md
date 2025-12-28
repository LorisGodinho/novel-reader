# BGMs Disponíveis no Novel Reader

## 📋 BGMs Incluídas (6 faixas)

O projeto conta com **6 BGMs equalizadas** para loop perfeito, todas processadas profissionalmente.

### ⚔️ BGMs de Combate (3)
- `combat_battle_1.mp3` (4.12 MB) - Épica e dramática
- `combat_battle_3.mp3` (4.12 MB) - Intensa e energética  
- `combat_synthetic_2.mp3` (4.12 MB) - Sintética com tons graves profundos

### 📖 BGMs de Leitura (3)
- `reading_chinese_1.mp3` (5.49 MB) - Música chinesa tradicional
- `reading_synthetic_2.mp3` (5.49 MB) - Tons harmônicos suaves
- `reading_synthetic_3.mp3` (5.49 MB) - Ambiente contemplativo

**Total**: ~33 MB de áudio de alta qualidade

## ✨ Características Técnicas

Todas as BGMs foram processadas com:

- ✅ **Equalização constante**: Volume consistente do início ao fim (sem picos/vales)
- ✅ **Fade in/out**: 2 segundos de transição suave para loop perfeito
- ✅ **Normalização**: -16 LUFS (combate) / -20 LUFS (leitura)
- ✅ **Qualidade**: MP3 192kbps
- ✅ **Loop perfeito**: Sem interrupções audíveis na transição

## 🎵 Como Foram Criadas

### BGMs do YouTube
- Baixadas de fontes sem copyright usando `yt-dlp`
- Cortado o melhor trecho equalizado (3-4 minutos)
- Processadas com FFmpeg: normalização, fade, equalização

### BGMs Sintéticas
- Criadas com Python (numpy + scipy)
- Tons harmônicos cuidadosamente escolhidos
- Frequências otimizadas para cada categoria

## 📝 Scripts Disponíveis

### 1. Baixar do YouTube
```powershell
python baixar_musicas.py
```
Baixa e processa BGMs do YouTube automaticamente.

### 2. Criar Sintéticas
```powershell
python criar_bgms_sinteticas.py
```
Gera BGMs sintéticas de alta qualidade.

## 🎮 Uso no Aplicativo

As BGMs são detectadas automaticamente pelo Novel Reader:
- **Combate**: Busca arquivos `combat_*.mp3`
- **Leitura**: Busca arquivos `reading_*.mp3`

## 🔧 Como Adicionar Mais BGMs

Veja o guia completo em [COMO_ADICIONAR_MUSICAS.md](COMO_ADICIONAR_MUSICAS.md)

## Sites de Música Livre (Referência)

✅ **YouTube Audio Library** - Sem copyright
✅ **Pixabay Music** - CC0, uso comercial permitido
✅ **Free Music Archive** - Creative Commons
✅ **Incompetech** - Creative Commons com atribuição
✅ **YouTube Audio Library** - Gratuito para uso

## Alternativa Rápida

Se não quiser baixar agora, o sistema funciona sem as músicas. Os botões simplesmente não terão efeito até você adicionar os arquivos.

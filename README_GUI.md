# Novel Reader GUI - v2.0

Sistema de narração com interface gráfica completa.

## 🎯 Características

- ✅ Interface gráfica com tkinter
- ✅ Controles visuais por botões
- ✅ Sistema simplificado (sem emoções)
- ✅ Música de fundo (ambiente/combate)
- ✅ Controles só funcionam com janela em foco
- ✅ Pausa e continua do mesmo parágrafo
- ✅ Navegação por capítulos e parágrafos
- ✅ 5 vozes Microsoft Edge TTS gratuitas

## 🚀 Como Usar

### Iniciar o Sistema

```bash
cd C:\Users\loris\Desktop\novel_reader
.venv\Scripts\python novel_reader_gui.py
```

### Interface

**Seleção:**
- Novel: Martial World
- Voz: 5 opções (Francisca padrão)
- Capítulo: Escolher número
- Parágrafo: Escolher número inicial

**Navegação:**
- `◄◄ Anterior / Próximo ►►` - Navega entre capítulos
- `◄ Anterior / Próximo ►` - Navega entre parágrafos

**Controles Principais:**
- `▶ Iniciar Narração` - Começa a narrar
- `⏸ Pausar` - Pausa no parágrafo atual
- `▶ Continuar` - Continua do mesmo parágrafo

**Música de Fundo:**
- `🎵 Normal` - Música ambiente tranquila
- `⚔️ Combate` - Música tensa de ação
- `🔇 Mutar / 🔊 Desmutar` - Liga/desliga música

**Status:**
- Mostra posição atual (cap/par)
- Exibe parágrafo sendo narrado
- Indicadores visuais de estado

## 🎵 Configurar Músicas

1. Baixe músicas royalty-free de:
   - Pixabay Music
   - Free Music Archive
   - Incompetech
   - YouTube Audio Library

2. Salve como:
   - `assets/audio/background/ambient.mp3` (música calma)
   - `assets/audio/background/combat.mp3` (música ação)

Veja `assets/audio/MUSICAS.md` para links e instruções.

## 🎮 Controles

### Teclado (quando janela em foco)
Os controles de teclado foram removidos. Use os botões da interface.

### Mouse
Todos os controles são clicáveis:
- Botões de navegação
- Seleção de capítulo/parágrafo (spinbox)
- Play/Pause
- Música

## 📋 Diferenças da Versão Anterior

### Removido:
- ❌ Sistema de emoções
- ❌ Tags de texto ([grito], [sussurro], etc)
- ❌ Controles de teclado (ESPAÇO, setas)
- ❌ Interface terminal

### Adicionado:
- ✅ Interface gráfica completa
- ✅ Música de fundo dinâmica
- ✅ Controles visuais
- ✅ Display do parágrafo atual
- ✅ Navegação rápida
- ✅ Foco da janela necessário

### Melhorado:
- ✅ Pausa/retoma no parágrafo correto
- ✅ Navegação mais precisa
- ✅ Feedback visual imediato
- ✅ Sem bugs de paralelismo

## 🔧 Troubleshooting

**Música não toca:**
- Verifique se os arquivos MP3 estão em `assets/audio/background/`
- Nomes corretos: `ambient.mp3` e `combat.mp3`

**Controles não funcionam:**
- Certifique-se que a janela está em foco (clique nela)
- Os controles são desabilitados quando perde o foco

**Voz não carrega:**
- Verifique conexão com internet (Edge TTS precisa)
- Aguarde alguns segundos no primeiro uso

## 💾 Backups

- `_backup_v1_terminal/` - Versão terminal com controles de teclado
- `_backup_working/` - Código original funcional

Para voltar à versão terminal, copie arquivos de `_backup_v1_terminal/`.

## 📦 Dependências

- edge-tts 7.2.6
- pygame 2.6.1  
- pillow 10.x (para futura expansão)
- tkinter (incluído no Python)

## 🎬 Uso Típico

1. Abrir `novel_reader_gui.py`
2. Selecionar capítulo inicial (ex: 961)
3. Clicar "▶ Iniciar Narração"
4. Opcionalmente ativar música (🎵 Normal)
5. Usar botões para navegar durante narração
6. Clicar "⏸ Pausar" quando necessário
7. Continua exatamente de onde parou

Aproveite sua leitura de Martial World! 📖🎧

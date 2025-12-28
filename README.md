# 📚 Novel Reader - Sistema de Narração Inteligente

Sistema avançado de leitura e narração de novels com interface gráfica moderna, TTS usando Microsoft Edge Neural Voices, música de fundo adaptativa e controles intuitivos.

## ✨ Características Principais

### 🎨 Interface Gráfica Moderna
- **Tema Escuro** inspirado em Catppuccin Mocha
- **Interface Redimensionável** com layout responsivo inteligente (mínimo 1000x700)
- **Controles Visuais Avançados** com ícones e tooltips informativos
- **Barras de Progresso** para capítulo atual e progresso total da novel
- **Status Badge** com indicadores coloridos em tempo real

### 🎙️ Sistema de Narração Avançado
- **TTS Neural de Alta Qualidade** usando Microsoft Edge (gratuito)
- **5 Vozes em Português**: Francisca, Thalita, Antonio, Donato, Brenda
- **Controles de Velocidade Flexíveis**:
  - 5 velocidades fixas: 0.5×, 1×, 1.25×, 1.5×, 2×
  - Barra de ajuste fino para controle preciso
- **Pré-carregamento Inteligente** com cache LRU (10 parágrafos)
- **Transições Instantâneas** entre parágrafos via sistema de fila dedicado
- **Transição Automática** entre capítulos

### 🎵 Sistema de Áudio
- **Música de Fundo** com suporte a todos arquivos MP3/WAV/OGG
- **Gerenciamento de Músicas** na tela de configurações
- **Teste de Músicas** isolado antes de aplicar
- **Controles Independentes** de volume para narração e música
- **Ícones Dinâmicos** que mudam conforme níveis de volume
- **Botão de Mute** para silenciar rapidamente

### 📖 Recursos de Leitura
- **Modo de Leitura Imersivo** com capítulo completo e navegação por clique
- **Estilização de Texto** com 4 paletas de cores e ajuste de tamanho (9-20pt)
- **Navegação Fluida** entre capítulos e parágrafos
- **Salvamento Automático** de progresso
- **Restauração de Sessão** ao reabrir o programa
- **Contador de Tempo** de narração em tempo real
- **Estimativa de Tempo** restante por capítulo
- **Controles Ocultos** com botão flutuante para visualização limpa
- **100% Gratuito** - Sem necessidade de API keys

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

**Bibliotecas principais:**
- `pygame 2.6.1` - Sistema de áudio e reprodução
- `edge-tts 7.2.7` - Síntese de voz usando Microsoft Edge
- `tkinter` - Interface gráfica (já incluso no Python)

## 📖 Como Usar

### Executar a Interface Gráfica

```bash
python novel_reader_gui.py
```

### 🎮 Controles da Interface

#### Controles Principais
- **▶️ Iniciar Narração** - Inicia a narração do parágrafo atual
- **⏸️ Pausar** - Pausa/continua a narração
- **⏹️ Parar** - Para completamente a narração
- **🔄 Reiniciar Cap** - Reinicia o capítulo do início

#### Navegação
- **◄◄ / ►►** - Navegar entre capítulos
- **◄ / ►** - Navegar entre parágrafos
- **Spinbox Cap/Par** - Digitar número específico + Enter

#### Controles de Áudio
- **Volume Narração** - Slider de 0-100%
- **Volume Música** - Slider de 0-100%
- **Velocidade** - Botões: 0.5×, 1×, 1.25×, 1.5×, 2×, 3× + ajuste fino
- **Seleção de Voz** - 5 vozes em português
- **Música** - Normal (🎵) / Combate (⚔️) / Mutar (🔇)

### 🎯 Recursos Especiais

- **Pré-carregamento**: Próximo parágrafo carrega automaticamente durante narração atual
- **Transição Automática**: Ao terminar um capítulo, passa automaticamente para o próximo
- **Salvamento de Progresso**: Posição salva automaticamente ao fechar
- **Restauração de Sessão**: Retoma de onde parou ao reabrir
- **Tela de Configurações**: Acesso a músicas, texto, aparência, perfil e novels
- **Tema Tokyo Night Storm**: Design moderno com WCAG 2.1 compliance

## 📁 Estrutura do Projeto

```
novel_reader/
├── novel_reader_gui.py       # Interface gráfica principal ⭐
├── narrador.py                # Sistema CLI (legacy)
├── requirements.txt           # Dependências do projeto
├── config/                    # Configurações e progresso
│   ├── progresso.json        # Progresso salvo automaticamente
│   ├── vozes_config.json
│   └── sites_config.json
├── core/                      # Núcleo do sistema
│   ├── emocoes.py
│   └── multi_vozes.py
├── engines/                   # Engines de narração
│   └── narracao.py
├── src/                       # Utilitários
│   ├── leitor.py             # Leitor de capítulos
│   ├── gerenciador_vozes.py
│   └── wiki_personagens.py
├── extratores/                # Extratores de sites
│   ├── centralnovel.py       # Extrator para site de novels
│   └── template_generico.py
├── novels/                    # Novels armazenadas
│   └── martial_world/
│       ├── metadata.json
│       └── capitulos/         # Capítulos em JSON
└── assets/                    # Assets (áudio, etc)
    └── audio/
        └── background/
            ├── reading_*.mp3  # BGMs para leitura
            └── combat_*.mp3   # BGMs para combate
```

## 🔧 Extração de Capítulos

### Extrair de Site de Novels

```python
from extratores.centralnovel import ExtratorCentralNovel

extrator = ExtratorCentralNovel()
extrator.extrair_novel("martial-world", inicio=1, fim=2266)
```

### Adicionar Nova Novel

1. Crie a estrutura de diretórios em `novels/nome_da_novel/`
2. Adicione `metadata.json` com informações da novel
3. Salve capítulos em formato JSON em `capitulos/`

## 📦 Dependências Completas

```
edge-tts==7.2.7          # TTS usando Microsoft Edge
pygame==2.6.1            # Sistema de áudio
requests==2.32.5         # HTTP requests
beautifulsoup4==4.14.3   # Web scraping
lxml==5.3.0              # Parser XML/HTML
```

## 🎭 Vozes Disponíveis

| Nome | Voz Neural | Descrição |
|------|------------|-----------|
| Francisca | pt-BR-FranciscaNeural | Feminino BR - Calma e clara (padrão) |
| Thalita | pt-BR-ThalitaNeural | Feminino BR - Jovem e vibrante |
| Brenda | pt-BR-BrendaNeural | Feminino BR - Expressiva e dramática |
| Antonio | pt-BR-AntonioNeural | Masculino BR - Natural e madura |
| Donato | pt-BR-DonatoNeural | Masculino BR - Jovem e energética |

## ⚙️ Configurações Técnicas

### Sistema de Cache
- **Cache LRU** (Least Recently Used): Mantém últimos 10 parágrafos
- **Thread dedicada** para pré-carregamento em background
- **Fila de tarefas** para gerenciar solicitações de cache

### Performance de Áudio
- **Buffer**: 256 bytes (baixa latência)
- **Frequência**: 44100 Hz (alta qualidade)
- **Canais**: 2 (estéreo)
- **Sleep entre parágrafos**: 0.01s (responsividade máxima)

### Tema Escuro - Paleta Catppuccin Mocha
```python
BG_PRINCIPAL = '#1e1e2e'      # Background principal
BG_SECUNDARIO = '#313244'     # Background secundário
ACCENT_PRIMARY = '#89b4fa'    # Azul (realces)
ACCENT_SUCCESS = '#a6e3a1'    # Verde (sucesso)
ACCENT_WARNING = '#f9e2af'    # Amarelo (avisos)
```

## 🐛 Solução de Problemas

### Música não carregada
- Verifique se existem arquivos de áudio em `assets/audio/background/`
- Formatos suportados: MP3, WAV, OGG
- Use "🔄 Atualizar Lista" na aba Músicas das configurações para recarregar

### Erro ao carregar capítulo
- Confirme que o arquivo JSON existe em `novels/[nome]/capitulos/cap_XXXX.json`
- Verifique formato do JSON (número, título, conteúdo)

### Narração não inicia
- Verifique conexão com internet (Edge TTS requer conexão)
- Confirme instalação correta de `edge-tts`: `pip install edge-tts==7.2.7`

### Performance lenta
- Reduza `max_cache_size` em `EngineNarracaoSimples` (padrão: 10)
- Verifique espaço em disco para arquivos temporários TTS

## 📊 Estatísticas

- **Linhas de Código**: ~1400+ (GUI principal)
- **Vozes**: 5 em português
- **Velocidades**: 6 fixas + ajuste fino contínuo
- **Cache**: Até 10 parágrafos simultâneos
- **Capítulos**: Suporte ilimitado

## 🤝 Contribuindo

Contribuições são bem-vindas! Áreas para melhoria:
- Novos extratores de sites de novels
- Suporte a mais idiomas/vozes
- Melhorias na interface
- Otimizações de performance
- Sistema de marcadores/favoritos
- Exportação de audiobook completo

## 📜 Licença

Este projeto é open source. Use, modifique e distribua livremente.

## 🎯 Roadmap Futuro

- [ ] Sistema de marcadores e favoritos
- [ ] Exportação de áudio completo (audiobook)
- [ ] Suporte a mais TTS engines (ElevenLabs, Google TTS)
- [ ] Interface web (Flask/FastAPI)
- [ ] Tema claro alternável
- [ ] Sincronização multi-dispositivo
- [ ] Estatísticas detalhadas de leitura
- [ ] Sistema de notas e anotações inline
- [ ] Detecção de emoções automática no texto
- [ ] Suporte a múltiplas novels simultâneas

---

**Desenvolvido com ❤️ para leitores de novels**

📧 **GitHub**: [LorisGodinho/novel-reader](https://github.com/LorisGodinho/novel-reader)

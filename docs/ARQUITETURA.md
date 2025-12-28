# 🏗️ Arquitetura do Novel Reader

## 📋 Visão Geral

O **Novel Reader** é uma aplicação desktop orientada a objetos desenvolvida em Python, seguindo o padrão arquitetural **MVC** (Model-View-Controller) adaptado para aplicações desktop, com elementos de **arquitetura em camadas**.

## 🎯 Objetivo Principal

> **Proporcionar imersão total ao leitor de novels através de:**
> - Narração com voz neural de alta qualidade
> - Ambientação sonora adaptativa
> - Interface intuitiva e moderna
> - Experiência fluida e responsiva

---

## 📐 Padrão Arquitetural

### **MVC Adaptado + Arquitetura em Camadas**

```
┌─────────────────────────────────────────────┐
│           CAMADA DE APRESENTAÇÃO            │
│  ┌─────────────────────────────────────┐   │
│  │     novel_reader_gui.py (VIEW)      │   │
│  │  - NovelReaderGUI (Interface)       │   │
│  │  - TemaEscuro (Estilização)         │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│          CAMADA DE CONTROLE                 │
│  ┌─────────────────────────────────────┐   │
│  │  narrador.py (CONTROLLER)           │   │
│  │  - ControladorNarracao              │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│          CAMADA DE NEGÓCIO                  │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ src/leitor   │  │ core/        │        │
│  │ - LeitorNovel│  │ - Emocoes    │        │
│  │              │  │ - MultiVozes │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│          CAMADA DE SERVIÇOS                 │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ engines/     │  │ extratores/  │        │
│  │ - Narração   │  │ - Web Scraper│        │
│  │ - TTS        │  │              │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
                    ↓ ↑
┌─────────────────────────────────────────────┐
│          CAMADA DE DADOS                    │
│  ┌─────────────────────────────────────┐   │
│  │  novels/ (JSON)                     │   │
│  │  config/ (JSON)                     │   │
│  │  assets/ (MP3)                      │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

---

## 🔧 Componentes Principais

### **1. CAMADA DE APRESENTAÇÃO (View)**

#### **NovelReaderGUI** (`novel_reader_gui.py`)
**Responsabilidade**: Interface gráfica do usuário

**Padrão**: Singleton (uma única instância da GUI)

**Características**:
- Interface Tkinter com ttk
- Tema escuro Catppuccin Mocha
- Layout responsivo com grid system
- Controles visuais avançados

**Classes**:
```python
class NovelReaderGUI:
    """Interface principal da aplicação."""
    - __init__(root)
    - criar_interface()
    - criar_cabecalho()
    - criar_secao_controles()
    - criar_area_visualizacao()
    - criar_controles_playback()
    - toggle_narracao()
    - loop_narracao()
    - atualizar_display()
```

#### **TemaEscuro** (`novel_reader_gui.py`)
**Responsabilidade**: Estilização da interface

```python
class TemaEscuro:
    """Configurações de tema escuro moderno."""
    - BG_PRINCIPAL = "#1e1e2e"
    - ACCENT_PRIMARY = "#89b4fa"
    - aplicar_tema(root)
```

#### **MusicaFundo** (`novel_reader_gui.py`)
**Responsabilidade**: Gerenciamento de música ambiente

```python
class MusicaFundo:
    """Gerenciador de música de fundo."""
    - __init__()
    - carregar_musicas()
    - tocar_normal()
    - tocar_combate()
    - mutar()
    - set_volume()
```

### **2. CAMADA DE NEGÓCIO (Model/Business Logic)**

#### **LeitorNovel** (`src/leitor.py`)
**Responsabilidade**: Leitura e gerenciamento de capítulos

**Padrão**: Repository Pattern

```python
class LeitorNovel:
    """Leitor e gerenciador de novels."""
    - __init__(caminho_novel)
    - carregar_capitulo(numero)
    - listar_capitulos_disponiveis()
    - obter_total_paragrafos(numero)
    - salvar_progresso(cap, par)
    - carregar_progresso()
```

#### **ProcessadorEmocoes** (`core/emocoes.py`)
**Responsabilidade**: Detecção e aplicação de emoções

**Padrão**: Strategy Pattern

```python
class ProcessadorEmocoes:
    """Processa tags de emoção no texto."""
    - EMOCOES = {...}  # Dicionário de configurações
    - detectar_emocoes(texto)
    - processar_texto_com_emocoes(texto)
    - aplicar_emocao(config)
```

#### **GerenciadorVozesMulti** (`core/multi_vozes.py`)
**Responsabilidade**: Gerenciamento de múltiplas vozes

```python
class GerenciadorVozesMulti:
    """Gerencia vozes para diferentes personagens."""
    - associar_personagem_voz(personagem, voz)
    - obter_voz_personagem(personagem)
    - detectar_dialogos(texto)
```

### **3. CAMADA DE SERVIÇOS**

#### **EngineNarracaoSimples** (`novel_reader_gui.py`)
**Responsabilidade**: Motor de narração com TTS

**Padrão**: Producer-Consumer com Thread Pool

```python
class EngineNarracaoSimples:
    """Engine de narração com cache e pré-carregamento."""
    - __init__(voz, canal)
    - solicitar_precarregamento(texto)
    - narrar(texto, callback_pausado)
    - _worker_precarregamento()  # Thread dedicada
    - _gerar_audio_async(texto)
    - set_velocidade(velocidade)
```

**Sistema de Cache**:
- Cache LRU (Least Recently Used)
- OrderedDict para gerenciamento automático
- Limite: 10 parágrafos em memória
- Thread dedicada para pré-carregamento

#### **ExtratorCentralNovel** (`extratores/centralnovel.py`)
**Responsabilidade**: Extração de capítulos de sites

**Padrão**: Adapter Pattern

```python
class ExtratorCentralNovel:
    """Extrator de novels do site CentralNovel."""
    - extrair_novel(slug, inicio, fim)
    - extrair_capitulo(url, numero)
    - _limpar_texto(texto)
    - _salvar_capitulo(dados, novel, numero)
```

### **4. CAMADA DE DADOS**

#### **Estrutura de Arquivos**

```
novels/
└── martial_world/
    ├── metadata.json
    └── capitulos/
        ├── cap_0001.json
        ├── cap_0002.json
        └── ...

config/
├── progresso.json      # Estado da aplicação
├── vozes_config.json   # Configurações de voz
└── sites_config.json   # URLs de extração

assets/
└── audio/
    └── background/
        ├── ambient.mp3
        └── combat.mp3
```

#### **Formato de Dados**

**Capítulo** (JSON):
```json
{
    "numero": 1,
    "titulo": "Título do Capítulo",
    "conteudo": [
        "Parágrafo 1...",
        "Parágrafo 2...",
        "..."
    ]
}
```

**Progresso** (JSON):
```json
{
    "capitulo": 971,
    "paragrafo": 18,
    "tempo_total": 3600.5
}
```

---

## 🔄 Fluxo de Dados

### **Fluxo de Narração**

```
┌──────────────────────┐
│ Usuário clica        │
│ "Iniciar Narração"   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ NovelReaderGUI       │
│ toggle_narracao()    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ LeitorNovel          │
│ carregar_capitulo()  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ EngineNarracaoSimples│
│ solicitar_pre-       │
│ carregamento()       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Thread Worker        │
│ _worker_pre-         │
│ carregamento()       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Edge TTS (async)     │
│ _gerar_audio_async() │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Cache OrderedDict    │
│ pygame.Sound         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Pygame Mixer         │
│ Reproduz áudio       │
└──────────────────────┘
```

### **Fluxo de Pré-carregamento**

```
Parágrafo N narrando
    ↓
Solicita pré-carregamento N+1
    ↓
Adiciona à Queue
    ↓
Thread Worker processa
    ↓
Gera áudio (async)
    ↓
Armazena em cache LRU
    ↓
Parágrafo N+1 instantâneo (cache hit)
```

---

## 🎨 Padrões de Design Utilizados

### **1. Singleton**
- `NovelReaderGUI` - Uma única instância da interface

### **2. Repository Pattern**
- `LeitorNovel` - Abstrai acesso aos dados de novels

### **3. Strategy Pattern**
- `ProcessadorEmocoes` - Diferentes estratégias de emoção

### **4. Producer-Consumer**
- `EngineNarracaoSimples` - Fila de pré-carregamento com thread worker

### **5. Adapter Pattern**
- `ExtratorCentralNovel` - Adapta dados de sites para formato interno

### **6. Observer Pattern**
- Callbacks de pausa na narração
- Atualização de UI via `root.after()`

### **7. Factory Pattern**
- Criação de objetos `pygame.Sound` no cache

---

## 🔐 Princípios SOLID

### **Single Responsibility Principle (SRP)**
- Cada classe tem responsabilidade única bem definida
- `TemaEscuro` → Estilização
- `MusicaFundo` → Áudio ambiente
- `LeitorNovel` → Leitura de capítulos

### **Open/Closed Principle (OCP)**
- Extensível via herança
- Novos extratores podem ser criados herdando `ExtratorGenerico`

### **Liskov Substitution Principle (LSP)**
- Extratores são substituíveis
- Engines de narração podem ser trocados

### **Interface Segregation Principle (ISP)**
- Interfaces específicas e não inchadas
- Cada componente expõe apenas o necessário

### **Dependency Inversion Principle (DIP)**
- Dependência de abstrações, não implementações
- `LeitorNovel` usa interface genérica de leitura

---

## 🧵 Concorrência e Threading

### **Threads Utilizadas**

1. **Main Thread (GUI)**
   - Interface Tkinter
   - Eventos de usuário
   - Atualizações de UI

2. **Thread de Narração**
   - Loop principal de narração
   - Controle de fluxo de parágrafos
   - `loop_narracao()`

3. **Thread de Pré-carregamento**
   - Worker dedicado (daemon)
   - Processa fila de cache
   - `_worker_precarregamento()`

4. **Thread de Tempo**
   - Atualiza contador de tempo
   - `atualizar_tempo()`

### **Sincronização**

- **Queue (FIFO)** - Comunicação entre threads
- **root.after()** - Atualização segura de UI
- **daemon=True** - Threads finalizadas com aplicação

---

## 📊 Performance

### **Otimizações Implementadas**

1. **Cache LRU**
   - 10 parágrafos em memória
   - OrderedDict para acesso O(1)
   - Remoção automática de antigos

2. **Pré-carregamento Inteligente**
   - Thread dedicada não-bloqueante
   - Próximo parágrafo sempre pronto
   - Transições instantâneas

3. **Áudio Otimizado**
   - Buffer: 256 bytes (baixa latência)
   - Frequência: 44100 Hz (alta qualidade)
   - Canais: 2 (estéreo)

4. **Async/Await**
   - Geração de TTS assíncrona
   - Edge TTS não bloqueia

---

## 🔌 Dependências Externas

```python
# Interface Gráfica
tkinter         # GUI nativa Python
ttk             # Widgets temáticos

# Áudio
pygame          # Reprodução de áudio
edge-tts        # Síntese de voz (Microsoft)

# Web Scraping
requests        # HTTP requests
beautifulsoup4  # Parse HTML
lxml            # Parser rápido

# Utilitários
asyncio         # Programação assíncrona
threading       # Concorrência
queue           # Comunicação entre threads
collections     # OrderedDict (cache LRU)
```

---

## 📝 Convenções de Código

### **Nomenclatura**

- **Classes**: PascalCase (`NovelReaderGUI`)
- **Funções**: snake_case (`carregar_capitulo`)
- **Constantes**: UPPER_CASE (`VOZES`, `EMOCOES`)
- **Privados**: underscore (`_worker_precarregamento`)

### **Docstrings**

```python
def carregar_capitulo(self, numero: int) -> Optional[Dict]:
    """
    Carrega um capítulo específico.
    
    Args:
        numero: Número do capítulo
        
    Returns:
        Dicionário com dados do capítulo ou None
    """
```

### **Type Hints**

- Uso de `typing` para anotação de tipos
- `Optional`, `Dict`, `List`, `Tuple`

---

## 🚀 Escalabilidade

### **Pontos de Extensão**

1. **Novos Extratores**
   - Herdar `ExtratorGenerico`
   - Implementar métodos abstratos

2. **Novos Engines TTS**
   - Implementar interface de `EngineNarracao`
   - Substituir em `NovelReaderGUI`

3. **Novos Temas**
   - Criar classes similares a `TemaEscuro`
   - Aplicar via método `aplicar_tema()`

4. **Plugins de Emoção**
   - Adicionar em `ProcessadorEmocoes.EMOCOES`
   - Configurar parâmetros

---

## 🔒 Segurança

- Sem credenciais hardcoded
- Configurações em arquivos separados
- Validação de entrada de usuário
- Tratamento de exceções robusto

---

## 📈 Futuras Melhorias Arquiteturais

1. **Event Bus** - Desacoplamento de componentes
2. **Plugin System** - Arquitetura de plugins
3. **Banco de Dados** - SQLite para metadados
4. **API REST** - Backend separado
5. **WebSockets** - Sincronização multi-dispositivo

---

**Última atualização**: Dezembro 2025  
**Versão da Arquitetura**: 2.0

# 📊 Diagramas UML - Novel Reader

Este diretório contém todos os diagramas UML do projeto Novel Reader em formato PlantUML.

## 🎯 Diagramas Disponíveis

### 1. Diagrama de Casos de Uso
**Arquivo**: [casos_de_uso.puml](casos_de_uso.puml)

Mostra todos os casos de uso do sistema organizados por ator:
- 👤 **Leitor Principal**: UC01-UC07 (narração, controles, navegação)
- 🔧 **Admin de Conteúdo**: UC08, UC11 (extração, vozes)
- 🤖 **Sistema**: UC09, UC10, UC13 (persistência, emoções, cache)

**Principais relacionamentos**:
- `<<include>>`: UC01 inclui UC09 e UC13
- `<<extend>>`: UC02 estende UC01
- `<<extend>>`: UC05 estende UC06

### 2. Diagrama de Classes
**Arquivo**: [diagrama_classes.puml](diagrama_classes.puml)

Diagrama completo da arquitetura orientada a objetos:
- **Camada de Apresentação**: NovelReaderGUI, TemaEscuro, MusicaFundo
- **Camada de Negócio**: LeitorNovel, ProcessadorEmocoes, GerenciadorVozes
- **Camada de Serviços**: EngineNarracaoSimples, ExtratorCentralNovel
- **Camada de Controle**: ControladorNarracao (CLI legacy)
- **Estruturas de Dados**: Capitulo, Metadata, Progresso

**Padrões de Design**:
- Repository (LeitorNovel)
- Singleton (EngineNarracaoSimples)
- Strategy (ProcessadorEmocoes)
- Adapter (ExtratorGenerico)

### 3. Diagrama de Sequência - Iniciar Narração
**Arquivo**: [sequencia_narracao.puml](sequencia_narracao.puml)

Fluxo completo de inicialização da narração:
1. Carregamento de progresso
2. Leitura de capítulo do JSON
3. Pré-carregamento assíncrono
4. Processamento de emoções
5. Geração de áudio via Edge TTS
6. Reprodução com Pygame
7. Atualização da interface

**Destaque**: Mostra interação entre todos os componentes principais.

### 4. Diagrama de Sequência - Navegação
**Arquivo**: [sequencia_navegacao.puml](sequencia_navegacao.puml)

Demonstra o sistema de cache LRU em ação:
- **Cache Hit**: Transição instantânea (~50ms)
- **Cache Miss**: Geração sob demanda (~500-1500ms)
- **Pré-carregamento**: Thread worker em background
- **Salvamento**: Persistência automática

**Destaque**: Performance crítica do sistema de transições.

### 5. Diagrama de Componentes
**Arquivo**: [arquitetura_componentes.puml](arquitetura_componentes.puml)

Visão arquitetural completa com todas as camadas:
- **Apresentação**: GUI, Tema, Tooltips
- **Controle**: EventLoop, GerenciadorEstado
- **Negócio**: Leitor, Processadores, Vozes
- **Serviços**: Engine (com Cache LRU + Thread Worker), Música, Extrator
- **Infraestrutura**: EdgeTTS, Pygame, Tkinter, AsyncIO
- **Dados**: novels/, config/, assets/, temp/

**Destaque**: Mostra dependências entre componentes e uso de bibliotecas externas.

### 6. Diagrama de Atividades - Extração
**Arquivo**: [atividade_extracao.puml](atividade_extracao.puml)

Fluxo de extração de novels de sites:
1. Parâmetros de entrada (slug, range)
2. Loop por capítulos
3. Requisição HTTP com retry
4. Parsing HTML (BeautifulSoup)
5. Limpeza de formatação
6. Salvamento JSON
7. Rate limiting (1 req/seg)
8. Relatório final

**Destaque**: Tratamento de erros e retry logic.

### 7. Diagrama de Estados - Playback
**Arquivo**: [estado_playback.puml](estado_playback.puml)

Máquina de estados completa do sistema de playback:
- **Iniciando**: Carregamento inicial
- **Parado**: Aguardando ação do usuário
- **Narrando**: PreCarregando → Reproduzindo → ProximoParagrafo
- **Pausado**: Estado preservado
- **Navegação Manual**: Transições entre estados

**Destaque**: Todos os estados possíveis e transições entre eles.

---

## 🚀 Como Visualizar os Diagramas

### Opção 1: VS Code com PlantUML
1. Extensão PlantUML já está instalada
2. Abra qualquer arquivo `.puml`
3. Pressione `Alt+D` para preview
4. Ou clique com botão direito → "Preview Current Diagram"

### Opção 2: Exportar para PNG/SVG
1. Abra arquivo `.puml` no VS Code
2. Clique com botão direito
3. Selecione "Export Current Diagram"
4. Escolha formato: PNG, SVG, EPS, PDF

### Opção 3: PlantUML Online
Acesse: https://www.plantuml.com/plantuml/uml/
- Cole o conteúdo do arquivo `.puml`
- Visualize online
- Baixe como imagem

### Opção 4: Linha de Comando
```bash
# Instalar PlantUML CLI (requer Java)
choco install plantuml

# Gerar PNG
plantuml casos_de_uso.puml

# Gerar SVG
plantuml -tsvg casos_de_uso.puml

# Gerar todos os diagramas
plantuml *.puml
```

---

## 📁 Estrutura de Diretórios

```
docs/
├── ARQUITETURA.md          # Documentação textual da arquitetura
├── CASOS_DE_USO.md         # Especificação de casos de uso
├── DIAGRAMA_CLASSES.md     # Diagrama de classes em ASCII
├── REQUISITOS.md           # Documento de requisitos
└── diagrams/               # Diagramas UML PlantUML
    ├── README.md           # Este arquivo
    ├── casos_de_uso.puml
    ├── diagrama_classes.puml
    ├── sequencia_narracao.puml
    ├── sequencia_navegacao.puml
    ├── arquitetura_componentes.puml
    ├── atividade_extracao.puml
    └── estado_playback.puml
```

---

## 🎨 Convenções Visuais

### Cores por Camada
- 🟢 **Verde claro** (#DDFFDD): Camada de Apresentação
- 🔵 **Azul claro** (#DDDDFF): Camada de Negócio
- 🟡 **Amarelo claro** (#FFFFDD): Camada de Serviços
- 🔴 **Vermelho claro** (#FFDDDD): Camada de Controle
- 🟣 **Rosa** (#Pink): Infraestrutura
- ⚪ **Cinza claro** (#FFEEEE): Estruturas de Dados

### Relacionamentos
- `-->` : Associação
- `*--` : Composição (parte de)
- `o--` : Agregação (contém)
- `--|>` : Herança (é um)
- `..>` : Dependência (usa)
- `..|>` : Implementa interface

### Stereotypes
- `<<dataclass>>` : Estrutura de dados
- `<<abstract>>` : Classe abstrata
- `<<interface>>` : Interface
- `<<include>>` : Inclusão obrigatória
- `<<extend>>` : Extensão opcional

---

## 📋 Checklist de Manutenção

Ao atualizar o código, lembre-se de atualizar os diagramas:

- [ ] Adicionar novas classes ao `diagrama_classes.puml`
- [ ] Atualizar relacionamentos se mudarem
- [ ] Adicionar novos casos de uso se houver funcionalidades
- [ ] Atualizar sequências se fluxos mudarem
- [ ] Revisar estados se lógica de playback mudar
- [ ] Exportar versões PNG para README principal

---

## 🛠️ Ferramentas Recomendadas

- **VS Code** + **PlantUML Extension** (jebbs.plantuml)
- **IntelliJ IDEA** + **PlantUML Integration Plugin**
- **PlantUML Online Server**: https://www.plantuml.com
- **PlantUML CLI** (Java): https://plantuml.com/download
- **Kroki** (API para diagramas): https://kroki.io

---

## 📖 Referências

- **PlantUML Docs**: https://plantuml.com/
- **PlantUML Class Diagram**: https://plantuml.com/class-diagram
- **PlantUML Use Case**: https://plantuml.com/use-case-diagram
- **PlantUML Sequence**: https://plantuml.com/sequence-diagram
- **PlantUML Activity**: https://plantuml.com/activity-diagram-beta
- **PlantUML State**: https://plantuml.com/state-diagram
- **PlantUML Component**: https://plantuml.com/component-diagram

---

**Última Atualização**: 27/12/2025  
**Versão**: 1.0  
**Autor**: Loris Godinho

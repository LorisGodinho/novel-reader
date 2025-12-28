# 🎭 Modelo de Casos de Uso - Novel Reader

## 📋 Visão Geral

Sistema de narração de novels com interface gráfica, focado em proporcionar imersão através de narração de qualidade, ambientação sonora e interface intuitiva.

---

## 👥 Atores

### 🎧 Leitor Principal
- **Descrição**: Usuário que consome a novel através da narração
- **Objetivo**: Experiência imersiva de leitura com narração automatizada
- **Nível de Conhecimento**: Básico a intermediário em uso de software

### 🔧 Administrador de Conteúdo
- **Descrição**: Usuário que configura e extrai novels de sites
- **Objetivo**: Manter biblioteca de novels atualizada
- **Nível de Conhecimento**: Intermediário a avançado

---

## 🎯 Casos de Uso Principais

### 📚 UC01 - Iniciar Narração de Novel

**Ator Principal**: Leitor

**Pré-condições**:
- Novel carregada no sistema
- Arquivo de áudio funcional
- Pygame inicializado

**Fluxo Principal**:
1. Leitor abre a aplicação
2. Sistema exibe interface com lista de novels disponíveis
3. Leitor seleciona novel desejada
4. Sistema carrega metadados da novel (título, autor, total de capítulos)
5. Sistema restaura progresso anterior (se existir)
6. Leitor seleciona capítulo inicial
7. Sistema carrega conteúdo do capítulo em formato de parágrafos
8. Leitor clica em botão "Iniciar Narração" (▶)
9. Sistema inicia pré-carregamento do primeiro parágrafo
10. Sistema executa narração com TTS Edge
11. Sistema atualiza display com texto atual
12. Sistema atualiza barra de progresso

**Fluxos Alternativos**:

**3a. Novel não possui capítulos extraídos**
- Sistema exibe mensagem informativa
- Redireciona para UC08 (Extrair Novel)

**5a. Não há progresso salvo**
- Sistema inicia do capítulo 1, parágrafo 1

**9a. Falha no pré-carregamento**
- Sistema exibe mensagem de erro
- Tenta gerar áudio diretamente sem cache

**Pós-condições**:
- Narração em execução
- Progress bar atualizado
- Texto visível na área de visualização

**Requisitos Especiais**:
- Latência de transição < 100ms entre parágrafos
- Cache LRU de até 10 parágrafos

---

### ⏯️ UC02 - Controlar Playback

**Ator Principal**: Leitor

**Pré-condições**:
- Narração iniciada (UC01)

**Fluxo Principal**:
1. Sistema está narrando parágrafo atual
2. Leitor interage com controles de playback
3. Sistema responde à ação solicitada
4. Sistema atualiza estado visual dos botões

**Sub-casos**:

**UC02.1 - Pausar Narração**
- Leitor clica em botão "Pausar" (⏸)
- Sistema pausa canal de áudio Pygame
- Sistema mantém posição atual
- Botão muda para "Continuar" (▶)

**UC02.2 - Retomar Narração**
- Leitor clica em botão "Continuar" (▶) [durante pausa]
- Sistema despausa canal de áudio
- Narração continua do ponto pausado
- Botão muda para "Pausar" (⏸)

**UC02.3 - Parar Narração Completamente**
- Leitor clica em botão "Parar" (⏹)
- Sistema para canal de áudio
- Sistema limpa cache de pré-carregamento
- Sistema salva progresso atual
- Botão volta para estado inicial "Iniciar Narração"

**Pós-condições**:
- Estado do playback reflete ação do usuário
- Progresso salvo (se parado completamente)

---

### 🔊 UC03 - Ajustar Velocidade de Narração

**Ator Principal**: Leitor

**Pré-condições**:
- Interface carregada

**Fluxo Principal**:
1. Leitor visualiza controles de velocidade
2. Leitor interage com controle desejado
3. Sistema aplica nova velocidade
4. Sistema atualiza tooltip/display com valor atual

**Sub-casos**:

**UC03.1 - Usar Botões de Velocidade Fixa**
- Leitor clica em um dos 6 botões fixos: [0.5×] [1×] [1.25×] [1.5×] [2×] [3×]
- Sistema define velocidade exata correspondente
- Destaca botão selecionado visualmente

**UC03.2 - Ajuste Fino com Slider**
- Leitor arrasta barra de ajuste fino
- Sistema atualiza velocidade em tempo real (50% a 400%)
- Tooltip exibe valor atual: "Velocidade: 1.75×"

**Fluxos Alternativos**:

**2a. Narração em andamento**
- Nova velocidade é aplicada ao próximo parágrafo
- Parágrafo atual continua com velocidade anterior

**Pós-condições**:
- Velocidade de narração atualizada
- Preferência salva em progresso

---

### 🎚️ UC04 - Controlar Volume de Áudio

**Ator Principal**: Leitor

**Pré-condições**:
- Interface carregada

**Fluxo Principal**:
1. Leitor visualiza sliders de volume
2. Leitor ajusta slider desejado
3. Sistema aplica novo volume ao canal correspondente
4. Tooltip exibe valor percentual

**Sub-casos**:

**UC04.1 - Ajustar Volume de Narração**
- Leitor arrasta slider "Volume Narração"
- Sistema atualiza canal de narração (0-100%)

**UC04.2 - Ajustar Volume de Música de Fundo**
- Leitor arrasta slider "Volume Música"
- Sistema atualiza canal de música (0-100%)

**UC04.3 - Mutar Música de Fundo**
- Leitor clica em botão "Mutar Música"
- Sistema salva volume atual e define para 0
- Ícone muda para indicar mudo (🔇)
- Novo clique restaura volume anterior

**Pós-condições**:
- Volume aplicado aos canais de áudio
- Mudanças refletidas instantaneamente

---

### ⏭️ UC05 - Navegar Entre Parágrafos

**Ator Principal**: Leitor

**Pré-condições**:
- Capítulo carregado
- Narração pode estar ativa ou pausada

**Fluxo Principal**:
1. Leitor decide mudar de parágrafo
2. Leitor clica em botão de navegação
3. Sistema valida se há parágrafo na direção solicitada
4. Sistema para narração atual (se ativa)
5. Sistema atualiza índice de parágrafo
6. Sistema atualiza display com novo texto
7. Sistema atualiza progresso
8. Sistema solicita pré-carregamento do próximo
9. Se narração estava ativa, inicia narração do novo parágrafo

**Sub-casos**:

**UC05.1 - Parágrafo Anterior**
- Leitor clica em botão "Parágrafo Anterior" (◀)
- Sistema retrocede 1 parágrafo
- Se já no primeiro parágrafo, exibe feedback visual (botão desabilitado)

**UC05.2 - Próximo Parágrafo**
- Leitor clica em botão "Próximo Parágrafo" (▶)
- Sistema avança 1 parágrafo
- Se último parágrafo do capítulo, chama UC06

**Fluxos Alternativos**:

**3a. Primeiro parágrafo (tentativa de retroceder)**
- Sistema desabilita botão "Anterior"
- Não executa ação

**3b. Último parágrafo (tentativa de avançar)**
- Sistema verifica se há próximo capítulo
- Se sim: executa UC06.2
- Se não: desabilita botão "Próximo"

**Pós-condições**:
- Parágrafo alterado
- Display atualizado
- Progresso salvo

---

### 📖 UC06 - Navegar Entre Capítulos

**Ator Principal**: Leitor

**Pré-condições**:
- Novel com múltiplos capítulos
- Sistema operacional

**Fluxo Principal**:
1. Leitor decide mudar de capítulo
2. Leitor interage com controle de capítulo
3. Sistema valida disponibilidade do capítulo
4. Sistema para narração atual
5. Sistema carrega novo capítulo
6. Sistema redefine posição para parágrafo inicial (1 ou último)
7. Sistema atualiza interface
8. Sistema salva progresso

**Sub-casos**:

**UC06.1 - Capítulo Anterior**
- Leitor clica em botão "Capítulo Anterior" (⏮)
- Sistema decrementa número do capítulo
- Posição vai para último parágrafo do capítulo anterior

**UC06.2 - Próximo Capítulo (Manual)**
- Leitor clica em botão "Próximo Capítulo" (⏭)
- Sistema incrementa número do capítulo
- Posição vai para primeiro parágrafo do próximo capítulo

**UC06.3 - Próximo Capítulo (Automático)**
- Sistema detecta fim do capítulo atual durante narração contínua
- Aguarda 2 segundos
- Automaticamente carrega próximo capítulo
- Continua narração sem interrupção

**UC06.4 - Selecionar Capítulo Específico**
- Leitor abre combobox de capítulos
- Leitor seleciona número desejado da lista
- Sistema carrega capítulo selecionado
- Posição vai para primeiro parágrafo

**Fluxos Alternativos**:

**3a. Capítulo não existe**
- Sistema exibe mensagem: "Capítulo X não disponível"
- Mantém capítulo atual

**5a. Erro ao carregar arquivo JSON**
- Sistema exibe mensagem de erro
- Oferece opção de recarregar ou voltar ao anterior

**6a. Transição automática - último capítulo**
- Sistema detecta que é o último capítulo
- Para narração
- Exibe mensagem: "Fim da novel"

**Pós-condições**:
- Novo capítulo carregado
- Interface atualizada com novo conteúdo
- Progresso salvo

---

### 🎵 UC07 - Gerenciar Música de Fundo

**Ator Principal**: Leitor

**Pré-condições**:
- Arquivos de música presentes em assets/audio/background/
- Pygame mixer inicializado

**Fluxo Principal**:
1. Sistema inicia com música normal tocando em loop
2. Leitor navega pela novel
3. Sistema detecta mudança de contexto (normal ↔ combate)
4. Sistema faz crossfade entre músicas
5. Nova música toca em loop

**Sub-casos**:

**UC07.1 - Música Ambiente Normal**
- Sistema detecta narrativa normal
- Toca "normal.mp3" em volume ambiente
- Loop infinito

**UC07.2 - Música de Combate**
- Sistema detecta palavras-chave: "lutou", "atacou", "combate"
- Faz fade out da música normal
- Inicia "combate.mp3" com fade in
- Loop infinito até fim do combate

**UC07.3 - Controle Manual de Volume**
- Estende UC04.2
- Leitor ajusta volume da música
- Sistema aplica ao canal de música

**UC07.4 - Mutar Música**
- Estende UC04.3
- Música continua tocando mas em volume 0
- Economia de recursos

**Fluxos Alternativos**:

**4a. Arquivo de música não encontrado**
- Sistema registra warning no console
- Continua operação sem música de fundo

**Pós-condições**:
- Música de fundo apropriada ao contexto
- Volume de acordo com preferência do usuário

---

### 📥 UC08 - Extrair Novel de Site

**Ator Principal**: Administrador de Conteúdo

**Pré-condições**:
- Conexão com internet
- Site de novels acessível
- Espaço em disco disponível

**Fluxo Principal**:
1. Administrador identifica novel desejada em site suportado
2. Administrador executa script de extração: `extrair_martial_world.py`
3. Sistema solicita parâmetros: slug, capítulo inicial, capítulo final
4. Administrador fornece informações
5. Sistema inicia processo de extração
6. Para cada capítulo:
   - Sistema faz requisição HTTP
   - Sistema parseia HTML com BeautifulSoup
   - Sistema extrai título e conteúdo
   - Sistema limpa formatação
   - Sistema divide em parágrafos
   - Sistema salva em JSON estruturado
7. Sistema cria arquivo metadata.json
8. Sistema exibe relatório de conclusão

**Sub-casos**:

**UC08.1 - Extração do CentralNovel**
- Administrador usa ExtratorCentralNovel
- URL base: https://centralnovel.com
- Formato: /novel-slug/capitulo-numero/

**UC08.2 - Extração Genérica**
- Administrador adapta ExtratorGenerico
- Define seletores CSS customizados
- Implementa lógica específica do site

**Fluxos Alternativos**:

**6a. Erro de conexão**
- Sistema aguarda 5 segundos
- Tenta novamente (máx. 3 tentativas)
- Se falhar: pula capítulo, continua próximo

**6b. Capítulo já extraído**
- Sistema verifica existência do arquivo JSON
- Pula extração, passa para próximo

**6c. Erro de parsing**
- Sistema registra erro em log
- Salva HTML bruto para análise manual
- Continua para próximo capítulo

**Pós-condições**:
- Capítulos salvos em `novels/nome_novel/capitulos/`
- Metadata atualizado
- Novel disponível para narração

**Requisitos Especiais**:
- Rate limiting: máx. 1 req/segundo
- User-Agent customizado
- Respeito ao robots.txt

---

### 💾 UC09 - Salvar e Restaurar Progresso

**Ator Principal**: Sistema (automático)

**Pré-condições**:
- Pasta config/ acessível
- Permissões de escrita

**Fluxo Principal**:
1. Sistema monitora eventos de mudança de estado
2. Ao detectar evento de salvamento:
   - Parada de narração
   - Mudança de capítulo/parágrafo
   - Fechamento da aplicação
3. Sistema coleta dados de progresso:
   - Novel atual
   - Capítulo atual
   - Parágrafo atual
   - Timestamp
4. Sistema serializa dados em JSON
5. Sistema salva em `config/progresso.json`

**Sub-casos**:

**UC09.1 - Salvamento Automático**
- Trigger: Mudança de parágrafo/capítulo
- Frequência: A cada transição
- Assíncrono: Não bloqueia interface

**UC09.2 - Restauração ao Iniciar**
- Sistema lê `config/progresso.json` no startup
- Se válido: carrega último estado
- Se inválido: inicia do capítulo 1

**UC09.3 - Salvamento ao Fechar**
- Trigger: Evento de fechamento da janela
- Sistema garante salvamento antes de encerrar
- Limpa recursos (threads, arquivos temporários)

**Fluxos Alternativos**:

**5a. Erro de escrita**
- Sistema tenta salvar em arquivo temporário alternativo
- Registra erro em log
- Continua operação normalmente

**UC09.2a. Arquivo de progresso corrompido**
- Sistema detecta JSON inválido
- Faz backup do arquivo corrompido
- Inicia com progresso padrão

**Pós-condições**:
- Progresso persistido
- Experiência contínua entre sessões

---

### 🎭 UC10 - Processar Emoções no Texto

**Ator Principal**: Sistema (automático)

**Pré-condições**:
- ProcessadorEmocoes inicializado
- Detecção automática ativada

**Fluxo Principal**:
1. Sistema recebe texto do parágrafo
2. Sistema analisa texto com regex patterns
3. Sistema detecta tags emocionais ou contextos
4. Sistema classifica emoção: sussurro, grito, riso, choro, etc.
5. Sistema aplica configuração de emoção:
   - Ajusta rate (velocidade)
   - Ajusta pitch (tom)
   - Ajusta volume
6. Sistema passa configuração para engine TTS
7. Engine gera áudio com emoção aplicada

**Emoções Suportadas**:
- **Sussurro**: `<sussurro>` ou contexto baixo
- **Grito**: `<grito>` ou "!" repetido
- **Riso**: "haha", "rsrs", "kkkk"
- **Choro**: "snif", contexto triste
- **Raiva**: "GRRRR", contexto agressivo
- **Susto**: "AH!", "EEK!"
- **Pensamento**: `<pensamento>` ou *itálico*
- **Narração**: texto neutro, padrão
- **Diálogo**: "aspas duplas"
- **Ênfase**: palavras em MAIÚSCULAS

**Sub-casos**:

**UC10.1 - Detecção Manual (Tags)**
- Autor inclui tags no texto: `<grito>Socorro!</grito>`
- Sistema identifica tag exata
- Aplica configuração correspondente

**UC10.2 - Detecção Automática (Contexto)**
- Sistema analisa pontuação: "!!!", "???"
- Sistema analisa palavras-chave
- Sistema infere emoção mais provável

**UC10.3 - Desativar Detecção**
- Usuário desativa detecção automática
- Sistema usa apenas tags manuais
- Narração mais uniforme

**Fluxos Alternativos**:

**4a. Múltiplas emoções no mesmo parágrafo**
- Sistema divide parágrafo em segmentos
- Aplica emoção a cada segmento individualmente
- Concatena áudios gerados

**6a. Configuração de emoção inválida**
- Sistema usa configuração padrão (neutra)
- Registra warning em log

**Pós-condições**:
- Áudio gerado com expressividade
- Imersão aumentada

---

### 🔤 UC11 - Gerenciar Vozes de Personagens

**Ator Principal**: Administrador de Conteúdo

**Pré-condições**:
- GerenciadorVozesMulti disponível
- Arquivo vozes_config.json acessível

**Fluxo Principal**:
1. Administrador identifica personagens principais da novel
2. Administrador acessa configuração de vozes
3. Administrador associa cada personagem a uma voz:
   - Protagonista masculino: "pt-BR-AntonioNeural"
   - Protagonista feminino: "pt-BR-FranciscaNeural"
   - Antagonista: "pt-BR-ThalitaNeural"
   - Narrador: "pt-BR-DonatoNeural"
4. Sistema salva mapeamento em JSON
5. Durante narração, sistema detecta diálogos
6. Sistema identifica personagem pelo contexto
7. Sistema aplica voz correspondente

**Sub-casos**:

**UC11.1 - Detecção de Diálogos**
- Sistema identifica texto entre aspas: "Olá!"
- Sistema versa contexto anterior para identificar falante
- Sistema aplica voz do personagem

**UC11.2 - Voz de Narrador**
- Texto fora de diálogo
- Sistema usa voz padrão de narrador

**UC11.3 - Voz Não Mapeada**
- Personagem desconhecido
- Sistema usa voz padrão
- Registra personagem para futura configuração

**Fluxos Alternativos**:

**6a. Personagem ambíguo**
- Sistema não consegue identificar falante com certeza
- Usa voz de narrador
- Marca para revisão manual

**Pós-condições**:
- Vozes distintas para personagens
- Maior clareza em diálogos
- Imersão aprimorada

---

### 🎨 UC12 - Alternar Tema Visual

**Ator Principal**: Leitor

**Pré-condições**:
- Interface gráfica inicializada

**Fluxo Principal**:
1. Sistema inicia com tema escuro Catppuccin Mocha
2. Leitor visualiza interface com:
   - Fundo: #1e1e2e (Mocha Base)
   - Acento: #89b4fa (Blue)
   - Texto: #cdd6f4 (Text)
   - Secundário: #313244 (Surface0)
3. Sistema aplica tema a todos os widgets
4. Tooltips e hover states usam paleta consistente

**Sub-casos**:

**UC12.1 - Tema Escuro (Padrão)**
- Reduz cansaço visual
- Ideal para leitura noturna
- Menor consumo de energia (OLED)

**UC12.2 - Tema Claro (Futuro)**
- Botão de toggle tema
- Paleta Catppuccin Latte
- Melhora legibilidade em ambientes claros

**Fluxos Alternativos**:

**3a. Tema personalizado do OS**
- Sistema detecta preferência do sistema operacional
- Aplica tema correspondente automaticamente

**Pós-condições**:
- Interface visualmente consistente
- Conforto visual otimizado

---

### ⚡ UC13 - Otimizar Performance com Cache

**Ator Principal**: Sistema (automático)

**Pré-condições**:
- EngineNarracaoSimples inicializado
- Thread de pré-carregamento ativa

**Fluxo Principal**:
1. Sistema mantém cache LRU de 10 parágrafos
2. Ao narrar parágrafo atual:
3. Sistema solicita pré-carregamento do próximo via Queue
4. Thread worker processa requisição:
   - Verifica se já está em cache
   - Se não: gera áudio com Edge TTS
   - Salva em arquivo temporário
   - Carrega em pygame.Sound
   - Adiciona ao cache LRU
5. Quando usuário avança, áudio já está pronto
6. Sistema remove parágrafos mais antigos do cache (FIFO)

**Sub-casos**:

**UC13.1 - Hit de Cache**
- Parágrafo solicitado já está em cache
- Tempo de transição: ~50ms
- Sem necessidade de geração

**UC13.2 - Miss de Cache**
- Parágrafo não está em cache
- Sistema gera sob demanda
- Tempo de transição: ~500-1500ms

**UC13.3 - Pré-carregamento Agressivo**
- Sistema pré-carrega 2-3 parágrafos à frente
- Melhora experiência em navegação rápida

**Fluxos Alternativos**:

**4a. Fila de pré-carregamento cheia**
- Sistema descarta requisições antigas
- Prioriza parágrafo imediatamente próximo

**6a. Cache cheio (10 parágrafos)**
- Sistema remove item mais antigo (LRU)
- Libera memória para novo item

**Pós-condições**:
- Transições instantâneas
- Uso de memória controlado (~50MB)
- CPU ociosa durante narração

**Requisitos Especiais**:
- Máx 10 parágrafos em cache (limite de memória)
- Thread worker dedicado (não bloqueia GUI)
- Queue thread-safe para comunicação

---

## 📊 Diagrama de Casos de Uso

```
                      NOVEL READER - Casos de Uso

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                                                                    │
│  👤 Leitor                                                         │
│   │                                                                │
│   │──────UC01──────▶ Iniciar Narração                             │
│   │                      │                                         │
│   │                      │ <<include>>                             │
│   │                      ↓                                         │
│   │                  UC09 - Salvar Progresso                       │
│   │                                                                │
│   │──────UC02──────▶ Controlar Playback                           │
│   │                   ├─ UC02.1: Pausar                            │
│   │                   ├─ UC02.2: Retomar                           │
│   │                   └─ UC02.3: Parar                             │
│   │                                                                │
│   │──────UC03──────▶ Ajustar Velocidade                           │
│   │                   ├─ UC03.1: Botões Fixos                      │
│   │                   └─ UC03.2: Slider Fino                       │
│   │                                                                │
│   │──────UC04──────▶ Controlar Volume                             │
│   │                   ├─ UC04.1: Volume Narração                   │
│   │                   ├─ UC04.2: Volume Música                     │
│   │                   └─ UC04.3: Mutar Música                      │
│   │                                                                │
│   │──────UC05──────▶ Navegar Parágrafos                           │
│   │                   ├─ UC05.1: Anterior                          │
│   │                   └─ UC05.2: Próximo                           │
│   │                                                                │
│   │──────UC06──────▶ Navegar Capítulos                            │
│   │                   ├─ UC06.1: Anterior                          │
│   │                   ├─ UC06.2: Próximo (Manual)                  │
│   │                   ├─ UC06.3: Próximo (Auto)                    │
│   │                   └─ UC06.4: Selecionar Específico             │
│   │                                                                │
│   └──────UC07──────▶ Gerenciar Música Fundo                       │
│                       ├─ UC07.1: Ambiente Normal                   │
│                       ├─ UC07.2: Combate                           │
│                       ├─ UC07.3: Volume Manual                     │
│                       └─ UC07.4: Mutar                             │
│                                                                    │
│                                                                    │
│  🔧 Admin Conteúdo                                                 │
│   │                                                                │
│   │──────UC08──────▶ Extrair Novel                                │
│   │                   ├─ UC08.1: CentralNovel                      │
│   │                   └─ UC08.2: Genérico                          │
│   │                                                                │
│   └──────UC11──────▶ Gerenciar Vozes                              │
│                       ├─ UC11.1: Detectar Diálogos                 │
│                       ├─ UC11.2: Voz Narrador                      │
│                       └─ UC11.3: Voz Não Mapeada                   │
│                                                                    │
│                                                                    │
│  🤖 Sistema (Auto)                                                 │
│   │                                                                │
│   │──────UC09──────▶ Salvar/Restaurar Progresso                   │
│   │                   ├─ UC09.1: Salvamento Auto                   │
│   │                   ├─ UC09.2: Restauração                       │
│   │                   └─ UC09.3: Salvar ao Fechar                  │
│   │                                                                │
│   │──────UC10──────▶ Processar Emoções                            │
│   │                   ├─ UC10.1: Detecção Manual                   │
│   │                   ├─ UC10.2: Detecção Auto                     │
│   │                   └─ UC10.3: Desativar                         │
│   │                                                                │
│   └──────UC13──────▶ Otimizar com Cache                           │
│                       ├─ UC13.1: Hit Cache                         │
│                       ├─ UC13.2: Miss Cache                        │
│                       └─ UC13.3: Pré-carregamento                  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

RELACIONAMENTOS:

UC01 <<include>> UC09
UC01 <<include>> UC13
UC02 <<extend>> UC01 (durante narração)
UC05 <<extend>> UC06 (limites de capítulo)
UC06.3 <<extend>> UC06.2 (transição automática)
UC07 <<parallel>> UC01 (execução simultânea)
UC10 <<include>> UC01 (processamento de texto)
UC13 <<include>> UC01 (performance)

```

---

## 🔄 Fluxos de Interação Comuns

### Fluxo Típico de Uso

```
1. [UC09.2] Sistema restaura progresso
2. [UC01] Leitor inicia narração
   ├─ [UC13] Sistema pré-carrega próximos parágrafos
   ├─ [UC10] Sistema processa emoções
   └─ [UC07] Música de fundo inicia
3. Durante narração:
   ├─ [UC02] Leitor pausa/retoma conforme necessário
   ├─ [UC03] Ajusta velocidade para conforto
   ├─ [UC04] Ajusta volumes
   └─ [UC05/06] Navega entre parágrafos/capítulos
4. [UC06.3] Transições automáticas entre capítulos
5. [UC09.1] Sistema salva progresso continuamente
6. [UC09.3] Ao fechar, progresso garantido
```

### Fluxo de Configuração Inicial

```
1. [UC08] Admin extrai novel de site
2. [UC11] Admin configura vozes de personagens
3. [UC01] Sistema está pronto para uso
```

---

## 📈 Matriz de Rastreabilidade

| Caso de Uso | Requisito Funcional | Prioridade | Complexidade |
|-------------|---------------------|------------|--------------|
| UC01 | RF01 - Narração TTS | Alta | Média |
| UC02 | RF02 - Controles Playback | Alta | Baixa |
| UC03 | RF03 - Velocidade Ajustável | Média | Baixa |
| UC04 | RF04 - Controle Volume | Média | Baixa |
| UC05 | RF05 - Navegação Parágrafos | Alta | Baixa |
| UC06 | RF06 - Navegação Capítulos | Alta | Média |
| UC07 | RF07 - Música Fundo | Baixa | Média |
| UC08 | RF08 - Extração de Novels | Alta | Alta |
| UC09 | RF09 - Persistência | Alta | Média |
| UC10 | RF10 - Processamento Emoções | Média | Alta |
| UC11 | RF11 - Multi-vozes | Baixa | Alta |
| UC12 | RF12 - Temas Visuais | Baixa | Baixa |
| UC13 | RNF01 - Performance | Alta | Alta |

---

## ✅ Critérios de Aceitação

### UC01 - Iniciar Narração
- [ ] Narração inicia em menos de 2 segundos
- [ ] Áudio é reproduzido sem cortes
- [ ] Display atualiza com texto correto
- [ ] Barra de progresso funciona corretamente

### UC02 - Controlar Playback
- [ ] Pausa interrompe áudio imediatamente
- [ ] Retomar continua do ponto exato
- [ ] Parar libera recursos e salva progresso

### UC03 - Ajustar Velocidade
- [ ] 6 botões fixos funcionam corretamente
- [ ] Slider permite ajuste fino
- [ ] Mudanças aplicadas ao próximo parágrafo

### UC05/UC06 - Navegação
- [ ] Transições entre parágrafos < 100ms
- [ ] Transições entre capítulos < 500ms
- [ ] Navegação não causa crashes

### UC09 - Persistência
- [ ] Progresso salvo em cada transição
- [ ] Restauração funciona 100% do tempo
- [ ] Não há perda de dados

### UC13 - Performance
- [ ] Cache LRU funciona corretamente
- [ ] Uso de memória < 100MB
- [ ] Thread de pré-carregamento não trava GUI

---

**Versão do Documento**: 1.0  
**Última Atualização**: Dezembro 2025  
**Status**: Aprovado para Implementação


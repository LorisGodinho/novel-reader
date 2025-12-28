# 📋 Documento de Requisitos - Novel Reader

## 📌 Informações do Projeto

**Nome do Projeto**: Novel Reader  
**Versão**: 2.0  
**Data**: Dezembro 2025  
**Status**: Em Produção  
**Licença**: MIT

---

## 🎯 Visão Geral do Produto

### Objetivo

O Novel Reader é um sistema de narração automatizada de novels (romances literários) que proporciona uma experiência imersiva através de narração de alta qualidade via TTS (Text-to-Speech), ambientação sonora adaptativa e interface intuitiva.

### Escopo

**Incluído no Escopo**:
- Interface gráfica moderna e responsiva
- Narração de texto com Microsoft Edge TTS
- Sistema de pré-carregamento para transições instantâneas
- Controles completos de playback (play, pause, stop)
- Navegação por capítulos e parágrafos
- Música de fundo adaptativa (ambiente/combate)
- Processamento de emoções no texto
- Persistência automática de progresso
- Extração de novels de sites web
- Suporte a múltiplas vozes para personagens

**Excluído do Escopo**:
- Conversão de ebooks (EPUB, PDF) para formato do sistema
- Edição de texto das novels
- Comunidade online ou compartilhamento social
- Suporte a idiomas além de Português BR
- Aplicativo mobile (Android/iOS)
- Sincronização em nuvem

### Público-Alvo

- **Primário**: Leitores de novels brasileiros (18-35 anos)
- **Secundário**: Pessoas com dificuldades de leitura visual
- **Terciário**: Consumidores de audiobooks alternativos

---

## 📊 Requisitos Funcionais

### RF01 - Narração de Texto com TTS

**Prioridade**: Alta  
**Complexidade**: Média

**Descrição**: Sistema deve narrar o texto da novel usando Microsoft Edge TTS com vozes neurais em português brasileiro.

**Critérios de Aceitação**:
- [ ] Suporte a 5 vozes PT-BR: Antonio, Donato, Francisca, Thalita, Brenda
- [ ] Geração de áudio em formato MP3 via edge-tts
- [ ] Taxa de amostragem: 44100 Hz
- [ ] Qualidade de áudio sem distorções
- [ ] Tempo máximo de geração: 3 segundos por parágrafo

**Regras de Negócio**:
- Voz padrão: pt-BR-AntonioNeural
- Áudios salvos em diretório temporário
- Limpeza automática de arquivos temporários ao fechar

---

### RF02 - Controles de Playback

**Prioridade**: Alta  
**Complexidade**: Baixa

**Descrição**: Usuário deve poder controlar a reprodução da narração com botões intuitivos.

**Critérios de Aceitação**:
- [ ] Botão Iniciar/Pausar/Continuar alterna entre estados
- [ ] Botão Parar encerra narração e retorna ao estado inicial
- [ ] Feedback visual imediato nos botões (mudança de ícone/texto)
- [ ] Estado dos botões persiste corretamente entre transições

**Regras de Negócio**:
- Pausa não perde posição no áudio
- Parar salva progresso automaticamente
- Navegação durante pausa não quebra estado

---

### RF03 - Ajuste de Velocidade de Narração

**Prioridade**: Média  
**Complexidade**: Baixa

**Descrição**: Usuário pode ajustar a velocidade de narração entre 0.5× e 4×.

**Critérios de Aceitação**:
- [ ] 6 botões fixos: 0.5×, 1×, 1.25×, 1.5×, 2×, 3×
- [ ] Slider de ajuste fino: 50% a 400%
- [ ] Tooltip mostra velocidade atual
- [ ] Mudanças aplicadas ao próximo parágrafo
- [ ] Velocidade persiste entre sessões

**Regras de Negócio**:
- Velocidade padrão: 1× (100%)
- Valores fora do range são limitados automaticamente
- Botão clicado fica destacado visualmente

---

### RF04 - Controle de Volume

**Prioridade**: Média  
**Complexidade**: Baixa

**Descrição**: Usuário pode ajustar volumes de narração e música independentemente.

**Critérios de Aceitação**:
- [ ] Slider para volume de narração (0-100%)
- [ ] Slider para volume de música (0-100%)
- [ ] Botão mutar música (toggle)
- [ ] Mudanças aplicadas instantaneamente
- [ ] Volumes persistem entre sessões

**Regras de Negócio**:
- Volume padrão narração: 70%
- Volume padrão música: 30%
- Mutar música preserva valor anterior para restauração

---

### RF05 - Navegação por Parágrafos

**Prioridade**: Alta  
**Complexidade**: Baixa

**Descrição**: Usuário pode navegar entre parágrafos do capítulo atual.

**Critérios de Aceitação**:
- [ ] Botão "Parágrafo Anterior" retrocede 1 parágrafo
- [ ] Botão "Próximo Parágrafo" avança 1 parágrafo
- [ ] Botões desabilitados quando no limite (primeiro/último)
- [ ] Display atualiza com novo texto imediatamente
- [ ] Barra de progresso reflete posição correta

**Regras de Negócio**:
- Primeiro parágrafo: botão anterior desabilitado
- Último parágrafo: botão próximo tenta avançar para próximo capítulo
- Navegação durante narração para e reinicia com novo parágrafo

---

### RF06 - Navegação por Capítulos

**Prioridade**: Alta  
**Complexidade**: Média

**Descrição**: Usuário pode navegar entre capítulos da novel.

**Critérios de Aceitação**:
- [ ] Botão "Capítulo Anterior" carrega capítulo anterior
- [ ] Botão "Próximo Capítulo" carrega próximo capítulo
- [ ] Combobox permite seleção direta de capítulo
- [ ] Transição automática ao fim do último parágrafo
- [ ] Confirmação visual de mudança de capítulo

**Regras de Negócio**:
- Ao retroceder capítulo: vai para último parágrafo
- Ao avançar capítulo: vai para primeiro parágrafo
- Transição automática aguarda 2 segundos após fim
- Capítulo inexistente: exibe mensagem de erro

---

### RF07 - Música de Fundo Adaptativa

**Prioridade**: Baixa  
**Complexidade**: Média

**Descrição**: Sistema toca música de fundo que se adapta ao contexto da narrativa.

**Critérios de Aceitação**:
- [ ] Música ambiente em loop durante narrativa normal
- [ ] Música de combate durante cenas de ação
- [ ] Transição suave (fade in/out) entre músicas
- [ ] Volume independente do volume de narração
- [ ] Opção de mutar música

**Regras de Negócio**:
- Arquivos esperados: `assets/audio/background/normal.mp3`, `combate.mp3`
- Detecção de combate por palavras-chave: "lutou", "atacou", "combate"
- Ausência de arquivos não impede funcionamento do sistema

---

### RF08 - Extração de Novels de Sites

**Prioridade**: Alta  
**Complexidade**: Alta

**Descrição**: Sistema permite extrair novels de sites web para formato local JSON.

**Critérios de Aceitação**:
- [ ] Extração de CentralNovel.com
- [ ] Suporte a range de capítulos (início-fim)
- [ ] Parsing de título e conteúdo
- [ ] Limpeza de formatação HTML
- [ ] Salvamento em estrutura JSON padronizada
- [ ] Criação de arquivo metadata.json

**Regras de Negócio**:
- Rate limiting: máximo 1 requisição por segundo
- Retry em caso de erro: 3 tentativas
- Capítulos já existentes são pulados
- User-Agent personalizado para evitar bloqueio

**Estrutura JSON Esperada**:
```json
{
  "numero": 1,
  "titulo": "Título do Capítulo",
  "conteudo": [
    "Parágrafo 1",
    "Parágrafo 2",
    "..."
  ]
}
```

---

### RF09 - Persistência de Progresso

**Prioridade**: Alta  
**Complexidade**: Média

**Descrição**: Sistema salva e restaura progresso automaticamente.

**Critérios de Aceitação**:
- [ ] Salvamento automático a cada transição de parágrafo/capítulo
- [ ] Salvamento garantido ao fechar aplicação
- [ ] Restauração automática ao iniciar
- [ ] Arquivo JSON em `config/progresso.json`
- [ ] Tratamento de arquivo corrompido

**Regras de Negócio**:
- Salvamento assíncrono (não bloqueia interface)
- Arquivo corrompido é ignorado, inicia do capítulo 1
- Backup automático antes de sobrescrever

**Estrutura de Progresso**:
```json
{
  "novel": "martial_world",
  "capitulo": 5,
  "paragrafo": 12,
  "timestamp": "2025-12-27T10:30:00"
}
```

---

### RF10 - Processamento de Emoções

**Prioridade**: Média  
**Complexidade**: Alta

**Descrição**: Sistema detecta e aplica emoções ao texto narrado.

**Critérios de Aceitação**:
- [ ] Detecção de 10 tipos de emoção: sussurro, grito, riso, choro, raiva, susto, pensamento, diálogo, ênfase, narração
- [ ] Suporte a tags manuais: `<grito>texto</grito>`
- [ ] Detecção automática por contexto e pontuação
- [ ] Ajuste de rate, pitch e volume por emoção
- [ ] Opção de desativar detecção automática

**Regras de Negócio**:
- Detecção automática ativa por padrão
- Múltiplas emoções no parágrafo: segmentação
- Configurações de emoção definidas em core/emocoes.py

**Exemplos de Detecção**:
- "!!!" → grito (rate +15%, pitch +10%, volume +20%)
- "haha" → riso (rate +20%, pitch +15%)
- MAIÚSCULAS → ênfase (pitch +10%, volume +10%)

---

### RF11 - Múltiplas Vozes para Personagens

**Prioridade**: Baixa  
**Complexidade**: Alta

**Descrição**: Sistema atribui vozes diferentes para personagens distintos.

**Critérios de Aceitação**:
- [ ] Mapeamento personagem → voz configurável
- [ ] Detecção de diálogos (texto entre aspas)
- [ ] Identificação de falante por contexto
- [ ] Voz de narrador para texto não-diálogo
- [ ] Persistência de mapeamento em vozes_config.json

**Regras de Negócio**:
- Voz padrão usada para personagens não mapeados
- Detecção de falante por última menção antes da fala
- Configuração manual necessária via arquivo JSON

---

### RF12 - Interface Responsiva e Temas

**Prioridade**: Baixa  
**Complexidade**: Baixa

**Descrição**: Interface moderna, responsiva e com tema escuro confortável.

**Critérios de Aceitação**:
- [ ] Janela redimensionável (mínimo 1000×700)
- [ ] Layout adaptativo via grid
- [ ] Tema escuro Catppuccin Mocha
- [ ] Tooltips informativos em todos os controles
- [ ] Ícones visuais + texto descritivo

**Regras de Negócio**:
- Tamanho inicial: 1100×800
- Tamanho mínimo: 1000×700
- Paleta de cores definida em TemaEscuro
- Modo compacto em janelas pequenas (<900px largura)

---

## ⚙️ Requisitos Não-Funcionais

### RNF01 - Performance

**Categoria**: Eficiência

**Descrição**: Sistema deve proporcionar transições instantâneas entre parágrafos.

**Métricas**:
- Transição entre parágrafos: < 100ms (com cache hit)
- Transição entre capítulos: < 500ms
- Uso de memória: < 100MB
- Uso de CPU durante narração: < 5%

**Implementação**:
- Cache LRU de 10 parágrafos pré-carregados
- Thread dedicado para pré-carregamento
- Geração assíncrona com asyncio

---

### RNF02 - Usabilidade

**Categoria**: Interface

**Descrição**: Interface deve ser intuitiva para usuários com conhecimento básico.

**Métricas**:
- Tempo para iniciar primeira narração: < 30 segundos (novo usuário)
- Taxa de erros de interação: < 5%
- Satisfação do usuário: > 4/5

**Implementação**:
- Tooltips explicativos
- Feedback visual imediato
- Botões com ícones + texto
- Estado do sistema sempre visível

---

### RNF03 - Confiabilidade

**Categoria**: Disponibilidade

**Descrição**: Sistema deve ser estável e não perder dados.

**Métricas**:
- Taxa de crashes: < 0.1%
- Perda de progresso: 0%
- Uptime durante sessão: 99.9%

**Implementação**:
- Tratamento de exceções em todas as operações críticas
- Salvamento redundante de progresso
- Logs de erro para debugging
- Testes de stress com 1000+ parágrafos

---

### RNF04 - Compatibilidade

**Categoria**: Portabilidade

**Descrição**: Sistema deve funcionar em Windows 10/11.

**Métricas**:
- Compatibilidade Windows 10+: 100%
- Python 3.10+: Sim
- Sem dependências nativas complexas

**Implementação**:
- Uso de bibliotecas cross-platform (Tkinter, Pygame)
- Edge TTS funciona em qualquer SO com Python
- PyInstaller para distribuição standalone

---

### RNF05 - Manutenibilidade

**Categoria**: Manutenção

**Descrição**: Código deve ser organizado e documentado.

**Métricas**:
- Cobertura de documentação: > 80%
- Complexidade ciclomática: < 10 por função
- Linhas por classe: < 500

**Implementação**:
- Arquitetura MVC + Layers
- Docstrings em todas as classes e funções
- README.md completo
- Documentação de arquitetura (ARQUITETURA.md)

---

### RNF06 - Segurança

**Categoria**: Segurança

**Descrição**: Sistema não deve expor dados sensíveis do usuário.

**Métricas**:
- Sem coleta de dados pessoais
- Sem conexão externa (exceto extração de novels)
- Arquivos locais com permissões adequadas

**Implementação**:
- Todas as operações são locais
- Sem telemetria ou analytics
- Progresso salvo apenas localmente

---

### RNF07 - Escalabilidade

**Categoria**: Desempenho

**Descrição**: Sistema deve suportar novels grandes sem degradação.

**Métricas**:
- Suporte a novels com 2000+ capítulos
- Carregamento de capítulo com 500+ parágrafos: < 1 segundo
- Tamanho máximo de novel: 500MB de JSON

**Implementação**:
- Carregamento lazy de capítulos (não carrega todos de uma vez)
- Cache limitado (LRU) para controlar memória
- Limpeza de arquivos temporários periódica

---

## 🛠️ Requisitos de Sistema

### Hardware Mínimo

- **Processador**: Intel Core i3 / AMD Ryzen 3 (2.0 GHz)
- **Memória RAM**: 4 GB
- **Espaço em Disco**: 500 MB (instalação) + espaço para novels
- **Placa de Som**: Qualquer (integrada)
- **Resolução de Tela**: 1280×720 (HD)

### Hardware Recomendado

- **Processador**: Intel Core i5 / AMD Ryzen 5 (3.0 GHz+)
- **Memória RAM**: 8 GB
- **Espaço em Disco**: 2 GB
- **Placa de Som**: Dedicada ou de alta qualidade
- **Resolução de Tela**: 1920×1080 (Full HD)

### Software

- **Sistema Operacional**: Windows 10/11 (64-bit)
- **Python**: 3.10 ou superior (se executando via código-fonte)
- **Dependências Python**:
  - tkinter (incluído no Python)
  - pygame 2.6.1
  - edge-tts 7.2.7
  - requests 2.31+
  - beautifulsoup4 4.12+

### Conectividade

- **Internet**: Necessária apenas para extração de novels
- **Offline**: Funcionamento completo após novels extraídas

---

## 📦 Estrutura de Dados

### Capítulo JSON

```json
{
  "numero": 1,
  "titulo": "O Início da Jornada",
  "conteudo": [
    "Era uma vez, em uma terra distante...",
    "O protagonista acordou cedo naquela manhã.",
    "Ele não sabia que sua vida mudaria para sempre."
  ]
}
```

### Metadata JSON

```json
{
  "titulo": "Martial World",
  "autor": "Cocooned Cow",
  "genero": "Xianxia",
  "total_capitulos": 2311,
  "idioma": "pt-BR",
  "fonte": "CentralNovel",
  "data_extracao": "2025-12-27"
}
```

### Progresso JSON

```json
{
  "novel": "martial_world",
  "capitulo": 15,
  "paragrafo": 7,
  "tempo_total_segundos": 14523,
  "ultima_sessao": "2025-12-27T15:30:00",
  "velocidade_preferida": 125,
  "volume_narracao": 70,
  "volume_musica": 30
}
```

### Vozes Config JSON

```json
{
  "vozes_disponiveis": {
    "antonio": "pt-BR-AntonioNeural",
    "donato": "pt-BR-DonatoNeural",
    "francisca": "pt-BR-FranciscaNeural",
    "thalita": "pt-BR-ThalitaNeural",
    "brenda": "pt-BR-BrendaNeural"
  },
  "mapeamento_personagens": {
    "Lin Ming": "antonio",
    "Qin Xingxuan": "francisca",
    "Narrador": "donato"
  },
  "voz_padrao": "antonio"
}
```

---

## 🔐 Restrições e Premissas

### Restrições

1. **Técnicas**:
   - Limitado a vozes do Microsoft Edge TTS
   - Requer conexão para extração (não para narração)
   - Apenas Windows (por enquanto)

2. **Legais**:
   - Uso pessoal apenas (novels devem ter permissão de distribuição)
   - Respeito a robots.txt dos sites de extração
   - Não redistribuir com conteúdo protegido por direitos autorais

3. **Operacionais**:
   - Usuário responsável por obter novels legalmente
   - Sem suporte oficial a modificações de código
   - Atualizações manuais (sem auto-update)

### Premissas

1. **Usuário**:
   - Tem conhecimento básico de computação
   - Sabe como executar um arquivo .exe ou Python script
   - Possui novels em formato compatível ou acesso a sites suportados

2. **Sistema**:
   - Python instalado (se executando código-fonte)
   - Permissões de leitura/escrita em diretórios do projeto
   - Placa de som funcional

3. **Conteúdo**:
   - Novels estão em português brasileiro
   - Formatação do site de origem é consistente
   - Textos não possuem caracteres especiais excessivos

---

## 📊 Casos de Teste Prioritários

### CT01 - Narração Básica

**Pré-condições**: Novel com pelo menos 1 capítulo carregada

**Passos**:
1. Abrir aplicação
2. Clicar em "Iniciar Narração"
3. Aguardar reprodução de áudio

**Resultado Esperado**:
- Áudio reproduz corretamente
- Texto aparece na tela
- Barra de progresso atualiza

---

### CT02 - Navegação Rápida

**Pré-condições**: Narração ativa

**Passos**:
1. Clicar em "Próximo Parágrafo" 10 vezes rapidamente
2. Clicar em "Parágrafo Anterior" 5 vezes rapidamente
3. Clicar em "Próximo Capítulo"

**Resultado Esperado**:
- Transições são instantâneas (< 100ms)
- Sem travamentos
- Display sempre atualizado corretamente

---

### CT03 - Persistência

**Pré-condições**: Novel carregada

**Passos**:
1. Narrar até capítulo 3, parágrafo 5
2. Fechar aplicação
3. Reabrir aplicação

**Resultado Esperado**:
- Sistema restaura capítulo 3, parágrafo 5
- Velocidade e volumes restaurados

---

### CT04 - Cache LRU

**Pré-condições**: Narração ativa

**Passos**:
1. Narrar 15 parágrafos consecutivos
2. Voltar para parágrafo 5 (dentro do cache)
3. Voltar para parágrafo 1 (fora do cache)

**Resultado Esperado**:
- Parágrafo 5: transição instantânea (cache hit)
- Parágrafo 1: pequeno delay (cache miss, ~500ms)

---

### CT05 - Extração de Novel

**Pré-condições**: Conexão com internet, site acessível

**Passos**:
1. Executar script de extração
2. Fornecer URL da novel
3. Definir range de capítulos (1-10)
4. Aguardar conclusão

**Resultado Esperado**:
- 10 arquivos JSON criados em `novels/nome_novel/capitulos/`
- Arquivo `metadata.json` criado
- Sem erros de parsing

---

## 📈 Métricas de Sucesso

### KPIs do Produto

1. **Tempo Médio de Sessão**: > 30 minutos
2. **Taxa de Retenção (7 dias)**: > 60%
3. **Capítulos Narrados por Sessão**: > 3
4. **Taxa de Erros por Sessão**: < 1%

### Métricas Técnicas

1. **Cobertura de Código**: > 70% (testes unitários)
2. **Tempo de Build**: < 2 minutos
3. **Tamanho do Executável**: < 100MB
4. **Tempo de Startup**: < 3 segundos

---

## 🗺️ Roadmap Futuro

### Versão 2.1 (Q1 2026)

- [ ] Tema claro (Catppuccin Latte)
- [ ] Modo de leitura noturna com filtro de luz azul
- [ ] Atalhos de teclado customizáveis
- [ ] Estatísticas de leitura (tempo total, capítulos concluídos)

### Versão 2.2 (Q2 2026)

- [ ] Suporte a mais sites de extração (Novel Updates, Royal Road)
- [ ] Sistema de bookmarks/favoritos
- [ ] Exportação de progresso para backup
- [ ] Notas e anotações por capítulo

### Versão 3.0 (Q3 2026)

- [ ] Suporte a Linux e macOS
- [ ] Aplicativo mobile (Android)
- [ ] Sincronização em nuvem (opcional)
- [ ] Comunidade: ratings e comentários

---

## 📝 Glossário

- **Novel**: Obra literária longa, geralmente de origem asiática (chinesa, coreana, japonesa)
- **TTS**: Text-to-Speech, tecnologia de conversão de texto em fala
- **Edge TTS**: Serviço de TTS da Microsoft, gratuito e de alta qualidade
- **LRU Cache**: Least Recently Used Cache, estratégia de cache que remove itens menos usados
- **Xianxia**: Gênero de fantasia chinês focado em cultivo de artes marciais
- **Parsing**: Processo de análise e extração de dados de documentos (HTML, JSON)
- **Pygame**: Biblioteca Python para desenvolvimento de jogos e multimídia
- **Tkinter**: Biblioteca Python para criação de interfaces gráficas

---

## 👥 Stakeholders

### Desenvolvimento
- **Desenvolvedor Principal**: Responsável por implementação e manutenção
- **Testadores**: Comunidade de usuários beta

### Usuários
- **Leitor Final**: Consumidor primário do produto
- **Admin de Conteúdo**: Gerencia biblioteca de novels

### Externos
- **Microsoft**: Provedor do Edge TTS
- **Sites de Novels**: Fontes de conteúdo (CentralNovel, etc.)

---

## 📞 Contato e Suporte

- **Repositório**: https://github.com/LorisGodinho/novel-reader
- **Issues**: GitHub Issues para bugs e sugestões
- **Documentação**: README.md e pasta docs/

---

**Aprovação do Documento**:

| Nome | Cargo | Data | Assinatura |
|------|-------|------|------------|
| Loris Godinho | Product Owner | 27/12/2025 | ✓ |
| Loris Godinho | Tech Lead | 27/12/2025 | ✓ |

---

**Histórico de Revisões**:

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 27/12/2025 | Loris Godinho | Criação do documento |

---

**Status**: APROVADO PARA DESENVOLVIMENTO ✅

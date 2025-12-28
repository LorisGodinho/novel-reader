# 📋 Changelog - Novel Reader

## [2.5.0] - 28/12/2025

### ✨ Adicionado
- **Modo de Leitura Imersivo**: Visualização do capítulo completo com navegação por clique nos parágrafos
- **Estilização de Texto**: 4 paletas de cores personalizadas (Tokyo Night, Solarized, Sepia, Mint)
- **Controles Ocultos**: Botão flutuante "👁️ Mostrar Controles" para leitura limpa
- **Confirmação ao Fechar**: Diálogo de confirmação para evitar fechamento acidental
- **Tema Tokyo Night Storm**: Design moderno com compliance WCAG 2.1

### 🔧 Melhorado
- **Sistema de Música**: Agora carrega todos arquivos MP3/WAV/OGG automaticamente (sem prefixos específicos)
- **Gerenciamento de Música**: Lista não carrega automaticamente ao abrir configurações (apenas ao clicar em "🔄 Atualizar Lista")
- **Teste de Música**: Seleção atualiza corretamente ao escolher diferentes músicas
- **Tela de Configurações**: Música de teste para automaticamente ao fechar a janela
- **Layout Vertical**: Controles na parte superior, texto na parte inferior (melhor responsividade)
- **Responsividade**: Interface se adapta melhor a diferentes tamanhos de janela

### ❌ Removido
- **Aba de Vozes**: Removida da tela de configurações (simplificação da interface)
- **Velocidade 3×**: Limitada a 2× (limitação do Edge TTS)
- **Sistema Leitura/Combate**: Unificado em música de fundo única

### 🐛 Corrigido
- Cache de voz limpa corretamente ao trocar de voz
- Erro `AttributeError: 'Leitor' object has no attribute 'novel_id'` corrigido
- Botões de navegação respondem imediatamente mesmo durante narração
- Música de teste não continua tocando após fechar configurações
- Seleção de música no teste sempre atualiza para a música correta

---

## [2.0.0] - 12/12/2025

### ✨ Adicionado
- Interface gráfica completa com tkinter
- Tema escuro baseado em Catppuccin Mocha
- Sistema de highlight progressivo durante narração
- Controles visuais com botões e ícones
- Status badge dinâmico (PARADO/NARRANDO/PAUSADO)
- Sistema de música de fundo (Normal/Combate)
- Pré-carregamento inteligente com cache LRU
- Salvamento automático de progresso
- 5 vozes em português (Edge TTS)

### 🔧 Melhorado
- Performance com threading dedicado
- Sistema de áudio com pygame mixer
- Navegação entre capítulos e parágrafos
- Controles de velocidade (0.5× a 3×)

### ❌ Removido
- Sistema de emoções complexo
- Tags de texto especiais
- Interface de terminal
- Controles de teclado

---

## [1.0.0] - Versão Inicial

### ✨ Características
- Sistema CLI básico de narração
- Suporte a múltiplas vozes
- Sistema de emoções com tags
- Extração de capítulos de sites
- Formato JSON para armazenamento

---

**Legenda:**
- ✨ Adicionado: Novos recursos
- 🔧 Melhorado: Mudanças em recursos existentes
- ❌ Removido: Recursos descontinuados
- 🐛 Corrigido: Correções de bugs

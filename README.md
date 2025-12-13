# Novel Reader - Martial World

Sistema de narração automática de novels com TTS (Text-to-Speech) utilizando Microsoft Edge TTS gratuito.

## 🎯 Características

- **Narração com emoções**: Sistema de detecção e aplicação de emoções no texto
- **5 vozes em português**: Francisca, Thalita, Antonio, Raquel, Duarte
- **Controles interativos**: Pausar, avançar, retroceder durante a narração
- **Narração contínua**: Modo automático para múltiplos capítulos
- **100% gratuito**: Utiliza Microsoft Edge TTS sem necessidade de API keys

## 🚀 Instalação

1. Ative o ambiente virtual:
```bash
.venv\Scripts\activate
```

2. Instale as dependências (se necessário):
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

Execute o narrador:
```bash
.venv\Scripts\python narrador.py
```

### Menu Principal

1. **Narrar capítulo único** - Narra um capítulo específico
2. **Narração contínua** - Narra múltiplos capítulos automaticamente
3. **Trocar voz** - Escolha entre 5 vozes disponíveis
4. **Detecção automática** - Liga/desliga detecção de emoções
5. **Listar capítulos** - Mostra capítulos disponíveis
6. **Sair** - Encerra o programa

### ⌨️ Controles Durante a Narração

- **ESPAÇO** - Pausar/Retomar (mostra capítulo e parágrafo atual)
- **→** (seta direita) - Próximo parágrafo
- **←** (seta esquerda) - Parágrafo anterior
- **Q** - Parar narração

### 📝 Sistema de Emoções

Tags disponíveis para adicionar nos capítulos:

- `[sussurro]` - Voz baixa e suave
- `[grito]` - Voz alta e intensa
- `[riso]` - Tom alegre
- `[misterioso]` - Voz grave e lenta
- `[animado]` - Voz rápida e energética
- `[triste]` - Voz baixa e melancólica
- `[raiva]` - Voz intensa
- `[suspiro]` - Suspiro

**Detecção automática**: O sistema detecta palavras como "sussurrou", "gritou", "riu" e aplica emoções automaticamente.

## 📁 Estrutura do Projeto

```
novel_reader/
├── core/              # Sistema de emoções
├── engines/           # Engine de narração
├── extratores/        # Web scrapers
├── src/               # Leitor de capítulos
├── novels/            # Capítulos extraídos
├── narrador.py        # Script principal
└── _backup_working/   # Backup do código funcional
```

## 🔧 Extração de Capítulos

Para extrair mais capítulos:
```bash
.venv\Scripts\python extrair_martial_world.py
```

## 💾 Backup

Uma cópia de segurança do código está em `_backup_working/` caso precise restaurar.

## 📦 Dependências

- edge-tts 7.2.6
- pygame 2.6.1
- pynput 1.8.1
- requests 2.32.5
- beautifulsoup4 4.14.3

## 🎭 Vozes Disponíveis

| Nome | Descrição |
|------|-----------|
| Francisca | Feminino BR - Calma (padrão) |
| Thalita | Feminino BR - Multilíngue |
| Antonio | Masculino BR |
| Raquel | Feminino PT |
| Duarte | Masculino PT |

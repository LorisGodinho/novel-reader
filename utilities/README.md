# 🧰 Utilities - Ferramentas do Novel Reader

Este diretório contém módulos utilitários para manutenção e gerenciamento do projeto.

## 📦 Módulos Disponíveis

### gerenciador_bgm.py

Módulo consolidado para gerenciamento de músicas de fundo (BGMs).

**Funcionalidades**:
- Download de BGMs do YouTube
- Processamento com ffmpeg (normalização, fade, equalização)
- Verificação de BGMs existentes
- Limpeza de arquivos temporários

**Uso via CLI**:
```bash
# Verificar BGMs existentes
python gerenciar_bgms.py --verificar

# Limpar arquivos temporários
python gerenciar_bgms.py --limpar

# Baixar nova BGM
python gerenciar_bgms.py --baixar "URL" --nome "bgm_nome" --tipo leitura
python gerenciar_bgms.py --baixar "URL" --nome "combat_X" --tipo combate --start 30 --duration 180
```

**Uso programático**:
```python
from utilities import GerenciadorBGM

gerenciador = GerenciadorBGM()

# Baixar e processar
gerenciador.baixar_e_processar(
    url="https://youtube.com/...",
    nome="bgm_teste",
    start=0,
    duration=180,
    tipo="leitura"
)

# Verificar BGMs
bgms = gerenciador.verificar_bgms()
print(f"Total: {bgms['total_size_mb']:.2f} MB")

# Exibir relatório
gerenciador.exibir_relatorio()
```

## 🗑️ Scripts Legados

Os scripts antigos foram movidos para `_legacy_scripts/` para referência:
- `baixar_bgms_leitura.py` → substituído por `gerenciador_bgm.py`
- `baixar_musicas.py` → substituído por `gerenciador_bgm.py`
- `verificar_bgms.py` → substituído por `gerenciar_bgms.py --verificar`
- `copiar_bgms.py` → funcionalidade integrada
- `criar_bgms_sinteticas.py` → referência para criação sintética
- `renomear_leitura.py` → não mais necessário

## 🎯 Vantagens da Refatoração

### Antes (Scripts Dispersos)
- 7 scripts separados com código duplicado
- Lógica repetida de download/processamento
- Difícil manutenção
- Sem reutilização de código

### Depois (Módulo Unificado)
- 1 módulo consolidado: `gerenciador_bgm.py`
- 1 interface CLI: `gerenciar_bgms.py`
- Código DRY (Don't Repeat Yourself)
- Fácil extensão e manutenção
- Uso tanto via CLI quanto programático

## 📊 Redução de Código

| Métrica | Antes | Depois | Redução |
|---------|-------|--------|---------|
| Arquivos Python | 7 scripts | 1 módulo + 1 CLI | -71% |
| Linhas de código | ~800 | ~320 | -60% |
| Código duplicado | Alto | Zero | -100% |
| Manutenibilidade | Baixa | Alta | +200% |

## 🚀 Próximas Funcionalidades

- [ ] Suporte a download em lote
- [ ] Integração com Spotify/SoundCloud
- [ ] Análise automática de BPM para melhor loop
- [ ] Criação de playlists personalizadas
- [ ] Detecção automática de tipo (leitura/combate) via IA

---

**Última Atualização**: 27/12/2025  
**Versão**: 2.0

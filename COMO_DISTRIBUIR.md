# Como Distribuir o Novel Reader

## 📦 Executável Criado

O executável foi compilado com sucesso em: **`dist/NovelReader/`**

## 🎯 Para Compartilhar

### Opção 1: Compartilhar Pasta Completa (Recomendado)

Compartilhe toda a pasta **`dist/NovelReader/`** que contém:
- `NovelReader.exe` - Executável principal (7 MB)
- `_internal/` - Bibliotecas necessárias
- Subpastas criadas automaticamente:
  - `assets/` - Áudios de fundo
  - `novels/` - Capítulos extraídos
  - `config/` - Configurações e progresso
  - `src/`, `extratores/`, `core/` - Código necessário

### Opção 2: Compactar em ZIP

```powershell
# Criar arquivo ZIP para distribuição
Compress-Archive -Path ".\dist\NovelReader\*" -DestinationPath ".\NovelReader_v1.0.zip"
```

O arquivo ZIP terá aproximadamente 100-150 MB (com dependências + capítulos).

## ✅ Como Usar (para quem receber)

1. **Extrair** a pasta `NovelReader` (ou descompactar o ZIP)
2. **Abrir** a pasta extraída
3. **Clicar duas vezes** em `NovelReader.exe`
4. **Aguardar** a interface abrir (pode levar 5-10 segundos na primeira vez)
5. **Usar** normalmente conforme instruções do programa

## 📋 Requisitos do Sistema

- **Windows 10/11** (64-bit)
- **Conexão com Internet** (para gerar narração Edge TTS)
- **~200 MB** de espaço em disco
- **Placa de som** para áudio

## 🔍 Estrutura Final

```
NovelReader/
├── NovelReader.exe          ← Clicar aqui para executar
├── LEIA-ME.txt             ← Instruções de uso
├── _internal/              ← Bibliotecas (não mexer)
├── assets/
│   └── audio/
│       └── background/     ← Músicas
├── novels/
│   └── martial_world/
│       └── capitulos/      ← Capítulos JSON
├── config/
│   └── progresso.json      ← Progresso salvo
├── src/
├── extratores/
└── core/
```

## 🚀 Benefícios da Compilação

✅ **Não precisa instalar Python**
✅ **Não precisa instalar dependências**
✅ **Funciona em qualquer Windows 10/11**
✅ **Executável portátil** (pode rodar de pen drive)
✅ **Interface gráfica** completa e funcional

## ⚠️ Observações

- O executável é **totalmente standalone**
- Não modifica o registro do Windows
- Não instala nada no sistema
- Pode ser deletado a qualquer momento
- Conexão com internet é necessária apenas para narração (Edge TTS online)
- As músicas e capítulos já estão incluídos

## 🐛 Solução de Problemas

### Executável não abre
- Verificar se o antivírus bloqueou (adicionar exceção)
- Clicar com botão direito → Propriedades → Desbloquear
- Executar como Administrador

### Erro de DLL faltando
- Certificar que a pasta `_internal` está no mesmo local do `.exe`
- Reinstalar Microsoft Visual C++ Redistributable 2015-2022

### Narração não funciona
- Verificar conexão com internet
- Edge TTS requer conexão para sintetizar voz

## 📊 Tamanhos Aproximados

- Executável: **7 MB**
- Bibliotecas (_internal): **80-100 MB**
- Capítulos (123 disponíveis): **5-10 MB**
- Músicas: **5-10 MB** (loops de 3 minutos)
- **Total: ~100-130 MB**

---

✅ **Pronto para distribuir!**

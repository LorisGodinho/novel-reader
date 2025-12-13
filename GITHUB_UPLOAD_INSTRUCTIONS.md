# 🚀 Como subir o Novel Reader para o GitHub

## Opção 1: Usando o Script Automático

1. Execute o arquivo `upload_github.bat` (duplo clique)
2. Siga as instruções na tela

## Opção 2: Manual (Linha de Comando)

### Passo 1: Instalar Git (se não tiver)
Baixe em: https://git-scm.com/download/win

### Passo 2: Configurar Git (primeira vez)
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

### Passo 3: Inicializar Repositório
```bash
cd c:\Users\loris\Desktop\projetos\novel_reader
git init
git add .
git commit -m "🎉 Initial commit - Novel Reader v2.0"
git branch -M main
```

### Passo 4: Criar Repositório no GitHub
1. Acesse: https://github.com/new
2. Nome do repositório: `novel-reader`
3. Descrição: "Sistema avançado de narração de novels com TTS e interface moderna"
4. Público ou Privado (sua escolha)
5. **NÃO** adicione README, .gitignore ou licença
6. Clique em "Create repository"

### Passo 5: Conectar e Fazer Push
```bash
# Substitua SEU_USUARIO pelo seu username do GitHub
git remote add origin https://github.com/SEU_USUARIO/novel-reader.git
git push -u origin main
```

## Opção 3: Usando GitHub Desktop

1. Baixe GitHub Desktop: https://desktop.github.com/
2. Instale e faça login com sua conta GitHub
3. File → Add Local Repository
4. Selecione a pasta: `c:\Users\loris\Desktop\projetos\novel_reader`
5. Clique em "Publish repository"
6. Configure nome e descrição
7. Clique em "Publish repository"

## 🎯 Estrutura Recomendada do Repositório

```
novel-reader/
├── README.md                 ✅ Criado
├── .gitignore               ✅ Existe
├── requirements.txt          ✅ Existe
├── upload_github.bat         ✅ Criado
└── [resto dos arquivos]      ✅ Prontos
```

## ⚠️ Antes de Fazer Push

### Revisar arquivos sensíveis:
- `config/progresso.json` (seu progresso pessoal)
- `config/elevenlabs_config.py` (chaves de API se houver)

### Arquivos grandes:
- Considere se quer incluir `novels/` (pode ser grande)
- Verifique `assets/audio/` (arquivos de áudio)

### Editar .gitignore se necessário:
```bash
# Descomentar estas linhas se quiser ignorar:
# novels/
# assets/audio/
```

## 🔧 Comandos Úteis

### Ver status dos arquivos:
```bash
git status
```

### Ver arquivos que serão commitados:
```bash
git diff --cached
```

### Desfazer último commit (se errou):
```bash
git reset --soft HEAD~1
```

### Atualizar repositório:
```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

## 📝 Sugestão de Descrição para o Repositório

**Descrição curta:**
> Sistema avançado de narração de novels com TTS, interface moderna e música adaptativa

**Tópicos/Tags:**
- `python`
- `tts`
- `text-to-speech`
- `novel-reader`
- `edge-tts`
- `tkinter`
- `pygame`
- `audiobook`
- `narration`

## ✅ Checklist Final

- [ ] Git instalado
- [ ] Repositório inicializado
- [ ] Arquivos adicionados
- [ ] Commit criado
- [ ] Repositório criado no GitHub
- [ ] Remote configurado
- [ ] Push realizado com sucesso

## 🆘 Problemas Comuns

### "Git não é reconhecido"
- Instale o Git: https://git-scm.com/download/win
- Reinicie o terminal após instalar

### "Permission denied (publickey)"
- Configure SSH ou use HTTPS
- Para HTTPS: use token pessoal ao invés de senha

### "Repository not found"
- Verifique se o repositório foi criado no GitHub
- Confirme a URL do remote: `git remote -v`

### Arquivos muito grandes
```bash
# Para novels grandes, usar Git LFS
git lfs install
git lfs track "*.json"
git lfs track "*.mp3"
```

---

**Depois do upload, compartilhe o link:**
`https://github.com/SEU_USUARIO/novel-reader`

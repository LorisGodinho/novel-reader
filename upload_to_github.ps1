# Script para upload do Novel Reader para GitHub
# Repositório: git@github.com:LorisGodinho/novel-reader.git

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Novel Reader - GitHub Upload" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Git está instalado
try {
    $gitVersion = git --version
    Write-Host "[✓] Git detectado: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "[✗] Git não está instalado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Por favor, instale o Git:" -ForegroundColor Yellow
    Write-Host "https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "[1/6] Inicializando repositório Git..." -ForegroundColor Yellow
git init

Write-Host ""
Write-Host "[2/6] Adicionando todos os arquivos..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "[3/6] Criando commit inicial..." -ForegroundColor Yellow
git commit -m "🎉 Initial commit - Novel Reader v2.0

Sistema completo de narração de novels com:
- Interface gráfica moderna com tema escuro
- TTS usando Edge Neural Voices
- Sistema de cache LRU otimizado
- Pré-carregamento inteligente
- Controles de velocidade (0.5x-3x)
- Música de fundo adaptativa
- Transição automática entre capítulos
- Salvamento de progresso"

Write-Host ""
Write-Host "[4/6] Configurando branch principal como 'main'..." -ForegroundColor Yellow
git branch -M main

Write-Host ""
Write-Host "[5/6] Adicionando remote 'origin'..." -ForegroundColor Yellow
git remote add origin git@github.com:LorisGodinho/novel-reader.git

Write-Host ""
Write-Host "[6/6] Fazendo push para GitHub..." -ForegroundColor Yellow
git push -u origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  ✓ Upload concluído com sucesso!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Repositório disponível em:" -ForegroundColor Cyan
Write-Host "https://github.com/LorisGodinho/novel-reader" -ForegroundColor Cyan
Write-Host ""
pause

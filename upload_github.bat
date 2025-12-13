@echo off
echo ========================================
echo   Novel Reader - GitHub Upload Script
echo ========================================
echo.

REM Verificar se Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Git não está instalado!
    echo.
    echo Por favor, instale o Git:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/7] Inicializando repositório Git...
git init

echo.
echo [2/7] Adicionando todos os arquivos...
git add .

echo.
echo [3/7] Criando commit inicial...
git commit -m "🎉 Initial commit - Novel Reader v2.0 - Sistema completo de narração TTS com interface moderna"

echo.
echo [4/7] Configurando branch principal como 'main'...
git branch -M main

echo.
echo ========================================
echo   PRÓXIMOS PASSOS MANUAIS:
echo ========================================
echo.
echo 1. Acesse: https://github.com/new
echo 2. Crie um novo repositório com o nome: novel-reader
echo 3. NÃO adicione README, .gitignore ou licença
echo 4. Copie a URL do repositório (ex: https://github.com/SEU_USUARIO/novel-reader.git)
echo 5. Execute o comando abaixo substituindo SEU_USUARIO:
echo.
echo    git remote add origin https://github.com/SEU_USUARIO/novel-reader.git
echo    git push -u origin main
echo.
echo ========================================
pause

# Script para finalizar configuração das BGMs
$bgmPath = "c:\Users\loris\Desktop\projetos\novel_reader\assets\audio\background"

Write-Host "🎵 FINALIZANDO CONFIGURAÇÃO DAS BGMs`n" -ForegroundColor Cyan

# 1. Limpar temporários
Write-Host "🗑️ Limpando arquivos temporários..."
Remove-Item "$bgmPath\temp_*" -Force -ErrorAction SilentlyContinue
Write-Host "✅ Temporários removidos`n"

# 2. Restaurar reading_chinese_1 do backup
Write-Host "📥 Restaurando reading_chinese_1 do backup..."
Copy-Item "$bgmPath\_backup_old\reading_chinese_1.mp3" "$bgmPath\" -Force
Write-Host "✅ reading_chinese_1.mp3 restaurada`n"

# 3. Usar as sintéticas do backup para as outras 2 de leitura
Write-Host "📥 Copiando BGMs sintéticas de leitura..."
Copy-Item "$bgmPath\_backup_old\reading_synthetic_2.mp3" "$bgmPath\reading_chinese_2.mp3" -Force
Copy-Item "$bgmPath\_backup_old\reading_synthetic_3.mp3" "$bgmPath\reading_chinese_3.mp3" -Force
Write-Host "✅ reading_chinese_2.mp3 (sintética) copiada"
Write-Host "✅ reading_chinese_3.mp3 (sintética) copiada`n"

# 4. Verificar resultado final
Write-Host "=" * 70
Write-Host "📊 BGMs FINAIS:" -ForegroundColor Green
Write-Host "=" * 70

Get-ChildItem "$bgmPath\*.mp3" -Exclude "temp_*" | 
    Select-Object Name, @{Name="Tamanho(MB)";Expression={[math]::Round($_.Length/1MB, 2)}} | 
    Sort-Object Name | 
    Format-Table -AutoSize

Write-Host "`n✅ Configuração concluída!" -ForegroundColor Green
Write-Host "🎮 Execute: python novel_reader_gui.py" -ForegroundColor Cyan

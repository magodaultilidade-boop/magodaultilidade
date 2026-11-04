@echo off
title Salvando no GitHub...
color 0A
echo ========================================================
echo   ENVIANDO PROJETO PARA O GITHUB (BACKUP SEGURO NA NUVEM)
echo ========================================================
echo.
echo Conectando ao GitHub...
"C:\Program Files\Git\cmd\git.exe" push origin main
echo.
echo ========================================================
if %ERRORLEVEL% EQU 0 (
    echo [SUCESSO] Seu projeto e o Obsidian estao 100%% salvos no GitHub!
) else (
    echo [AVISO] Se pediu login no navegador, confirme para concluir.
)
echo ========================================================
echo.
pause


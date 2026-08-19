@echo off
title Hato - Publicar en GitHub
echo.
echo ==========================================
echo   HATO - PUBLICAR CAMBIOS EN GITHUB
echo ==========================================
echo.

set /p MENSAJE=Escribe el mensaje del commit: 
if "%MENSAJE%"=="" (
    echo.
    echo ERROR: Debes escribir un mensaje de commit.
    pause
    exit /b 1
)

echo.
echo --- Estado actual ---
ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git status"

echo.
echo --- Agregando cambios al commit ---
echo Se excluye explicitamente dbHato.sqlite3
ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git add -A -- . ':(exclude)dbHato.sqlite3'"

if errorlevel 1 (
    echo.
    echo ERROR al preparar los cambios.
    pause
    exit /b 1
)

echo.
echo --- Cambios preparados ---
ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git status && git diff --cached --stat"

echo.
set /p CONFIRMAR=Confirmar commit y push a origin/main? [S/N]: 
if /I not "%CONFIRMAR%"=="S" (
    echo.
    echo Operacion cancelada. No se hizo commit ni push.
    pause
    exit /b 0
)

echo.
echo --- Commit ---
ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git commit -m \"%MENSAJE%\""

if errorlevel 1 (
    echo.
    echo El commit no se pudo completar.
    pause
    exit /b 1
)

echo.
echo --- Push a GitHub ---
ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git push origin main"

if errorlevel 1 (
    echo.
    echo ERROR: El push fallo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   PUBLICACION COMPLETADA
echo ==========================================
ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git status && git log -1 --oneline"
echo.
pause

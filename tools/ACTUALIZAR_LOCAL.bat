@echo off
title Hato - Actualizar Local desde GitHub
echo.
echo ==========================================
echo   HATO - ACTUALIZAR LOCAL
echo ==========================================
echo.

ssh htovar@192.168.56.101 "cd ~/Sistemas/Hato/app && git status && git pull --rebase origin main && git status"

echo.
echo ==========================================
echo   Actualizacion terminada.
echo ==========================================
pause

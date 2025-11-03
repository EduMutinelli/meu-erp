@echo off
chcp 65001 > nul
title ERP System - API
echo ===============================
echo    INICIANDO API DO ERP SYSTEM
echo ===============================
echo.

cd /d "%~dp0"
call check_environment.bat

echo.
echo Iniciando servidor da API...
echo 📍 URL: http://localhost:8001
echo ⏹️  Pressione Ctrl+C para parar
echo.

cd api
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
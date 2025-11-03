@echo off
chcp 65001 > nul
title ERP System - Full Stack
echo ================================
echo    INICIANDO ERP SYSTEM COMPLETO
echo ================================
echo.

REM Verifica se o Python está instalado
python --version > nul 2>&1
if errorlevel 1 (
    echo ERRO: Python não encontrado!
    echo Instale o Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Verificando dependências...
python -c "import fastapi, uvicorn, streamlit, requests, pandas" > nul 2>&1
if errorlevel 1 (
    echo Dependências não encontradas. Instalando...
    
    if exist "requirements\api_requirements.txt" (
        echo Instalando dependências da API...
        python -m pip install -r requirements\api_requirements.txt
    )

    if exist "requirements\cliente_requirements.txt" (
        echo Instalando dependências do Cliente...
        python -m pip install -r requirements\cliente_requirements.txt
    )
) else (
    echo Dependências já instaladas.
)

echo.
echo Iniciando API e Frontend...
echo.
echo API: http://localhost:8001
echo Frontend: http://localhost:8501
echo.
echo Pressione Ctrl+C em qualquer janela para parar
echo.

REM Inicia a API em uma nova janela
start "ERP API" cmd /k "cd /d %~dp0\api && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001"

timeout /t 5 /nobreak > nul

echo Iniciando Frontend...
cd cliente
python -m streamlit run main.py

pause
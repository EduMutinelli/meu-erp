@echo off
chcp 65001 > nul
title Verificador de Ambiente - ERP System
echo ================================
echo    VERIFICANDO AMBIENTE DO ERP
echo ================================
echo.

echo 1. Verificando Python...
python --version
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo 📥 Baixe em: https://www.python.org/downloads/
    goto :error
) else (
    echo ✅ Python encontrado!
)

echo.
echo 2. Verificando dependências...
python -c "import streamlit, fastapi, pandas, sqlalchemy, requests" > nul 2>&1
if errorlevel 1 (
    echo ❌ Algumas dependências estão faltando!
    echo 💡 Execute install.bat para instalar
) else (
    echo ✅ Todas as dependências OK!
)

echo.
echo 3. Verificando estrutura de pastas...
if exist "data" (echo ✅ Pasta data OK) else (echo ❌ Pasta data faltando)
if exist "logs" (echo ✅ Pasta logs OK) else (echo ❌ Pasta logs faltando)
if exist "api" (echo ✅ Pasta api OK) else (echo ❌ Pasta api faltando)
if exist "cliente" (echo ✅ Pasta cliente OK) else (echo ❌ Pasta cliente faltando)
if exist "requirements" (echo ✅ Pasta requirements OK) else (echo ❌ Pasta requirements faltando)

echo.
echo 4. Verificando arquivos essenciais...
if exist "api\main.py" (echo ✅ api\main.py OK) else (echo ❌ api\main.py faltando)
if exist "cliente\main.py" (echo ✅ cliente\main.py OK) else (echo ❌ cliente\main.py faltando)

echo.
echo =================================
echo    VERIFICAÇÃO CONCLUÍDA!
echo =================================
goto :end

:error
echo.
echo ❌ Problemas encontrados! Corrija antes de executar o sistema.
:end
pause
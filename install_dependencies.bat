@echo off
chcp 65001 > nul
title Instalador do Sistema ERP
echo ===============================
echo    INSTALANDO SISTEMA ERP
echo ===============================
echo.

echo Instalando dependências...
python -m pip install -r requirements/cliente_requirements.txt

echo.
echo ✅ Instalação concluída!
echo 🚀 Execute start_frontend.bat para iniciar
echo.
pause
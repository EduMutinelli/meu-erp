@echo off
chcp 65001 > nul
title Sistema ERP
echo ===============================
echo    INICIANDO SISTEMA ERP
echo ===============================
echo.

cd cliente
python -m streamlit run main.py
pause
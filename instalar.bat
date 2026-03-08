@echo off
echo.
echo ==========================================
echo    DARK VOICE CLONER v2 - SETUP
echo ==========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Instale em: https://python.org/downloads
    echo Marque "Add Python to PATH" na instalacao!
    pause
    exit /b 1
)

echo [1/3] Criando ambiente virtual...
py -3.11 -m venv venv 2>nul || python -m venv venv
if errorlevel 1 (
    echo [ERRO] Falha ao criar ambiente virtual.
    pause
    exit /b 1
)

echo [2/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo [3/3] Instalando dependencias...
python -m pip install --upgrade pip -q
pip install flask werkzeug soundfile numpy kokoro-onnx
pip install misaki[en,ja,ko,zh,es,fr,de,it,pt,ru,ar,hi]

echo.
echo ==========================================
echo  Pronto! Execute: iniciar.bat
echo ==========================================
pause

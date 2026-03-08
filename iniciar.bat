@echo off
call venv\Scripts\activate.bat 2>nul
if errorlevel 1 (
    echo Ambiente virtual nao encontrado. Execute instalar.bat primeiro.
    pause
    exit /b 1
)
echo.
echo  Dark Voice Cloner v2 iniciando...
echo  Acesse: http://localhost:5000
echo.
python app.py
pause

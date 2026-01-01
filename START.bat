@echo off
echo ========================================
echo RAG++ Analytical Reasoning Engine
echo ========================================
echo.

echo Starting Backend Server...
cd backend
start cmd /k "python main.py"

timeout /t 5 /nobreak >nul

echo.
echo Opening Frontend...
cd ..\frontend
start index.html

echo.
echo ========================================
echo System Started!
echo ========================================
echo Backend: http://localhost:8000
echo Frontend: Opening in browser...
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to exit...
pause >nul

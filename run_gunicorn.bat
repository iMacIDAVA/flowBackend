@echo off
cd /d "%~dp0"
echo Starting Django Service with Gunicorn...
gunicorn consultation_platform.wsgi:application --bind 0.0.0.0:8000 --workers 4
pause 
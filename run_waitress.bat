@echo off
cd /d "%~dp0"
echo Starting Django Service with Waitress...
python -m waitress --host=0.0.0.0 --port=8000 consultation_platform.wsgi:application
pause 
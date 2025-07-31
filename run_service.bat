@echo off
cd /d "%~dp0"
echo Starting Django Service...
python manage.py runserver 0.0.0.0:8000
pause 
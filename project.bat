@echo off
cd /d C:\msys64\mingw64\include\system\Project\braille_converter
venv\Scripts\python.exe manage.py runserver
pause


@REM venv\Scripts\activate.ps1
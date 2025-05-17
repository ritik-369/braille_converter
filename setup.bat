@echo off
SET VENV_DIR=venv

:: Clear the screen
cls

:: Remove existing virtual environment if it exists
IF EXIST %VENV_DIR% (
    echo Removing existing virtual environment...
    rmdir /s /q %VENV_DIR%
)

:: Create a new virtual environment
echo Creating a new virtual environment...
python -m venv %VENV_DIR%

:: Activate virtual environment in a new cmd session
echo Activating virtual environment...
call %VENV_DIR%\Scripts\activate

:: Ensure the virtual environment's Python & Pip are used
SET PYTHON=%VENV_DIR%\Scripts\python.exe
SET PIP=%VENV_DIR%\Scripts\pip.exe

:: Install dependencies
IF EXIST requirements.txt (
    echo Installing dependencies...
    %PIP% install -r requirements.txt
) ELSE (
    echo No requirements.txt found, skipping installation.
)

:: Run Django migrations
echo Running Django migrations...
%PYTHON% manage.py makemigrations
%PYTHON% manage.py migrate

cls
:: Confirm completion
echo.
echo Setup complete!
echo Press any key to exit...
pause >nul

@echo off
setlocal

REM Function to check if Python is installed
:CheckPython
python --version 2>nul | findstr /R "^Python 3" >nul
if errorlevel 1 (
    echo Python 3 is not installed. Attempting to install...
    goto InstallPython
) else (
    goto CheckTkinter
)

REM Function to install Python using msiexec
:InstallPython
set PYTHON_MSI_URL=https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.msi
set MSI_INSTALLER=python_installer.msi

echo Downloading Python MSI installer...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_MSI_URL% -OutFile %MSI_INSTALLER%"

echo Installing Python...
msiexec /i %MSI_INSTALLER% /quiet /qn ALLUSERS=1 ADDLOCAL=ALL TARGETDIR="%ProgramFiles%\Python310"

if errorlevel 1 (
    echo Python installation failed. Please install Python manually.
    pause
    exit /b
) else (
    echo Python installed successfully.
    del %MSI_INSTALLER%
    setx PATH "%ProgramFiles%\Python310;%ProgramFiles%\Python310\Scripts;%PATH%"
    goto CheckPython
)

REM Check for tkinter module
:CheckTkinter
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo tkinter is not installed.
    echo Please install it by running: pip install tk
    pause
    exit /b
)

REM Run the Python GUI script
:RunScript
python "nail_polish_gui.py"
pause

@echo off

REM Clean previous builds
rmdir /s /q build
rmdir /s /q dist

REM Install dependencies
pip install -r requirements.txt

REM Run tests
pytest
if errorlevel 1 (
    echo Tests failed
    exit /b 1
)

REM Build package
python setup.py sdist bdist_wheel

REM Build executable
pyinstaller pyinstaller.spec --clean

echo Build complete! Executable is in dist/
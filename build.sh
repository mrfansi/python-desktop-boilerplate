#!/bin/bash

# Clean previous builds
rm -rf build/ dist/

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest || exit 1

# Build package
python setup.py sdist bdist_wheel

# Build executable
pyinstaller pyinstaller.spec --clean

echo "Build complete! Executable is in dist/"
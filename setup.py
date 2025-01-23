from setuptools import setup, find_packages

setup(
    name="python-desktop-boilerplate",
    version="1.0.0",
    description="Modern Python desktop application boilerplate",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PySide6>=6.5.0",
        "dependency-injector>=4.41.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "run-app=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
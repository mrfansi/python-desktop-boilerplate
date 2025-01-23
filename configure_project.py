#!/usr/bin/env python3
"""Project configuration script for Python Desktop Boilerplate."""

import os
import re
import secrets
import json
from pathlib import Path
from typing import Dict

def remove_quotes(value: str) -> str:
    """Remove surrounding quotes from value if present."""
    return value.strip('"') if value.startswith('"') and value.endswith('"') else value

def add_quotes_if_contains_spaces(value: str) -> str:
    """Add quotes around value if it contains spaces."""
    return f'"{value}"' if ' ' in value else value

def get_project_details() -> Dict[str, str]:
    """Prompt user for project details."""
    print("Python Desktop Boilerplate Configuration")
    print("=" * 40)
    
    details = {
        'project_name': add_quotes_if_contains_spaces(input("Project name: ").strip()),
        'project_version': input("Project version [1.0.0]: ").strip() or "1.0.0",
        'description': add_quotes_if_contains_spaces(input("Project description: ").strip()),
        'author': add_quotes_if_contains_spaces(input("Author name: ").strip()),
        'author_email': add_quotes_if_contains_spaces(input("Author email: ").strip()),
        'license': input("License [MIT]: ").strip() or "MIT",
    }
    
    # Generate slug version of project name
    details['project_slug'] = re.sub(r'[^a-zA-Z0-9]+', '-', details['project_name']).lower()
    
    return details

def generate_env_variables(project_name: str, project_version: str) -> Dict[str, str]:
    """Generate required environment variables."""
    return {
        'APP_NAME': project_name,
        'APP_VERSION': project_version,
        'SECRET_KEY': secrets.token_urlsafe(32),
        'DEBUG_MODE': 'true'
    }

def update_setup_py(project_details: Dict[str, str]):
    """Update setup.py with project details."""
    setup_path = Path('setup.py')
    if not setup_path.exists():
        raise FileNotFoundError("setup.py not found")
        
    with open(setup_path, 'r') as f:
        content = f.read()
        
    replacements = {
        'name="python-desktop-boilerplate"': f'name="{remove_quotes(project_details["project_slug"])}"',
        'version="1.0.0"': f'version="{remove_quotes(project_details["project_version"])}"',
        'description="Modern Python desktop application boilerplate"': f'description="{remove_quotes(project_details["description"])}"',
        'author="Your Name"': f'author="{remove_quotes(project_details["author"])}"',
        'author_email="your.email@example.com"': f'author_email="{remove_quotes(project_details["author_email"])}"',
        'License :: OSI Approved :: MIT License': f'License :: OSI Approved :: {project_details["license"]} License',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(setup_path, 'w') as f:
        f.write(content)

def update_readme(project_details: Dict[str, str]):
    """Update README.md title and description only."""
    readme_path = Path('README.md')
    if not readme_path.exists():
        raise FileNotFoundError("README.md not found")
        
    with open(readme_path, 'r') as f:
        content = f.read()
        
    # Update only title and description
    content = re.sub(
        r'# Python Desktop Boilerplate\n\nA modern Python desktop application boilerplate',
        f'# {project_details["project_name"]}\n\n{project_details["description"]}',
        content,
        1  # Only replace first occurrence
    )
    
    with open(readme_path, 'w') as f:
        f.write(content)

def update_config_json(project_details: Dict[str, str]):
    """Update config.json with project details."""
    config_path = Path('config.json')
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")
        
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        # Update name and version (remove quotes if present)
        config['app']['name'] = remove_quotes(project_details['project_name'])
        config['app']['version'] = remove_quotes(project_details['project_version'])
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in config.json: {str(e)}")

def create_env_file(env_vars: Dict[str, str]):
    """Create or update .env file with environment variables."""
    env_path = Path('.env')
    with open(env_path, 'w') as f:
        for key, value in env_vars.items():
            f.write(f'{key}={value}\n')

def main():
    try:
        # Get project details
        project_details = get_project_details()
        
        # Generate environment variables
        env_vars = generate_env_variables(
            project_details['project_name'],
            project_details['project_version']
        )
        
        # Update configuration files
        update_setup_py(project_details)
        update_readme(project_details)
        update_config_json(project_details)
        create_env_file(env_vars)
        
        print("\nProject configuration complete!")
        print(f"Created/updated files: .env, setup.py, README.md, config.json")
        print("\nNext steps:")
        print("1. Review the configuration files")
        print("2. Run 'pip install -r requirements.txt' to install dependencies")
        print("3. Run 'python main.py' to start the application")
        
    except Exception as e:
        print(f"\nError during configuration: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
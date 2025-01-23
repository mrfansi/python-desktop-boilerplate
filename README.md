# Python Desktop Boilerplate

A modern Python desktop application boilerplate using PySide6 and dependency injection.

## Features

- Qt-based GUI framework
- Dependency injection architecture
- Environment-based configuration
- Structured error handling
- Production-ready logging
- Comprehensive testing infrastructure
- Secure environment validation

## Requirements

- Python 3.10+
- PySide6
- Dependency Injector

## Development Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Environment Variables

Required:
- `APP_NAME`: Application name
- `APP_VERSION`: Application version
- `SECRET_KEY`: Secret key for encryption

Optional:
- `DEBUG_MODE`: Enable debug mode (true/false)
- `DATABASE_URL`: Database connection URL

## Testing

Run tests with:
```bash
pytest
```

Generate coverage report:
```bash
coverage run -m pytest
coverage report -m
```

## Security Considerations

- Always keep `.env` file out of version control
- Use strong secret keys
- Validate all environment variables
- Implement proper error handling

## Docker Deployment

Build the Docker image:
```bash
docker build -t python-desktop-app .
```

Run the container:
```bash
docker run -it --rm \
  -e SECRET_KEY=your_secret_key \
  -e APP_NAME="My App" \
  python-desktop-app
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Write tests for new features
4. Submit pull request

## License

MIT License
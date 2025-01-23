#!/bin/bash
set -e

# Set default environment variables
export APP_NAME=${APP_NAME:-"Python Desktop App"}
export APP_VERSION=${APP_VERSION:-"1.0.0"}
export DEBUG_MODE=${DEBUG_MODE:-"false"}

# Validate required environment variables
required_vars=("SECRET_KEY")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "Error: $var is not set"
        exit 1
    fi
done

# Run database migrations if needed
if [ -f "manage.py" ]; then
    python manage.py migrate
fi

# Execute the command
exec "$@"
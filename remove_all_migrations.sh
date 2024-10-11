#!/bin/bash

# Define the path to your project's main directory
PROJECT_PATH="."

# Go to your Django project's directory
cd "$PROJECT_PATH"

# Find all "migrations" directories and remove all Python files within them, excluding __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

# Print a message when done
echo "Deleted all migration files (except __init__.py)"

#!/usr/bin/env bash
# exit on error
set -o errexit
# Activate the virtual environment
source /opt/render/project/src/.venv/bin/activate

# Upgrade pip and install poetry
pip install --upgrade pip
pip install poetry==1.5.1

# Install dependencies using poetry
poetry install

# Run Django management commands
python manage.py collectstatic --no-input
python manage.py migrate

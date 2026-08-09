#!/usr/bin/env bash

ENV_NAME="my_env"

echo "Creating virtual environment: $ENV_NAME"
python3 -m venv $ENV_NAME

echo "Activating environment"
source $ENV_NAME/bin/activate

echo "Upgrading pip"
pip install --upgrade pip

echo "Installing dependencies"
pip install -r requirements.txt

echo "Done!"
echo "To activate later, run:"
echo "source $ENV_NAME/bin/activate"
#!/bin/bash

echo "Setting up your ANM project environment..."

# Creating virtual environment
if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "Virtual environment created."
fi

# Activating the virtual environment just created
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Installing dependencies
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
  echo "Dependencies installed from requirements.txt."
else
  echo "No requirements.txt found, installing default packages."
  pip install pandas numpy matplotlib networkx cerberus pymongo
fi

# Installing tkinter
if [ "$(uname)" == "Linux" ]; then
  echo "Checking for tkinter (may require sudo permissions)..."
  sudo apt-get update
  sudo apt-get install -y python3-tk
fi

echo "Setup complete. To activate the environment use:"
echo "source venv/bin/activate"
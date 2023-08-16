#!/bin/bash

# Navigate to 'client' directory
cd client

# Set up a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Deactivate the virtual environment
python3 setups.py

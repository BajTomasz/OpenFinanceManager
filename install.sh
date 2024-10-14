#!/bin/bash

python -m  venv .venv   
source .venv/bin/activate    
pip install -r requirements.txt
black *.py --line-length 120
isort *.py
flake8 *.py --max-line-length 120
python main.py
deactivate

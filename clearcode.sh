#!/bin/bash

source .venv/bin/activate    
black *.py --line-length 120
isort *.py
flake8 *.py --max-line-length 120
deactivate
#!/bin/bash -e 

## pytest
python -m pytest "src/tests" 

## Coverage
python -m pytest "src/tests" -p no:warnings --cov="src" --cov-report html


## Linting
flake8 src
black src --check
isort src

## Security
bandit -c .bandit.yml -r .
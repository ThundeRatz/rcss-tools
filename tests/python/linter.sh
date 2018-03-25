#!/bin/bash
set -e
cd "$(dirname "$0")"/../..
flake='python3 -m flake8 --max-line-length=100 --max-complexity=10'

# Let __init__.py have unused imports
$flake --exclude=__init__.py .
$flake --filename=__init__.py --ignore=F401 .

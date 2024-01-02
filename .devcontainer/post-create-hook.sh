#!/bin/bash

set -euf
set -o pipefail

poetry install

echo "Installing pre-commit hooks..."
pre-commit install
echo "Done."

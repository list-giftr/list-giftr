#!/bin/bash

set -euf
set -o pipefail

poetry install

echo "Installing pre-commit hooks..."
poetry run pre-commit install
echo "Done."

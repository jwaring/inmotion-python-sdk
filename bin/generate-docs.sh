#!/usr/bin/env bash
# Generate static HTML API docs from the inmotion package's docstrings using pdoc, themed to
# match inmotion.io (see docs-template/).
#
# Usage:
#   bin/generate-docs.sh
#
# Override the output location with INMOTION_DOCS_DIR if you don't want the
# default (./docs). Requires the 'dev' optional dependency group
# (`uv pip install -e '.[dev]'`).

set -euo pipefail

DOCS_DIR="${INMOTION_DOCS_DIR:-docs}"

cd "$(dirname "$0")/.."

uv run pdoc \
    --output-directory "$DOCS_DIR" \
    --template-directory docs-template \
    --logo inmotion-logo.svg \
    --logo-link https://inmotion.io \
    --footer-text "inmotion $(uv run python -c 'import importlib.metadata as m; print(m.version("inmotion-sdk"))')" \
    inmotion

cp docs-template/inmotion-logo.svg "$DOCS_DIR/"

echo
echo "Docs generated at $DOCS_DIR/index.html"

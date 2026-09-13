#!/usr/bin/env bash
# Build inmotion and publish it into a local wheelhouse directory so that other
# local projects can depend on it as an ordinary `inmotion>=X.Y.Z` dependency,
# resolved via `uv`'s --find-links mechanism, without hardcoding a filesystem
# path to this repository.
#
# Usage:
#   bin/publish-local.sh
#
# Override the wheelhouse location with INMOTION_WHEELHOUSE_DIR if you don't
# want the default (~/.local/share/inmotion-wheelhouse). Consumers must set
# the same directory via UV_FIND_LINKS when running `uv sync` / `uv run`.

set -euo pipefail

WHEELHOUSE_DIR="${INMOTION_WHEELHOUSE_DIR:-$HOME/.local/share/inmotion-wheelhouse}"

cd "$(dirname "$0")/.."

mkdir -p "$WHEELHOUSE_DIR"

echo "Building inmotion..."
uv build --out-dir "$WHEELHOUSE_DIR"

echo
echo "Published to $WHEELHOUSE_DIR:"
ls -1 "$WHEELHOUSE_DIR"
echo
echo "Consumers should resolve it via:"
echo "  export UV_FIND_LINKS=\"$WHEELHOUSE_DIR\""
echo "  uv sync"

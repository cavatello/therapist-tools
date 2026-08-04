#!/bin/bash
# Double-click this file in Finder to start the local preview server.
cd "$(dirname "$0")/.."
echo "Starting local preview for: $(pwd)"
exec python3 _dev/serve.py 8080

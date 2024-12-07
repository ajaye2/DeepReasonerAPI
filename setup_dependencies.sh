#!/bin/bash

# Print the current directory and list files for debugging
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

# Install the root package as editable without caching
pip install --no-cache-dir -e .

# Print success message
echo "All dependencies installed successfully."

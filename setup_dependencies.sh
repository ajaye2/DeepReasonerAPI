#!/bin/bash

# Print the current directory and list files for debugging
echo "Current directory: $(pwd)"
echo "Files in current directory:"
ls -la

# Navigate to the submodule directory
cd algorithms/llm-reasoners

# Install the submodule as editable without caching
pip install --no-cache-dir -e .

# Return to the root directory
cd ../../

# Install the root dependencies without caching
pip install --no-cache-dir -r requirements.txt

# Print success message
echo "Submodule dependencies installed successfully."

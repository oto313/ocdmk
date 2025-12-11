#!/bin/bash
# Wrapper script to run generate_schematics.py with the virtual environment

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Set KiCad symbol directories for different versions
export KICAD_SYMBOL_DIR="/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
export KICAD8_SYMBOL_DIR="/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
export KICAD7_SYMBOL_DIR="/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"
export KICAD6_SYMBOL_DIR="/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols"

# Activate the virtual environment and run the script
source venv_schematics/bin/activate
python3 generate_schematics.py "$@"


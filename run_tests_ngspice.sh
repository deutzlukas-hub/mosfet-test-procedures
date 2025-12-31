#!/bin/bash

# Stop on error
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_DIR="$SCRIPT_DIR/tests/ngspice"
DATA_DIR="$SCRIPT_DIR/results/data/ngspice"
MODELS_DIR="$SCRIPT_DIR/models"

TECHNOLOGY="$1"
MODEL="$2"
TEST_SUBDIR="$3"

# Make sure MODEL is provided
if [ -z "$MODEL" ]; then
    echo "Usage: $0 <MODEL>"
    exit 1
fi

# Append TEST_SUBDIR to TEST_DIR path if TEST_SUBDIR is provided as second argument
if [ -n "$TEST_SUBDIR" ]; then
    TEST_PATH="$TEST_DIR/$TEST_SUBDIR"
else
    TEST_PATH="$TEST_DIR"
fi

TMP_INCLUDE_DIR="$SCRIPT_DIR/tests/ngspice/tmp"
mkdir -p "$TMP_INCLUDE_DIR"

# Write the include line into modelcard.nmos/pmos (tests include these temp files)
cat > "$TMP_INCLUDE_DIR/modelcard.nmos" << EOF
.include ../../../models/ngspice/$MODEL/modelcard.nmos
EOF
cat > "$TMP_INCLUDE_DIR/modelcard.pmos" << EOF
.include ../../../models/ngspice/$MODEL/modelcard.pmos
EOF
cat > "$TMP_INCLUDE_DIR/technology.params" << EOF
.include ../../../technology/ngspice/$TECHNOLOGY.params
EOF

export OSDI="./models/ngspice/$MODEL/$MODEL.osdi"

# Loop through tests in tests/ngspice
find "$TEST_PATH" -type f -name "*.sp" | while IFS= read -r file; do
    # Skip if not a regular file
    [ -f "$file" ] || continue

    FILENAME=$(basename "$file")
    PARENT_DIR=$(basename "$(dirname "$file")")
    OUTPUT_DIR="$DATA_DIR/$TECHNOLOGY/$MODEL/$PARENT_DIR"
    mkdir -p "$OUTPUT_DIR"

    FILEPATH="$OUTPUT_DIR/$FILENAME.out"

    echo ""
    echo "-------------------------------------------------------------------------------------------------------------"
    echo "Run test $FILENAME..."
    echo "-------------------------------------------------------------------------------------------------------------"

    # Export FILEPATH for decks that use it and also capture stdout to the same file
    export FILEPATH
    ngspice -b "$file"
    echo "Output saved to: $FILEPATH"

done





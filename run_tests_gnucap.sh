#!/bin/bash

# Stop on error
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_DIR="$SCRIPT_DIR/tests/gnucap"
DATA_DIR="$SCRIPT_DIR/results/data/gnucap"
MODELS_DIR="$SCRIPT_DIR/models"
TECHNOLOGY_DIR="$SCRIPT_DIR/technology"

TECHNOLOGY=$1
MODEL="$2"
TEST_SUBDIR="$3"

GNUCAP_ARGS="-a mgsim -a ./models/gnucap/${MODEL}/${MODEL}.so \
-i ./models/gnucap/${MODEL}/nmos.paramset \
-i ./models/gnucap/${MODEL}/pmos.paramset \
-i ./technology/gnucap/${TECHNOLOGY}.params"


# Append TEST_SUBDIR to TEST_DIR path if TEST_SUBDIR is provided as second argument
if [ -n "$TEST_SUBDIR" ]; then
    TEST_PATH="$TEST_DIR/$TEST_SUBDIR"
else
    TEST_PATH="$TEST_DIR"
fi


# Loop through tests in tests/gnucap
find "$TEST_PATH" -type f -name "*.gc" | while IFS= read -r file; do
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
    gnucap $GNUCAP_ARGS $file > "$FILEPATH"
    echo "Output saved to: $FILEPATH"

done
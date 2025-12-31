#!/bin/bash
# Stop on error
set -e

# Enable debug output
# set -x

# List of models (replace with your actual model names, without extension)
MODELS=("bsim4" "psp104")

TECHNOLOGY=$1
if [ -z "$TECHNOLOGY" ]; then
    TECHNOLOGY="cmos90"
fi

echo "INFO: Starting tests with technology: $TECHNOLOGY"
echo ""

# Loop through all models
for MODEL in "${MODELS[@]}"; do
    echo "=============================="
    echo "INFO: Running tests for model: $MODEL"
    echo "=============================="

    # Call run_tests.sh with the model name
    echo "INFO: Running Gnucap tests..."
    if ! "./run_tests_gnucap.sh" "$TECHNOLOGY" "$MODEL"; then
        echo "ERROR: Gnucap tests failed for model $MODEL"
    fi

    echo "INFO: Running ngspice tests..."
    if ! "./run_tests_ngspice.sh" "$TECHNOLOGY" "$MODEL"; then
        echo "ERROR: ngspice tests failed for model $MODEL"
    fi
done

echo "INFO: Finished tests!


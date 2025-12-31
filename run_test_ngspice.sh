#!/usr/bin/env bash
# Run a single ngspice test by subdir/name
#
# Usage (aligned with run_tests_ngspice.sh):
#   bash ./run_test_ngspice.sh <MODEL> <TECHNOLOGY> <SUBDIR>/<TEST_NAME_OR_PATTERN>
#
# Examples:
#   bash ./run_test_ngspice.sh bsim483 cmos90 dc/inverter.sp
#   bash ./run_test_ngspice.sh psp104 cmos90 transient/b4_ring_oscillator_5.sp
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_DIR="$SCRIPT_DIR/tests/ngspice"
RESULT_DIR_BASE="$SCRIPT_DIR/results/data/ngspice"
TMP_MODELCARD_DIR="$SCRIPT_DIR/tests/ngspice/tmp"

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <MODEL> <TECHNOLOGY> <SUBDIR>/<TEST_NAME_OR_PATTERN>" >&2
  exit 1
fi

MODEL="$1"
TECHNOLOGY="$2"
SUBDIR_AND_NAME="$3"

# Split the third argument into subdir and filename/pattern
SUBDIR="${SUBDIR_AND_NAME%%/*}"
NAME="${SUBDIR_AND_NAME#*/}"

SEARCH_ROOT="$TEST_DIR/$SUBDIR"

# Prepare tmp modelcards and technology params that include the in-tree files
mkdir -p "$TMP_MODELCARD_DIR"
cat > "$TMP_MODELCARD_DIR/modelcard.nmos" << EOF
.include ../../../models/ngspice/$MODEL/modelcard.nmos
EOF
cat > "$TMP_MODELCARD_DIR/modelcard.pmos" << EOF
.include ../../../models/ngspice/$MODEL/modelcard.pmos
EOF
cat > "$TMP_MODELCARD_DIR/technology.params" << EOF
.include ../../../technology/ngspice/$TECHNOLOGY.params
EOF

# Find matches within the specified subdir (no recursion beyond it)
mapfile -t MATCHES < <(find "$SEARCH_ROOT" -maxdepth 1 -type f -name "${NAME}" | sort)

if [[ ${#MATCHES[@]} -eq 0 ]]; then
  echo "No test matched: $SUBDIR_AND_NAME under $SEARCH_ROOT" >&2
  exit 2
fi

TEST_FILE="${MATCHES[0]}"
FILENAME="$(basename "$TEST_FILE")"
PARENT_DIR="$(basename "$(dirname "$TEST_FILE")")"
OUTPUT_DIR="$RESULT_DIR_BASE/$MODEL/$PARENT_DIR"
OUTFILE="$OUTPUT_DIR/$FILENAME.out"
mkdir -p "$OUTPUT_DIR"

# Export OSDI path and FILEPATH for decks that use it
export OSDI="./models/ngspice/$MODEL/$MODEL.osdi"
export FILEPATH="$OUTFILE"

echo "Running ngspice test: $TEST_FILE"
echo "Model: $MODEL"
echo "Technology: $TECHNOLOGY"
echo "Output: $OUTFILE"

ngspice -b "$TEST_FILE"
echo "Done. Output written to $OUTFILE"


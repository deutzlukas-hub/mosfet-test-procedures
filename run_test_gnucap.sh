#!/usr/bin/env bash
# Run a single Gnucap test by (partial) name
#
# New Usage (order changed):
#   bash ./run_single_gnucap.sh <MODEL> <SUBDIR>/<TEST_NAME_OR_PATTERN>
#
# Examples:
#   bash ./run_single_gnucap.sh psp104 transient/not.gc
#   bash ./run_single_gnucap.sh bsim483 dc/id_vg_nmos.gc
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEST_DIR="$SCRIPT_DIR/tests/gnucap"
RESULT_DIR_BASE="$SCRIPT_DIR/results/data/gnucap"

MODEL="$1"
TECHNOLOGY=$2
SUBDIR_AND_NAME="$3"

SUBDIR="${SUBDIR_AND_NAME%%/*}"
NAME="${SUBDIR_AND_NAME#*/}"

# Find matches (*.gc) within the specified subdir, exclude modules if encountered
SEARCH_ROOT="$TEST_DIR/$SUBDIR"
mapfile -t MATCHES < <(find "$SEARCH_ROOT" -maxdepth 1 -type f -name "${NAME}" | sort)

TEST_FILE="${MATCHES[0]}"
FILENAME="$(basename "$TEST_FILE")"
PARENT_DIR="$(basename "$(dirname "$TEST_FILE")")"
OUTPUT_DIR="$RESULT_DIR_BASE/$MODEL/$PARENT_DIR"
OUTFILE="$OUTPUT_DIR/$FILENAME.out"
mkdir -p "$OUTPUT_DIR"

GNUCAP_ARGS="-a mgsim -a ./models/gnucap/${MODEL}/${MODEL}.so \
-i ./models/gnucap/${MODEL}/nmos.paramset \
-i ./models/gnucap/${MODEL}/pmos.paramset \
-i ./technology/gnucap/${TECHNOLOGY}.params"

echo "Running Gnucap test: $TEST_FILE"
echo "Model: $MODEL"

gnucap $GNUCAP_ARGS "$TEST_FILE" > "$OUTFILE"
echo "Done. Output written to $OUTFILE"


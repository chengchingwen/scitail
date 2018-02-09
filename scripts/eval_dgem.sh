#!/bin/bash
set -e

python scripts/predict_input.py

echo "# -----------------------------------------------"
echo "# Evaluating DGEM model"
echo "# -----------------------------------------------"
python scitail/run.py predict \
       SciTailModelsV1/dgem/model.tar.gz \
       SciTailV1/dgem_format/input.jsonl \
       --output-file SciTailV1/dgem_format/output.jsonl \
       --silent

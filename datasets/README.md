# Datasets

This directory contains the datasets used for evaluation.

## Supported Formats
- JSON (`.json`)
- JSON Lines (`.jsonl`)
- CSV (`.csv`)

## Structure
Place your dataset files directly in this directory or organize them into subfolders by task or category.

## Metric Configuration
Metrics for each dataset are configured in `src/evaluation/registry.py`.
To add a new dataset:
1. Add your dataset file here.
2. In `src/evaluation/registry.py`, add an entry to `DATASET_METRICS_MAP` mapping your dataset name to a list of metric names.
   Example:
   ```python
   DATASET_METRICS_MAP = {
       "my_new_dataset": ["answer_accuracy", "answer_relevance"]
   }
   ```

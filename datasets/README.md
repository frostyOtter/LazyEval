# Datasets

**Place dataset files here.** Supported formats: `.json`, `.jsonl`, `.csv`.

## 📂 Structure
```
datasets/
├── manual/              # Custom manual tests
│   └── test_v1.json
├── production/          # Production logs
│   └── logs_2023.jsonl
└── README.md
```

## 📄 Format Example
Your dataset items should generally look like this:

```json
{
  "id": "item_01",
  "query": "What is the capital of France?",
  "reference": "Paris",
  "context": "Paris is the capital and most populous city of France."
}
```

## 🔌 Integration
To add new datasets, simply drop the file here and reference it in `src/evaluation/registry.py`:
```python
DATASET_METRICS_MAP = {
    "my_new_dataset": ["answer_accuracy", "answer_relevance"]
}
```

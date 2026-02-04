# LazyEval

Automated evaluation platform for language models.

## Overview

LazyEval is a simple, focused evaluation platform that:
- Loads datasets from HuggingFace (starting with `Mahesh2841/Agriculture`)
- Sends each item to your model API (OpenAI-compatible, e.g., vLLM)
- Collects responses and sends them to Langfuse for LLM-as-Judge evaluation
- Backs up results to timestamped JSON files

## Features

- ✅ **Simple Sequential Processing**: No complexity, just straightforward evaluation
- ✅ **HuggingFace Integration**: Automatic dataset loading and validation
- ✅ **OpenAI-Compatible API**: Works with vLLM or any OpenAI-compatible endpoint
- ✅ **Langfuse Integration**: Automatic trace logging and LLM-as-Judge evaluation
- ✅ **JSON Backups**: Timestamped result files for offline analysis
- ✅ **Type-Safe Configuration**: Pydantic models with validation
- ✅ **Comprehensive Logging**: Loguru for both console and file logging

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd LazyEval

# Install dependencies with uv
uv sync --dev
```

## Configuration

### 1. Environment Variables

Create a `.env` file (use `.env.example` as template):

```bash
# Model API Configuration
MODEL_NAME=your-model-name
MODEL_BASE_URL=https://your-api-endpoint.com/v1
MODEL_API_KEY=your-api-key

# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk-xxxxx
LANGFUSE_SECRET_KEY=sk-xxxxx
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 2. Application Settings

Edit `configs/config.yaml` to customize settings:

```yaml
model:
  temperature: 0.7
  top_p: 1.0
  max_tokens: 1000

dataset:
  name: "Mahesh2841/Agriculture"
  max_samples: null  # null = all samples

evaluation:
  skip_on_error: true

output:
  results_dir: "results"
  log_dir: "logs"
```

## Usage

Simply run:

```bash
uv run main.py
```

The platform will:
1. Load the Agriculture dataset from HuggingFace
2. Process each item sequentially through your model
3. Send traces to Langfuse (for LLM-as-Judge evaluation)
4. Save results to `results/results_YYYYMMDD_HHMMSS.json`
5. Log everything to `logs/lazyeval_YYYYMMDD_HHMMSS.log`

## Project Structure

```
LazyEval/
├── main.py                          # Entry point
├── src/
│   ├── config/                      # Configuration management
│   │   ├── models.py               # Pydantic config models
│   │   └── loader.py               # Config loader (env + YAML)
│   ├── datasets/                    # Dataset loaders
│   │   ├── base.py                 # Base interface
│   │   ├── models.py               # Dataset item models
│   │   └── agriculture.py          # Agriculture dataset loader
│   ├── models/                      # Model client
│   │   └── client.py               # OpenAI-compatible client
│   ├── evaluation/                  # Evaluation engine
│   │   ├── models.py               # Result models
│   │   └── runner.py               # Sequential runner
│   └── integrations/                # External integrations
│       ├── langfuse_client.py      # Langfuse exporter
│       └── json_export.py          # JSON backup exporter
├── tests/                           # Test suite
├── configs/                         # Configuration files
├── results/                         # JSON result backups
├── logs/                            # Log files
└── plans/                          # Planning documents
```

## Extending LazyEval

### Adding New Datasets

1. Create a Pydantic model in `src/datasets/models.py`
2. Implement a loader in `src/datasets/` extending `BaseDatasetLoader`
3. Update `main.py` to use your new loader

### Using Different Model Endpoints

Just update `.env` with your endpoint details. Works with:
- vLLM
- Any OpenAI-compatible API
- Local or remote endpoints

## Development

### Running Tests

```bash
uv run pytest tests/ -v
```

### Running with Coverage

```bash
uv run pytest tests/ --cov=src --cov-report=html
```

## Troubleshooting

**No results generated?**
- Check your `.env` file has valid API keys
- Verify your model endpoint is accessible
- Check `logs/` for detailed error messages

**Langfuse not receiving data?**
- Verify Langfuse API keys in `.env`
- Check network connectivity to Langfuse host
- Look for errors in logs

**Dataset loading fails?**
- Ensure you have internet connection (for HuggingFace)
- Check dataset name is correct in `config.yaml`
- Verify dataset schema matches `AgricultureDatasetItem`

## License

[Your License Here]

# LazyEval 🦥

**Automated evaluation platform for language models.**

Simple, sequential, and type-safe. Loads datasets, queries your model (vLLM/OpenAI), and logs traces to Langfuse for LLM-as-Judge evaluation.

## 🚀 Quick Start

### 1. Install
```bash
git clone <your-repo-url>
cd LazyEval
uv sync --dev
```

### 2. Configure
Create a `.env` file:
```bash
# Model (OpenAI compatible)
MODEL_NAME=your-model
MODEL_BASE_URL=http://localhost:8000/v1
MODEL_API_KEY=sk-xxx

# Evaluation (Langfuse)
LANGFUSE_PUBLIC_KEY=pk-xxx
LANGFUSE_SECRET_KEY=sk-xxx
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 3. Run
```bash
uv run main.py
```
*Results are saved to `results/` and logged to `logs/`.*

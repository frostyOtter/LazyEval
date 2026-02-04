# LazyEval Platform - Clarifying Questions

## Dataset Management

### Q1: Dataset Format & Structure
**Question**: What format(s) will the datasets be in?
- JSON files (JSONL, JSON arrays)?
- CSV/TSV files?
- HuggingFace datasets format?
- Custom format?

**Follow-up**: What is the expected schema? For example:
```json
{
  "id": "example_1",
  "input": "What is the capital of France?",
  "expected_output": "Paris",
  "metadata": {...}
}
```

**Answer**: Start with this dataset `Mahesh2841/Agriculture`, then we can add more datasets later.
Example data slice:
```
[
    {
    "instruction": "Answer the following question",
    "input": "What are some methods for improving soil fertility?",
    "response": "Improving soil fertility can be achieved through various methods such as crop rotation, cover cropping, and adding organic matter like compost or manure. Additionally, using green manures, practicing conservation tillage, and applying appropriate fertilizers based on soil testing can help enhance soil fertility and promote healthier plant growth."
    },
    {
    "instruction": "Answer the following question",
    "input": "How can I prevent erosion on my farmland?",
    "response": "Preventing erosion on farmland involves implementing conservation practices like contour plowing, terracing, and planting windbreaks or cover crops. Maintaining vegetation along waterways, installing silt fences, and using erosion control blankets can also help minimize soil erosion and protect the integrity of farmland."
    },
]
```


### Q2: Dataset Discovery
**Question**: Should the platform:
- Watch the data folder for new datasets in real-time?
- Only scan on startup?
- Require manual refresh/reload?

**Answer**: Only scan on startup.

### Q3: Dataset Validation
**Question**: What happens when a dataset is malformed or missing required fields?
- Skip and log error?
- Fail the entire evaluation run?
- Attempt to auto-fix common issues?

**Answer**: When we add a new dataset, it will have to successfully pass the test from pytest. Which require the dataset to follow a predefined protocol, or a predefined format for that dataset.
If anything happens, skip and log the errors.

## Model Integration

### Q4: vLLM Deployment
**Question**: Will you be:
- Running vLLM locally on your machine?
- Deploying on a remote server/cloud?
- Using an existing vLLM endpoint?

**Answer**: I will run vLLM somewhere else, and I will provide the endpoint, api-key, model-name. Or it could be a 3rd party that support OpenAI generic API
At the very least, we just need a mode class that initialize with a model-name, endpoint and api-key.

### Q5: Model Selection
**Question**: Should the platform:
- Support multiple models simultaneously?
- Allow switching between models via configuration?
- Always use a single default model?

**Answer**: Only 1 model at a time. But we should design it in a way that we can easily add more models in the future.

**Follow-up**: Should we compare results across different models?

**Answer**: Not in this MVP. But we should design it in a way that we can easily add more models in the future.

### Q6: API Configuration
**Question**: What OpenAI API parameters should be configurable?
- `temperature`, `top_p`, `max_tokens`?
- `n` (number of completions)?
- `stream` vs non-streaming responses?

**Answer**: temperature, top_p, max_tokens, also, all will be non streaming.

## Evaluation Criteria

### Q7: Evaluation Types
**Question**: What types of evaluation are you planning?
- **Exact Match**: Response must exactly match expected output
- **Semantic Similarity**: Using embeddings/similarity scores
- **Rule-based**: Custom validation rules
- **LLM-as-Judge**: Using another LLM to evaluate quality
- **Domain-specific metrics**: Based on your use case

**Answer**: For each datasets, I will define a evaluation function that will be used to evaluate the dataset. This function will be used to evaluate the dataset. For the `Mahesh2841/Agriculture` dataset, the evaluation function will be LLM-as-Judge metrics.

### Q9: Ground Truth
**Question**: Will datasets include:
- Expected/reference outputs for comparison?
- Multiple acceptable answers?
- Just inputs (exploratory evaluation)?

**Answer**: For the `Mahesh2841/Agriculture` dataset, it include expected/reference outputs for comparison.
For other datasets, it depends, I will implement it based on the dataset.

## Langfuse Integration

### Q10: Langfuse Usage
**Question**: What Langfuse features are most important?
- Trace logging (all API calls)
- Custom metrics/scores
- Prompt versioning
- Dataset management within Langfuse
- User feedback collection

**Follow-up**: Do you have an existing Langfuse project, or should we set one up?

**Answer**: I have an existing Langfuse project, and I will provide the API key and project ID.

### Q11: Data Storage
**Question**: Should evaluation results be stored:
- Only in Langfuse?
- Also in local files (JSON/CSV) for backup?
- In a local database (SQLite, PostgreSQL)?

**Answer**: Langfuse and JSON files for backup.

## Execution & Workflow

### Q12: Evaluation Triggering
**Question**: How should evaluations be initiated?
- CLI command: `lazyeval run --dataset=my_dataset`
- Watch mode: Auto-run when new datasets appear
- API endpoint: Trigger via HTTP request
- Scheduled: Cron-like periodic evaluation

**Answer**: CLI command, but make it `uv run main.py`, then it will run the automatic evaluation flow logic from source code.

### Q13: Batch Processing
**Question**: For efficiency:
- Should we batch multiple inputs in single API calls?
- What's an acceptable batch size?
- Should we implement rate limiting to avoid overwhelming the API?

**Answer**: No, just single input at a time. No batch processing. Make it simplep first.

### Q14: Concurrency
**Question**: Should evaluations run:
- Sequentially (one at a time, safer)
- In parallel (multiple datasets/inputs simultaneously, faster)
- Configurable parallelism level?

**Answer**: Sequentially (one at a time, safer). Make it simple first.

## Extensibility & Future

### Q15: Custom Evaluation Logic
**Question**: Do you need:
- Plugin system for custom metrics?
- Support for preprocessing/postprocessing steps?
- Custom dataset loaders?

**Answer**: No, just custom dataset loaders. No plugin system for custom metrics. No preprocessing/postprocessing steps.

### Q16: Reporting
**Question**: Beyond Langfuse, do you need:
- Generated reports (PDF/HTML)?
- Email notifications on completion?
- Comparison views between evaluation runs?

**Answer**: No, just Langfuse. No PDF/HTML reports. No email notifications. No comparison views between evaluation runs.

## Deployment & Environment

### Q17: Deployment Target
**Question**: Where will LazyEval run?
- Local development machine
- Cloud server (AWS, GCP, Azure)
- Docker container
- Kubernetes cluster

**Answer**: Local development machine.

### Q18: Configuration Management
**Question**: How should configuration be managed?
- YAML/TOML config files?
- Environment variables?
- Mix of both?

**Answer**: Mix of both. Environment variables for sensitive information (API keys, etc.), and YAML/TOML config files for other configuration.

**Follow-up**: Should different environments (dev, staging, prod) have separate configs?

**Answer**: No, just one environment for now.

---

## Priority Classification

### 🔴 High Priority (Blocking)
Must be answered before detailed architecture design:
- Q1: Dataset format
- Q4: vLLM deployment
- Q7: Evaluation types
- Q8: Metrics priority
- Q12: Evaluation triggering

### 🟡 Medium Priority (Important)
Should be answered during early implementation:
- Q2, Q5, Q6, Q9, Q10, Q13

### 🟢 Low Priority (Can defer)
Can be decided during implementation or as features evolve:
- Q3, Q11, Q14, Q15, Q16, Q17, Q18

---

## Next Steps

Once you've answered the high-priority questions, I can:
1. Create a detailed domain model
2. Design the architecture with specific implementation patterns
3. Generate an implementation roadmap
4. Start building the core components

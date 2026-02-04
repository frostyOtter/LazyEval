# LazyEval Platform - Implementation Roadmap

## Philosophy: Working Backwards from the End Goal

Following your preferred approach, we'll work backwards from the desired end state and identify what needs to be built at each phase.

## End Goal Vision

```
User runs: `lazyeval run --dataset my_eval_data.json`

Platform automatically:
1. ✅ Loads the dataset
2. ✅ Sends each item to the vLLM-hosted model
3. ✅ Collects responses
4. ✅ Calculates metrics
5. ✅ Pushes results to Langfuse dashboard
6. ✅ Shows summary in CLI
```

## Reverse Planning: What Do We Need?

### To View Results in Langfuse → Need:
- Integration with Langfuse SDK
- Proper trace/span structure
- Metric scores in Langfuse format
- ⬅️ **This requires: Calculated metrics**

### To Calculate Metrics → Need:
- EvalResults with model outputs and expected outputs
- MetricCalculator implementations
- ⬅️ **This requires: Completed model inferences**

### To Get Model Outputs → Need:
- Working ModelClient that calls vLLM
- EvalItems with input prompts
- ⬅️ **This requires: Loaded dataset + Running vLLM server**

### To Load Dataset → Need:
- DatasetLoader that reads files
- Schema validation
- ⬅️ **This requires: Defined data format**

### To Start Everything → Need:
- CLI interface
- Configuration management
- ⬅️ **This requires: Basic project structure**

---

## Implementation Phases

### Phase 0: Foundation (Week 0)
**Goal**: Set up project scaffolding

- [x] ~~Create plans folder and documentation~~ *(Current)*
- [ ] Initialize project with `uv` (pyproject.toml)
- [ ] Set up basic project structure (src/, tests/, configs/)
- [ ] Configure logging with loguru
- [ ] Set up development environment

**Deliverable**: Empty but properly structured Python project

---

### Phase 1: Dataset Management (Week 1)
**Goal**: Load and validate datasets from files

#### Minimal Version
```python
# Can load a single JSON file with this structure:
[
  {
    "id": "1",
    "input": "What is 2+2?",
    "expected": "4"
  }
]
```

**Tasks**:
1. Define Pydantic models for `EvalItem` and `Dataset`
2. Implement `JSONDatasetLoader`
3. Add basic schema validation
4. Write unit tests for dataset loading

**Success Criteria**: Can load example dataset and iterate over items

**Files to Create**:
- `src/domain/models.py` - Core Pydantic models
- `src/datasets/loader.py` - Dataset loading logic
- `tests/test_dataset_loader.py` - Tests
- `data/examples/simple_eval.json` - Example dataset

---

### Phase 2: Model Integration (Week 1-2)
**Goal**: Connect to vLLM and get responses

#### Minimal Version
```python
# Can call vLLM with a prompt and get response
client = ModelClient(base_url="http://localhost:8000")
response = await client.generate("What is 2+2?")
# response = "4"
```

**Tasks**:
1. Implement `ModelClient` using httpx/OpenAI SDK
2. Handle basic errors and retries
3. Add configuration for temperature, max_tokens, etc.
4. Write integration tests (with mock server)

**Prerequisites**: 
- Running vLLM server (you'll need to set this up separately)
- Or use a mock endpoint for testing

**Success Criteria**: Can send prompts and receive responses

**Files to Create**:
- `src/models/client.py` - Model client implementation
- `src/models/config.py` - Model configuration
- `tests/test_model_client.py` - Tests (with mocking)

---

### Phase 3: Evaluation Engine (Week 2)
**Goal**: Orchestrate dataset → model → results flow

#### Minimal Version
```python
# Can run evaluation on a dataset
evaluator = EvaluationEngine(dataset, model_client)
results = await evaluator.run()
# results = [EvalResult(...), EvalResult(...), ...]
```

**Tasks**:
1. Implement `EvaluationEngine` orchestrator
2. Create `EvalResult` model
3. Add progress tracking (simple logging)
4. Handle errors gracefully
5. Save results to JSON files

**Success Criteria**: End-to-end flow from dataset to saved results

**Files to Create**:
- `src/evaluation/engine.py` - Core evaluation logic
- `src/evaluation/runner.py` - Async execution
- `tests/test_evaluation_engine.py` - Tests

---

### Phase 4: Metrics Calculation (Week 3)
**Goal**: Calculate meaningful metrics from results

#### Minimal Version (Start Simple)
```python
# Exact match metric only
calculator = ExactMatchMetric()
score = calculator.calculate(result)
# score.value = 1.0 or 0.0
```

**Tasks**:
1. Define `MetricCalculator` interface
2. Implement basic metrics:
   - Exact Match
   - Pass Rate (aggregate)
   - Average Latency
3. Create `MetricScore` model
4. Add metric aggregation logic

**Later** (if needed):
- BLEU/ROUGE for text similarity
- LLM-as-judge metrics
- Custom domain metrics

**Success Criteria**: Can calculate and aggregate metrics from results

**Files to Create**:
- `src/metrics/base.py` - Metric interface
- `src/metrics/exact_match.py` - Exact match implementation
- `src/metrics/aggregators.py` - Aggregation logic
- `tests/test_metrics.py` - Tests

---

### Phase 5: Langfuse Integration (Week 3-4)
**Goal**: Push traces and metrics to Langfuse

#### Minimal Version
```python
# Can send evaluation run to Langfuse
langfuse_exporter = LangfuseExporter(api_key=...)
await langfuse_exporter.export(eval_run, results, metrics)
# ✓ Visible in Langfuse dashboard
```

**Tasks**:
1. Install and configure Langfuse SDK
2. Map our domain models to Langfuse traces
3. Send individual inferences as spans
4. Attach metric scores to traces
5. Test with real Langfuse account

**Prerequisites**: Langfuse account and API keys

**Success Criteria**: Results visible in Langfuse dashboard

**Files to Create**:
- `src/integrations/langfuse_client.py` - Langfuse integration
- `src/integrations/mappers.py` - Domain → Langfuse mapping
- `configs/langfuse.example.yaml` - Config template

---

### Phase 6: CLI Interface (Week 4)
**Goal**: Provide user-friendly command-line interface

#### Minimal Version
```bash
lazyeval run --dataset data/my_eval.json --model-url http://localhost:8000
```

**Tasks**:
1. Implement CLI using `typer` or `click`
2. Add commands:
   - `run` - Execute evaluation
   - `list` - List available datasets
   - `config` - Show/edit configuration
3. Add configuration file support (YAML/TOML)
4. Pretty output with rich/tqdm

**Success Criteria**: User can run evaluations via CLI

**Files to Create**:
- `src/cli/main.py` - CLI entry point
- `src/cli/commands.py` - Command implementations
- `src/config/loader.py` - Config management

---

### Phase 7: Polish & Testing (Week 5)
**Goal**: Make production-ready

**Tasks**:
1. Comprehensive error handling
2. Add detailed logging
3. Write integration tests
4. Add concurrency/batching (if needed)
5. Performance optimization
6. Documentation (README, API docs)

---

## Minimal Viable Product (MVP)

**Scope for MVP** (Phases 0-4 + minimal Phase 5):
- Load JSON datasets
- Call vLLM via OpenAI API
- Calculate exact match and pass rate
- Basic Langfuse integration
- Simple CLI

**Out of scope for MVP**:
- Multiple dataset formats
- Advanced metrics
- Real-time watching
- Web UI
- Complex error recovery

**Estimated Timeline**: 3-4 weeks for MVP

---

## Decision Points

At each phase, we'll pause to validate:

### After Phase 1 (Dataset Management)
**Question**: Is the data format suitable? Do we need additional fields?

### After Phase 2 (Model Integration)
**Question**: Is vLLM performance acceptable? Do we need batching?

### After Phase 3 (Evaluation Engine)
**Question**: Should we add parallel processing? How do we handle failures?

### After Phase 4 (Metrics)
**Question**: Are basic metrics sufficient, or do we need advanced ones immediately?

---

## Next Steps

1. **Answer clarifying questions** in [01_clarifying_questions.md](file:///Users/thai.tran/personal/LazyEval/plans/01_clarifying_questions.md)
2. **Validate domain model** in [02_domain_model.md](file:///Users/thai.tran/personal/LazyEval/plans/02_domain_model.md)
3. **Begin Phase 0** - Set up project structure
4. **Iterate incrementally** through phases

Would you like to proceed with a specific phase, or do you want to refine the plan first?

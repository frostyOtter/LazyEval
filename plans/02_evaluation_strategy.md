# Evaluation Strategy Implementation Plan

## Goal Description
Implement a flexible evaluation strategy where each dataset is mapped to specific evaluation functions. Specifically, enable "LLM-as-Judge" metrics for the `Mahesh2841/Agriculture` dataset as requested.

## User Review Required
> [!IMPORTANT]
> - `src/evaluation/models.py`: Modifying `EvalResult` schema to include `metrics`.
> - `src/evaluation/runner.py`: Updating `run()` logic to compute metrics post-generation.

## Proposed Changes

### Configuration & Models
#### [MODIFY] [models.py](file:///Users/thai.tran/personal/LazyEval/src/evaluation/models.py)
- Add `metrics: dict[str, float]` and `evaluation_details: dict[str, Any]` to `EvalResult`.

### Metrics & Strategies
#### [NEW] [llm_judge.py](file:///Users/thai.tran/personal/LazyEval/src/metrics/llm_judge.py)
- Implement a basic `LLMJudge` class or functions that use a model client to score responses.
- Implement specific prompts for correctness and safety.

#### [NEW] [registry.py](file:///Users/thai.tran/personal/LazyEval/src/evaluation/registry.py)
- Define `get_evaluation_functions(dataset_name: str)` which returns a list of metric callables.
- Hardcode the mapping for `Mahesh2841/Agriculture` -> `[answer_relevance]`.

### Evaluation Logic
#### [MODIFY] [runner.py](file:///Users/thai.tran/personal/LazyEval/src/evaluation/runner.py)
- In `run()` method, look up evaluation functions for the current dataset.
- Execute functions on the generated result.
- Store results in the `EvalResult` object.

### Datasets
#### [MODIFY] [README.md](file:///Users/thai.tran/personal/LazyEval/datasets/README.md)
- Update documentation to explain how to register metrics for new datasets.

## Verification Plan
### Automated Tests
- Create a test `tests/test_evaluation_registry.py` to verify correct function lookup.
- Create a test `tests/test_runner_metrics.py` mocking the LLM judge to ensure scores are recorded.

### Manual Verification
- Run `main.py` (once updated) with a dummy agriculture dataset and verify logs show "Evaluating with LLM Judge".

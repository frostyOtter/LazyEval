# Evaluation Strategy: Dataset-Centric Metrics

## Context
Currently, `EvaluationRunner` looks up metrics from a central registry (`src/evaluation/registry.py`) using the dataset name. The user proposes moving this logic into the dataset module itself, specifically `src/datasets/agriculture.py` for the current use case, by adding a `metrics` function.

## Goals
1. Decouple `EvaluationRunner` from specific metric knowledge.
2. Colocate metric definitions with the dataset they evaluate.
3. Allow each dataset to define exactly which metrics apply to it.

## Proposed Design

### 1. `metrics` Function in Dataset Module
In `src/datasets/agriculture.py`, we will add a function `metrics()`:

```python
# src/datasets/agriculture.py

def metrics() -> list[callable]:
    """
    Returns a list of metric functions applicable to this dataset.
    Each metric function should accept (instruction, prediction, reference) or a subset.
    """
    from src.metrics import answer_accuracy, answer_relevance
    return [
        answer_accuracy,
        answer_relevance
    ]
```

### 2. Update `EvaluationRunner`
The runner will no longer look up metrics by string name. Instead, it will retrieve them from the `DatasetLoader` or the module.

Since the runner currently holds a `DatasetLoader` instance, we can add a `get_metrics()` method to the `BaseDatasetLoader` interface, which the concrete `AgricultureDatasetLoader` implements (or delegates to the module's `metrics` function).

**Option A: Method on Loader**
```python
class AgricultureDatasetLoader(BaseDatasetLoader):
    def get_metrics(self):
        return metrics() # Calls the module-level function
```

**Option B: Direct Access (Simpler)**
If the user specifically wants just the `def metrics` function in the file, the runner might need to inspect the module or the loader needs to expose it. Option A is cleaner for the `Runner`.

## Clarifying Questions

1. **Metric Signature**: What should the standard signature for a metric function be? Currently, `runner.py` does some dispatching:
   ```python
   if name == "answer_relevance":
       score = func(query=item.instruction, prediction=output)
   elif name == "answer_accuracy":
       score = func(prediction=output, reference=item.response)
   ```
   Should we standardize the arguments (e.g., passing a context object or `kwargs`) so the runner doesn't need these `if/else` blocks?

**Answer**: Implement as suggestion in 2. Update `EvaluationRunner` to accept a list of metric functions.

2. **Configuration**: Should the `metrics` function take arguments (like `EvaluationConfig`) to selectively enable/disable metrics?

**Answer**: No. The `metrics` function just should use the defined metrics from `src/metrics`, and the evaluations registry should remove the mapping between metric name and function. We no longer need registry.

3. **Return Type**: Should `metrics` return just the functions, or a dictionary mapping names to functions? (Likely functions are better if they have `__name__`).

**Answer**: just the functions.

## Implementation Plan

1. **Modify `src/datasets/agriculture.py`**:
   - Import necessary metric functions.
   - Implement `def metrics(): ...`.

2. **Modify `src/datasets/base.py`**:
   - Add `get_metrics()` abstract method to `BaseDatasetLoader`.

3. **Modify `src/evaluation/runner.py`**:
   - Remove usage of `get_metric_functions` from registry.
   - Use `self.dataset_loader.get_metrics()` to get the list of functions.
   - Refactor the execution loop to call these functions generically.

4. **Deprecate/Remove valid parts of `src/evaluation/registry.py`**:
   - If it's no longer needed.

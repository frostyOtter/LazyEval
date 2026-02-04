# Metrics

This module contains evaluation metrics for assessing LLM outputs across **accuracy, correctness, relevance, and hallucination-related dimensions**.
Each metric is designed to answer a *distinct evaluation question* and should be combined deliberately depending on the task (QA, RAG, chat, etc.).

---

## Available Metrics

### `answer_accuracy.py`

**Purpose**
Measures **exact-match accuracy** between a model prediction and a reference answer.

**What it checks**

* Strict string or token-level match
* No semantic flexibility

**Use when**

* Deterministic outputs
* Closed-form answers (math, IDs, labels)
* Golden datasets with canonical answers

**Function**

```python
calculate_answer_accuracy(prediction, reference, case_sensitive=False)
```

**Notes**

* Penalizes paraphrases
* Not suitable for open-ended generation

---

### `answer_correctness.py`

**Purpose**
Evaluates whether the answer is **factually and logically correct** relative to a reference answer.

**What it checks**

* Semantic equivalence
* Logical consistency
* Partial correctness (depending on implementation)

**Use when**

* Open-ended QA
* Explanatory answers
* Reasoning-heavy tasks

**Function**

```python
calculate_answer_correctness(prediction, reference)
```

**Notes**

* More flexible than `answer_accuracy`
* Still requires a **ground-truth reference**

---

### `answer_relevance.py`

**Purpose**
Measures how well the generated answer **addresses the user query or instruction**, regardless of factual correctness.

**What it checks**

* On-topic alignment
* Instruction following
* Penalizes off-topic or generic responses

**Use when**

* Chatbots
* Assistants
* Search / retrieval responses

**Function**

```python
calculate_answer_relevance(query, prediction)
```

**Notes**

* Does **not** evaluate truth
* An answer can be relevant but incorrect

---

### `response_groundedness.py`

**Purpose**
Assesses whether the response is **supported by the provided context**, primarily for hallucination detection.

**What it checks**

* Claims can be traced back to context
* Penalizes unsupported statements

**Use when**

* Retrieval-Augmented Generation (RAG)
* Document QA
* Enterprise / compliance-sensitive systems

**Function**

```python
calculate_response_groundedness(prediction, context)
```

**Notes**

* Does not require a ground-truth answer
* Context may be incorrect; groundedness does not imply real-world truth

---

## Metric Relationship Summary

| Metric                | Requires Reference | Requires Context | Checks Truth     | Checks On-Topic | Detects Hallucination |
| --------------------- | ------------------ | ---------------- | ---------------- | --------------- | --------------------- |
| Answer Accuracy       | ✅                  | ❌                | ✅ (strict)       | ❌               | ❌                     |
| Answer Correctness    | ✅                  | ❌                | ✅ (semantic)     | ❌               | ❌                     |
| Answer Relevance      | ❌                  | ❌                | ❌                | ✅               | ❌                     |
| Response Groundedness | ❌                  | ✅                | ⚠️ (via context) | ❌               | ✅                     |

---

## Recommended Metric Combinations

### Deterministic QA

* `answer_accuracy`

### Open-ended QA

* `answer_correctness`
* `answer_relevance`

### RAG Systems

* `answer_relevance`
* `response_groundedness`
* (`answer_correctness` if references exist)

### Chat / Assistant Evaluation

* `answer_relevance`
* (optionally) `response_groundedness`

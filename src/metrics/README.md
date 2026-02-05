# Metrics

**Evaluation metrics for assessing LLM outputs.**

> [!TIP]
> **Quick Reference**: Choose metrics based on your evaluation goal.

| Metric | Checks | Use for | Diff |
| :--- | :--- | :--- | :--- |
| **Accuracy** | Exact match (strict) | Math, Classification, IDs | `==` |
| **Correctness** | Factual truth (semantic) | QA, Reasoning | `~=` |
| **Relevance** | Response vs. Query | Chat, RAG, Search | `?` |
| **Groundedness** | Response vs. Context | RAG, Hallucination Check | `⊆` |

---

## ⚡️ Cheat Sheet

### `answer_accuracy`
*   **Goal**: Exact equality.
*   **Good for**: "What is 2+2?", "Extract the ID".
*   **Bad for**: Chat, Explanations.
*   **Func**: `calculate_answer_accuracy(pred, ref)`

### `answer_correctness`
*   **Goal**: Meaning matches, even if words differ.
*   **Good for**: "Explain quantum physics", Standard QA.
*   **Requires**: Ground truth reference.
*   **Func**: `calculate_answer_correctness(pred, ref)`

### `answer_relevance`
*   **Goal**: Did the model answer *the specific question asked*?
*   **Good for**: Chatbots, avoiding generic refusals.
*   **Note**: An answer can be *relevant* but *wrong*.
*   **Func**: `calculate_answer_relevance(query, pred)`

### `response_groundedness`
*   **Goal**: Does the context *support* the answer? (Anti-hallucination).
*   **Good for**: RAG systems.
*   **Note**: Checks if `Answer ⊆ Context`.
*   **Func**: `calculate_response_groundedness(pred, context)`

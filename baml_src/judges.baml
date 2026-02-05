// Defines the judge functions for metrics evaluation using LLM

function AnswerCorrectness(prediction: string, ground_truth: string) -> float {
  client JudgeClient
  prompt #"
    You are an expert evaluator for a question answering system.

    Compare the PREDICTION with the GROUND_TRUTH.
    Rate the correctness of the PREDICTION on a scale from 0.0 to 1.0, where:
    0.0: The prediction is completely incorrect or irrelevant.
    0.5: The prediction is partially correct but misses key details.
    1.0: The prediction is fully correct and captures the meaning of the ground truth.

    PREDICTION: "{{ prediction }}"
    GROUND_TRUTH: "{{ ground_truth }}"

    Return ONLY the numeric score (e.g., 0.8). Do not include any explanation.
    
    {{ ctx.output_format }}
  "#
}

function AnswerRelevance(query: string, prediction: string) -> float {
  client JudgeClient
  prompt #"
    You are an expert evaluator for a question answering system.
    
    Evaluate the relevance of the PREDICTION to the QUERY.
    Rate the relevance on a scale from 0.0 to 1.0, where:
    0.0: The prediction is not relevant to the query at all.
    0.5: The prediction is somewhat relevant but includes hallucinations or irrelevant info.
    1.0: The prediction is perfectly relevant and directly answers the query.

    QUERY: "{{ query }}"
    PREDICTION: "{{ prediction }}"

    Return ONLY the numeric score (e.g., 0.8). Do not include any explanation.

    {{ ctx.output_format }}
  "#
}

function ResponseGroundedness(context: string, prediction: string) -> float {
  client JudgeClient
  prompt #"
    You are an expert evaluator for a question answering system.
    
    Evaluate whether the PREDICTION is supported by the CONTEXT (groundedness).
    Rate the groundedness on a scale from 0.0 to 1.0, where:
    0.0: The prediction contains information NOT present in the context (hallucination).
    0.5: The prediction is partially supported but contains some unsupported claims.
    1.0: The prediction is fully supported by the provided context.

    CONTEXT: "{{ context }}"
    PREDICTION: "{{ prediction }}"

    Return ONLY the numeric score (e.g., 0.8). Do not include any explanation.

    {{ ctx.output_format }}
  "#
}

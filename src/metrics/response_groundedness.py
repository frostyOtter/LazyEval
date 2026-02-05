from loguru import logger


def calculate_response_groundedness(**kwargs) -> float:
    """
    Calculates if the response is grounded in the provided context.

    Args:
        **kwargs: Must contain 'prediction' and 'context'.

    Returns:
        Score between 0.0 and 1.0.
    """
    prediction = kwargs.get("prediction")
    context = kwargs.get("input")  # Mapping context to input as per runner eval_context
    if context is None:
        context = kwargs.get("context")  # Fallback if explicit context passed

    if prediction is None:
        logger.warning(
            f"Missing required arguments for groundedness: prediction={prediction}"
        )
        return 0.0
    # Minimal implementation: Check overlap
    logger.warning("calculate_response_groundedness is a stub. Requires LLM judge.")

    if not context:
        return 0.0

    # Very naive overlap
    pred_words = set(prediction.lower().split())
    context_words = set(context.lower().split())

    if not pred_words:
        return 0.0

    overlap = pred_words.intersection(context_words)
    score = len(overlap) / len(pred_words)

    return min(1.0, score)

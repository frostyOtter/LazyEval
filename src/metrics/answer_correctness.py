from loguru import logger


def calculate_answer_correctness(**kwargs) -> float:
    """
    Calculates the correctness of the answer.

    Ideally this would use an LLM or fuzzy matching to determine if the
    meaning is correct even if the wording differs.

    For the minimal version, this falls back to simple inclusion check or token overlap.

    Args:
        **kwargs: Must contain 'prediction' and 'reference'.

    Returns:
        Score between 0.0 and 1.0.
    """
    prediction = kwargs.get("prediction")
    reference = kwargs.get("reference")

    if prediction is None or reference is None:
        logger.warning(
            f"Missing required arguments for correctness: prediction={prediction}, reference={reference}"
        )
        return 0.0
    # Minimal implementation: check if reference key terms are in prediction
    # This is a placeholder for a more sophisticated LLM-based evaluator

    if not prediction or not reference:
        return 0.0

    pred_lower = prediction.lower()

    # Handle list of references (e.g. from Mirage dataset)
    if isinstance(reference, list):
        references = [str(r).lower() for r in reference]
    elif (
        isinstance(reference, str)
        and reference.strip().startswith("[")
        and reference.strip().endswith("]")
    ):
        try:
            import ast

            parsed = ast.literal_eval(reference)
            if isinstance(parsed, list):
                references = [str(r).lower() for r in parsed]
            else:
                references = [reference.lower()]
        except (ValueError, SyntaxError):
            references = [reference.lower()]
    else:
        references = [str(reference).lower()]

    # Simple containment check against any of the references
    for ref_lower in references:
        if ref_lower in pred_lower or pred_lower in ref_lower:
            logger.debug(f"Correctness: containment found for reference '{ref_lower}'")
            return 1.0

    # TODO: Implement fuzzaldrin or LLM-based judging
    logger.debug("Correctness: no containment, returning 0.0 (placeholder)")
    return 0.0

from loguru import logger


def calculate_answer_relevance(**kwargs) -> float:
    """
    Calculates how relevant the answer is to the query.

    This usually requires an LLM to judge if the answer addresses the question.

    Args:
        **kwargs: Must contain 'query' and 'prediction'.

    Returns:
        Score between 0.0 and 1.0.
    """
    query = kwargs.get("query")
    prediction = kwargs.get("prediction")

    if query is None or prediction is None:
        logger.warning(
            f"Missing required arguments for relevance: query={query}, prediction={prediction}"
        )
        return 0.0

    # Minimal implementation: always return 1.0 or TODO
    # because relevance requires semantic understanding

    logger.warning("calculate_answer_relevance is a stub. Requires LLM judge.")
    return 0.5  # Placeholder

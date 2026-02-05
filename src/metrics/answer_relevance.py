from baml_client.async_client import b as stream_baml_client
from loguru import logger


async def calculate_answer_relevance(**kwargs) -> float:
    """
    Calculates how relevant the answer is to the query using BAML-defined LLM judge.

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

    try:
        score = await stream_baml_client.AnswerRelevance(
            query=query, prediction=prediction
        )
        return float(score)

    except Exception as e:
        logger.error(f"Error in answer_relevance: {e}")
        return 0.0

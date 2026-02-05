from baml_client.async_client import b as stream_baml_client
from loguru import logger


async def calculate_response_groundedness(**kwargs) -> float:
    """
    Calculates if the response is grounded in the provided context using BAML-defined LLM judge.

    Args:
        **kwargs: Must contain 'prediction' and 'context'.

    Returns:
        Score between 0.0 and 1.0.
    """
    prediction = kwargs.get("prediction")
    context = kwargs.get("context")

    if prediction is None or context is None:
        logger.warning(
            f"Missing required arguments for groundedness: prediction={prediction}, context={context}"
        )
        return 0.0

    try:
        score = await stream_baml_client.ResponseGroundedness(
            context=context, prediction=prediction
        )
        return float(score)

    except Exception as e:
        logger.error(f"Error in response_groundedness: {e}")
        return 0.0

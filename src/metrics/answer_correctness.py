from baml_client.async_client import b as stream_baml_client
from loguru import logger


async def calculate_answer_correctness(**kwargs) -> float:
    """
    Calculates the correctness of the answer using BAML-defined LLM judge.

    Args:
        **kwargs: Must contain 'prediction' and 'ground_truth'.

    Returns:
        Score between 0.0 and 1.0.
    """
    prediction = kwargs.get("prediction")
    ground_truth = kwargs.get("ground_truth")

    if prediction is None or ground_truth is None:
        logger.warning(
            f"Missing required arguments for correctness: prediction={prediction}, ground_truth={ground_truth}"
        )
        return 0.0

    try:
        # The BAML function returns a float as defined in judges.baml
        score = await stream_baml_client.AnswerCorrectness(
            prediction=prediction, ground_truth=ground_truth
        )
        return float(score)

    except Exception as e:
        logger.error(f"Error in answer_correctness: {e}")
        return 0.0

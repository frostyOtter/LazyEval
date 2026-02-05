from loguru import logger


def calculate_answer_accuracy(**kwargs) -> float:
    """
    Calculates exact match accuracy between prediction and reference.

    Args:
        **kwargs: Must contain 'prediction' and 'reference'. 'case_sensitive' is optional.

    Returns:
        1.0 if match, 0.0 otherwise.
    """
    prediction = kwargs.get("prediction")
    reference = kwargs.get("reference")
    case_sensitive = kwargs.get("case_sensitive", False)

    if prediction is None or reference is None:
        logger.warning(
            f"Missing required arguments for accuracy: prediction={prediction}, reference={reference}"
        )
        return 0.0

    if not isinstance(prediction, str) or not isinstance(reference, str):
        logger.warning(
            f"Invalid input types for accuracy: pred={type(prediction)}, ref={type(reference)}"
        )
        return 0.0

    pred_norm = prediction if case_sensitive else prediction.lower()
    ref_norm = reference if case_sensitive else reference.lower()

    match = pred_norm.strip() == ref_norm.strip()

    logger.debug(f"Accuracy check: matching={match}")
    return 1.0 if match else 0.0

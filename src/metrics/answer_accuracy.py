from loguru import logger


def calculate_answer_accuracy(**kwargs) -> float:
    """
    Calculates exact match accuracy between prediction and reference.

    Args:
        **kwargs: Must contain 'prediction' and 'ground_truth'. 'case_sensitive' is optional.

    Returns:
        1.0 if match, 0.0 otherwise.
    """
    prediction = kwargs.get("prediction")
    ground_truth = kwargs.get("ground_truth")
    case_sensitive = kwargs.get("case_sensitive", False)

    if prediction is None or ground_truth is None:
        logger.warning(
            f"Missing required arguments for accuracy: prediction={prediction}, ground_truth={ground_truth}"
        )
        return 0.0

    if not isinstance(prediction, str) or not isinstance(ground_truth, str):
        logger.warning(
            f"Invalid input types for accuracy: pred={type(prediction)}, qt={type(ground_truth)}"
        )
        return 0.0

    pred_norm = prediction if case_sensitive else prediction.lower()
    ref_norm = ground_truth if case_sensitive else ground_truth.lower()

    match = pred_norm.strip() == ref_norm.strip()

    logger.debug(f"Accuracy check: matching={match}")
    return 1.0 if match else 0.0

from loguru import logger

def calculate_answer_accuracy(prediction: str, reference: str, case_sensitive: bool = False) -> float:
    """
    Calculates exact match accuracy between prediction and reference.
    
    Args:
        prediction: The model's output text.
        reference: The expected ground truth text.
        case_sensitive: Whether to perform case-sensitive comparison.
        
    Returns:
        1.0 if match, 0.0 otherwise.
    """
    if not isinstance(prediction, str) or not isinstance(reference, str):
        logger.warning(f"Invalid input types for accuracy: pred={type(prediction)}, ref={type(reference)}")
        return 0.0

    pred_norm = prediction if case_sensitive else prediction.lower()
    ref_norm = reference if case_sensitive else reference.lower()
    
    match = pred_norm.strip() == ref_norm.strip()
    
    logger.debug(f"Accuracy check: matching={match}")
    return 1.0 if match else 0.0

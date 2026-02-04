from loguru import logger

def calculate_answer_correctness(prediction: str, reference: str) -> float:
    """
    Calculates the correctness of the answer.
    
    Ideally this would use an LLM or fuzzy matching to determine if the 
    meaning is correct even if the wording differs.
    
    For the minimal version, this falls back to simple inclusion check or token overlap.
    
    Args:
        prediction: The model's output text.
        reference: The expected ground truth text.
        
    Returns:
        Score between 0.0 and 1.0.
    """
    # Minimal implementation: check if reference key terms are in prediction
    # This is a placeholder for a more sophisticated LLM-based evaluator
    
    if not prediction or not reference:
        return 0.0
        
    pred_lower = prediction.lower()
    ref_lower = reference.lower()
    
    # Simple containment check as a baseline
    if ref_lower in pred_lower or pred_lower in ref_lower:
        logger.debug("Correctness: exact containment found")
        return 1.0
        
    # TODO: Implement fuzzaldrin or LLM-based judging
    logger.debug("Correctness: no containment, returning 0.0 (placeholder)")
    return 0.0

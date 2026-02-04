from loguru import logger

def calculate_response_groundedness(prediction: str, context: str) -> float:
    """
    Calculates if the response is grounded in the provided context.
    
    Args:
        prediction: The model's output text.
        context: The context retrieved or provided.
        
    Returns:
        Score between 0.0 and 1.0.
    """
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

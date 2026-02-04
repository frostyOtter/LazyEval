from loguru import logger

def calculate_answer_relevance(query: str, prediction: str) -> float:
    """
    Calculates how relevant the answer is to the query.
    
    This usually requires an LLM to judge if the answer addresses the question.
    
    Args:
        query: The input question/instruction.
        prediction: The model's output text.
        
    Returns:
        Score between 0.0 and 1.0.
    """
    # Minimal implementation: always return 1.0 or TODO
    # because relevance requires semantic understanding
    
    logger.warning("calculate_answer_relevance is a stub. Requires LLM judge.")
    return 0.5  # Placeholder

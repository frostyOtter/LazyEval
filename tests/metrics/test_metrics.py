import pytest
from unittest.mock import MagicMock

from src.metrics.answer_accuracy import calculate_answer_accuracy
from src.metrics.answer_correctness import calculate_answer_correctness
from src.metrics.answer_relevance import calculate_answer_relevance
from src.metrics.response_groundedness import calculate_response_groundedness


@pytest.fixture
def mock_judge_client():
    client = MagicMock()
    # Default behavior: return a high score
    client.generate.return_value = ("0.9", 100.0)
    return client


def test_answer_accuracy():
    # Exact match
    assert calculate_answer_accuracy(prediction="A", ground_truth="A") == 1.0
    # Case insensitive
    assert calculate_answer_accuracy(prediction="a", ground_truth="A") == 1.0
    # Mismatch
    assert calculate_answer_accuracy(prediction="A", ground_truth="B") == 0.0
    # Missing kwargs
    assert calculate_answer_accuracy(prediction="A") == 0.0


def test_answer_correctness_with_judge(mock_judge_client):
    mock_judge_client.generate.return_value = ("Score: 0.8", 100.0)
    score = calculate_answer_correctness(
        prediction="Paris is capital of France",
        ground_truth="Paris",
        judge_client=mock_judge_client,
    )
    assert score == 0.8
    # verify call args
    call_args = mock_judge_client.generate.call_args[0][0]
    assert "PREDICTION" in call_args
    assert "GROUND_TRUTH" in call_args


def test_answer_correctness_no_judge():
    # Should log warning and return 0.0
    assert calculate_answer_correctness(prediction="A", ground_truth="A") == 0.0


def test_answer_relevance_with_judge(mock_judge_client):
    mock_judge_client.generate.return_value = ("1.0", 100.0)
    score = calculate_answer_relevance(
        query="What is capital of France?",
        prediction="Paris",
        judge_client=mock_judge_client,
    )
    assert score == 1.0
    call_args = mock_judge_client.generate.call_args[0][0]
    assert "QUERY" in call_args
    assert "PREDICTION" in call_args


def test_response_groundedness_with_judge(mock_judge_client):
    mock_judge_client.generate.return_value = ("0.5", 100.0)
    score = calculate_response_groundedness(
        prediction="Paris is in Germany",
        context="Paris is in France",
        judge_client=mock_judge_client,
    )
    assert score == 0.5
    call_args = mock_judge_client.generate.call_args[0][0]
    assert "CONTEXT" in call_args
    assert "PREDICTION" in call_args


def test_response_groundedness_fallback():
    # Test fallback logic (naive overlap)
    score = calculate_response_groundedness(
        prediction="Paris is in France", context="Paris is the capital of France"
    )
    # Overlap: "paris", "is", "in", "france" (4 words in pred)
    # Context has "paris", "is", "the", "capital", "of", "france"
    # Intersection: "paris", "is", "france" (3 words)
    # Score: 3/4 = 0.75
    assert score == 0.75

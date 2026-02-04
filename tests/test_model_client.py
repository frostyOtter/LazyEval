"""Tests for model client."""

from unittest.mock import MagicMock, patch

import pytest

from src.config.models import ModelConfig
from src.models.client import ModelClient


@patch('src.models.client.OpenAI')
def test_model_client_initialization(mock_openai_class):
    """Test ModelClient initialization."""
    config = ModelConfig(
        model_name="test-model",
        base_url="http://test.com/v1",
        api_key="test-key",
        temperature=0.7,
        top_p=1.0,
        max_tokens=1000
    )
    
    client = ModelClient(config)
    
    # Verify OpenAI client was initialized correctly
    mock_openai_class.assert_called_once_with(
        base_url="http://test.com/v1",
        api_key="test-key"
    )
    assert client.config == config


@patch('src.models.client.OpenAI')
def test_model_client_generate(mock_openai_class):
    """Test model generation."""
    # Mock OpenAI client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "This is a test response"
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai_class.return_value = mock_client
    
    # Create client
    config = ModelConfig(
        model_name="test-model",
        base_url="http://test.com/v1",
        api_key="test-key"
    )
    client = ModelClient(config)
    
    # Generate response
    output, latency = client.generate("Test prompt")
    
    # Assertions
    assert output == "This is a test response"
    assert latency > 0  # Should have some latency
    
    # Verify API was called correctly
    mock_client.chat.completions.create.assert_called_once()
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args['model'] == "test-model"
    assert call_args['messages'] == [{"role": "user", "content": "Test prompt"}]
    assert call_args['temperature'] == 0.7
    assert call_args['stream'] is False


@patch('src.models.client.OpenAI')
def test_model_client_error_handling(mock_openai_class):
    """Test error handling in model client."""
    # Mock OpenAI client to raise exception
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai_class.return_value = mock_client
    
    config = ModelConfig(
        model_name="test-model",
        base_url="http://test.com/v1",
        api_key="test-key"
    )
    client = ModelClient(config)
    
    # Should raise exception
    with pytest.raises(Exception, match="API Error"):
        client.generate("Test prompt")

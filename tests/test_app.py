import pytest
from unittest.mock import Mock, patch
import json


def test_index_route(client):
    """Test that the index route renders successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Ask Steven" in response.data


def test_ask_route_invalid_method(client):
    """Test that GET requests to /ask are not allowed."""
    response = client.get('/ask')
    assert response.status_code == 405


@patch('app.client.chat.completions.create')
def test_ask_route_success(mock_openai, client):
    """Test successful question submission to /ask endpoint."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "This is a sarcastic answer"
    mock_openai.return_value = mock_response

    response = client.post('/ask', data={
        'question': 'What is the meaning of life?',
        'history': '[]'
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data
    assert data['answer'] == "This is a sarcastic answer"

    mock_openai.assert_called_once()
    call_args = mock_openai.call_args
    assert call_args.kwargs['model'] == 'gpt-4'
    assert call_args.kwargs['max_tokens'] == 500
    assert call_args.kwargs['temperature'] == 0.8


@patch('app.client.chat.completions.create')
def test_ask_route_with_history(mock_openai, client):
    """Test /ask endpoint with conversation history."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Another sarcastic response"
    mock_openai.return_value = mock_response

    history = [
        {"role": "user", "content": "Previous question"},
        {"role": "assistant", "content": "Previous answer"}
    ]

    response = client.post('/ask', data={
        'question': 'Follow up question',
        'history': json.dumps(history)
    })

    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data

    call_args = mock_openai.call_args
    messages = call_args.kwargs['messages']
    assert len(messages) == 4  # system + 2 history + new question
    assert messages[0]['role'] == 'system'
    assert messages[1]['role'] == 'user'
    assert messages[2]['role'] == 'assistant'
    assert messages[3]['role'] == 'user'
    assert messages[3]['content'] == 'Follow up question'


@patch('app.client.chat.completions.create')
def test_ask_route_invalid_history_json(mock_openai, client):
    """Test /ask endpoint handles invalid JSON in history gracefully."""
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Response despite bad history"
    mock_openai.return_value = mock_response

    response = client.post('/ask', data={
        'question': 'A question',
        'history': 'invalid json{'
    })

    assert response.status_code == 200

    call_args = mock_openai.call_args
    messages = call_args.kwargs['messages']
    assert len(messages) == 2  # system + new question (no history)

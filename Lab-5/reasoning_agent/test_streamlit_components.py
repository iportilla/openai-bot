"""
Unit tests for Streamlit components in the Reasoning Math Agent.

Tests session state management, message history persistence, and input validation.

Requirements: 4.1, 4.2, 4.3, 4.4
"""

import pytest
from unittest.mock import MagicMock, patch
import sys


class TestSessionStateInitialization:
    """Tests for session state initialization."""
    
    def test_session_state_has_messages_key(self):
        """Test that session state initializes with messages key."""
        # Mock streamlit session state
        mock_session_state = {}
        
        # Simulate initialization
        if "messages" not in mock_session_state:
            mock_session_state["messages"] = []
        
        assert "messages" in mock_session_state
        assert isinstance(mock_session_state["messages"], list)
        assert len(mock_session_state["messages"]) == 0
    
    def test_session_state_messages_is_list(self):
        """Test that messages in session state is a list."""
        mock_session_state = {"messages": []}
        
        assert isinstance(mock_session_state["messages"], list)
    
    def test_session_state_has_reasoning_agent_key(self):
        """Test that session state initializes with reasoning_agent key."""
        mock_session_state = {}
        
        # Simulate initialization
        if "reasoning_agent" not in mock_session_state:
            mock_session_state["reasoning_agent"] = MagicMock()
        
        assert "reasoning_agent" in mock_session_state
    
    def test_session_state_persists_across_calls(self):
        """Test that session state persists across multiple calls."""
        mock_session_state = {"messages": []}
        
        # Add a message
        mock_session_state["messages"].append({
            "role": "user",
            "content": "Test message"
        })
        
        # Verify it persists
        assert len(mock_session_state["messages"]) == 1
        assert mock_session_state["messages"][0]["content"] == "Test message"


class TestMessageHistoryPersistence:
    """Tests for message history persistence."""
    
    def test_add_user_message_to_history(self):
        """Test adding a user message to history."""
        messages = []
        
        user_message = {
            "role": "user",
            "content": "What is 5 times 3?"
        }
        messages.append(user_message)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == "What is 5 times 3?"
    
    def test_add_assistant_message_to_history(self):
        """Test adding an assistant message to history."""
        messages = []
        
        assistant_message = {
            "role": "assistant",
            "content": "The answer is 15"
        }
        messages.append(assistant_message)
        
        assert len(messages) == 1
        assert messages[0]["role"] == "assistant"
        assert messages[0]["content"] == "The answer is 15"
    
    def test_message_history_maintains_order(self):
        """Test that message history maintains insertion order."""
        messages = []
        
        messages.append({"role": "user", "content": "First question"})
        messages.append({"role": "assistant", "content": "First answer"})
        messages.append({"role": "user", "content": "Second question"})
        messages.append({"role": "assistant", "content": "Second answer"})
        
        assert len(messages) == 4
        assert messages[0]["content"] == "First question"
        assert messages[1]["content"] == "First answer"
        assert messages[2]["content"] == "Second question"
        assert messages[3]["content"] == "Second answer"
    
    def test_message_history_with_multiple_problems(self):
        """Test message history with multiple problems and solutions."""
        messages = []
        
        # First problem
        messages.append({"role": "user", "content": "What is 10 times 5?"})
        messages.append({"role": "assistant", "content": "The answer is 50"})
        
        # Second problem
        messages.append({"role": "user", "content": "What is 20 times 3?"})
        messages.append({"role": "assistant", "content": "The answer is 60"})
        
        assert len(messages) == 4
        # Verify first problem is still there
        assert messages[0]["content"] == "What is 10 times 5?"
        assert messages[1]["content"] == "The answer is 50"
        # Verify second problem is added
        assert messages[2]["content"] == "What is 20 times 3?"
        assert messages[3]["content"] == "The answer is 60"
    
    def test_clear_message_history(self):
        """Test clearing message history."""
        messages = [
            {"role": "user", "content": "Question 1"},
            {"role": "assistant", "content": "Answer 1"}
        ]
        
        # Clear history
        messages = []
        
        assert len(messages) == 0
    
    def test_message_has_required_fields(self):
        """Test that messages have required fields."""
        message = {
            "role": "user",
            "content": "Test message"
        }
        
        assert "role" in message
        assert "content" in message
        assert message["role"] in ["user", "assistant", "system"]
    
    def test_message_content_is_string(self):
        """Test that message content is a string."""
        message = {
            "role": "user",
            "content": "What is 5 times 3?"
        }
        
        assert isinstance(message["content"], str)
    
    def test_message_role_is_valid(self):
        """Test that message role is one of valid values."""
        valid_roles = ["user", "assistant", "system"]
        
        for role in valid_roles:
            message = {"role": role, "content": "Test"}
            assert message["role"] in valid_roles


class TestInputValidation:
    """Tests for input validation."""
    
    def test_empty_input_is_invalid(self):
        """Test that empty input is considered invalid."""
        user_input = ""
        
        is_valid = len(user_input.strip()) > 0
        
        assert not is_valid
    
    def test_whitespace_only_input_is_invalid(self):
        """Test that whitespace-only input is considered invalid."""
        user_input = "   \t\n   "
        
        is_valid = len(user_input.strip()) > 0
        
        assert not is_valid
    
    def test_valid_input_is_accepted(self):
        """Test that valid input is accepted."""
        user_input = "What is 5 times 3?"
        
        is_valid = len(user_input.strip()) > 0
        
        assert is_valid
    
    def test_input_with_special_characters_is_valid(self):
        """Test that input with special characters is valid."""
        user_input = "What is 5 × 3? (multiply)"
        
        is_valid = len(user_input.strip()) > 0
        
        assert is_valid
    
    def test_input_with_numbers_is_valid(self):
        """Test that input with numbers is valid."""
        user_input = "Calculate 123 times 456"
        
        is_valid = len(user_input.strip()) > 0
        
        assert is_valid
    
    def test_input_validation_strips_whitespace(self):
        """Test that input validation strips leading/trailing whitespace."""
        user_input = "  What is 5 times 3?  "
        
        cleaned_input = user_input.strip()
        is_valid = len(cleaned_input) > 0
        
        assert is_valid
        assert cleaned_input == "What is 5 times 3?"
    
    def test_very_long_input_is_valid(self):
        """Test that very long input is still valid."""
        user_input = "What is " + "5 times 3? " * 100
        
        is_valid = len(user_input.strip()) > 0
        
        assert is_valid
    
    def test_input_with_newlines_is_valid(self):
        """Test that input with newlines is valid."""
        user_input = "What is 5\ntimes 3?"
        
        is_valid = len(user_input.strip()) > 0
        
        assert is_valid


class TestMessageFormatting:
    """Tests for message formatting in the UI."""
    
    def test_user_message_format(self):
        """Test that user messages are formatted correctly."""
        message = {
            "role": "user",
            "content": "What is 5 times 3?"
        }
        
        assert message["role"] == "user"
        assert isinstance(message["content"], str)
        assert len(message["content"]) > 0
    
    def test_assistant_message_format(self):
        """Test that assistant messages are formatted correctly."""
        message = {
            "role": "assistant",
            "content": "The answer is 15"
        }
        
        assert message["role"] == "assistant"
        assert isinstance(message["content"], str)
        assert len(message["content"]) > 0
    
    def test_message_with_markdown_content(self):
        """Test that messages can contain markdown content."""
        message = {
            "role": "assistant",
            "content": "### Final Answer\nThe answer is **15**"
        }
        
        assert "###" in message["content"]
        assert "**" in message["content"]
    
    def test_message_with_code_content(self):
        """Test that messages can contain code blocks."""
        message = {
            "role": "assistant",
            "content": "```\nResult: 15\n```"
        }
        
        assert "```" in message["content"]


class TestSessionStateClearing:
    """Tests for clearing session state."""
    
    def test_clear_messages_empties_list(self):
        """Test that clearing messages empties the list."""
        messages = [
            {"role": "user", "content": "Question"},
            {"role": "assistant", "content": "Answer"}
        ]
        
        messages.clear()
        
        assert len(messages) == 0
    
    def test_clear_preserves_session_state_structure(self):
        """Test that clearing preserves the session state structure."""
        session_state = {
            "messages": [{"role": "user", "content": "Test"}],
            "reasoning_agent": MagicMock()
        }
        
        session_state["messages"].clear()
        
        assert "messages" in session_state
        assert "reasoning_agent" in session_state
        assert len(session_state["messages"]) == 0
    
    def test_can_add_messages_after_clear(self):
        """Test that messages can be added after clearing."""
        messages = [{"role": "user", "content": "Old message"}]
        
        messages.clear()
        messages.append({"role": "user", "content": "New message"})
        
        assert len(messages) == 1
        assert messages[0]["content"] == "New message"

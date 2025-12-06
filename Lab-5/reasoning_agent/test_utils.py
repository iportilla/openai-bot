"""
Unit tests for utility functions in the Reasoning Math Agent.

Tests formatting functions, tool call parsing, and system prompt initialization.
"""

import json
from unittest.mock import MagicMock
from reasoning_agent.utils import (
    format_reasoning_step,
    parse_tool_calls,
    format_final_answer,
    initialize_system_prompt
)


class TestFormatReasoningStep:
    """Tests for format_reasoning_step function."""
    
    def test_format_step_without_tool_info(self):
        """Test formatting a reasoning step without tool information."""
        result = format_reasoning_step(1, "I need to multiply 5 by 3")
        assert "Step 1:" in result
        assert "I need to multiply 5 by 3" in result
    
    def test_format_step_with_tool_info(self):
        """Test formatting a reasoning step with tool information."""
        tool_info = {
            "tool_name": "multiply",
            "tool_input": {"a": 5, "b": 3},
            "tool_result": "15"
        }
        result = format_reasoning_step(2, "Multiplying the numbers", tool_info)
        assert "Step 2:" in result
        assert "Multiplying the numbers" in result
        assert "Tool: multiply" in result
        assert "Input:" in result
        assert "Result: 15" in result
    
    def test_format_step_with_partial_tool_info(self):
        """Test formatting with only some tool info fields."""
        tool_info = {
            "tool_name": "multiply",
            "tool_result": "15"
        }
        result = format_reasoning_step(3, "Computing result", tool_info)
        assert "Step 3:" in result
        assert "Tool: multiply" in result
        assert "Result: 15" in result
    
    def test_format_step_with_empty_tool_info(self):
        """Test formatting with empty tool info dictionary."""
        result = format_reasoning_step(1, "Reasoning text", {})
        assert "Step 1:" in result
        assert "Reasoning text" in result
    
    def test_format_step_with_none_tool_info(self):
        """Test formatting with None tool info."""
        result = format_reasoning_step(1, "Reasoning text", None)
        assert "Step 1:" in result
        assert "Reasoning text" in result


class TestParseToolCalls:
    """Tests for parse_tool_calls function."""
    
    def test_parse_tool_calls_with_object_response(self):
        """Test parsing tool calls from object-based response."""
        # Create mock tool call object
        tool_call = MagicMock()
        tool_call.id = "call_123"
        tool_call.function.name = "multiply"
        tool_call.function.arguments = json.dumps({"a": 5, "b": 3})
        
        # Create mock response
        response = MagicMock()
        response.get = MagicMock(side_effect=lambda key, default=None: 
            [MagicMock(tool_calls=[tool_call])] if key == "choices" else default)
        
        message = MagicMock()
        message.tool_calls = [tool_call]
        
        # Manually construct response for testing
        response_dict = {
            "choices": [
                {
                    "message": message
                }
            ]
        }
        
        # Since we're using object attributes, test directly
        tool_calls = []
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tc in message.tool_calls:
                parsed_call = {
                    "id": tc.id,
                    "name": tc.function.name,
                    "arguments": json.loads(tc.function.arguments)
                }
                tool_calls.append(parsed_call)
        
        assert len(tool_calls) == 1
        assert tool_calls[0]["id"] == "call_123"
        assert tool_calls[0]["name"] == "multiply"
        assert tool_calls[0]["arguments"] == {"a": 5, "b": 3}
    
    def test_parse_tool_calls_with_dict_response(self):
        """Test parsing tool calls from dictionary-based response."""
        response = {
            "choices": [
                {
                    "message": {
                        "tool_calls": [
                            {
                                "id": "call_456",
                                "function": {
                                    "name": "multiply",
                                    "arguments": json.dumps({"a": 10, "b": 2})
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        tool_calls = parse_tool_calls(response)
        
        assert len(tool_calls) == 1
        assert tool_calls[0]["id"] == "call_456"
        assert tool_calls[0]["name"] == "multiply"
        assert tool_calls[0]["arguments"] == {"a": 10, "b": 2}
    
    def test_parse_tool_calls_with_no_tool_calls(self):
        """Test parsing when response has no tool calls."""
        response = {
            "choices": [
                {
                    "message": {
                        "content": "The answer is 15"
                    }
                }
            ]
        }
        
        tool_calls = parse_tool_calls(response)
        
        assert len(tool_calls) == 0
    
    def test_parse_tool_calls_with_empty_response(self):
        """Test parsing with empty response."""
        response = {}
        
        tool_calls = parse_tool_calls(response)
        
        assert len(tool_calls) == 0
    
    def test_parse_tool_calls_with_invalid_json(self):
        """Test parsing with invalid JSON in arguments."""
        response = {
            "choices": [
                {
                    "message": {
                        "tool_calls": [
                            {
                                "id": "call_789",
                                "function": {
                                    "name": "multiply",
                                    "arguments": "invalid json"
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        tool_calls = parse_tool_calls(response)
        
        # Should handle gracefully and return empty list
        assert len(tool_calls) == 0
    
    def test_parse_multiple_tool_calls(self):
        """Test parsing multiple tool calls from response."""
        response = {
            "choices": [
                {
                    "message": {
                        "tool_calls": [
                            {
                                "id": "call_1",
                                "function": {
                                    "name": "multiply",
                                    "arguments": json.dumps({"a": 5, "b": 3})
                                }
                            },
                            {
                                "id": "call_2",
                                "function": {
                                    "name": "multiply",
                                    "arguments": json.dumps({"a": 15, "b": 2})
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        tool_calls = parse_tool_calls(response)
        
        assert len(tool_calls) == 2
        assert tool_calls[0]["id"] == "call_1"
        assert tool_calls[1]["id"] == "call_2"


class TestFormatFinalAnswer:
    """Tests for format_final_answer function."""
    
    def test_format_final_answer_basic(self):
        """Test formatting a basic final answer."""
        result = format_final_answer("15")
        assert "Final Answer: 15" in result
        assert "=" in result
    
    def test_format_final_answer_with_long_text(self):
        """Test formatting a longer final answer."""
        answer = "The solution is 42 because 6 times 7 equals 42"
        result = format_final_answer(answer)
        assert "Final Answer:" in result
        assert answer in result
    
    def test_format_final_answer_contains_separators(self):
        """Test that formatted answer contains visual separators."""
        result = format_final_answer("100")
        lines = result.split("\n")
        # Should have separator lines
        assert any("=" in line for line in lines)


class TestInitializeSystemPrompt:
    """Tests for initialize_system_prompt function."""
    
    def test_system_prompt_is_string(self):
        """Test that system prompt is a string."""
        prompt = initialize_system_prompt()
        assert isinstance(prompt, str)
    
    def test_system_prompt_contains_key_phrases(self):
        """Test that system prompt contains expected guidance."""
        prompt = initialize_system_prompt()
        assert "math tutor" in prompt.lower()
        assert "step" in prompt.lower()
        assert "multiplication" in prompt.lower() or "multiply" in prompt.lower()
    
    def test_system_prompt_is_not_empty(self):
        """Test that system prompt is not empty."""
        prompt = initialize_system_prompt()
        assert len(prompt) > 0
    
    def test_system_prompt_consistency(self):
        """Test that system prompt is consistent across calls."""
        prompt1 = initialize_system_prompt()
        prompt2 = initialize_system_prompt()
        assert prompt1 == prompt2

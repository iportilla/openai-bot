"""
Utility functions for message formatting and parsing in the Reasoning Math Agent.

This module provides helpers for:
- Formatting reasoning steps for display
- Parsing tool calls from OpenAI API responses
- Formatting final answers
- Initializing system prompts
"""

import json
from typing import Optional, List, Dict, Any


def format_reasoning_step(step_num: int, reasoning: str, tool_info: Optional[Dict[str, Any]] = None) -> str:
    """
    Format a reasoning step for display.
    
    Args:
        step_num: The step number in the reasoning sequence
        reasoning: The reasoning text for this step
        tool_info: Optional dictionary containing tool call information:
                   - tool_name: Name of the tool called
                   - tool_input: Input parameters for the tool
                   - tool_result: Result returned by the tool
    
    Returns:
        Formatted string representation of the reasoning step
    
    Requirements: 1.2, 1.3, 1.4
    """
    formatted = f"Step {step_num}: {reasoning}"
    
    if tool_info:
        if tool_info.get("tool_name"):
            formatted += f"\n  Tool: {tool_info['tool_name']}"
        if tool_info.get("tool_input"):
            formatted += f"\n  Input: {tool_info['tool_input']}"
        if tool_info.get("tool_result"):
            formatted += f"\n  Result: {tool_info['tool_result']}"
    
    return formatted


def parse_tool_calls(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse tool calls from an OpenAI API response.
    
    Extracts tool call information from the response message, handling
    the OpenAI function calling format.
    
    Args:
        response: The response dictionary from OpenAI API chat.completions.create()
    
    Returns:
        List of tool call dictionaries, each containing:
        - id: Unique identifier for the tool call
        - name: Name of the tool to call
        - arguments: Dictionary of arguments for the tool
    
    Requirements: 1.2, 1.3, 1.4
    """
    tool_calls = []
    
    try:
        message = response.get("choices", [{}])[0].get("message", {})
        
        # Check if message has tool_calls attribute (for object responses)
        if hasattr(message, "tool_calls") and message.tool_calls:
            for tool_call in message.tool_calls:
                parsed_call = {
                    "id": tool_call.id,
                    "name": tool_call.function.name,
                    "arguments": json.loads(tool_call.function.arguments)
                }
                tool_calls.append(parsed_call)
        # Also handle dictionary-based responses
        elif isinstance(message, dict) and "tool_calls" in message:
            for tool_call in message["tool_calls"]:
                parsed_call = {
                    "id": tool_call.get("id"),
                    "name": tool_call.get("function", {}).get("name"),
                    "arguments": json.loads(tool_call.get("function", {}).get("arguments", "{}"))
                }
                tool_calls.append(parsed_call)
    except (KeyError, IndexError, json.JSONDecodeError, AttributeError):
        # If parsing fails, return empty list
        pass
    
    return tool_calls


def format_final_answer(answer: str) -> str:
    """
    Format the final answer for display.
    
    Provides clear visual formatting to distinguish the final answer
    from intermediate reasoning steps.
    
    Args:
        answer: The final answer text
    
    Returns:
        Formatted string representation of the final answer
    
    Requirements: 1.2, 1.3, 1.4
    """
    return f"\n{'='*50}\nFinal Answer: {answer}\n{'='*50}"


def initialize_system_prompt() -> str:
    """
    Initialize the system prompt for the reasoning agent.
    
    Returns the system prompt that guides the agent's behavior during
    reasoning and problem-solving.
    
    Returns:
        System prompt string that defines the agent's role and behavior
    
    Requirements: 1.2, 1.3, 1.4
    """
    return """You are a helpful math tutor that solves mathematical problems step-by-step.

Your approach:
1. Break down the problem into logical steps
2. Use the multiplication tool when you need to multiply numbers
3. Show your reasoning clearly at each step
4. Provide a clear final answer

When you have enough information to provide a final answer, state it clearly and concisely.
Do not ask for more information - solve the problem with what you have."""

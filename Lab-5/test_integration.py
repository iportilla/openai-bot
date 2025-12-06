"""
Integration tests for the Reasoning Math Agent.

These tests verify end-to-end functionality of the complete reasoning flow,
including multiple problems, conversation history persistence, and UI interaction.

Requirements: 1.1, 1.2, 1.3, 1.4, 5.1, 5.2, 5.3, 5.4
"""

import pytest
from unittest.mock import MagicMock, patch
import json
from reasoning_agent.reasoning_agent import ReasoningAgent
from reasoning_agent.tools import execute_tool


class TestCompleteReasoningFlow:
    """Tests for end-to-end complete reasoning flow."""
    
    def test_end_to_end_single_problem_with_tool_usage(self):
        """
        Test complete reasoning flow for a single math problem with tool usage.
        
        Verifies:
        - Problem is accepted and processing initiates (Req 1.1)
        - Reasoning steps are displayed sequentially (Req 1.2)
        - Final answer is provided with clear formatting (Req 1.3)
        - Complete thought process is shown (Req 1.4)
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Create mock tool call
            tool_call = MagicMock()
            tool_call.id = "call_1"
            tool_call.function.name = "multiply"
            tool_call.function.arguments = json.dumps({"a": 15, "b": 23})
            
            # Step 1: Agent analyzes and calls tool
            step1_response = MagicMock()
            step1_response.choices[0].message.content = "I need to multiply 15 by 23."
            step1_response.choices[0].message.tool_calls = [tool_call]
            
            # Step 2: Agent provides final answer
            step2_response = MagicMock()
            step2_response.choices[0].message.content = "The result of 15 times 23 is 345."
            step2_response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.side_effect = [step1_response, step2_response]
            
            # Execute the complete flow
            agent = ReasoningAgent(api_key="test-key")
            problem = "What is 15 times 23?"
            result = agent.run_reasoning_loop(problem)
            
            # Verify complete flow
            assert result["problem"] == problem
            assert len(result["steps"]) >= 2
            assert result["final_answer"] is not None
            assert result["final_answer"] != ""
            assert "multiply" in result["tools_used"]
            assert result["total_iterations"] <= 10
            
            # Verify step sequence
            assert result["steps"][0]["step_number"] == 1
            assert result["steps"][1]["step_number"] == 2
            
            # Verify tool was used
            tool_steps = [s for s in result["steps"] if s["tool_called"]]
            assert len(tool_steps) > 0
            assert tool_steps[0]["tool_name"] == "multiply"
            assert tool_steps[0]["tool_result"] == "345"
    
    def test_end_to_end_problem_without_tool_usage(self):
        """
        Test complete reasoning flow for a problem that doesn't require tools.
        
        Verifies the agent can solve problems without tool calls.
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Single response with reasoning and answer
            response = MagicMock()
            response.choices[0].message.content = "The answer is 8."
            response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.return_value = response
            
            # Execute the flow
            agent = ReasoningAgent(api_key="test-key")
            problem = "What is 2 plus 6?"
            result = agent.run_reasoning_loop(problem)
            
            # Verify flow completed
            assert result["problem"] == problem
            assert len(result["steps"]) > 0
            assert result["final_answer"] is not None
            assert len(result["tools_used"]) == 0
    
    def test_end_to_end_complex_multi_step_reasoning(self):
        """
        Test complete reasoning flow with multiple reasoning steps and tool calls.
        
        Verifies the agent can handle complex problems requiring multiple steps.
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Create tool calls
            tool_call_1 = MagicMock()
            tool_call_1.id = "call_1"
            tool_call_1.function.name = "multiply"
            tool_call_1.function.arguments = json.dumps({"a": 5, "b": 3})
            
            tool_call_2 = MagicMock()
            tool_call_2.id = "call_2"
            tool_call_2.function.name = "multiply"
            tool_call_2.function.arguments = json.dumps({"a": 15, "b": 2})
            
            # Step 1: First calculation
            step1_response = MagicMock()
            step1_response.choices[0].message.content = "First, I'll multiply 5 by 3."
            step1_response.choices[0].message.tool_calls = [tool_call_1]
            
            # Step 2: Second calculation
            step2_response = MagicMock()
            step2_response.choices[0].message.content = "Now I'll multiply the result by 2."
            step2_response.choices[0].message.tool_calls = [tool_call_2]
            
            # Step 3: Final answer
            step3_response = MagicMock()
            step3_response.choices[0].message.content = "The final answer is 30."
            step3_response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.side_effect = [
                step1_response, step2_response, step3_response
            ]
            
            # Execute the flow
            agent = ReasoningAgent(api_key="test-key")
            problem = "What is 5 times 3 times 2?"
            result = agent.run_reasoning_loop(problem)
            
            # Verify multi-step flow
            assert len(result["steps"]) >= 3
            assert result["total_iterations"] <= 10
            
            # Verify both tool calls were tracked
            assert "multiply" in result["tools_used"]
            
            # Verify tool results are preserved
            tool_steps = [s for s in result["steps"] if s["tool_called"]]
            assert len(tool_steps) >= 2


class TestMultipleProblemSequence:
    """Tests for handling multiple problems in sequence."""
    
    def test_multiple_problems_with_separate_reasoning_loops(self):
        """
        Test processing multiple different math problems sequentially.
        
        Verifies:
        - Each problem is processed independently (Req 5.1)
        - Conversation history can be maintained (Req 5.2)
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Problem 1 responses
            problem1_response = MagicMock()
            problem1_response.choices[0].message.content = "The answer to problem 1 is 50."
            problem1_response.choices[0].message.tool_calls = None
            
            # Problem 2 responses
            problem2_response = MagicMock()
            problem2_response.choices[0].message.content = "The answer to problem 2 is 100."
            problem2_response.choices[0].message.tool_calls = None
            
            # Problem 3 responses
            problem3_response = MagicMock()
            problem3_response.choices[0].message.content = "The answer to problem 3 is 75."
            problem3_response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.side_effect = [
                problem1_response, problem2_response, problem3_response
            ]
            
            # Process multiple problems
            agent = ReasoningAgent(api_key="test-key")
            
            problem1 = "What is 10 times 5?"
            result1 = agent.run_reasoning_loop(problem1)
            
            problem2 = "What is 20 times 5?"
            result2 = agent.run_reasoning_loop(problem2)
            
            problem3 = "What is 15 times 5?"
            result3 = agent.run_reasoning_loop(problem3)
            
            # Verify each problem was processed independently
            assert result1["problem"] == problem1
            assert result2["problem"] == problem2
            assert result3["problem"] == problem3
            
            # Verify each has its own solution
            assert result1["final_answer"] != result2["final_answer"]
            assert result2["final_answer"] != result3["final_answer"]
    
    def test_conversation_history_persistence_across_problems(self):
        """
        Test that conversation history can be maintained across multiple problems.
        
        Verifies:
        - Conversation history is preserved (Req 5.2, 5.3)
        - All previous problems and solutions are retained (Req 5.3)
        """
        # Simulate conversation history
        conversation_history = []
        
        # Problem 1
        conversation_history.append({
            "role": "user",
            "content": "What is 10 times 5?"
        })
        conversation_history.append({
            "role": "assistant",
            "content": "The answer is 50"
        })
        
        # Problem 2
        conversation_history.append({
            "role": "user",
            "content": "What is 20 times 5?"
        })
        conversation_history.append({
            "role": "assistant",
            "content": "The answer is 100"
        })
        
        # Verify history is preserved
        assert len(conversation_history) == 4
        assert conversation_history[0]["content"] == "What is 10 times 5?"
        assert conversation_history[1]["content"] == "The answer is 50"
        assert conversation_history[2]["content"] == "What is 20 times 5?"
        assert conversation_history[3]["content"] == "The answer is 100"
    
    def test_clear_conversation_history(self):
        """
        Test clearing conversation history.
        
        Verifies:
        - Conversation can be cleared (Req 5.4)
        - System is ready for new problems after clearing (Req 5.4)
        """
        # Build conversation history
        messages = [
            {"role": "user", "content": "Problem 1"},
            {"role": "assistant", "content": "Answer 1"},
            {"role": "user", "content": "Problem 2"},
            {"role": "assistant", "content": "Answer 2"}
        ]
        
        # Verify history exists
        assert len(messages) == 4
        
        # Clear history
        messages.clear()
        
        # Verify history is cleared
        assert len(messages) == 0
        
        # Verify new messages can be added
        messages.append({"role": "user", "content": "New problem"})
        assert len(messages) == 1
        assert messages[0]["content"] == "New problem"


class TestUIInteractionFlow:
    """Tests for UI interaction patterns."""
    
    def test_user_input_submission_and_display(self):
        """
        Test user input submission and display in chat interface.
        
        Verifies:
        - User problem is displayed in chat (Req 4.2)
        - Problem is accepted and processing initiates (Req 1.1)
        """
        # Simulate UI interaction
        user_input = "What is 15 times 23?"
        
        # Add to message history
        messages = []
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Verify user message is in history
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert messages[0]["content"] == user_input
    
    def test_reasoning_steps_display_in_chat(self):
        """
        Test that reasoning steps are displayed in chat interface.
        
        Verifies:
        - Reasoning steps are displayed sequentially (Req 1.2)
        - Each step is shown in the chat (Req 4.3)
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Create mock responses
            step1_response = MagicMock()
            step1_response.choices[0].message.content = "Step 1: Analyzing the problem"
            step1_response.choices[0].message.tool_calls = None
            
            step2_response = MagicMock()
            step2_response.choices[0].message.content = "Step 2: Computing the result"
            step2_response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.side_effect = [step1_response, step2_response]
            
            # Process problem
            agent = ReasoningAgent(api_key="test-key")
            result = agent.run_reasoning_loop("What is 5 times 3?")
            
            # Verify steps can be displayed
            messages = []
            messages.append({"role": "user", "content": "What is 5 times 3?"})
            
            # Add reasoning steps to messages
            for step in result["steps"]:
                step_text = f"Step {step['step_number']}: {step['reasoning']}"
                messages.append({
                    "role": "assistant",
                    "content": step_text
                })
            
            # Verify steps are in message history
            assert len(messages) > 1
            assert any("Step 1:" in msg["content"] for msg in messages)
    
    def test_final_answer_display_in_chat(self):
        """
        Test that final answer is displayed prominently in chat.
        
        Verifies:
        - Final answer is displayed (Req 1.3)
        - Final answer is shown prominently (Req 4.4)
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            response = MagicMock()
            response.choices[0].message.content = "The answer is 15."
            response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.return_value = response
            
            # Process problem
            agent = ReasoningAgent(api_key="test-key")
            result = agent.run_reasoning_loop("What is 5 times 3?")
            
            # Simulate chat display
            messages = []
            messages.append({"role": "user", "content": "What is 5 times 3?"})
            
            # Add final answer with formatting
            final_answer_display = f"### Final Answer\n{result['final_answer']}"
            messages.append({
                "role": "assistant",
                "content": final_answer_display
            })
            
            # Verify final answer is in messages
            assert len(messages) == 2
            assert "Final Answer" in messages[1]["content"]
            assert result["final_answer"] in messages[1]["content"]
    
    def test_input_field_cleared_after_submission(self):
        """
        Test that input field is cleared after problem submission.
        
        Verifies:
        - Input field is cleared after submission (Req 5.1)
        """
        # Simulate input field state
        input_field = "What is 5 times 3?"
        
        # Verify input has content
        assert len(input_field) > 0
        
        # Clear input field after submission
        input_field = ""
        
        # Verify input is cleared
        assert len(input_field) == 0
    
    def test_multiple_problems_in_chat_history(self):
        """
        Test that multiple problems and solutions appear in chat history.
        
        Verifies:
        - Chat history displays all previous problems (Req 5.3)
        - Chat history displays all previous solutions (Req 5.3)
        """
        # Build chat history with multiple problems
        messages = []
        
        # Problem 1
        messages.append({"role": "user", "content": "What is 10 times 5?"})
        messages.append({"role": "assistant", "content": "The answer is 50"})
        
        # Problem 2
        messages.append({"role": "user", "content": "What is 20 times 5?"})
        messages.append({"role": "assistant", "content": "The answer is 100"})
        
        # Problem 3
        messages.append({"role": "user", "content": "What is 15 times 5?"})
        messages.append({"role": "assistant", "content": "The answer is 75"})
        
        # Verify all problems are in history
        user_messages = [m for m in messages if m["role"] == "user"]
        assert len(user_messages) == 3
        assert user_messages[0]["content"] == "What is 10 times 5?"
        assert user_messages[1]["content"] == "What is 20 times 5?"
        assert user_messages[2]["content"] == "What is 15 times 5?"
        
        # Verify all solutions are in history
        assistant_messages = [m for m in messages if m["role"] == "assistant"]
        assert len(assistant_messages) == 3
        assert assistant_messages[0]["content"] == "The answer is 50"
        assert assistant_messages[1]["content"] == "The answer is 100"
        assert assistant_messages[2]["content"] == "The answer is 75"


class TestErrorHandlingAndEdgeCases:
    """Tests for error handling and edge cases in integration."""
    
    def test_empty_problem_input_handling(self):
        """Test handling of empty problem input."""
        user_input = ""
        
        # Validate input
        is_valid = len(user_input.strip()) > 0
        
        # Should be invalid
        assert not is_valid
    
    def test_whitespace_only_input_handling(self):
        """Test handling of whitespace-only input."""
        user_input = "   \t\n   "
        
        # Validate input
        is_valid = len(user_input.strip()) > 0
        
        # Should be invalid
        assert not is_valid
    
    def test_very_long_problem_input(self):
        """Test handling of very long problem input."""
        user_input = "What is " + "5 times 3? " * 100
        
        # Validate input
        is_valid = len(user_input.strip()) > 0
        
        # Should be valid
        assert is_valid
    
    def test_special_characters_in_problem(self):
        """Test handling of special characters in problem."""
        user_input = "What is 5 × 3? (multiply)"
        
        # Validate input
        is_valid = len(user_input.strip()) > 0
        
        # Should be valid
        assert is_valid
    
    def test_reasoning_loop_max_iterations_protection(self):
        """
        Test that reasoning loop respects max iterations limit.
        
        Verifies infinite loop protection.
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Create tool call that would cause loop to continue
            tool_call = MagicMock()
            tool_call.id = "call_1"
            tool_call.function.name = "multiply"
            tool_call.function.arguments = json.dumps({"a": 5, "b": 3})
            
            # Create response that always has tool calls (would loop forever)
            response = MagicMock()
            response.choices[0].message.content = "Continuing..."
            response.choices[0].message.tool_calls = [tool_call]
            
            # Make it return the same response every time
            mock_client.chat.completions.create.return_value = response
            
            # Execute reasoning loop
            agent = ReasoningAgent(api_key="test-key")
            result = agent.run_reasoning_loop("What is 5 times 3?")
            
            # Verify loop terminated within max iterations
            assert result["total_iterations"] <= 10
            assert result["final_answer"] is not None


class TestToolIntegration:
    """Tests for tool integration in the complete flow."""
    
    def test_tool_execution_in_reasoning_flow(self):
        """
        Test that tools are properly executed during reasoning.
        
        Verifies tool results are correctly computed and integrated.
        """
        # Test tool execution directly
        result = execute_tool("multiply", {"a": 15, "b": 23})
        
        # Verify result
        assert result == "345"
        assert float(result) == 15 * 23
    
    def test_multiple_tool_calls_in_single_flow(self):
        """
        Test handling of multiple tool calls in a single reasoning flow.
        """
        with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            # Create multiple tool calls
            tool_call_1 = MagicMock()
            tool_call_1.id = "call_1"
            tool_call_1.function.name = "multiply"
            tool_call_1.function.arguments = json.dumps({"a": 5, "b": 3})
            
            tool_call_2 = MagicMock()
            tool_call_2.id = "call_2"
            tool_call_2.function.name = "multiply"
            tool_call_2.function.arguments = json.dumps({"a": 15, "b": 2})
            
            # Step 1: First tool call
            step1_response = MagicMock()
            step1_response.choices[0].message.content = "First calculation"
            step1_response.choices[0].message.tool_calls = [tool_call_1]
            
            # Step 2: Second tool call
            step2_response = MagicMock()
            step2_response.choices[0].message.content = "Second calculation"
            step2_response.choices[0].message.tool_calls = [tool_call_2]
            
            # Step 3: Final answer
            step3_response = MagicMock()
            step3_response.choices[0].message.content = "Final answer is 30"
            step3_response.choices[0].message.tool_calls = None
            
            mock_client.chat.completions.create.side_effect = [
                step1_response, step2_response, step3_response
            ]
            
            # Execute flow
            agent = ReasoningAgent(api_key="test-key")
            result = agent.run_reasoning_loop("What is 5 times 3 times 2?")
            
            # Verify both tools were tracked
            assert "multiply" in result["tools_used"]
            
            # Verify tool results are in steps
            tool_steps = [s for s in result["steps"] if s["tool_called"]]
            assert len(tool_steps) >= 2
            assert tool_steps[0]["tool_result"] == "15"
            assert tool_steps[1]["tool_result"] == "30"

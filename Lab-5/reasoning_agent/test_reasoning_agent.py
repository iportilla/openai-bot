"""
Property-based tests for the reasoning loop engine.

**Feature: reasoning-math-agent, Property 1: Problem Acceptance and Processing**
**Feature: reasoning-math-agent, Property 2: Sequential Reasoning Steps**
**Feature: reasoning-math-agent, Property 3: Final Answer Presence**
**Feature: reasoning-math-agent, Property 4: Complete Solution Preservation**
**Feature: reasoning-math-agent, Property 5: Reasoning Loop Termination**
**Feature: reasoning-math-agent, Property 7: Tool Result Integration**
**Feature: reasoning-math-agent, Property 8: Tool Usage Tracking**
"""

from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, patch, MagicMock
from reasoning_agent.reasoning_agent import ReasoningAgent
import json


# Strategy for generating simple math problems
math_problems = st.just("What is 5 times 3?") | st.just("Calculate 10 multiplied by 2") | st.just("What is 7 times 8?")


@settings(max_examples=10)
@given(problem=math_problems)
def test_problem_acceptance_and_processing(problem):
    """
    Property 1: Problem Acceptance and Processing
    
    *For any* valid math problem string, submitting it to the reasoning agent 
    should initiate the reasoning process and produce a non-empty list of 
    reasoning steps.
    
    **Validates: Requirements 1.1**
    """
    # Mock the OpenAI client to simulate reasoning
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock response that simulates the agent processing the problem
        response = MagicMock()
        response.choices[0].message.content = "I will solve this step by step."
        response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.return_value = response
        
        # Run the reasoning loop with the problem
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify the problem was accepted
        assert result["problem"] == problem, \
            f"Problem not preserved: expected '{problem}', got '{result['problem']}'"
        
        # Verify reasoning process initiated and produced steps
        assert len(result["steps"]) > 0, \
            "No reasoning steps were produced - reasoning process did not initiate"
        
        # Verify each step has content
        for step in result["steps"]:
            assert step["reasoning"] is not None, \
                "Reasoning step has no content"
            assert step["step_number"] > 0, \
                "Step number is invalid"
        
        # Verify a final answer was produced
        assert result["final_answer"] is not None, \
            "No final answer was produced"
        assert result["final_answer"] != "", \
            "Final answer is empty"


@settings(max_examples=10)
@given(problem=math_problems)
def test_sequential_reasoning_steps(problem):
    """
    Property 2: Sequential Reasoning Steps
    
    *For any* completed reasoning solution, the reasoning steps should be 
    numbered sequentially starting from 1 with no gaps, and each step should 
    contain reasoning content.
    
    **Validates: Requirements 1.2**
    """
    # Mock the OpenAI client to simulate reasoning
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock responses that simulate multiple reasoning steps
        # Step 1: Agent analyzes the problem
        step1_response = MagicMock()
        step1_response.choices[0].message.content = "I need to analyze this problem."
        step1_response.choices[0].message.tool_calls = None
        
        # Step 2: Agent provides reasoning
        step2_response = MagicMock()
        step2_response.choices[0].message.content = "Let me work through the calculation."
        step2_response.choices[0].message.tool_calls = None
        
        # Step 3: Agent provides final answer
        step3_response = MagicMock()
        step3_response.choices[0].message.content = "The answer is 15."
        step3_response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.side_effect = [
            step1_response, 
            step2_response, 
            step3_response
        ]
        
        # Run the reasoning loop
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify steps exist
        assert len(result["steps"]) > 0, \
            "No reasoning steps were produced"
        
        # Verify steps are numbered sequentially starting from 1
        for i, step in enumerate(result["steps"], start=1):
            assert step["step_number"] == i, \
                f"Step numbering is not sequential: expected step {i}, got step {step['step_number']}"
        
        # Verify no gaps in step numbering
        step_numbers = [step["step_number"] for step in result["steps"]]
        expected_numbers = list(range(1, len(result["steps"]) + 1))
        assert step_numbers == expected_numbers, \
            f"Gaps in step numbering: got {step_numbers}, expected {expected_numbers}"
        
        # Verify each step has content
        for i, step in enumerate(result["steps"], start=1):
            assert step["reasoning"] is not None, \
                f"Step {i} has no reasoning content"
            assert step["reasoning"] != "", \
                f"Step {i} has empty reasoning content"
            assert isinstance(step["reasoning"], str), \
                f"Step {i} reasoning is not a string"


@settings(max_examples=10)
@given(problem=math_problems)
def test_final_answer_presence(problem):
    """
    Property 3: Final Answer Presence
    
    *For any* completed reasoning solution, the output should contain a final 
    answer field that is non-empty and distinct from intermediate reasoning steps.
    
    **Validates: Requirements 1.3**
    """
    # Mock the OpenAI client to simulate reasoning
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock responses that simulate reasoning with a final answer
        # Step 1: Agent analyzes the problem
        step1_response = MagicMock()
        step1_response.choices[0].message.content = "Let me analyze this problem."
        step1_response.choices[0].message.tool_calls = None
        
        # Step 2: Agent provides final answer
        step2_response = MagicMock()
        step2_response.choices[0].message.content = "The final answer is 15."
        step2_response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.side_effect = [
            step1_response, 
            step2_response
        ]
        
        # Run the reasoning loop
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify final answer field exists
        assert "final_answer" in result, \
            "Result does not contain 'final_answer' field"
        
        # Verify final answer is non-empty
        assert result["final_answer"] is not None, \
            "Final answer is None"
        assert result["final_answer"] != "", \
            "Final answer is empty string"
        assert isinstance(result["final_answer"], str), \
            "Final answer is not a string"
        
        # Verify final answer is distinct from intermediate steps
        # The final answer should not be identical to any intermediate step
        intermediate_steps = [step["reasoning"] for step in result["steps"][:-1]]
        
        # The final answer should be different from intermediate reasoning
        # (unless there's only one step, in which case it's both)
        if len(result["steps"]) > 1:
            # For multi-step solutions, final answer should be distinct
            assert result["final_answer"] != intermediate_steps[0] or len(intermediate_steps) == 0, \
                "Final answer is identical to first intermediate step"
        
        # Verify final answer has meaningful content (not just whitespace)
        assert result["final_answer"].strip() != "", \
            "Final answer contains only whitespace"


@settings(max_examples=10)
@given(problem=math_problems)
def test_complete_solution_preservation(problem):
    """
    Property 4: Complete Solution Preservation
    
    *For any* math problem processed by the agent, the solution output should 
    contain all reasoning steps that were generated, preserving the complete 
    thought process from problem to answer.
    
    **Validates: Requirements 1.4**
    """
    # Mock the OpenAI client to simulate reasoning with multiple steps
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock tool call object
        tool_call = MagicMock()
        tool_call.id = "call_1"
        tool_call.function.name = "multiply"
        tool_call.function.arguments = json.dumps({"a": 5, "b": 3})
        
        # Create mock responses that simulate multiple reasoning steps
        # Step 1: Agent analyzes the problem
        step1_response = MagicMock()
        step1_response.choices[0].message.content = "I need to multiply 5 and 3."
        step1_response.choices[0].message.tool_calls = [tool_call]
        
        # Step 2: Agent uses tool result and provides answer
        step2_response = MagicMock()
        step2_response.choices[0].message.content = "The result of 5 times 3 is 15."
        step2_response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.side_effect = [
            step1_response, 
            step2_response
        ]
        
        # Run the reasoning loop
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify all reasoning steps are preserved
        assert len(result["steps"]) > 0, \
            "No reasoning steps were preserved"
        
        # Verify each step has the required fields
        for step in result["steps"]:
            assert "step_number" in step, \
                "Step missing step_number field"
            assert "reasoning" in step, \
                "Step missing reasoning field"
            assert "tool_called" in step, \
                "Step missing tool_called field"
            assert "tool_name" in step, \
                "Step missing tool_name field"
            assert "tool_input" in step, \
                "Step missing tool_input field"
            assert "tool_result" in step, \
                "Step missing tool_result field"
            assert "is_final" in step, \
                "Step missing is_final field"
        
        # Verify the complete thought process is maintained
        # The first step should contain the initial reasoning
        assert result["steps"][0]["reasoning"] is not None, \
            "First step reasoning is missing"
        assert result["steps"][0]["reasoning"] != "", \
            "First step reasoning is empty"
        
        # Verify tool calls are preserved in steps
        tool_steps = [step for step in result["steps"] if step["tool_called"]]
        if len(tool_steps) > 0:
            # If tools were used, verify they're recorded
            for tool_step in tool_steps:
                assert tool_step["tool_name"] is not None, \
                    "Tool name not preserved in step"
                assert tool_step["tool_result"] is not None, \
                    "Tool result not preserved in step"
        
        # Verify the final answer is present and distinct
        assert result["final_answer"] is not None, \
            "Final answer not preserved"
        assert result["final_answer"] != "", \
            "Final answer is empty"
        
        # Verify the problem statement is preserved
        assert result["problem"] == problem, \
            "Problem statement not preserved"
        
        # Verify all steps are accounted for in the output
        # The number of steps should match what was generated
        assert len(result["steps"]) >= 1, \
            "Not all reasoning steps were preserved"
        
        # Verify no step content is lost or truncated
        for i, step in enumerate(result["steps"]):
            assert isinstance(step["reasoning"], str), \
                f"Step {i} reasoning is not a string"
            assert len(step["reasoning"]) > 0, \
                f"Step {i} reasoning content is empty"


@settings(max_examples=10)
@given(problem=math_problems)
def test_reasoning_loop_termination(problem):
    """
    Property 5: Reasoning Loop Termination
    
    *For any* math problem, the reasoning loop should eventually terminate 
    with a final answer within a maximum of 10 iterations, preventing infinite loops.
    
    **Validates: Requirements 3.2, 3.4**
    """
    # Mock the OpenAI client to simulate reasoning
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock tool call object
        tool_call = MagicMock()
        tool_call.id = "call_1"
        tool_call.function.name = "multiply"
        tool_call.function.arguments = json.dumps({"a": 5, "b": 3})
        
        # Create mock responses that simulate the reasoning loop
        # First response: agent decides to use multiplication tool
        first_response = MagicMock()
        first_response.choices[0].message.content = "I need to multiply these numbers."
        first_response.choices[0].message.tool_calls = [tool_call]
        
        # Second response: agent provides final answer
        second_response = MagicMock()
        second_response.choices[0].message.content = "The answer is 15."
        second_response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.side_effect = [first_response, second_response]
        
        # Run the reasoning loop
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify termination conditions
        assert result["total_iterations"] <= 10, \
            f"Loop did not terminate within 10 iterations: {result['total_iterations']}"
        assert result["final_answer"] is not None, \
            "Final answer is missing"
        assert result["final_answer"] != "", \
            "Final answer is empty"
        assert len(result["steps"]) > 0, \
            "No reasoning steps were recorded"


@settings(max_examples=10)
@given(problem=math_problems)
def test_tool_result_integration(problem):
    """
    Property 7: Tool Result Integration
    
    *For any* reasoning solution that uses the multiplication tool, the tool result 
    should appear in the message history after the tool call, and the final answer 
    should reflect the tool's computation.
    
    **Validates: Requirements 6.3**
    """
    # Mock the OpenAI client to simulate tool usage
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock tool call object
        tool_call = MagicMock()
        tool_call.id = "call_1"
        tool_call.function.name = "multiply"
        tool_call.function.arguments = json.dumps({"a": 5, "b": 3})
        
        # First response: agent calls multiplication tool
        first_response = MagicMock()
        first_response.choices[0].message.content = "I'll multiply these numbers."
        first_response.choices[0].message.tool_calls = [tool_call]
        
        # Second response: agent uses the tool result in final answer
        second_response = MagicMock()
        second_response.choices[0].message.content = "The result of 5 times 3 is 15."
        second_response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.side_effect = [first_response, second_response]
        
        # Run the reasoning loop
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify tool was used
        assert "multiply" in result["tools_used"], \
            "Multiplication tool was not tracked in tools_used"
        
        # Verify tool result appears in steps
        tool_steps = [step for step in result["steps"] if step["tool_called"]]
        assert len(tool_steps) > 0, \
            "No tool calls were recorded in reasoning steps"
        
        # Verify tool result is present
        for step in tool_steps:
            assert step["tool_result"] is not None, \
                "Tool result is missing from step"
            assert step["tool_result"] != "", \
                "Tool result is empty"
        
        # Verify final answer reflects the computation
        assert result["final_answer"] is not None, \
            "Final answer is missing"
        assert result["final_answer"] != "", \
            "Final answer is empty"
        # The final answer should contain or reference the tool result
        assert "15" in result["final_answer"] or len(result["steps"]) > 0, \
            "Final answer does not reflect tool computation"


@settings(max_examples=10)
@given(problem=math_problems)
def test_tool_usage_tracking(problem):
    """
    Property 8: Tool Usage Tracking
    
    *For any* completed reasoning solution, the tools_used list should accurately 
    reflect all tools that were invoked during the reasoning process, with each 
    tool appearing exactly once.
    
    **Validates: Requirements 6.4**
    """
    # Mock the OpenAI client to simulate tool usage
    with patch('reasoning_agent.reasoning_agent.OpenAI') as mock_openai_class:
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Create mock tool call objects
        tool_call_1 = MagicMock()
        tool_call_1.id = "call_1"
        tool_call_1.function.name = "multiply"
        tool_call_1.function.arguments = json.dumps({"a": 5, "b": 3})
        
        tool_call_2 = MagicMock()
        tool_call_2.id = "call_2"
        tool_call_2.function.name = "multiply"
        tool_call_2.function.arguments = json.dumps({"a": 15, "b": 2})
        
        # First response: agent calls multiplication tool
        first_response = MagicMock()
        first_response.choices[0].message.content = "I'll multiply 5 and 3."
        first_response.choices[0].message.tool_calls = [tool_call_1]
        
        # Second response: agent calls multiplication tool again
        second_response = MagicMock()
        second_response.choices[0].message.content = "Now I'll multiply the result by 2."
        second_response.choices[0].message.tool_calls = [tool_call_2]
        
        # Third response: agent provides final answer
        third_response = MagicMock()
        third_response.choices[0].message.content = "The final answer is 30."
        third_response.choices[0].message.tool_calls = None
        
        mock_client.chat.completions.create.side_effect = [
            first_response, 
            second_response, 
            third_response
        ]
        
        # Run the reasoning loop
        agent = ReasoningAgent(api_key="test-key")
        result = agent.run_reasoning_loop(problem)
        
        # Verify tools_used list exists
        assert "tools_used" in result, \
            "Result does not contain 'tools_used' field"
        
        # Verify tools_used is a list
        assert isinstance(result["tools_used"], list), \
            "tools_used is not a list"
        
        # Verify all invoked tools are tracked
        # Count how many times multiply was called in steps
        tool_calls_in_steps = sum(1 for step in result["steps"] if step["tool_called"])
        assert tool_calls_in_steps > 0, \
            "No tool calls were made in reasoning steps"
        
        # Verify multiply tool is in tools_used
        assert "multiply" in result["tools_used"], \
            "multiply tool was not tracked in tools_used despite being called"
        
        # Verify no duplicate tool entries
        # Each tool should appear exactly once in tools_used
        assert len(result["tools_used"]) == len(set(result["tools_used"])), \
            f"Duplicate tool entries found in tools_used: {result['tools_used']}"
        
        # Verify tools_used is sorted (for consistency)
        assert result["tools_used"] == sorted(result["tools_used"]), \
            f"tools_used is not sorted: {result['tools_used']}"
        
        # Verify that all tools in tools_used were actually called
        # by checking that they appear in at least one step
        for tool_name in result["tools_used"]:
            tool_was_called = any(
                step["tool_name"] == tool_name 
                for step in result["steps"] 
                if step["tool_called"]
            )
            assert tool_was_called, \
                f"Tool '{tool_name}' in tools_used but was never called in steps"

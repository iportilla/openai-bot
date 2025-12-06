# Implementation Plan: Reasoning Math Agent

## Overview
This implementation plan breaks down the Reasoning Math Agent into discrete, manageable coding tasks. Each task builds incrementally on previous tasks, starting with core utilities and the reasoning engine, then building the UI, and finally adding comprehensive tests.

---

- [x] 1. Set up project structure and core utilities
  - Create `Lab-5/` directory with subdirectories: `Lab-5/reasoning_agent/`
  - Create `Lab-5/requirements.txt` with dependencies: `openai`, `streamlit`, `python-dotenv`, `hypothesis`
  - Create `Lab-5/.env.sample` with template for `OPENAI_API_KEY`
  - Create `Lab-5/README.md` with lab overview and instructions
  - _Requirements: 1.1, 3.1_

- [x] 2. Implement tool registry and multiplication tool
  - Create `Lab-5/reasoning_agent/tools.py` with:
    - `multiply(a: float, b: float) -> float` function
    - `get_tool_definitions()` function that returns OpenAI function calling format
    - `execute_tool(tool_name: str, tool_input: dict) -> str` function for tool execution
  - _Requirements: 6.1, 6.2_

- [x] 2.1 Write property test for multiplication tool
  - **Property 6: Multiplication Tool Correctness**
  - **Validates: Requirements 6.2**
  - Use `hypothesis` to generate random numeric inputs
  - Verify `multiply(a, b) == a * b` for all inputs

- [x] 3. Implement reasoning loop engine
  - Create `Lab-5/reasoning_agent/reasoning_agent.py` with:
    - `ReasoningAgent` class with initialization of OpenAI client
    - `run_reasoning_loop(problem: str, messages: list) -> dict` method
    - Loop logic that:
      - Calls OpenAI API with tool definitions
      - Parses tool calls from responses
      - Executes tools and collects results
      - Adds results back to message history
      - Determines when problem is solved (max 10 iterations)
      - Returns structured output with all steps
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 6.1, 6.3_

- [x] 3.1 Write property test for reasoning loop termination
  - **Property 5: Reasoning Loop Termination**
  - **Validates: Requirements 3.2, 3.4**
  - Verify loop terminates within 10 iterations
  - Verify final answer is present in output

- [x] 3.2 Write property test for tool result integration
  - **Property 7: Tool Result Integration**
  - **Validates: Requirements 6.3**
  - Verify tool results appear in message history
  - Verify final answer reflects tool computation

- [x] 4. Implement message formatting and utilities
  - Create `Lab-5/reasoning_agent/utils.py` with:
    - `format_reasoning_step(step_num: int, reasoning: str, tool_info: dict) -> str` function
    - `parse_tool_calls(response: dict) -> list` function
    - `format_final_answer(answer: str) -> str` function
    - `initialize_system_prompt() -> str` function
  - _Requirements: 1.2, 1.3, 1.4_

- [x] 4.1 Write unit tests for message formatting
  - Test formatting functions produce expected output
  - Test parsing of tool calls from API responses
  - Test system prompt initialization

- [x] 5. Implement Streamlit web interface
  - Create `Lab-5/app.py` with:
    - Streamlit page configuration and title
    - Session state initialization for message history
    - Chat message display loop using `st.chat_message()`
    - User input field using `st.chat_input()`
    - Integration with `ReasoningAgent` to process problems
    - Display of reasoning steps as they're generated
    - Clear visual separation between steps and final answer
    - Button to clear conversation history
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 5.1 Write unit tests for Streamlit components
  - Test session state management
  - Test message history persistence
  - Test input validation

- [x] 6. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Write property test for problem acceptance and processing
  - **Property 1: Problem Acceptance and Processing**
  - **Validates: Requirements 1.1**
  - Generate random math problems
  - Verify reasoning process initiates and produces steps

- [x] 8. Write property test for sequential reasoning steps
  - **Property 2: Sequential Reasoning Steps**
  - **Validates: Requirements 1.2**
  - Verify steps are numbered sequentially
  - Verify no gaps in step numbering
  - Verify each step has content

- [x] 9. Write property test for final answer presence
  - **Property 3: Final Answer Presence**
  - **Validates: Requirements 1.3**
  - Verify final answer field exists
  - Verify final answer is non-empty
  - Verify final answer is distinct from steps

- [x] 10. Write property test for complete solution preservation
  - **Property 4: Complete Solution Preservation**
  - **Validates: Requirements 1.4**
  - Verify all reasoning steps are preserved
  - Verify complete thought process is maintained

- [x] 11. Write property test for tool usage tracking
  - **Property 8: Tool Usage Tracking**
  - **Validates: Requirements 6.4**
  - Verify tools_used list is accurate
  - Verify no duplicate tool entries
  - Verify all invoked tools are tracked

- [x] 12. Final Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Write integration tests
  - Create `Lab-5/test_integration.py` with:
    - End-to-end test of complete reasoning flow
    - Test with multiple different math problems
    - Verify conversation history across multiple problems
    - Test UI interaction flow
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 5.1, 5.2, 5.3, 5.4_

- [x] 14. Write documentation and examples
  - Create example problems and expected outputs
  - Document the reasoning loop pattern
  - Add inline code comments explaining agentic flow
  - Create usage guide in README

# How Kiro Created Lab 5: A Guide for Junior Developers

## Introduction

This document explains how **Kiro**, an AI-powered IDE assistant, created Lab 5 (Reasoning Math Agent) from scratch. If you're a junior developer or CS student, this guide will help you understand the **spec-driven development process** and how AI can help you build complex features systematically.

## What is Kiro?

Kiro is an intelligent development assistant that helps you:
- Transform rough ideas into detailed specifications
- Design systems with formal correctness properties
- Create implementation plans with clear tasks
- Write and test code incrementally
- Document your work comprehensively

Think of Kiro as a senior developer who guides you through the entire development process, from initial concept to working code.

## The Three-Phase Development Process

Kiro used a structured three-phase approach to create Lab 5:

### Phase 1: Requirements Gathering 📋

**What happened:**
- Kiro took the initial idea: "Build an educational chatbot that demonstrates agentic reasoning"
- Converted it into formal requirements using the EARS (Easy Approach to Requirements Syntax) pattern
- Created acceptance criteria that could be tested

**Key files created:**
- `.kiro/specs/reasoning-math-agent/requirements.md`

**Why this matters:**
- Requirements define WHAT the system should do (not HOW)
- They're written in a structured format that's unambiguous
- Each requirement has acceptance criteria that can be verified

**Example requirement from Lab 5:**
```
Requirement 1: Problem Acceptance and Processing
User Story: As a student, I want to see how the agent solves math problems 
step-by-step, so that I can understand the reasoning process.

Acceptance Criteria:
1. WHEN a user submits a math problem THEN the system SHALL accept 
   the problem and initiate the reasoning process
2. WHEN the agent reasons through a problem THEN the system SHALL 
   display each reasoning step sequentially
```

### Phase 2: System Design 🏗️

**What happened:**
- Kiro designed the architecture based on requirements
- Identified components (UI, reasoning engine, tools, utilities)
- Defined data models and interfaces
- **Most importantly**: Created correctness properties

**Key files created:**
- `.kiro/specs/reasoning-math-agent/design.md`

**The Design Document Includes:**

1. **Architecture Diagrams** - Visual representation of how components interact
2. **Component Descriptions** - What each piece does
3. **Data Models** - Structure of data flowing through the system
4. **Correctness Properties** - Formal statements about what the system should do

**Example Correctness Property:**
```
Property 1: Problem Acceptance and Processing
For any valid math problem string, submitting it to the reasoning agent 
should initiate the reasoning process and produce a non-empty list of 
reasoning steps.
```

**Why Correctness Properties Matter:**
- They bridge the gap between human requirements and machine-verifiable code
- They enable property-based testing (testing with many random inputs)
- They catch bugs that unit tests might miss

### Phase 3: Implementation Planning 📝

**What happened:**
- Kiro broke down the design into concrete coding tasks
- Created a task list with clear dependencies
- Marked some tasks as optional (tests, documentation)
- Ensured each task was actionable by a developer

**Key files created:**
- `.kiro/specs/reasoning-math-agent/tasks.md`

**Task Structure:**
```
- [ ] 1. Set up project structure and core utilities
  - Create Lab-5/ directory with subdirectories
  - Create requirements.txt with dependencies
  - Create .env.sample with template

- [ ] 2. Implement tool registry and multiplication tool
  - Create tools.py with multiply() function
  - Create get_tool_definitions() for OpenAI format
  - Create execute_tool() for tool execution

- [ ]* 2.1 Write property test for multiplication tool
  - Property 6: Multiplication Tool Correctness
  - Validates: Requirements 6.2
```

**Key Features:**
- Tasks build incrementally (each depends on previous ones)
- Sub-tasks marked with `*` are optional (tests, documentation)
- Each task references specific requirements
- Property-based tests are integrated into the implementation flow

## The Spec-Driven Development Workflow

Here's the workflow Kiro followed:

```
1. REQUIREMENTS PHASE
   ├─ Gather initial idea
   ├─ Write user stories
   ├─ Define acceptance criteria
   └─ Get user approval

2. DESIGN PHASE
   ├─ Create architecture
   ├─ Define components
   ├─ Analyze acceptance criteria for testability
   ├─ Write correctness properties
   └─ Get user approval

3. IMPLEMENTATION PHASE
   ├─ Create task list
   ├─ Execute tasks incrementally
   ├─ Write code and tests
   ├─ Verify against correctness properties
   └─ Get user approval

4. DOCUMENTATION PHASE
   ├─ Write comprehensive README
   ├─ Add inline code comments
   ├─ Create usage examples
   └─ Document the agentic pattern
```

## Key Concepts Kiro Used

### 1. EARS Pattern (Requirements)

EARS provides six patterns for writing requirements:

- **Ubiquitous**: "THE system SHALL do X"
- **Event-driven**: "WHEN Y happens, THE system SHALL do X"
- **State-driven**: "WHILE in state Z, THE system SHALL do X"
- **Unwanted event**: "IF bad thing happens, THEN THE system SHALL do X"
- **Optional feature**: "WHERE option is enabled, THE system SHALL do X"
- **Complex**: Combinations of the above

**Why it matters:** Removes ambiguity and ensures requirements are testable.

### 2. Correctness Properties (Design)

Kiro identified 8 correctness properties for Lab 5:

1. **Problem Acceptance** - Agent accepts and processes problems
2. **Sequential Steps** - Reasoning steps are numbered correctly
3. **Final Answer** - Solution has a clear final answer
4. **Solution Preservation** - All steps are preserved
5. **Loop Termination** - Loop exits within 10 iterations
6. **Tool Correctness** - Multiplication tool works correctly
7. **Tool Integration** - Tool results are incorporated
8. **Tool Tracking** - Tool usage is tracked accurately

**Why it matters:** These properties can be tested with property-based testing, catching bugs across many inputs.

### 3. Property-Based Testing (Implementation)

Instead of writing one test case:
```python
def test_multiply():
    assert multiply(2, 3) == 6
```

Kiro used property-based testing:
```python
@given(st.floats(), st.floats())
def test_multiply_property(a, b):
    result = multiply(a, b)
    assert result == a * b
```

**Why it matters:** Tests hundreds of random inputs automatically, finding edge cases you wouldn't think of.

## How Kiro Fixed Bugs

During implementation, Kiro encountered two critical bugs:

### Bug #1: Missing `type` Field in Tool Calls

**Error:** `Missing required parameter: 'messages[2].tool_calls[0].type'`

**Root Cause:** OpenAI API requires `type: "function"` for each tool call

**Fix:** Added the missing field to the tool call structure

**Lesson:** Always check API documentation for required fields

### Bug #2: Incorrect Message Role for Tool Results

**Error:** `An assistant message with 'tool_calls' must be followed by tool messages`

**Root Cause:** Tool results were being added as "user" messages instead of "tool" messages

**Fix:** Changed message role from "user" to "tool" and added `tool_call_id`

**Lesson:** Message format matters - OpenAI has specific requirements for tool calling

## The Agentic Reasoning Pattern

Lab 5 teaches a fundamental pattern for building autonomous agents:

```
User Problem
    ↓
Agent Reasoning Loop
    ├─ Call OpenAI API with tool definitions
    ├─ Model decides if tools are needed
    ├─ If yes: Execute tools, add results to history
    ├─ If no: Problem is solved
    └─ Repeat until solved
    ↓
Final Answer with Complete Reasoning
```

**Why this pattern matters:**
- It's used in research agents, code generation, data analysis, and more
- It demonstrates how AI can break down complex problems
- It shows how to maintain context across multiple steps
- It's transparent - users see the complete reasoning process

## Files Created by Kiro

### Specification Files (`.kiro/specs/reasoning-math-agent/`)
- `requirements.md` - Formal requirements with acceptance criteria
- `design.md` - Architecture, components, correctness properties
- `tasks.md` - Implementation plan with 14 tasks

### Implementation Files (`Lab-5/`)
- `app.py` - Streamlit web interface
- `reasoning_agent/reasoning_agent.py` - Core reasoning loop
- `reasoning_agent/tools.py` - Tool registry and definitions
- `reasoning_agent/utils.py` - Helper functions
- `requirements.txt` - Python dependencies
- `.env.sample` - Environment variable template
- `README.md` - Comprehensive documentation

### Test Files (`Lab-5/reasoning_agent/`)
- `test_reasoning_agent.py` - Tests for reasoning loop
- `test_tools.py` - Tests for tool execution
- `test_utils.py` - Tests for utility functions
- `test_streamlit_components.py` - Tests for UI components

## Learning Outcomes

By studying how Kiro created Lab 5, you'll learn:

1. **Spec-Driven Development** - How to plan before coding
2. **Formal Requirements** - How to write unambiguous specifications
3. **System Design** - How to architect complex systems
4. **Correctness Properties** - How to think about what "correct" means
5. **Property-Based Testing** - How to test with random inputs
6. **Agentic Patterns** - How to build autonomous systems
7. **Iterative Development** - How to build incrementally
8. **Documentation** - How to explain complex systems

## How You Can Use This Approach

### For Your Own Projects:

1. **Start with requirements** - Write down what your system should do
2. **Design before coding** - Think about architecture and correctness
3. **Plan your tasks** - Break work into manageable pieces
4. **Test as you go** - Write tests alongside code
5. **Document thoroughly** - Explain your design decisions

### For Learning:

1. **Read the spec files** - Understand the requirements and design
2. **Study the code** - See how design translates to implementation
3. **Run the tests** - Verify the correctness properties
4. **Modify and experiment** - Add new tools, change the system prompt
5. **Build your own agent** - Apply these patterns to your own problems

## Key Takeaways

- **Kiro is a workflow tool** - It guides you through systematic development
- **Specs matter** - Clear requirements and design prevent bugs
- **Correctness properties are powerful** - They catch bugs across many inputs
- **Agentic patterns are fundamental** - They're used in many AI systems
- **Documentation is essential** - It helps others (and future you) understand your work
- **Iterative development works** - Build incrementally, test continuously

## Next Steps

1. **Run Lab 5** - Try the reasoning agent with different problems
2. **Read the code** - Study how the agentic pattern is implemented
3. **Modify it** - Add new tools (division, square root, etc.)
4. **Build your own** - Create an agent for a different domain
5. **Use Kiro** - Apply this workflow to your own projects

## Resources

- **Lab 5 README**: Comprehensive guide to the reasoning agent
- **Design Document**: Detailed architecture and correctness properties
- **Requirements Document**: Formal specifications with acceptance criteria
- **Task List**: Implementation plan with 14 tasks
- **OpenAI Documentation**: Function calling and chat completions
- **Streamlit Documentation**: Building interactive web apps

## Questions?

If you have questions about:
- **How Kiro works** - Check the spec files
- **How to run Lab 5** - See the README in Lab-5/
- **How the agentic pattern works** - Study reasoning_agent.py
- **How to extend it** - See the "Extending the Agent" section in README

---

**Created by Kiro** - An AI-powered IDE assistant for spec-driven development

**Target Audience:** Junior developers, CS students, anyone learning about AI agents and systematic development

**Last Updated:** December 2024

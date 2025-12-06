# Lab 5: Reasoning Math Agent

## Overview

The Reasoning Math Agent is an educational chatbot that demonstrates agentic reasoning patterns by solving mathematical problems step-by-step. This lab teaches how to implement multi-step reasoning loops using the OpenAI API, where the agent iteratively processes problems and generates structured solutions.

## Learning Objectives

- Understand agentic reasoning patterns and multi-step problem solving
- Implement a reasoning loop that iterates until a problem is solved
- Use OpenAI's function calling capabilities to invoke tools
- Build a Streamlit web interface for interactive problem solving
- Learn how to structure agent outputs with reasoning steps and final answers

## Key Concepts

### Reasoning Loop
The core of this lab is the **reasoning loop** - an iterative process where:
1. The agent receives a math problem
2. It calls the OpenAI API with tool definitions
3. The model may request tool calls (e.g., multiplication)
4. The agent executes tools and returns results
5. The loop continues until the problem is solved
6. The final answer is returned with all reasoning steps

### Tool Calling
The agent uses OpenAI's function calling feature to invoke external tools:
- **Multiplication Tool**: Performs multiplication of two numbers
- Tools are defined in OpenAI format and the model decides when to call them
- Tool results are fed back into the reasoning loop

### Agentic Patterns
This lab demonstrates fundamental agent patterns:
- **Iterative reasoning**: Breaking problems into steps
- **Tool usage**: Invoking external functions during reasoning
- **State management**: Maintaining conversation history and reasoning steps
- **Termination conditions**: Knowing when the problem is solved

## Project Structure

```
Lab-5/
├── app.py                      # Streamlit web interface
├── reasoning_agent/
│   ├── __init__.py
│   ├── reasoning_agent.py      # Core reasoning loop engine
│   ├── tools.py                # Tool registry and definitions
│   └── utils.py                # Utility functions
├── requirements.txt            # Python dependencies
├── .env.sample                 # Environment variable template
└── README.md                   # This file
```

## Setup Instructions

### 1. Create Virtual Environment
```bash
cd Lab-5
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.sample .env
# Edit .env and add your OpenAI API key
```

### 4. Run the Application
```bash
streamlit run app.py
```

## How to Use

1. Start the application with `streamlit run app.py`
2. Enter a math problem in the chat input (e.g., "What is 15 times 23?")
3. Watch as the agent reasons through the problem step-by-step
4. The agent will show:
   - Each reasoning step
   - Any tools it calls (like multiplication)
   - The final answer
5. Submit multiple problems to explore different types of math reasoning

## Example Problems

### Simple Multiplication
- "What is 12 times 8?"
- "Calculate 25 multiplied by 4"
- "What is the product of 100 and 5?"

### Word Problems
- "If I have 3 groups of 7 items, how many total?"
- "A store sells 15 items per day. How many items are sold in 6 days?"
- "If each box contains 24 eggs and I have 5 boxes, how many eggs total?"

### Multi-Step Problems
- "What is 10 times 5, then multiply that result by 2?"
- "Calculate 7 times 8, then add 10 to the result"

### Expected Output Example

For the problem "What is 15 times 23?", the agent produces:

```
Step 1: I need to find the product of 15 and 23. Let me use the multiplication tool.
  Tool: multiply
  Input: {'a': 15, 'b': 23}
  Result: 345

Step 2: The multiplication is complete. The product of 15 and 23 is 345.

Final Answer: The product of 15 and 23 is 345.
```

## Architecture

The application consists of four main components:

### 1. Streamlit UI (`app.py`)
- Displays chat interface with message history
- Accepts user input for math problems
- Streams reasoning steps and final answers
- Manages session state for conversation history

### 2. Reasoning Loop Engine (`reasoning_agent.py`)
- Implements the core agentic reasoning pattern
- Calls OpenAI API with tool definitions
- Parses and executes tool calls
- Determines when reasoning is complete
- Returns structured output with all steps

### 3. Tool Registry (`tools.py`)
- Defines available tools (multiplication tool)
- Provides tool definitions in OpenAI format
- Executes tool calls and returns results

### 4. Utilities (`utils.py`)
- OpenAI API client initialization
- Message formatting helpers
- Tool result formatting
- System prompt initialization

## Understanding the Reasoning Loop

The reasoning loop is the heart of this agent. It's an iterative process where the agent reasons about a problem, decides whether to call tools, processes results, and determines when the problem is solved.

### High-Level Flow

```
1. User submits: "What is 15 times 23?"
2. Agent initializes message history with the problem
3. Agent calls OpenAI API with tool definitions
4. Model responds: "I need to multiply 15 by 23"
5. Agent executes: multiply(15, 23) → 345
6. Agent adds result to message history
7. Agent calls OpenAI API again with the result
8. Model responds: "The answer is 345"
9. Agent detects problem is solved
10. Agent returns final answer with all reasoning steps
```

### Detailed Reasoning Loop Pattern

The `run_reasoning_loop()` method in `reasoning_agent.py` implements this pattern:

```python
# 1. Initialize message history with the problem
messages = [{"role": "user", "content": problem}]

# 2. Loop until problem is solved (max 10 iterations)
while iteration < max_iterations:
    # 3. Call OpenAI API with tool definitions
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=get_tool_definitions()  # Includes multiply tool
    )
    
    # 4. Add assistant's response to message history
    messages.append({"role": "assistant", "content": response})
    
    # 5. Check if model requested tool calls
    if response.tool_calls:
        # 6. Execute each tool call
        for tool_call in response.tool_calls:
            result = execute_tool(tool_call.name, tool_call.arguments)
            
            # 7. Add tool result back to message history
            messages.append({"role": "user", "content": f"Tool result: {result}"})
    else:
        # 8. No tool calls = problem is solved
        final_answer = response.content
        break
```

### Key Concepts

**Message History**: The agent maintains a conversation history that grows with each iteration:
- User message: The original problem
- Assistant message: The agent's reasoning
- User message: Tool result (if tool was called)
- Assistant message: Next reasoning step
- ... (repeat until solved)

**Tool Definitions**: The agent is given tool definitions in OpenAI's function calling format. The model decides when to call tools based on the problem.

**Termination Condition**: The loop terminates when:
- The model doesn't request any tool calls (indicating it has the answer), OR
- The maximum iteration limit (10) is reached

**Reasoning Steps**: Each iteration produces a reasoning step that's recorded and displayed to the user.

### Why This Pattern Matters

This reasoning loop pattern is fundamental to building autonomous agents because it:
1. **Enables iterative problem-solving**: Complex problems can be broken into steps
2. **Allows tool usage**: The agent can invoke external functions when needed
3. **Maintains context**: The message history keeps all previous reasoning available
4. **Provides transparency**: Users can see the complete thought process
5. **Scales to complex tasks**: The same pattern works for more complex problems with more tools

## Testing

The lab includes comprehensive tests:

### Unit Tests
- Test multiplication tool correctness
- Test message formatting and parsing
- Test tool definition generation

### Property-Based Tests
- Verify multiplication tool works for all numeric inputs
- Verify reasoning loop terminates within 10 iterations
- Verify tool results are properly integrated
- Verify complete solutions preserve all reasoning steps

Run tests with:
```bash
pytest test_*.py -v
```

## Key Files to Understand

### 1. reasoning_agent.py - The Core Agentic Pattern
This is where the reasoning loop is implemented. Key points:

- **`run_reasoning_loop()`**: The main method that implements the agentic reasoning pattern
- **Message History**: Grows with each iteration (user → assistant → tool result → assistant → ...)
- **Tool Definitions**: Passed to the OpenAI API so the model knows what tools are available
- **Termination Logic**: The loop exits when the model doesn't request tool calls
- **Inline Comments**: Detailed comments explain each step of the agentic flow

### 2. tools.py - Tool Registry and Execution
Shows how tools are defined and executed:

- **`multiply()`**: The actual tool implementation
- **`get_tool_definitions()`**: Returns tool definitions in OpenAI function calling format
- **`execute_tool()`**: Routes tool calls to the correct implementation

### 3. app.py - UI Integration
Demonstrates how to integrate the reasoning agent with Streamlit:

- **Session State**: Maintains message history across user interactions
- **`process_user_problem()`**: Orchestrates the agentic flow and displays results
- **Display Logic**: Shows reasoning steps, tool calls, and final answers

### 4. utils.py - Helper Functions
Provides utility functions for formatting and parsing:

- **`format_reasoning_step()`**: Formats steps for display
- **`parse_tool_calls()`**: Extracts tool calls from API responses
- **`format_final_answer()`**: Formats the final answer
- **`initialize_system_prompt()`**: Defines the agent's behavior

## The Agentic Reasoning Pattern Explained

This lab teaches a fundamental pattern for building autonomous agents. Here's what makes it "agentic":

### 1. **Iterative Problem-Solving**
The agent doesn't try to solve the entire problem in one step. Instead, it:
- Reasons about what needs to be done
- Decides if it needs to call a tool
- Executes the tool
- Reasons about the result
- Repeats until the problem is solved

### 2. **Tool Usage**
The agent has access to tools (like multiplication) and decides when to use them:
- The model sees tool definitions
- The model decides which tool to call
- The agent executes the tool
- The result is fed back to the model

### 3. **Context Maintenance**
The message history maintains context across iterations:
- Each iteration adds to the history
- The model can see all previous reasoning
- This allows for complex multi-step problems

### 4. **Transparency**
The agent shows its complete reasoning process:
- Users can see each step
- Users can see which tools were called
- Users can understand how the answer was derived

### 5. **Scalability**
This pattern scales to more complex problems:
- Add more tools (division, square root, etc.)
- The same loop handles them all
- The model learns when to use each tool

## Common Patterns in Agent Development

This lab demonstrates patterns you'll see in many agent systems:

1. **Function Calling**: Using the model's ability to request function calls
2. **Message History**: Maintaining context across iterations
3. **Tool Registry**: Defining available tools for the agent
4. **Termination Conditions**: Knowing when the agent is done
5. **Result Formatting**: Presenting results clearly to users

These patterns are used in:
- Autonomous research agents
- Code generation agents
- Data analysis agents
- Customer service agents
- And many more applications

## Usage Guide

### Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open in browser:** The app will open at `http://localhost:8501`

3. **Submit a problem:** Type a math problem in the chat input field

4. **View results:** The agent displays:
   - Each reasoning step
   - Tool calls and their results
   - The final answer
   - Solution metadata (iterations, tools used)

### Programmatic Usage

You can also use the ReasoningAgent directly in Python:

```python
from reasoning_agent.reasoning_agent import ReasoningAgent

# Initialize the agent
agent = ReasoningAgent()

# Solve a problem
solution = agent.run_reasoning_loop("What is 15 times 23?")

# Access the results
print(f"Problem: {solution['problem']}")
print(f"Final Answer: {solution['final_answer']}")
print(f"Steps: {len(solution['steps'])}")
print(f"Tools Used: {solution['tools_used']}")

# Examine individual steps
for step in solution['steps']:
    print(f"Step {step['step_number']}: {step['reasoning']}")
    if step['tool_called']:
        print(f"  Tool: {step['tool_name']}")
        print(f"  Result: {step['tool_result']}")
```

### Customizing the Agent

**Change the model:**
```python
agent = ReasoningAgent(model="gpt-4")  # Use GPT-4 instead of gpt-4o-mini
```

**Modify the system prompt:**
Edit the `_initialize_system_prompt()` method in `reasoning_agent.py` to change how the agent behaves.

**Add new tools:**
1. Add the tool function to `tools.py`
2. Add the tool definition to `get_tool_definitions()`
3. Add the tool execution case to `execute_tool()`

## Further Learning

- Explore how changing the system prompt affects reasoning
- Try adding new tools (e.g., addition, division, square root)
- Experiment with different math problem types
- Modify the reasoning loop termination condition
- Study how the message history grows with each iteration
- Experiment with different temperature values (0.0 = deterministic, 1.0 = creative)

## Extending the Agent

### Adding a New Tool

To add a new tool (e.g., division), follow these steps:

**1. Add the tool implementation to `tools.py`:**
```python
def divide(a: float, b: float) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**2. Add the tool definition to `get_tool_definitions()`:**
```python
{
    "type": "function",
    "function": {
        "name": "divide",
        "description": "Divide one number by another",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "Numerator"},
                "b": {"type": "number", "description": "Denominator"}
            },
            "required": ["a", "b"]
        }
    }
}
```

**3. Add the execution case to `execute_tool()`:**
```python
elif tool_name == "divide":
    a = tool_input.get("a")
    b = tool_input.get("b")
    if a is None or b is None:
        raise ValueError("divide requires 'a' and 'b' parameters")
    result = divide(a, b)
    return str(result)
```

**4. Test it:**
```bash
streamlit run app.py
# Try: "What is 100 divided by 5?"
```

### Modifying the System Prompt

The system prompt controls how the agent behaves. Edit `_initialize_system_prompt()` in `reasoning_agent.py`:

```python
def _initialize_system_prompt(self) -> str:
    return """You are a helpful math tutor that solves mathematical problems step-by-step.
    
Your approach:
1. Break down the problem into logical steps
2. Use available tools when needed
3. Show your reasoning clearly at each step
4. Provide a clear final answer

Additional instructions:
- Be concise but thorough
- Explain why you're using each tool
- Double-check your work before providing the final answer"""
```

### Changing the Model

Use a different OpenAI model:

```python
# In app.py or when initializing the agent
agent = ReasoningAgent(model="gpt-4")  # Use GPT-4 for better reasoning
```

Available models:
- `gpt-4o-mini` (default, fast and cost-effective)
- `gpt-4o` (more capable)
- `gpt-4` (most capable, slower)

## Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure you've created `.env` file from `.env.sample`
- Verify your API key is correctly set in `.env`
- Check that the `.env` file is in the `Lab-5/` directory

### "Module not found" errors
- Ensure you've activated the virtual environment: `source .venv/bin/activate`
- Run `pip install -r requirements.txt`
- Verify you're running from the `Lab-5/` directory

### Reasoning loop doesn't terminate
- Check that the model is properly detecting when problems are solved
- Review the termination condition in `reasoning_agent.py`
- Try a simpler problem first (e.g., "What is 2 times 3?")

### Agent gives wrong answers
- Try a different model (e.g., `gpt-4` instead of `gpt-4o-mini`)
- Modify the system prompt to be more explicit about the task
- Check that tools are returning correct results

### Streamlit app won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that port 8501 is not in use
- Try: `streamlit run app.py --logger.level=debug` for more information

## References

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI Python Client](https://github.com/openai/openai-python)

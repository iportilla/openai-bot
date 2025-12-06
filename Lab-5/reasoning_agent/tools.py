"""
Tool registry and implementations for the Reasoning Math Agent.

This module demonstrates the tool calling pattern used in agentic systems:

1. Tool Implementations: Actual functions that perform work (multiply)
2. Tool Definitions: Metadata in OpenAI format that tells the model about tools
3. Tool Execution: Router that calls the correct implementation

The key insight: The model doesn't directly call Python functions. Instead:
- The model sees tool definitions and decides which tool to call
- The model returns a tool call request
- The agent executes the tool and returns the result
- The result is fed back to the model for further reasoning

This separation allows the model to reason about what needs to be done
without directly executing code.
"""


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    
    This is a simple tool implementation. In a real system, tools could be:
    - API calls (weather, stock prices, etc.)
    - Database queries
    - Complex computations
    - External services
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product of a and b
    """
    return a * b


def get_tool_definitions() -> list:
    """
    Get tool definitions in OpenAI function calling format.
    
    These definitions tell the OpenAI model:
    - What tools are available
    - What each tool does
    - What parameters each tool accepts
    
    The model uses this information to decide when and how to call tools.
    
    Format: OpenAI Function Calling specification
    - type: "function" (required)
    - function.name: Tool name (must match execute_tool routing)
    - function.description: What the tool does (helps model decide when to use it)
    - function.parameters: JSON schema describing input parameters
    
    Returns:
        List of tool definitions compatible with OpenAI API
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "multiply",  # Must match the name in execute_tool()
                "description": "Multiply two numbers together",  # Helps model decide when to use
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "First number to multiply"
                        },
                        "b": {
                            "type": "number",
                            "description": "Second number to multiply"
                        }
                    },
                    "required": ["a", "b"]  # Both parameters are required
                }
            }
        }
    ]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """
    Execute a tool by name with the given input.
    
    This is the router that connects tool calls from the model to actual
    implementations. When the model requests a tool call, this function:
    1. Receives the tool name and parameters
    2. Routes to the correct implementation
    3. Executes the tool
    4. Returns the result as a string
    
    The result is then fed back to the model for further reasoning.
    
    Args:
        tool_name: Name of the tool to execute (from model's tool call)
        tool_input: Dictionary of input parameters (from model's tool call)
    
    Returns:
        String representation of the tool result
    
    Raises:
        ValueError: If tool_name is not recognized
    """
    if tool_name == "multiply":
        # Extract parameters from the tool input
        a = tool_input.get("a")
        b = tool_input.get("b")
        
        # Validate that required parameters are present
        if a is None or b is None:
            raise ValueError("multiply requires 'a' and 'b' parameters")
        
        # Execute the tool
        result = multiply(a, b)
        
        # Return result as string (model will see this as text)
        return str(result)
    else:
        # Unknown tool - this shouldn't happen if tool definitions are correct
        raise ValueError(f"Unknown tool: {tool_name}")

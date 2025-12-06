"""
Property-based tests for the tool registry and implementations.

**Feature: reasoning-math-agent, Property 6: Multiplication Tool Correctness**
"""

from hypothesis import given, strategies as st
from reasoning_agent.tools import multiply, execute_tool


@given(a=st.floats(allow_nan=False, allow_infinity=False),
       b=st.floats(allow_nan=False, allow_infinity=False))
def test_multiply_correctness(a, b):
    """
    Property 6: Multiplication Tool Correctness
    
    *For any* two numeric inputs a and b, calling the multiplication tool 
    should return a result equal to a × b.
    
    **Validates: Requirements 6.2**
    """
    result = multiply(a, b)
    expected = a * b
    assert result == expected, f"multiply({a}, {b}) returned {result}, expected {expected}"


@given(a=st.floats(allow_nan=False, allow_infinity=False),
       b=st.floats(allow_nan=False, allow_infinity=False))
def test_execute_tool_multiply(a, b):
    """
    Property 6: Multiplication Tool Correctness (via execute_tool)
    
    *For any* two numeric inputs a and b, executing the multiply tool 
    through execute_tool should return the correct result as a string.
    
    **Validates: Requirements 6.2**
    """
    result_str = execute_tool("multiply", {"a": a, "b": b})
    result = float(result_str)
    expected = a * b
    assert result == expected, f"execute_tool returned {result}, expected {expected}"

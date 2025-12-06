"""
Reasoning loop engine for the Reasoning Math Agent.

This module implements the core agentic reasoning pattern:
- Iterative problem solving with OpenAI API
- Tool calling and result integration
- Reasoning step tracking and output formatting
"""

import os
import json
from typing import Optional
from openai import OpenAI
from reasoning_agent.tools import get_tool_definitions, execute_tool


class ReasoningAgent:
    """
    An agent that solves math problems through iterative reasoning.
    
    The agent uses OpenAI's function calling to invoke tools (like multiplication)
    and maintains a reasoning loop until the problem is solved.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the ReasoningAgent.
        
        Args:
            api_key: OpenAI API key. If None, uses OPENAI_API_KEY environment variable
            model: OpenAI model to use for reasoning
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment or arguments")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.max_iterations = 10
    
    def run_reasoning_loop(self, problem: str, messages: Optional[list] = None) -> dict:
        """
        Run the reasoning loop to solve a math problem.
        
        This is the core agentic reasoning pattern. The loop:
        1. Calls OpenAI API with tool definitions
        2. Parses tool calls from responses
        3. Executes tools and collects results
        4. Adds results back to message history
        5. Determines when problem is solved (max 10 iterations)
        6. Returns structured output with all steps
        
        The key insight: By feeding tool results back into the message history,
        the model can reason about the results and decide if more steps are needed.
        This creates an iterative problem-solving loop.
        
        Args:
            problem: The math problem to solve
            messages: Optional initial message history. If None, starts fresh.
        
        Returns:
            Dictionary containing:
            - problem: The original problem
            - steps: List of reasoning steps
            - final_answer: The conclusive solution
            - total_iterations: Number of iterations performed
            - tools_used: List of tools that were invoked
        
        Requirements: 3.1, 3.2, 3.3, 3.4, 6.1, 6.3
        """
        # Initialize message history - this maintains context across iterations
        if messages is None:
            messages = []
        
        # Add system prompt - defines the agent's role and behavior
        system_prompt = self._initialize_system_prompt()
        
        # Add the user's problem to start the conversation
        messages.append({
            "role": "user",
            "content": problem
        })
        
        # Track reasoning steps and tool usage for output
        reasoning_steps = []
        tools_used = set()
        iteration = 0
        final_answer = None
        
        # AGENTIC REASONING LOOP: Iterate until problem is solved or max iterations reached
        # This loop is the core of the agent - it's where the reasoning happens
        while iteration < self.max_iterations:
            iteration += 1
            
            # STEP 1: Call OpenAI API with tool definitions
            # The model sees the problem and tool definitions, and decides what to do
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system_prompt}] + messages,
                tools=get_tool_definitions(),  # Provides available tools to the model
                temperature=0.7
            )
            
            # Extract the model's response
            assistant_message = response.choices[0].message
            
            # STEP 2: Add assistant's response to message history
            # This maintains context for the next iteration
            # Note: Only add tool_calls if they exist, to avoid validation errors
            assistant_msg = {
                "role": "assistant",
                "content": assistant_message.content or ""
            }
            
            # Add tool_calls with proper structure if they exist
            if assistant_message.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",  # Required by OpenAI API
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in assistant_message.tool_calls
                ]
            
            messages.append(assistant_msg)
            
            # Record this reasoning step for output
            step = {
                "step_number": iteration,
                "reasoning": assistant_message.content or "",
                "tool_called": False,
                "tool_name": None,
                "tool_input": None,
                "tool_result": None,
                "is_final": False
            }
            
            # STEP 3: Check if the model requested tool calls
            # Tool calls indicate the model needs to perform a calculation
            if assistant_message.tool_calls:
                # Process each tool call (usually just one for multiplication)
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_input = json.loads(tool_call.function.arguments)
                    
                    # STEP 4: Execute the tool and get the result
                    tool_result = execute_tool(tool_name, tool_input)
                    
                    # Track which tools were used (for output)
                    tools_used.add(tool_name)
                    
                    # Update step information with tool details
                    step["tool_called"] = True
                    step["tool_name"] = tool_name
                    step["tool_input"] = tool_input
                    step["tool_result"] = tool_result
                    
                    # STEP 5: Add tool result back to message history
                    # This is crucial - the model will see the result and reason about it
                    # OpenAI API requires a "tool" message with the tool_call_id
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_result)
                    })
            else:
                # No tool calls - the model has provided reasoning without needing tools
                # This is likely the final answer
                step["is_final"] = True
                final_answer = assistant_message.content
            
            # Record this step in our reasoning steps list
            reasoning_steps.append(step)
            
            # STEP 6: Check if problem is solved
            # The problem is solved when the model doesn't request any tool calls
            # and provides content (the answer)
            if not assistant_message.tool_calls and assistant_message.content:
                final_answer = assistant_message.content
                break  # Exit the loop - problem is solved
        
        # If we hit max iterations without a clear final answer, use the last response
        if final_answer is None and reasoning_steps:
            final_answer = reasoning_steps[-1]["reasoning"]
        
        return {
            "problem": problem,
            "steps": reasoning_steps,
            "final_answer": final_answer or "Unable to determine answer",
            "total_iterations": iteration,
            "tools_used": sorted(list(tools_used))
        }
    
    def _initialize_system_prompt(self) -> str:
        """
        Initialize the system prompt for the reasoning agent.
        
        Returns:
            System prompt string that guides the agent's behavior
        
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

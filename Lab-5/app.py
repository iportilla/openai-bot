"""
Streamlit web interface for the Reasoning Math Agent.

This module provides an interactive chat interface for solving math problems
using the reasoning agent. Users can submit problems and watch the agent
reason through them step-by-step.

Requirements: 4.1, 4.2, 4.3, 4.4
"""

import streamlit as st
from reasoning_agent.reasoning_agent import ReasoningAgent
from reasoning_agent.utils import format_final_answer


def initialize_session_state():
    """
    Initialize Streamlit session state for message history.
    
    Creates session state variables if they don't exist:
    - messages: List of chat messages with role and content
    - reasoning_agent: Instance of ReasoningAgent
    
    Requirements: 4.1
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "reasoning_agent" not in st.session_state:
        try:
            st.session_state.reasoning_agent = ReasoningAgent()
        except ValueError as e:
            st.error(f"Error initializing agent: {e}")
            st.session_state.reasoning_agent = None


def display_message_history():
    """
    Display the chat message history using Streamlit chat components.
    
    Iterates through session state messages and displays them using
    st.chat_message() for proper formatting and styling.
    
    Requirements: 4.2
    """
    for message in st.session_state.messages:
        role = message.get("role", "user")
        content = message.get("content", "")
        
        with st.chat_message(role):
            st.markdown(content)


def process_user_problem(problem: str):
    """
    Process a user-submitted math problem through the reasoning agent.
    
    This function orchestrates the agentic flow:
    1. Adds the user's problem to the chat history
    2. Calls the reasoning agent to solve the problem
    3. Displays the reasoning steps and final answer
    4. Stores the complete solution in session state
    
    The reasoning agent handles the iterative loop internally, and this
    function focuses on displaying the results to the user.
    
    Args:
        problem: The math problem string submitted by the user
    
    Requirements: 4.3, 4.4
    """
    if not st.session_state.reasoning_agent:
        st.error("Reasoning agent not initialized. Please check your API key.")
        return
    
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": problem
    })
    
    # Display user message in the chat interface
    with st.chat_message("user"):
        st.markdown(problem)
    
    # Process through reasoning agent and display results
    with st.chat_message("assistant"):
        # Create a container for reasoning steps
        steps_container = st.container()
        
        # AGENTIC FLOW: Call the reasoning agent
        # This runs the iterative reasoning loop internally
        solution = st.session_state.reasoning_agent.run_reasoning_loop(
            problem=problem,
            messages=[]
        )
        
        # Display the reasoning steps and results
        with steps_container:
            st.markdown("### Reasoning Steps")
            
            # Display each reasoning step
            for step in solution.get("steps", []):
                step_num = step.get("step_number", 0)
                reasoning = step.get("reasoning", "")
                tool_name = step.get("tool_name")
                tool_input = step.get("tool_input")
                tool_result = step.get("tool_result")
                
                # Display the reasoning for this step
                st.markdown(f"**Step {step_num}:** {reasoning}")
                
                # If a tool was called, display the tool information
                if tool_name:
                    st.markdown(f"  - Tool: `{tool_name}`")
                    if tool_input:
                        st.markdown(f"  - Input: {tool_input}")
                    if tool_result:
                        st.markdown(f"  - Result: `{tool_result}`")
            
            # Display final answer with clear visual separation
            final_answer = solution.get("final_answer", "Unable to determine answer")
            st.markdown("---")
            st.markdown(f"### Final Answer\n{final_answer}")
            
            # Display metadata about the solution
            total_iterations = solution.get("total_iterations", 0)
            tools_used = solution.get("tools_used", [])
            
            # Collapsible section for detailed solution information
            with st.expander("Solution Details"):
                st.markdown(f"**Total Iterations:** {total_iterations}")
                st.markdown(f"**Tools Used:** {', '.join(tools_used) if tools_used else 'None'}")
    
    # Add assistant response to history
    assistant_response = f"""### Reasoning Steps
{chr(10).join([f"**Step {step.get('step_number')}:** {step.get('reasoning', '')}" for step in solution.get('steps', [])])}

---

### Final Answer
{solution.get('final_answer', 'Unable to determine answer')}"""
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_response
    })


def main():
    """
    Main Streamlit application entry point.
    
    Sets up the page configuration, initializes session state,
    displays the chat interface, and handles user input.
    
    Requirements: 4.1, 4.2, 4.3, 4.4
    """
    # Configure page
    st.set_page_config(
        page_title="Reasoning Math Agent",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add title
    st.title("🧮 Reasoning Math Agent")
    st.markdown("""
    This agent solves math problems step-by-step, showing its reasoning process.
    Submit a math problem and watch the agent work through it!
    """)
    
    # Initialize session state
    initialize_session_state()
    
    # Display message history
    display_message_history()
    
    # Create columns for input and clear button
    col1, col2 = st.columns([4, 1])
    
    with col1:
        # User input field
        user_input = st.chat_input(
            placeholder="Enter a math problem (e.g., 'What is 15 times 23?')",
            key="user_input"
        )
    
    with col2:
        # Clear conversation button
        if st.button("Clear History", key="clear_button"):
            st.session_state.messages = []
            st.rerun()
    
    # Process user input
    if user_input:
        process_user_problem(user_input)


if __name__ == "__main__":
    main()

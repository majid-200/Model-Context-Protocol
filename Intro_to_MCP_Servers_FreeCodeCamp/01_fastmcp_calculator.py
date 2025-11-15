"""
FASTMCP CALCULATOR SERVER                            
                                                                              
This is an MCP (Model Context Protocol) server that provides calculator
functions to AI assistants like Claude. Think of it as a toolbox that
Claude can reach into to perform calculations accurately.
""" 

from fastmcp import FastMCP
# FastMCP is a Python framework that makes it easy to create MCP servers.
# MCP allows AI assistants to use external tools and access resources safely.

# SERVER INITIALIZATION

# Create an MCP server instance with a descriptive name
# This name helps identify the server when multiple MCP servers are running
mcp = FastMCP(name="Calculator")

"""
Visual representation of MCP Architecture:

    ┌─────────────────┐
    │  AI Assistant   │  (Claude, GPT, etc.)
    │    (Client)     │
    └────────┬────────┘
             │
             │ ← Requests tools/resources via MCP protocol
             │
    ┌────────▼────────┐
    │   MCP Server    │  ← This is what we're building!
    │  (Calculator)   │
    └────────┬────────┘
             │
             │ ← Executes Python functions
             │
    ┌────────▼────────┐
    │   Tool Layer    │
    │  (multiply,     │
    │   add, etc.)    │
    └─────────────────┘
"""

# TOOL DEFINITIONS


# The @mcp.tool() decorator registers a function as an MCP tool
# This makes it available for AI assistants to call

# TOOL 1: MULTIPLY (Basic decorator usage)

# The docstring is important! FastMCP uses it to describe the tool
# to the AI assistant, helping it understand when to use this function.

@mcp.tool()  # ← Decorator with default settings
def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    args: 
        a (float): The first number.
        b (float): The second number.

    returns: 
        float: The product of the two numbers.
    
    Example: multiply(3, 4) → 12
    """
    return a * b

# TOOL 2: ADD (Custom decorator with metadata)

# Notice: The function is named 'add_numbers' but the tool is called 'add'
# This shows you can separate internal implementation names from the
# exposed tool names.

@mcp.tool(
    name="add",  # ← Custom name (otherwise uses function name)
    description="Add two numbers.",  # ← Custom description
    tags={"math", "arithmetic"}  # ← Tags for categorization/filtering
)
def add_numbers(x: float, y: float) -> float:
    """Add two numbers.

    args: 
        x (float): The first number.
        y (float): The second number.

    returns: 
        float: The sum of the two numbers.
    
    Example: add_numbers(5, 3) → 8
    """
    return x + y

# TOOL 3: SUBTRACT (Standard operation)

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers.

    args: 
        a (float): The first number (minuend).
        b (float): The second number (subtrahend).

    returns: 
        float: The difference of the two numbers.
    
    Example: subtract(10, 3) → 7
    """
    return a - b

# TOOL 4: DIVIDE (With error handling)

# This function includes error handling to prevent division by zero,
# which would crash the program. Good MCP tools should handle errors
# gracefully and provide clear error messages.

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers.

    args: 
        a (float): The dividend (number being divided).
        b (float): The divisor (number to divide by).

    returns: 
        float: The quotient of the two numbers.
    
    raises:
        ValueError: If b is zero (division by zero is undefined).
    
    Example: divide(10, 2) → 5.0
    """
    # Check for division by zero before attempting division
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

# SERVER EXECUTION

"""
Communication Flow:

    User asks Claude: "What is 15 × 23?"
           │
           ▼
    Claude sees it needs calculation
           │
           ▼
    Claude calls MCP server's multiply tool
           │
           ▼
    Server executes: multiply(15, 23)
           │
           ▼
    Server returns: 345
           │
           ▼
    Claude responds: "15 × 23 = 345"
"""

if __name__ == "__main__":
    # mcp.run() starts the MCP server
    # By default, it uses STDIO (Standard Input/Output) for communication
    # This means the server reads requests from stdin and writes responses to stdout
    
    # STDIO is perfect for local development and integration with tools like
    # Claude Desktop, which can launch and communicate with the server automatically
    
    mcp.run()  # STDIO by default
    
    # Alternative: mcp.run(transport="sse") for Server-Sent Events over HTTP

# npx @modelcontextprotocol/inspector python fastmcp_calculator.py

"""
KEY CONCEPTS           

1. MCP SERVER: A program that exposes tools/resources to AI assistants                                                                           
2. @mcp.tool(): Decorator that registers a Python function as a tool 
that can be called by the AI                                                                                                            
3. DOCSTRINGS: Describe what each tool does - crucial for AI to
understand when and how to use the tool                     
4. TYPE HINTS: (a: float) tells both Python and the MCP protocol
what types of data the function expects                                                                                                   
5. ERROR HANDLING: Good tools handle errors gracefully (see divide)                         
6. STDIO TRANSPORT: The server communicates via standard input/output,
making it easy to integrate with other tools           


HOW TO USE THIS SERVER                             
                                                        
1. Install FastMCP: pip install fastmcp                                                            
2. Run the server: python fastmcp_calculator.py                            
3. Configure Claude Desktop to use this server (see FastMCP docs)          
4. Ask Claude to do calculations - it will use these tools automatically!  
"""
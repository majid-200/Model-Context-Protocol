"""
FASTMCP CALCULATOR V2 - HTTP TRANSPORT                      
                                                            
This is a HYBRID approach combining the best of both worlds:                
- Simple FastMCP tool definitions (like Version 1)                          
- HTTP transport for network access (like FastAPI version)                  
                                                            
KEY INSIGHT: Same simple code, different transport method!                  
"""

from fastmcp import FastMCP

# Only need FastMCP - no FastAPI, no uvicorn!
# FastMCP handles everything internally

# SERVER INITIALIZATION

mcp = FastMCP(name="Calculator")

# Same simple initialization as Version 1
# The magic happens later when we choose the transport!


# TOOL DEFINITIONS

"""
Notice: The tool definitions are IDENTICAL to Version 1!
This is the beauty of FastMCP - write once, deploy anywhere.

┌─────────────────────────────────────────────────────────────────┐
│  Same Code Works With:                                          │
│                                                                 │
│  mcp.run()                           ← STDIO transport          │
│  mcp.run(transport="http")           ← HTTP transport           │
│  mcp.run(transport="sse")            ← Server-Sent Events       │
│                                                                 │
│  Just change ONE line, everything else stays the same!          │
└─────────────────────────────────────────────────────────────────┘
"""

# TOOL 1: MULTIPLY

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers.

    args: a (float): The first number.
          b (float): The second number.

    returns: float: The product of the two numbers.
    """
    return a * b


# TOOL 2: ADD (with custom metadata)

@mcp.tool(
    name="add",
    description="Add two numbers.",
    tags={"math", "arithmetic"}
)
def add_numbers(x: float, y: float) -> float:
    """Add two numbers.

    args: x (float): The first number.
          y (float): The second number.

    returns: float: The sum of the two numbers.
    """
    return x + y


# TOOL 3: SUBTRACT

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract two numbers.

    args: a (float): The first number.
          b (float): The second number.

    returns: float: The difference of the two numbers.
    """
    return a - b


# TOOL 4: DIVIDE (with error handling)

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide two numbers.

    args: a (float): The first number.
          b (float): The second number.

    returns: float: The quotient of the two numbers.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b



# SERVER EXECUTION WITH HTTP TRANSPORT


"""
THE KEY DIFFERENCE: We're changing the transport method!

Version 1 (STDIO):
mcp.run()  # or mcp.run(transport="stdio")

Version 2 (HTTP) - THIS FILE:
mcp.run(transport="http", host="localhost", port=8003)

Same code, different delivery method!
"""

if __name__ == "__main__":
    mcp.run(
        transport="http",      # ← Use HTTP instead of STDIO
        host="localhost",      # ← Server address (localhost = this computer only)
        port=8003             # ← Port number to listen on
    )
    
    # What happens when you run this:
    # 1. FastMCP starts an HTTP server on port 8003
    # 2. Creates MCP endpoints automatically
    # 3. Your tools become available over HTTP
    # 4. Prints: "Server running at http://localhost:8003"


"""
THREE VERSION COMPARISON                                 
                                                                                
VERSION 1: FastMCP with STDIO (fastmcp_calculator.py)                       
────────────────────────────────────────────────────────────                
    Code:        from fastmcp import FastMCP                                  
                mcp = FastMCP("Calculator")                                  
                @mcp.tool()                                                  
                def multiply(a, b): return a * b                             
                mcp.run()                                                    
                                                                            
    Transport:   STDIO (stdin/stdout)                                         
    Access:      Local only                                                   
    Complexity:  Simple                                                    
    Use Case:    Personal tools, Claude Desktop                               
                                                                            
─────────────────────────────────────────────────────────────────────────   
                                                                            
VERSION 2: FastAPI + FastApiMCP (fastapi-mcp_calculator.py)                
────────────────────────────────────────────────────────────                
    Code:        from fastapi import FastAPI                                  
                from fastapi_mcp import FastApiMCP                           
                app = FastAPI()                                              
                @app.post("/multiply")                                       
                def multiply(a, b): return {"result": a * b}                 
                mcp = FastApiMCP(app)                                        
                uvicorn.run(app, port=8002)                                  
                                                                            
    Transport:   HTTP (via FastAPI + Uvicorn)                                 
    Access:      Network accessible                                           
    Complexity:  Complex                                               
    Use Case:    Full web API + MCP dual purpose                              
                                                                            
─────────────────────────────────────────────────────────────────────────   
                                                                            
VERSION 3: FastMCP with HTTP (THIS FILE - fastmcp_calculatorV2.py)         
────────────────────────────────────────────────────────────                
    Code:        from fastmcp import FastMCP                                  
                mcp = FastMCP("Calculator")                                  
                @mcp.tool()                                                  
                def multiply(a, b): return a * b                             
                mcp.run(transport="http", port=8003)                         
                                                                            
    Transport:   HTTP (built into FastMCP)                                    
    Access:      Network accessible                                           
    Complexity:  Moderate                                                
    Use Case:    Network MCP tools with simple code                           

                                                                         

WHEN TO USE WHICH VERSION?                             
                                                                                
   Use Version 1 (FastMCP + STDIO) when:                                       
   ✓ Building personal tools for your own use                                  
   ✓ Maximum simplicity is priority                                            
   ✓ No need for network access                                                
   ✓ Using Claude Desktop locally                                              
                                                                                
   Use Version 2 (FastAPI + MCP) when:                                         
   ✓ Need a REAL web API for non-AI clients                                    
   ✓ Want to use FastAPI's full ecosystem (auth, middleware, etc.)             
   ✓ Need REST API documentation (Swagger/OpenAPI)                             
   ✓ Building production web services                                          
                                                                                
   Use Version 3 (FastMCP + HTTP) when:  ← THIS FILE                           
   ✓ Need network access but not a full web API                                
   ✓ Want simple code with HTTP benefits                                       
   ✓ Multiple machines need to access your MCP tools                           
   ✓ Sweet spot between simplicity and capability                              
                                                                            


TRANSPORT OPTIONS EXPLAINED                                
                                                                                
   FastMCP supports multiple transport methods:                                
                                                                                
   1. STDIO (Standard Input/Output)                                            
      mcp.run()  OR  mcp.run(transport="stdio")                                
      • Uses pipes for communication                                           
      • Local process only                                                     
      • No network ports needed                                                
      • Most secure (no network exposure)                                      
                                                                                
   2. HTTP (HyperText Transfer Protocol)                                       
      mcp.run(transport="http", host="localhost", port=8003)                   
      • Uses HTTP requests                                                     
      • Network accessible                                                     
      • Requires available port                                                
      • Can be accessed from other machines                                    
                                                                                
   3. SSE (Server-Sent Events)                                                 
      mcp.run(transport="sse", host="localhost", port=8004)                    
      • Similar to HTTP but with real-time updates                             
      • Keeps connection open                                                  
      • Good for streaming responses                                           


VISUAL: TRANSPORT COMPARISON                          
                                                                                
   STDIO Transport (Version 1):                                                
                                                                                
     ┌─────────┐ stdin/stdout ┌──────────┐                                    
     │ Claude  │ <──────────> │  Server  │                                    
     └─────────┘   (pipes)    └──────────┘                                    
          ↑                                                                     
          └─ Same machine only, direct connection                              
                                                                                
   ─────────────────────────────────────────────────────────────────────────   
                                                                                
   HTTP Transport (Version 3 - THIS FILE):                                     
                                                                                
     ┌─────────┐              ┌──────────┐                                    
     │ Claude  │   HTTP GET   │  Server  │                                    
     │ Machine │ ───────────→ │  :8003   │                                    
     │   A     │   Request    │ Machine  │                                    
     └─────────┘              │    B     │                                    
                              └──────────┘                                    
          ↑                        ↑                                           
          └── Network ─────────────┘                                           
              Can be different machines!                                       
                                                                                

HOW TO USE THIS SERVER                              
                                                                               
   1. Install FastMCP:                                                         
      pip install fastmcp                                                      
                                                                                
   2. Run the server:                                                          
      python 03_fastmcp_calculatorV2.py                                           
                                                                                
   3. You'll see:                                                              
      Server running at http://localhost:8003                                  
                                                                                
   4. Configure Claude to connect:                                             
      • In Claude Desktop settings                                             
      • Add MCP server with URL: http://localhost:8003                         
                                                                                
   5. Test with MCP Inspector:                                                 
      npx @modelcontextprotocol/inspector http://localhost:8003                
                                                                                
   6. Or test with curl:                                                       
      curl http://localhost:8003/mcp/tools                                     
      (Shows available tools)                                                  


KEY ADVANTAGES OF THIS VERSION                        
                                                                                
   ✓ SIMPLE CODE: Same clean @mcp.tool() syntax as STDIO version              
                                                                                
   ✓ NETWORK ACCESS: Can be accessed from other machines on your network      
                                                                                
   ✓ NO FASTAPI NEEDED: Don't need to learn FastAPI framework                 
                                                                                
   ✓ NO UVICORN NEEDED: FastMCP handles the web server internally             
                                                                                
   ✓ FLEXIBLE: Easy to switch between STDIO and HTTP by changing one line     
                                                                                
   ✓ MCP-FOCUSED: Not a general web API, specifically designed for MCP        
                                                                                
   ✓ BEST OF BOTH: Simplicity of V1 + network access of V2                    
                                                                                



IMPORTANT NOTES                                    
                                                                                
   PORT NUMBERS:                                                               
   • Must be between 1024-65535 (below 1024 need admin rights)                 
   • Must be available (not used by another program)                           
   • 8003 in this example, but you can use any available port                  
                                                                                
   HOST OPTIONS:                                                               
   • "localhost" = This computer only (secure, local testing)                  
   • "0.0.0.0" = All network interfaces (accessible from network)              
   • Specific IP = Only that network interface                                 
                                                                                
   SECURITY:                                                                   
   • HTTP transport exposes your tools to the network                          
   • Use "localhost" for local testing                                         
   • Consider authentication for production use                                
   • Be careful what tools you expose                                          
"""
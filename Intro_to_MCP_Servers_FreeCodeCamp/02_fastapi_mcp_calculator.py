"""
FASTAPI MCP CALCULATOR SERVER                          
                                                                        
This is an MCP server that uses HTTP instead of STDIO for communication.   
It creates a web API first, then converts it into an MCP server.           
                                                                        
KEY DIFFERENCE: This runs as a web server, not a command-line tool.        

"""

from fastapi import FastAPI
from fastapi_mcp import FastApiMCP

# FastAPI: A modern Python web framework for building APIs
# FastApiMCP: A bridge that converts FastAPI endpoints into MCP tools

# STEP 1: CREATE A FASTAPI APPLICATION (Web API)

"""
First, we build a regular web API. This can be used by:
- Web browsers
- Mobile apps  
- Other programs
- AND it will be converted to MCP tools!
"""

app = FastAPI(title="Calculator API")

# FastAPI() creates a web application
# "title" is what appears in the automatically generated documentation

# API ENDPOINT 1: MULTIPLY

# How it works as a web API:
# - Client sends POST request to http://localhost:8002/multiply
# - Body contains: {"a": 5, "b": 3}
# - Server responds with: {"result": 15}

# How it works as MCP:
# - Claude calls the multiply tool
# - Provides parameters a=5, b=3
# - Receives result: 15

@app.post("/multiply")  # ← This creates a POST endpoint at /multiply
def multiply_numbers(a: float, b: float):
    """
    Multiplies two numbers and returns the result.
    """
    result = a * b
    return {"result": result}  # ← Returns a dictionary (becomes JSON)

# API ENDPOINT 2: ADD

# API URL: POST http://localhost:8002/add
# Request body: {"a": 10, "b": 7}
# Response: {"result": 17}

@app.post("/add")
def add_numbers(a: float, b: float):
    """
    Adds two numbers and returns the result.
    """
    result = a + b
    return {"result": result}

# API ENDPOINT 3: SUBTRACT

# API URL: POST http://localhost:8002/subtract
# Request body: {"a": 20, "b": 8}
# Response: {"result": 12}

@app.post("/subtract")
def subtract_numbers(a: float, b: float):
    """
    Subtracts two numbers and returns the result.
    """
    result = a - b
    return {"result": result}

# API ENDPOINT 4: DIVIDE (with error handling)

# Includes error handling for division by zero.
# Instead of raising an exception, returns an error message.

# Success case:
# Request: {"a": 10, "b": 2}
# Response: {"result": 5.0}

# Error case:
# Request: {"a": 10, "b": 0}
# Response: {"error": "Division by zero is not allowed."}

@app.post("/divide")
def divide_numbers(a: float, b: float):
    """
    Divides two numbers and returns the result.
    """
    if b == 0:
        # Return error as JSON instead of raising exception
        # This is more friendly for web APIs
        return {"error": "Division by zero is not allowed."}
    
    result = a / b
    return {"result": result}

# STEP 2: CONVERT FASTAPI TO MCP

"""
This is where the magic happens! FastApiMCP automatically converts
all your FastAPI endpoints into MCP tools.

Before conversion:          After conversion:
┌──────────────────┐       ┌──────────────────┐
│  Web API         │       │  Web API         │
│  /multiply       │  ───> │  /multiply       │
│  /add            │       │  /add            │
│  /subtract       │       │  /subtract       │
│  /divide         │       │  /divide         │
└──────────────────┘       └────────┬─────────┘
                                    │
                           ┌────────▼─────────┐
                           │  MCP Tools       │
                           │  multiply_numbers│
                           │  add_numbers     │
                           │  subtract_numbers│
                           │  divide_numbers  │
                           └──────────────────┘
"""

# Create MCP server from FastAPI app
mcp = FastApiMCP(app, name="Calculator MCP")

# FastApiMCP takes your FastAPI app and wraps it with MCP capabilities
# Now it can be used BOTH as a web API AND as MCP tools!

# Mount the HTTP endpoints for MCP communication
mcp.mount_http()

# mount_http() adds special MCP endpoints to your FastAPI app:
# - SSE (Server-Sent Events) endpoint for real-time communication
# - These endpoints allow Claude to discover and use your tools

# SERVER STARTUP

"""
Communication Architecture:

STDIO Version (previous file):
┌──────────┐  stdin/stdout  ┌───────────┐
│  Claude  │ <────────────> │  Server   │
└──────────┘                └───────────┘
(Direct pipe communication)


HTTP Version (this file):
┌──────────┐                ┌───────────┐
│  Claude  │                │  Server   │
│          │   HTTP over    │ (running  │
│          │ <─ network ──> │  on port  │
│          │   requests     │   8002)   │
└──────────┘                └───────────┘
(Network communication via URLs)
"""

if __name__ == "__main__":
    # Import uvicorn - a lightning-fast web server for Python
    import uvicorn
    
    # Start the server
    uvicorn.run(
        app,                    # ← The FastAPI application to run
        host="localhost",       # ← Server address (localhost = your computer only)
        port=8002              # ← Port number (like an apartment number for services)
    )
    
    # Once running, you can:
    # 1. Visit http://localhost:8002/docs to see interactive API documentation
    # 2. Test endpoints manually in your browser
    # 3. Connect Claude to this server via MCP
    # 4. Use it as a regular web API from other programs

    # npx @modelcontextprotocol/inspector http://localhost:8002/mcp

    
"""
STDIO VS HTTP COMPARISON                                   
                                                        
STDIO Version (fastmcp_calculator.py):                                      
✓ Simpler to set up                                                         
✓ No port conflicts                                                         
✓ More secure (no network exposure)                                         
✓ Better for local-only tools                                               
✗ Can't be accessed remotely                                                
✗ Can't be used as a web API                                                
                                                        
HTTP Version (this file):                                                   
✓ Can be accessed over network                                              
✓ Works as both MCP AND regular web API                                     
✓ Better for services that multiple apps need                               
✓ Can scale to handle many requests                                         
✗ More complex setup                                                        
✗ Need to manage ports                                                      
✗ Network security considerations                                           
                                                                               
  
HOW TO USE THIS SERVER                                
                                                    
1. Install dependencies:                                                    
pip install fastapi fastapi-mcp uvicorn                                  
                                                    
2. Run the server:                                                          
python fastapi-mcp_calculator.py                                         
                                                    
3. Test in browser:                                                         
Visit http://localhost:8002/docs                                         
(FastAPI auto-generates interactive documentation!)                      
                                                    
4. Use with Claude:                                                         
Configure Claude Desktop to connect to http://localhost:8002             
                                                    
5. Or use as regular API:                                                   
POST http://localhost:8002/multiply with {"a": 5, "b": 3}               
                                                                               

KEY CONCEPTS                                       
                                              
1. FASTAPI: Web framework for building APIs quickly                         
                                                    
2. @app.post(): Decorator that creates a POST endpoint (URL)                
                                                    
3. UVICORN: Fast web server that runs your FastAPI application              
                                                    
4. PORT 8002: The "address" where your server listens for requests          
                                                    
5. localhost: Means "this computer only" - not visible to internet          
                                                    
6. FastApiMCP: Automatically converts API endpoints to MCP tools            
                                                    
7. SSE (Server-Sent Events): How MCP communicates over HTTP                 
                                                    
8. DUAL PURPOSE: This server works as BOTH a web API AND MCP server!       
                                                                               

TESTING EXAMPLES                                     
                                                                               
Using curl (command line):                                                  
curl -X POST "http://localhost:8002/multiply" \                             
    -H "Content-Type: application/json" \                                  
    -d '{"a": 5, "b": 3}'                                                  
Response: {"result": 15}                                                    
                                                                               
Using Python requests:                                                      
import requests                                                             
response = requests.post(                                                   
    "http://localhost:8002/add",                                            
    json={"a": 10, "b": 7}                                                  
)                                                                            
print(response.json())  # {"result": 17}                                    
                                                                               
Using Claude (via MCP):                                                     
User: "What is 25 times 4?"                                                 
Claude calls multiply_numbers tool with a=25, b=4                           
Claude responds: "25 times 4 equals 100"                                    
"""
"""
FREECODECAMP FEED SEARCHER MCP                             
                                                        
This MCP server searches FreeCodeCamp's content via RSS feeds.              
It demonstrates how to fetch and search external data sources.              
                                                        
USE CASE: Ask Claude to find FreeCodeCamp articles or videos on topics     
you're learning about!                                            
"""

from fastmcp import FastMCP
import feedparser

# FastMCP: Framework for creating MCP servers (we've seen this before!)
# feedparser: Library for reading RSS/Atom feeds (news feeds, podcasts, etc.)

"""
What is RSS?

RSS (Really Simple Syndication) is a web feed format that websites use to
publish frequently updated content (like news, blog posts, videos).

Think of it like subscribing to a newsletter, but in a standard format
that programs can read!

Example RSS feed structure:
┌────────────────────────────────────────┐
│  <rss>                                 │
│    <channel>                           │
│      <title>FreeCodeCamp News</title>  │
│      <item>                            │
│        <title>Learn Python</title>     │
│        <link>https://...</link>        │
│        <description>...</description>  │
│      </item>                           │
│      <item>                            │
│        <title>React Tutorial</title>   │
│        ...                             │
│      </item>                           │
│    </channel>                          │
│  </rss>                                │
└────────────────────────────────────────┘
"""


# SERVER INITIALIZATION

mcp = FastMCP(name="FreeCodeCamp Feed Searcher")

# Creates an MCP server that Claude can use to search FreeCodeCamp content


# TOOL 1: SEARCH FREECODECAMP NEWS ARTICLES

@mcp.tool()
def fcc_news_search(query: str, max_results: int = 3):
    """Search FreeCodeCamp news feed via RSS by title/description
    
    This tool searches through FreeCodeCamp's blog articles and returns
    matching results based on your search query.
    
    Args:
        query (str): The search term (e.g., "python", "react", "algorithms")
        max_results (int): Maximum number of results to return (default: 3)
    
    Returns:
        list: List of dictionaries containing matching articles
              Format: [{"title": "...", "url": "..."}, ...]
              Or: [{"message": "No results found"}] if nothing matches
    
    Example usage by Claude:
        User: "Find FreeCodeCamp articles about Python"
        Claude calls: fcc_news_search("python", max_results=3)
        Returns: [
            {"title": "Learn Python in 2025", "url": "https://..."},
            {"title": "Python Projects for Beginners", "url": "https://..."}
        ]
    """
    
    # STEP 1: Fetch the RSS feed
    
    # feedparser.parse() downloads and parses the RSS feed from the URL
    # This is like visiting a webpage, but for structured data
    feed = feedparser.parse("https://www.freecodecamp.org/news/rss/")
    
    """
    What feedparser returns:
    
    feed = {
        'entries': [                    ← List of all articles
            {
                'title': 'Article 1',
                'description': '...',
                'link': 'https://...',
                'published': '...'
            },
            {
                'title': 'Article 2',
                ...
            }
        ],
        'feed': {...}                   ← Metadata about the feed
    }
    """
    
    # STEP 2: Initialize results list and normalize query
    
    results = []  # Will store matching articles
    
    # Convert query to lowercase for case-insensitive searching
    # "Python" == "python" == "PYTHON" when searching
    query_lower = query.lower()
    
    # STEP 3: Search through all articles
    
    for entry in feed.entries:  # Loop through each article
        
        # Extract title and description from the entry
        # .get() is safe - returns "" if key doesn't exist (no crash!)
        title = entry.get("title", "")
        description = entry.get("description", "")
        
        # STEP 4: Check if query matches title OR description
        
        # Search in both title and description (case-insensitive)
        if query_lower in title.lower() or query_lower in description.lower():
            
            # Found a match! Add to results
            results.append({
                "title": title,
                "url": entry.get("link", "")  # The article URL
            })
        
        # STEP 5: Stop if we have enough results
        
        if len(results) >= max_results:
            break  # Stop searching once we have max_results items
    
    # STEP 6: Return results (or error message if nothing found)
    
    # Python trick: "results or [...]" means:
    # - If results is not empty, return results
    # - If results is empty [], return the default message
    return results or [{"message": "No results found"}]


# TOOL 2: SEARCH FREECODECAMP YOUTUBE VIDEOS

@mcp.tool()
def fcc_youtube_search(query: str, max_results: int = 3):
    """Search FreeCodeCamp Youtube channel via RSS by title
    
    This searches FreeCodeCamp's YouTube channel for video tutorials.
    Note: YouTube RSS feeds only include titles, not descriptions.
    
    Args:
        query (str): Search term (e.g., "javascript", "data structures")
        max_results (int): Maximum videos to return (default: 3)
    
    Returns:
        list: List of matching YouTube videos
              Format: [{"title": "...", "url": "..."}, ...]
    
    Example:
        User: "Find FreeCodeCamp videos about JavaScript"
        Claude calls: fcc_youtube_search("javascript", max_results=3)
    """
    
    # STEP 1: Fetch YouTube RSS feed
    
    # YouTube provides RSS feeds for channels using this URL pattern:
    # https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID
    # 
    # FreeCodeCamp's channel ID: UC8butISFwT-Wl7EV0hUK0BQ
    feed = feedparser.parse(
        "https://www.youtube.com/feeds/videos.xml?channel_id=UC8butISFwT-Wl7EV0hUK0BQ"
    )
    
    """
    YouTube RSS Feed Structure:
    ┌──────────────────────────────────────────────────┐
    │ <feed>                                           │
    │   <entry>                                        │
    │     <title>Full Python Course - 12 Hours</title>│
    │     <link>https://youtube.com/watch?v=...</link>│
    │     <published>2024-01-15T10:00:00Z</published> │
    │   </entry>                                       │
    │   <entry>                                        │
    │     <title>React Tutorial</title>                │
    │     ...                                          │
    │   </entry>                                       │
    │ </feed>                                          │
    └──────────────────────────────────────────────────┘
    """
    
    # STEP 2: Initialize search
    
    results = []
    query_lower = query.lower()
    
    # STEP 3: Search through video titles
    
    for entry in feed.entries:
        title = entry.get("title", "")
        
        # Only search in title (YouTube RSS doesn't include descriptions)
        if query_lower in title.lower():
            results.append({
                "title": title,
                "url": entry.get("link", "")  # YouTube video URL
            })
        
        if len(results) >= max_results:
            break  # Stop when we have enough results
    
    # Return results or "not found" message
    return results or [{"message": "No videos found"}]


# TOOL 3: SECRET MESSAGE (Easter Egg)

@mcp.tool()
def fcc_secret_message():
    """Returns a secret message of FreeCodeCamp
    
    This is a simple tool that returns a motivational message.
    It demonstrates that MCP tools don't always need to fetch external data -
    they can also provide static information or perform simple tasks!
    
    Returns:
        str: A motivational message
    
    Example:
        User: "What's the FreeCodeCamp secret message?"
        Claude calls: fcc_secret_message()
        Returns: "Keep exploring! and happy coding!"
    """
    return "Keep exploring! and happy coding!"
    
    # This could be expanded to:
    # - Return random motivational quotes
    # - Track user progress
    # - Provide learning tips
    # - etc.


# SERVER EXECUTION

"""
How This Works in Practice:

┌─────────────────────────────────────────────────────────────────┐
│ USER: "Find me FreeCodeCamp articles about machine learning"    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE: Recognizes this needs the fcc_news_search tool          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ MCP SERVER: Calls fcc_news_search("machine learning", 3)        │
│   1. Downloads RSS feed from FreeCodeCamp                       │
│   2. Searches through all articles                              │
│   3. Finds matches containing "machine learning"                │
│   4. Returns top 3 results                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ CLAUDE: Formats the results nicely for the user:                │
│   "I found 3 FreeCodeCamp articles about machine learning:      │
│   1. Introduction to Machine Learning - [link]                  │
│   2. Neural Networks Explained - [link]                         │
│   3. ML with Python Tutorial - [link]"                          │
└─────────────────────────────────────────────────────────────────┘
"""

if __name__ == "__main__":
    # Run the MCP server using STDIO (standard input/output)
    # This means it communicates via stdin/stdout, perfect for
    # local integration with Claude Desktop
    mcp.run()  # STDIO by default
    
    # No uvicorn needed! This uses STDIO, not HTTP


"""
KEY CONCEPTS                                     
                                                                                
1. RSS FEEDS: Standardized format for publishing updated content            
                (news, blogs, podcasts, videos)                                
                                                                            
2. FEEDPARSER: Python library that downloads and parses RSS/Atom feeds      
                Handles all the XML parsing complexity for you               
                                                                            
3. .get() METHOD: Safe way to access dictionary keys                        
                    Returns default value if key doesn't exist                
                    entry.get("title", "") means "get title, or '' if none"   
                                                                            
4. CASE-INSENSITIVE SEARCH: query.lower() ensures "Python" matches          
                            "python", "PYTHON", "PyThOn", etc.             
                                                                            
5. BREAK STATEMENT: Exits the loop early when condition is met              
                    Used here to stop after finding max_results             
                                                                            
6. OR OPERATOR: "results or [...]" returns results if not empty,            
                otherwise returns the default value                         
                                                                            
7. EXTERNAL DATA: This MCP server fetches live data from the internet       
                    Unlike the calculator which just did math                 
                                                                                

HOW TO USE THIS SERVER                              
                                                                                
1. Install dependencies:                                                    
    pip install fastmcp feedparser                                           
                                                                            
2. Run the server:                                                          
    python feed_mcp.py                                                       
                                                                            
3. Configure Claude Desktop to use this MCP server                          
                                                                            
4. Ask Claude questions like:                                               
    • "Find FreeCodeCamp articles about Python"                              
    • "Search FreeCodeCamp videos on React"                                  
    • "What's the FreeCodeCamp secret message?"                              
                                                                            
5. Test with MCP Inspector:                                                 
    npx @modelcontextprotocol/inspector python feed_mcp.py                   
                                                                            

COMPARISON WITH CALCULATOR                            
                                                                                
   Calculator MCP:                                                             
   • Pure computation (no external data)                                       
   • Always same result for same input                                         
   • Works offline                                                             
   • Fast (milliseconds)                                                       
                                                                                
   Feed Searcher MCP:                                                          
   • Fetches external data (from internet)                                     
   • Results change as FreeCodeCamp publishes new content                      
   • Requires internet connection                                              
   • Slower (network requests take time)                                       
                                                                                
   Both are valuable! Different tools for different jobs.                      
"""
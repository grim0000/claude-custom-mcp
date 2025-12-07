#!/usr/bin/env python3
"""
Obsidian MCP Server - Tools for interacting with Obsidian via Local REST API
"""

import sys
import logging
from mcp.server.fastmcp import FastMCP

# Import tools from modules
from tools.files import (
    list_files, 
    get_file_content, 
    create_or_update_file, 
    append_to_file, 
    delete_file, 
    get_active_file, 
    get_daily_note
)
from tools.search import (
    search_notes,
    get_backlinks,
    list_tags
)
from tools.commands import (
    list_commands,
    execute_command
)
from tools.markdown import (
    append_to_heading,
    get_frontmatter,
    update_frontmatter
)
from utils import API_KEY

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("obsidian-server")

# Initialize MCP server
mcp = FastMCP("obsidian-mcp")

# Register tools
mcp.tool()(list_files)
mcp.tool()(get_file_content)
mcp.tool()(create_or_update_file)
mcp.tool()(append_to_file)
mcp.tool()(delete_file)
mcp.tool()(search_notes)
mcp.tool()(get_active_file)
mcp.tool()(get_daily_note)
mcp.tool()(list_commands)
mcp.tool()(execute_command)

# Register new tools
mcp.tool()(get_backlinks)
mcp.tool()(list_tags)
mcp.tool()(append_to_heading)
mcp.tool()(get_frontmatter)
mcp.tool()(update_frontmatter)

if __name__ == "__main__":
    logger.info("Starting Obsidian MCP server...")
    if not API_KEY:
        logger.error("WARNING: OBSIDIAN_API_KEY is not set. Please check your .env file.")
        
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

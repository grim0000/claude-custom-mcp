#!/usr/bin/env python3
"""
System MCP Server - Tools for general system operations
"""

import sys
import logging
from mcp.server.fastmcp import FastMCP

# Import tools
from tools.resources import (
    get_system_stats,
    list_processes
)
from tools.desktop import (
    take_screenshot
)
from tools.forensics import (
    calculate_file_hash,
    list_open_ports,
    kill_process,
    get_recent_files,
    read_registry_key
)
from tools.automation import (
    move_mouse,
    click_mouse,
    type_text,
    press_key,
    get_screen_size,
    drag_mouse,
    scroll
)
from tools.steganography import (
    hide_text_in_image,
    reveal_text_from_image,
    get_exif_data,
    remove_exif_data
)
from tools.voice import (
    speak
)
from tools.accessibility import (
    get_ui_tree,
    click_element_by_name,
    get_cursor_position
)
from tools.vision import (
    locate_image_on_screen,
    wait_for_image
)
from tools.file_forensics import (
    analyze_file_signature,
    extract_strings
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("system-server")

# Initialize MCP server
mcp = FastMCP("system-mcp")

# Register tools
mcp.tool()(get_system_stats)
mcp.tool()(list_processes)
mcp.tool()(take_screenshot)
mcp.tool()(calculate_file_hash)
mcp.tool()(list_open_ports)
mcp.tool()(kill_process)
mcp.tool()(get_recent_files)
mcp.tool()(read_registry_key)
mcp.tool()(move_mouse)
mcp.tool()(click_mouse)
mcp.tool()(type_text)
mcp.tool()(press_key)
mcp.tool()(get_screen_size)
mcp.tool()(drag_mouse)
mcp.tool()(scroll)
mcp.tool()(hide_text_in_image)
mcp.tool()(reveal_text_from_image)
mcp.tool()(get_exif_data)
mcp.tool()(remove_exif_data)
mcp.tool()(speak)
mcp.tool()(get_ui_tree)
mcp.tool()(click_element_by_name)
mcp.tool()(get_cursor_position)
mcp.tool()(locate_image_on_screen)
mcp.tool()(wait_for_image)
mcp.tool()(analyze_file_signature)
mcp.tool()(extract_strings)

if __name__ == "__main__":
    logger.info("Starting System MCP server...")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

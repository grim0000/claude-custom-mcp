#!/usr/bin/env python3
"""
WiFi Nmap Tshark MCP Server - Tools for network scanning and packet capture
"""

import sys
import logging
from mcp.server.fastmcp import FastMCP

# Import tools from modules
from tools.wifi import (
    detect_os,
    scan_wifi,
    connect_wifi,
    get_interfaces
)
from tools.scanning import (
    run_nmap,
    ping_host,
    scan_local_network
)
from tools.packet import (
    run_tshark
)
from tools.dns import (
    lookup_dns,
    whois,
    get_public_ip
)
from tools.web_recon import (
    analyze_ssl_cert,
    check_security_headers
)
from tools.extra_utils import (
    encode_decode,
    generate_reverse_shell
)
from tools.net_audit import (
    grab_banner,
    enumerate_subdomains
)
from tools.reporting import (
    generate_security_report
)

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("wifi-nmap-server")

# Initialize MCP server
mcp = FastMCP("wifi-nmap")

# Register tools
mcp.tool()(detect_os)
mcp.tool()(scan_wifi)
mcp.tool()(connect_wifi)
mcp.tool()(get_interfaces)
mcp.tool()(run_nmap)
mcp.tool()(run_tshark)

# Register new tools
mcp.tool()(ping_host)
mcp.tool()(scan_local_network)
mcp.tool()(lookup_dns)
mcp.tool()(whois)
mcp.tool()(get_public_ip)
mcp.tool()(analyze_ssl_cert)
mcp.tool()(check_security_headers)
mcp.tool()(encode_decode)
mcp.tool()(generate_reverse_shell)
mcp.tool()(grab_banner)
mcp.tool()(enumerate_subdomains)
mcp.tool()(generate_security_report)

if __name__ == "__main__":
    logger.info("Starting WiFi/Nmap/Tshark MCP server...")
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

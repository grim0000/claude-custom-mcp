import logging
from utils import run_command, get_os_type

logger = logging.getLogger("scanning-tools")

async def run_nmap(target: str = "", args: str = "") -> str:
    """Runs an Nmap scan on a target. Args example: '-F' or '-sV'."""
    if not target:
        return "Error: Target is required (e.g., '192.168.1.1' or 'google.com')"
    
    logger.info(f"Running nmap on {target} with args: {args}")
    
    cmd = ["nmap", target]
    if args:
        cmd.extend(args.split())
        
    return run_command(cmd, timeout=300)

async def ping_host(host: str) -> str:
    """Pings a host to check reachability."""
    os_name = get_os_type()
    count_flag = "-n" if os_name == "Windows" else "-c"
    cmd = ["ping", count_flag, "4", host]
    return run_command(cmd)

async def scan_local_network() -> str:
    """Scans the local network for devices using ARP (requires arp-scan or similar) or ping sweep."""
    # Simple ping sweep using nmap is best if available
    # nmap -sn 192.168.1.0/24
    
    # We need to guess the subnet.
    # For now, let's try to use 'arp -a' which is built-in and fast.
    cmd = ["arp", "-a"]
    return run_command(cmd)

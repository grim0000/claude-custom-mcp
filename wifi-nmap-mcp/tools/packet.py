import logging
from utils import run_command

logger = logging.getLogger("packet-tools")

async def run_tshark(interface: str = "", duration: str = "10", filter: str = "") -> str:
    """Runs Tshark packet capture. Duration in seconds. Filter is BPF (e.g. 'tcp port 80')."""
    logger.info(f"Running tshark on {interface} for {duration}s")
    
    # Path might need to be configurable
    cmd = [r"C:\Program Files\Wireshark\tshark.exe", "-a", f"duration:{duration}"]
    
    if interface:
        cmd.extend(["-i", interface])
        
    if filter:
        cmd.append(filter) 
        
    return run_command(cmd, timeout=int(duration) + 5)

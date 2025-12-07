import platform
import subprocess
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("wifi-nmap-utils")

def get_os_type() -> str:
    """Detects the operating system."""
    return platform.system()

def run_command(command: list[str], timeout: int = 30) -> str:
    """Runs a system command and returns output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False
        )
        if result.returncode != 0:
            return f"Command failed with code {result.returncode}:\n{result.stderr}"
        return result.stdout
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"

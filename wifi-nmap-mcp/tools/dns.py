import socket
import logging
from utils import run_command

logger = logging.getLogger("dns-tools")

async def lookup_dns(domain: str) -> str:
    """Performs a DNS lookup for a domain."""
    try:
        ip = socket.gethostbyname(domain)
        # We could also do gethostbyname_ex to get aliases
        return f"Domain: {domain}\nIP: {ip}"
    except Exception as e:
        return f"DNS lookup failed: {e}"

async def whois(domain: str) -> str:
    """Retrieves WHOIS information for a domain using python-whois library."""
    try:
        import whois
        w = whois.whois(domain)
        return str(w)
    except ImportError:
        return "Error: python-whois library not installed."
    except Exception as e:
        return f"Error retrieving WHOIS info: {e}"

async def get_public_ip() -> str:
    """Gets the public IP address."""
    # We need to reach out to an external service.
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.ipify.org")
            return f"Public IP: {response.text}"
    except Exception as e:
        return f"Failed to get public IP: {e}"

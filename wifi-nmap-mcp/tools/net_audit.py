import socket
import logging
import asyncio

logger = logging.getLogger("net-audit-tools")

async def grab_banner(ip: str, port: int) -> str:
    """
    Connects to a port and returns the service banner (first response).
    Useful for identifying running services.
    """
    try:
        # Use simple socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((ip, port))
        
        # Send a generic payload just in case (e.g. HTTP needs a GET)
        # But for strictly banner grabbing, usually we just wait for the hello.
        # However, purely waiting might hang if server expects input.
        # Let's try to receive first.
        try:
            banner = s.recv(1024).decode().strip()
            s.close()
            return f"Banner for {ip}:{port} -> {banner}"
        except socket.timeout:
            # Maybe send something?
            s.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = s.recv(1024).decode().strip()
            s.close()
            return f"Banner for {ip}:{port} (after probe) -> {banner}"
            
    except Exception as e:
        return f"Failed to grab banner: {e}"

async def enumerate_subdomains(domain: str) -> str:
    """
    Checks for common subdomains by resolving them DNS.
    Simple enumeration using a built-in top-list.
    """
    common_subs = ["www", "mail", "remote", "blog", "webmail", "server", "ns1", "ns2", "smtp", "secure", "vpn", "m", "shop", "ftp", "admin"]
    
    found = []
    
    for sub in common_subs:
        full_domain = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            found.append(f"{full_domain} -> {ip}")
        except socket.gaierror:
            pass
        await asyncio.sleep(0.1) # Be nice
            
    if not found:
        return f"No common subdomains found for {domain}."
        
    return f"Subdomains found for {domain}:\n" + "\n".join(found)

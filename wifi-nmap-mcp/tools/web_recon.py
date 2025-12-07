import logging
import ssl
import socket
import httpx
from datetime import datetime

logger = logging.getLogger("web-recon-tools")

async def analyze_ssl_cert(domain: str) -> str:
    """Retrieves and analyzes the SSL certificate of a domain."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()
            
        subject = dict(x[0] for x in cert['subject'])
        issuer = dict(x[0] for x in cert['issuer'])
        not_before = cert['notBefore']
        not_after = cert['notAfter']
        
        # Calculate days remaining
        na_date = datetime.strptime(not_after, r"%b %d %H:%M:%S %Y %Z")
        remaining = (na_date - datetime.utcnow()).days
        
        return (
            f"Domain: {domain}\n"
            f"Subject: {subject.get('commonName', 'N/A')} ({subject.get('organizationName', 'N/A')})\n"
            f"Issuer: {issuer.get('commonName', 'N/A')} ({issuer.get('organizationName', 'N/A')})\n"
            f"Valid From: {not_before}\n"
            f"Valid Until: {not_after} ({remaining} days remaining)\n"
            f"Version: {cert.get('version')}"
        )
    except Exception as e:
        return f"Error analyzing SSL cert: {e}"

async def check_security_headers(url: str) -> str:
    """Checks for common security headers in the response."""
    if not url.startswith("http"):
        url = "https://" + url
        
    try:
        async with httpx.AsyncClient(verify=False) as client:
            resp = await client.get(url)
            headers = resp.headers
            
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]
        
        output = [f"Security Headers for {url}:"]
        
        for h in security_headers:
            if h in headers:
                output.append(f"[PASS] {h}: {headers[h]}")
            else:
                output.append(f"[MISS] {h}")
                
        output.append(f"\nServer: {headers.get('Server', 'Unknown')}")
        return "\n".join(output)
        
    except Exception as e:
        return f"Error checking headers: {e}"

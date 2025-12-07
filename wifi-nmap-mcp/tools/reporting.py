import logging
import asyncio
from tools.dns import lookup_dns, whois
from tools.scanning import ping_host, scan_local_network
from tools.web_recon import check_security_headers

logger = logging.getLogger("reporting-tools")

async def generate_security_report(target: str) -> str:
    """
    Automates a full reconnaissance scan on a target (domain or IP).
    Runs: DNS, Ping, Whois, and Header checks. 
    Returns a formatted Markdown report.
    This saves you from running 4 separate commands.
    """
    report = [f"# Security Recon Report for: {target}"]
    report.append(f"Generated at: {asyncio.get_event_loop().time()}")
    report.append("-" * 40)
    
    # 1. Quick Ping
    report.append("## 1. Availability (Ping)")
    try:
        ping_res = await ping_host(target)
        report.append(ping_res)
    except Exception as e:
        report.append(f"Ping failed: {e}")
        
    # 2. DNS Lookup
    report.append("\n## 2. DNS Information")
    try:
        dns_res = await lookup_dns(target)
        report.append(dns_res)
    except Exception as e:
        report.append(f"DNS lookup failed: {e}")
        
    # 3. Whois (if it's a domain)
    if not target.replace('.', '').isdigit(): # Simple check if it looks like a domain
        report.append("\n## 3. Whois Registration")
        try:
            # This can be slow, might want to limit?
            whois_res = await whois(target)
            # Truncate if too long? Whois is usually huge.
            report.append(whois_res[:2000] + "\n...(truncated)" if len(whois_res) > 2000 else whois_res)
            report.append("\nNote: Full Whois might have been truncated for readability.")
        except Exception as e:
            report.append(f"Whois failed: {e}")

    # 4. Security Headers (if it looks like a web server)
    report.append("\n## 4. Web Security Headers")
    try:
        # Try https first
        target_url = target if target.startswith("http") else f"https://{target}"
        headers_res = await check_security_headers(target_url)
        report.append(headers_res)
    except Exception as e:
        report.append(f"Header check failed: {e}")
        
    report.append("\n" + "=" * 40)
    report.append("End of Report.")
    
    return "\n".join(report)

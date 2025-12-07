import asyncio
import logging
from utils import get_os_type, run_command

logger = logging.getLogger("wifi-tools")

async def detect_os() -> str:
    """Detects the operating system running the server."""
    os_name = get_os_type()
    logger.info(f"Detected OS: {os_name}")
    return f"Current OS: {os_name}"

async def scan_wifi() -> str:
    """Scans for available WiFi networks using pywifi (Windows) or native commands."""
    os_name = get_os_type()
    logger.info("Scanning for WiFi networks...")
    
    if os_name == "Windows":
        try:
            import pywifi
            from pywifi import const
            import time
            
            wifi = pywifi.PyWiFi()
            if len(wifi.interfaces()) == 0:
                return "No WiFi interfaces found."
            
            iface = wifi.interfaces()[0]
            
            # Trigger scan
            iface.scan()
            # Wait for scan to complete (usually 2-5 seconds)
            await asyncio.sleep(5)
            
            results = iface.scan_results()
            
            if not results:
                return "No networks found."
            
            output = ["Available Networks:"]
            seen_ssids = set()
            
            for network in results:
                # Filter duplicates and empty SSIDs
                ssid = network.ssid
                if ssid and ssid not in seen_ssids:
                    seen_ssids.add(ssid)
                    # Signal strength is usually in dBm
                    signal = network.signal
                    output.append(f"SSID: {ssid:<20} | Signal: {signal} dBm | BSSID: {network.bssid}")
            
            return "\n".join(output)
            
        except ImportError:
            return "pywifi not installed. Falling back to netsh."
        except Exception as e:
            logger.error(f"pywifi error: {e}")
            # Fallback to netsh
            cmd = ["netsh", "wlan", "show", "networks", "mode=bssid"]
            return run_command(cmd)
            
    elif os_name == "Linux":
        # Linux command (requires wireless-tools or nmcli)
        cmd = ["nmcli", "dev", "wifi", "list"]
        result = run_command(cmd)
        if "Command failed" in result or "Error" in result:
             cmd = ["iwlist", "scan"] # This often requires sudo/root
             return run_command(cmd)
        return result
    elif os_name == "Darwin": # macOS
        cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"]
        return run_command(cmd)
    else:
        return f"WiFi scanning not implemented for OS: {os_name}"

async def connect_wifi(ssid: str, password: str) -> str:
    """Connects to a WiFi network. Windows only (via pywifi)."""
    os_name = get_os_type()
    if os_name != "Windows":
        return "WiFi connection currently only supported on Windows via pywifi."
        
    try:
        import pywifi
        from pywifi import const
        import time
        
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]
        
        iface.disconnect()
        await asyncio.sleep(1)
        
        profile = pywifi.Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)
        
        iface.connect(tmp_profile)
        
        # Wait for connection
        for _ in range(10):
            if iface.status() == const.IFACE_CONNECTED:
                return f"Successfully connected to {ssid}"
            await asyncio.sleep(1)
            
        return "Connection timed out or failed."
        
    except Exception as e:
        return f"Error connecting to WiFi: {e}"

async def get_interfaces() -> str:
    """Lists network interfaces."""
    os_name = get_os_type()
    logger.info("Listing network interfaces...")
    
    if os_name == "Windows":
        cmd = ["ipconfig", "/all"]
    else:
        cmd = ["ifconfig", "-a"] # or ip addr
    
    return run_command(cmd)

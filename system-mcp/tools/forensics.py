import hashlib
import os
import psutil
import logging
import time
import sys

logger = logging.getLogger("forensics-tools")

async def calculate_file_hash(filepath: str) -> str:
    """Calculates SHA256 and MD5 hashes of a file."""
    if not os.path.exists(filepath):
        return f"Error: File not found: {filepath}"
        
    try:
        sha256_hash = hashlib.sha256()
        md5_hash = hashlib.md5()
        
        with open(filepath, "rb") as f:
            # Read in chunks to handle large files
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
                md5_hash.update(byte_block)
                
        return (
            f"File: {filepath}\n"
            f"SHA256: {sha256_hash.hexdigest()}\n"
            f"MD5:    {md5_hash.hexdigest()}"
        )
    except Exception as e:
        return f"Error calculating hash: {e}"

async def list_open_ports() -> str:
    """Lists local processes listening on ports (like netstat)."""
    connections = psutil.net_connections(kind='inet')
    output = ["Open Ports (Listening):"]
    output.append(f"{'Proto':<5} | {'Local Address':<20} | {'PID':<6} | {'Process Name'}")
    output.append("-" * 60)
    
    for conn in connections:
        if conn.status == psutil.CONN_LISTEN:
            try:
                proc = psutil.Process(conn.pid)
                name = proc.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                name = "Unknown"
                
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            proto = "TCP" if conn.type == 1 else "UDP" # 1=TCP, 2=UDP
            
            output.append(f"{proto:<5} | {laddr:<20} | {conn.pid or 'N/A':<6} | {name}")
            
    return "\n".join(output)

async def kill_process(pid: int) -> str:
    """Terminates a process by its PID."""
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        proc.terminate()
        # Wait a bit
        try:
            proc.wait(timeout=3)
        except psutil.TimeoutExpired:
            proc.kill()
            
        return f"Successfully killed process {pid} ({name})"
    except psutil.NoSuchProcess:
        return f"Error: Process {pid} not found."
    except psutil.AccessDenied:
        return f"Error: Access denied to kill process {pid}."
    except Exception as e:
        return f"Error killing process: {e}"

async def get_recent_files(directory: str, minutes: int = 60) -> str:
    """Finds files in a directory modified within the last N minutes."""
    if not os.path.exists(directory):
        return f"Error: Directory not found: {directory}"
        
    now = time.time()
    cutoff = now - (minutes * 60)
    
    recent_files = []
    
    try:
        for root, dirs, files in os.walk(directory):
            for name in files:
                filepath = os.path.join(root, name)
                try:
                    mtime = os.path.getmtime(filepath)
                    if mtime > cutoff:
                        # Format time
                        time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
                        recent_files.append(f"{time_str} | {filepath}")
                except OSError:
                    pass
    except Exception as e:
        return f"Error scanning directory: {e}"
        
    if not recent_files:
        return f"No files modified in the last {minutes} minutes in {directory}."
        
    # Sort by time desc
    recent_files.sort(reverse=True)
    return f"Files modified in last {minutes} minutes:\n" + "\n".join(recent_files)

async def read_registry_key(path: str) -> str:
    """Reads a Windows Registry key value. Path format: HKLM\\Software\\..."""
    if sys.platform != "win32":
        return "Error: Registry tools only available on Windows."
        
    try:
        import winreg
    except ImportError:
        return "Error: winreg module not available."

    # Parse path
    # Example: HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    parts = path.split('\\')
    if len(parts) < 2:
        return "Error: Invalid registry path format."
        
    root_map = {
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKCR": winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKU": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
        "HKCC": winreg.HKEY_CURRENT_CONFIG
    }
    
    root_name = parts[0].upper()
    if root_name not in root_map:
        return f"Error: Unknown registry root: {root_name}"
        
    sub_key = "\\".join(parts[1:])
    
    try:
        output = [f"Registry Key: {path}"]
        with winreg.OpenKey(root_map[root_name], sub_key) as key:
            # List values
            i = 0
            while True:
                try:
                    name, value, type_ = winreg.EnumValue(key, i)
                    output.append(f"{name} = {value} (Type: {type_})")
                    i += 1
                except OSError:
                    break
        return "\n".join(output)
    except FileNotFoundError:
        return "Error: Registry key not found."
    except Exception as e:
        return f"Error reading registry: {e}"

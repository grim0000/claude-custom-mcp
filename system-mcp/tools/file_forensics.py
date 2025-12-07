import logging
import os
import re

logger = logging.getLogger("file-forensics")

async def analyze_file_signature(filepath: str) -> str:
    """
    Checks the file's 'Magic Bytes' to determine its true type.
    This helps detect malicious files disguising as something else (e.g., .jpg.exe).
    """
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"
        
    # Common magic bytes (Hex signatures)
    signatures = {
        "MZ": "Windows Executable (EXE/DLL)",
        "PK\x03\x04": "ZIP Archive / Office Doc / JAR",
        "%PDF": "PDF Document",
        "\x89PNG": "PNG Image",
        "\xFF\xD8\xFF": "JPEG Image",
        "GIF8": "GIF Image",
        "fail": "Unknown"
    }
    
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4) # Read first 4 bytes
            
            # Simple check
            header_str = ""
            try:
                header_str = header.decode('latin-1') # Best effort
            except:
                pass
                
            detected = "Unknown"
            
            if header.startswith(b'MZ'):
                detected = signatures['MZ']
            elif header.startswith(b'PK\x03\x04'):
                detected = signatures['PK\x03\x04']
            elif header.startswith(b'%PDF'):
                detected = signatures['%PDF']
            elif header.startswith(b'\x89PNG'):
                detected = signatures['\x89PNG']
            elif header.startswith(b'\xFF\xD8\xFF'):
                detected = signatures['\xFF\xD8\xFF']
            elif header.startswith(b'GIF8'):
                detected = signatures['GIF8']
            elif header.startswith(b'#!') or b'python' in header or b'bash' in header:
                detected = "Script (Shell/Python/Perl)"
            
            hex_head = header.hex().upper()
            return f"File: {os.path.basename(filepath)}\nFirst 4 bytes (Hex): {hex_head}\nDetected Type: {detected}"
            
    except Exception as e:
        return f"Error reading file: {e}"

async def extract_strings(filepath: str, min_len: int = 4) -> str:
    """
    Extracts readable ASCII and Unicode strings from a binary file.
    Useful for finding hidden URLs, IP addresses, or messages in malware.
    """
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"
        
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            
        # Regex to find consecutive printable chars
        # ASCII printable: 32-126
        # We also want to capture some unicode ranges if we were advanced, 
        # but basic 'strings' usually focuses on ASCII.
        
        regex = rb"[\x20-\x7E]{" + str(min_len).encode() + rb",}"
        matches = re.findall(regex, content)
        
        # Decode and filter
        decoded_strings = []
        for m in matches:
            try:
                s = m.decode('ascii')
                decoded_strings.append(s)
            except:
                pass
        
        # Limit output
        count = len(decoded_strings)
        preview = decoded_strings[:50] # First 50 strings
        
        output = [f"Found {count} strings (min length {min_len}). Showing first 50:"]
        output.extend(preview)
        
        if count > 50:
            output.append(f"\n... and {count - 50} more.")
            
        return "\n".join(output)
            
    except Exception as e:
        return f"Error processing file: {e}"

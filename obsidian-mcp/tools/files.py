import json
from utils import make_request

async def list_files(folder: str = "/") -> str:
    """Lists files in the vault. Use folder path to list subdirectories."""
    # Local REST API uses /vault/ endpoint to list files
    endpoint = f"vault/{folder}" if folder != "/" else "vault/"
    result = await make_request("GET", endpoint)
    
    try:
        data = json.loads(result)
        if "files" in data:
             # The API returns a list of strings (filenames/paths)
             files = data["files"]
             return "\n".join(files)
        return result # Return raw if structure is different
    except json.JSONDecodeError:
        return result

async def get_file_content(filepath: str) -> str:
    """Reads the content of a markdown file. Filepath should be relative to vault root."""
    endpoint = f"vault/{filepath}"
    return await make_request("GET", endpoint)

async def create_or_update_file(filepath: str, content: str) -> str:
    """Creates or updates a file with the given content. Overwrites existing content."""
    endpoint = f"vault/{filepath}"
    return await make_request("PUT", endpoint, data=content, content_type="text/markdown")

async def append_to_file(filepath: str, content: str) -> str:
    """Appends content to the end of an existing file."""
    endpoint = f"vault/{filepath}"
    return await make_request("POST", endpoint, data=content, content_type="text/markdown")

async def delete_file(filepath: str) -> str:
    """Deletes a file from the vault."""
    endpoint = f"vault/{filepath}"
    return await make_request("DELETE", endpoint)

async def get_active_file() -> str:
    """Gets the content of the currently active file in Obsidian."""
    endpoint = "active/"
    return await make_request("GET", endpoint)

async def get_daily_note() -> str:
    """Gets the content of today's daily note. Creates it if it doesn't exist."""
    endpoint = "periodic/daily/"
    return await make_request("GET", endpoint)

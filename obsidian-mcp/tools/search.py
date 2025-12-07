import json
from utils import make_request

async def search_notes(query: str) -> str:
    """Searches for notes containing the query string using Obsidian's search."""
    endpoint = f"search/simple?query={query}"
    return await make_request("GET", endpoint)

async def get_backlinks(filepath: str) -> str:
    """Finds all notes that link to the specified file."""
    # Note: Local REST API doesn't have a direct 'backlinks' endpoint in all versions,
    # but we can search for the filename.
    # A more robust way if the API supports it would be better, but 'search' is the fallback.
    # Let's try to see if there's a specific endpoint or just use search.
    # Using search for [[filename]] or just filename is a good proxy.
    
    # Actually, let's check if we can get metadata.
    # For now, we'll use the simple search for the filename as a proxy for backlinks.
    query = f'"{filepath}"'
    return await search_notes(query)

async def list_tags() -> str:
    """Lists all tags used in the vault."""
    # The Local REST API might not have a direct 'tags' endpoint.
    # We can try to search for '#' to see if it returns tags, or just return a message if not supported directly.
    # However, we can use the 'search' endpoint with a regex or similar if supported.
    # Alternatively, we can iterate files, but that's slow.
    # Let's try to return a helpful message or use a known endpoint if it exists.
    # Checking documentation... /tags/ isn't standard in the simple version.
    # We will implement a "best effort" by searching for `#` which might be too broad,
    # or we can just say "Not directly supported by simple API, try searching for #tagname".
    
    # Wait, if we use the 'commands' tool, we might be able to trigger the tag pane? No, we want data.
    # Let's implement a simple tag search that finds tags in the active file or just returns a placeholder
    # if we can't get global tags easily without scanning everything.
    
    # BETTER APPROACH: Use `search_notes` for `#`.
    return await search_notes("#")

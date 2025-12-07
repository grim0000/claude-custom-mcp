import json
from utils import make_request

async def list_commands() -> str:
    """Lists all available Obsidian commands."""
    endpoint = "commands/"
    result = await make_request("GET", endpoint)
    try:
        data = json.loads(result)
        if "commands" in data:
            cmds = [f"{c['id']}: {c['name']}" for c in data["commands"]]
            return "\n".join(cmds)
        return result
    except:
        return result

async def execute_command(command_id: str) -> str:
    """Executes an Obsidian command by its ID."""
    endpoint = f"commands/{command_id}"
    return await make_request("POST", endpoint)

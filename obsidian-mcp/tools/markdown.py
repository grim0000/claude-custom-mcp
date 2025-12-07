import json
from utils import make_request
from tools.files import get_file_content, create_or_update_file

# We need to import get_file_content and create_or_update_file from files.py? 
# No, that would be a circular dependency if files.py imports this.
# Better to import them from utils if they were there, or just use make_request directly.
# We'll use make_request directly to avoid circular imports.

async def append_to_heading(filepath: str, heading: str, content: str) -> str:
    """
    Appends content under a specific heading in a note.
    Creates the heading if it doesn't exist (appended to end).
    """
    # 1. Get file content
    endpoint_get = f"vault/{filepath}"
    current_content = await make_request("GET", endpoint_get)
    
    if "Error" in current_content and "not found" in current_content:
        return "Error: File not found."
        
    lines = current_content.split('\n')
    heading_found = False
    insert_index = -1
    
    # Normalize heading (remove leading # if user provided them, or match exact)
    # We'll assume user provides "Tasks" for "## Tasks" or "### Tasks"
    # Or user provides "## Tasks". Let's try to match loosely.
    
    target_heading = heading.strip()
    if not target_heading.startswith("#"):
        # Match any level heading with this text
        pass 
    
    final_lines = []
    for i, line in enumerate(lines):
        final_lines.append(line)
        # Check if line matches heading
        # Simple check: line starts with # and ends with heading
        if line.lstrip().startswith("#") and heading in line:
            heading_found = True
            # We want to append AFTER this section. 
            # So we need to find the next heading or end of file.
            # Actually, we can just insert after this line? 
            # Usually we want to append to the END of the section.
            
            # Look ahead for next heading
            for j in range(i + 1, len(lines)):
                if lines[j].lstrip().startswith("#"):
                    insert_index = j
                    break
            else:
                insert_index = len(lines) # End of file
            break
            
    if heading_found:
        # We found the heading, insert before the next heading (insert_index)
        # We need to reconstruct the file.
        # Wait, the loop above just found the index.
        
        # Re-construct:
        # 0 to insert_index -> content
        # insert_index -> new content
        # insert_index to end -> rest
        
        new_lines = lines[:insert_index] + ["", content, ""] + lines[insert_index:]
        new_content = "\n".join(new_lines)
        
    else:
        # Heading not found, append to end
        new_content = current_content + f"\n\n## {heading}\n{content}"
        
    # 2. Update file
    endpoint_put = f"vault/{filepath}"
    return await make_request("PUT", endpoint_put, data=new_content, content_type="text/markdown")

async def get_frontmatter(filepath: str) -> str:
    """Gets the YAML frontmatter of a note."""
    # Local REST API doesn't parse frontmatter separately in 'get content'.
    # We have to parse it manually from the content.
    endpoint = f"vault/{filepath}"
    content = await make_request("GET", endpoint)
    
    if content.startswith("---"):
        try:
            end_idx = content.find("---", 3)
            if end_idx != -1:
                return content[0:end_idx+3]
        except:
            pass
            
    return "No frontmatter found."

async def update_frontmatter(filepath: str, key: str, value: str) -> str:
    """Updates a key in the YAML frontmatter. Creates frontmatter if missing."""
    endpoint = f"vault/{filepath}"
    content = await make_request("GET", endpoint)
    
    import yaml # Need to check if pyyaml is available or do simple string manipulation
    # To avoid dependencies if possible, let's do simple string manipulation for now
    # or assume simple "key: value" format.
    
    # robust way:
    lines = content.split('\n')
    has_frontmatter = content.startswith("---")
    
    new_lines = []
    if has_frontmatter:
        # Find end
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_idx = i
                break
        
        if end_idx != -1:
            # We have frontmatter block
            fm_lines = lines[1:end_idx]
            key_found = False
            for j, line in enumerate(fm_lines):
                if line.strip().startswith(f"{key}:"):
                    fm_lines[j] = f"{key}: {value}"
                    key_found = True
                    break
            
            if not key_found:
                fm_lines.append(f"{key}: {value}")
                
            new_lines = ["---"] + fm_lines + ["---"] + lines[end_idx+1:]
        else:
            # Malformed?
            new_lines = [f"---\n{key}: {value}\n---\n"] + lines
    else:
        # No frontmatter
        new_lines = [f"---\n{key}: {value}\n---\n"] + lines
        
    new_content = "\n".join(new_lines)
    return await make_request("PUT", endpoint, data=new_content, content_type="text/markdown")

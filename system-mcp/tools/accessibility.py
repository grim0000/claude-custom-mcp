import logging
import pyautogui
import uiautomation as auto

logger = logging.getLogger("accessibility-tools")

async def get_cursor_position() -> str:
    """Gets the current mouse cursor position."""
    try:
        x, y = pyautogui.position()
        return f"Cursor Position: ({x}, {y})"
    except Exception as e:
        return f"Error getting cursor position: {e}"

async def get_ui_tree(max_depth: int = 3) -> str:
    """
    Gets a simplified tree of the UI elements for the currently active window.
    Useful for finding element names to click.
    """
    try:
        root = auto.GetRootControl()
        # Get focused window
        window = root.GetFocus()
        if not window:
            window = root
            
        output = [f"UI Tree for: {window.Name} ({window.ClassName})"]
        
        def walk(control, depth):
            if depth > max_depth:
                return
            
            indent = "  " * depth
            info = f"{indent}- Name: '{control.Name}' | Type: {control.ControlTypeName}"
            output.append(info)
            
            for child in control.GetChildren():
                walk(child, depth + 1)
                
        walk(window, 1)
        return "\n".join(output)
    except Exception as e:
        return f"Error getting UI tree: {e}"

async def click_element_by_name(name: str) -> str:
    """
    Finds a UI element by its Name and clicks it.
    Searches in the currently active window first, then root.
    """
    try:
        # Try to find in focused window first
        root = auto.GetRootControl()
        window = root.GetFocus()
        
        found = None
        if window:
            found = window.findfirst(name=name)
            
        if not found:
            # Search root (might be slow)
            found = root.findfirst(name=name)
            
        if found:
            found.Click()
            return f"Clicked element: '{name}'"
        else:
            return f"Element '{name}' not found."
            
    except Exception as e:
        return f"Error clicking element: {e}"

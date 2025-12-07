import logging
import os
import base64
from io import BytesIO

logger = logging.getLogger("desktop-tools")

async def take_screenshot() -> str:
    """Takes a screenshot and returns it as a base64 string (or saves to file)."""
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        
        # Save to buffer
        buffered = BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # For MCP, returning huge base64 might be too much for some clients.
        # But it's the most direct way. 
        # Alternatively, save to a temp file and return path.
        # Let's return a summary and maybe save to a temp file for now?
        # Or just return "Screenshot taken" if we can't display it.
        # But user wants the tool. Let's return a message saying where it is saved.
        
        import datetime
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        path = os.path.join(screenshots_dir, filename)
        
        screenshot.save(path)
        
        return f"Screenshot saved successfully to: {path}"
        
    except ImportError:
        return "Error: pyautogui not installed. Please install it to take screenshots."
    except Exception as e:
        return f"Error taking screenshot: {e}"

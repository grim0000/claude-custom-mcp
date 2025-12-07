import logging
import pyautogui
import time
import os

logger = logging.getLogger("vision-tools")

async def locate_image_on_screen(image_path: str, confidence: float = 0.9) -> str:
    """
    Locates an image on the screen. Returns the center coordinates (x, y).
    Requires the image file to exist.
    """
    if not os.path.exists(image_path):
        return f"Error: Image file not found: {image_path}"
        
    try:
        # confidence requires opencv-python
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            return f"Found at: ({location.x}, {location.y})"
        else:
            return "Image not found on screen."
    except Exception as e:
        return f"Error locating image: {e}"

async def wait_for_image(image_path: str, timeout: int = 10) -> str:
    """
    Waits for an image to appear on the screen within the timeout (seconds).
    Returns coordinates if found.
    """
    if not os.path.exists(image_path):
        return f"Error: Image file not found: {image_path}"
        
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.9)
            if location:
                return f"Found at: ({location.x}, {location.y})"
        except:
            pass
        time.sleep(0.5)
        
    return f"Timeout: Image not found after {timeout} seconds."

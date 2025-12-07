import pyautogui
import logging

logger = logging.getLogger("automation-tools")

# Fail-safe: moving mouse to corner will throw exception
pyautogui.FAILSAFE = True

async def move_mouse(x: int, y: int) -> str:
    """Moves the mouse cursor to the specified coordinates."""
    try:
        pyautogui.moveTo(x, y)
        return f"Moved mouse to ({x}, {y})"
    except Exception as e:
        return f"Error moving mouse: {e}"

async def click_mouse(button: str = "left") -> str:
    """Clicks the mouse button ('left', 'right', 'middle')."""
    try:
        pyautogui.click(button=button)
        return f"Clicked {button} button"
    except Exception as e:
        return f"Error clicking mouse: {e}"

async def type_text(text: str, interval: float = 0.0) -> str:
    """Types the given text. Interval is seconds between keys."""
    try:
        pyautogui.write(text, interval=interval)
        return f"Typed text: {text}"
    except Exception as e:
        return f"Error typing text: {e}"

async def press_key(key: str) -> str:
    """Presses a specific key (e.g., 'enter', 'esc', 'tab', 'ctrl', 'c')."""
    try:
        pyautogui.press(key)
        return f"Pressed key: {key}"
    except Exception as e:
        return f"Error pressing key: {e}"

async def get_screen_size() -> str:
    """Gets the screen resolution."""
    try:
        width, height = pyautogui.size()
        return f"Screen Size: {width}x{height}"
    except Exception as e:
        return f"Error getting screen size: {e}"

async def drag_mouse(x: int, y: int) -> str:
    """Drags the mouse to the specified coordinates (holding left click)."""
    try:
        pyautogui.dragTo(x, y, button='left')
        return f"Dragged mouse to ({x}, {y})"
    except Exception as e:
        return f"Error dragging mouse: {e}"

async def scroll(clicks: int) -> str:
    """Scrolls the mouse wheel. Positive for up, negative for down."""
    try:
        pyautogui.scroll(clicks)
        return f"Scrolled {clicks} clicks"
    except Exception as e:
        return f"Error scrolling: {e}"

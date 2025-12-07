import logging
import pyttsx3

logger = logging.getLogger("voice-tools")

async def speak(text: str) -> str:
    """Speaks the given text using the system's text-to-speech engine."""
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return f"Spoke: {text}"
    except Exception as e:
        return f"Error speaking text: {e}"

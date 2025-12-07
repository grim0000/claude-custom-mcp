import logging
import os
from PIL import Image
from PIL.ExifTags import TAGS

logger = logging.getLogger("steganography-tools")

async def hide_text_in_image(image_path: str, text: str) -> str:
    """Hides a secret text message inside an image using LSB steganography."""
    try:
        from stegano import lsb
        
        if not os.path.exists(image_path):
            return f"Error: Image not found: {image_path}"
            
        secret = lsb.hide(image_path, text)
        
        # Save as new file
        base, ext = os.path.splitext(image_path)
        new_path = f"{base}_secret.png" # PNG is lossless, better for steganography
        secret.save(new_path)
        
        return f"Message hidden successfully. Saved to: {new_path}"
    except ImportError:
        return "Error: stegano library not installed."
    except Exception as e:
        return f"Error hiding text: {e}"

async def reveal_text_from_image(image_path: str) -> str:
    """Reveals a secret text message hidden in an image."""
    try:
        from stegano import lsb
        
        if not os.path.exists(image_path):
            return f"Error: Image not found: {image_path}"
            
        clear_message = lsb.reveal(image_path)
        return f"Hidden Message: {clear_message}"
    except ImportError:
        return "Error: stegano library not installed."
    except Exception as e:
        return f"Error revealing text: {e}"

async def get_exif_data(image_path: str) -> str:
    """Extracts EXIF metadata from an image."""
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        
        if not exif_data:
            return "No EXIF data found."
            
        output = [f"EXIF Data for {image_path}:"]
        for tag_id in exif_data:
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            # Decode bytes if necessary
            if isinstance(data, bytes):
                try:
                    data = data.decode()
                except:
                    data = str(data)
            output.append(f"{tag}: {data}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error reading EXIF data: {e}"

async def remove_exif_data(image_path: str) -> str:
    """Removes EXIF metadata from an image."""
    try:
        image = Image.open(image_path)
        
        # We create a new image without data
        data = list(image.getdata())
        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(data)
        
        base, ext = os.path.splitext(image_path)
        new_path = f"{base}_clean{ext}"
        image_without_exif.save(new_path)
        
        return f"EXIF data removed. Saved to: {new_path}"
    except Exception as e:
        return f"Error removing EXIF data: {e}"

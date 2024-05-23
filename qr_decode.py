from pyzbar import pyzbar
from PIL import Image
from pyzbar import pyzbar
from PIL import Image
import os
import ctypes


def load_libiconv():
    """Loads libiconv.dll explicitly for pyzbar."""
    try:
        # Try to load from the system path first
        ctypes.cdll.LoadLibrary("libiconv.dll")
    except OSError:
        # If not found, load it from the same directory as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        libiconv_path = os.path.join(script_dir, "libiconv.dll")
        ctypes.cdll.LoadLibrary(libiconv_path)


# Load the library before using pyzbar
load_libiconv()

def decode_qr_code(image_path):
    try:
        image = Image.open(image_path)
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            return obj.data.decode('utf-8')
    except Exception as e:
        print(f"Error decoding QR code: {e}")
    return None

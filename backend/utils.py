import base64
import cv2
import numpy as np

def decode_image(base64_string: str) -> np.ndarray:
    """Decodes a base64 string to an OpenCV image and resizes it for faster processing."""
    # Remove header if present
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]
    
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Resize image. Smaller image = Faster DeepFace execution
    img = cv2.resize(img, (224, 224))
    return img

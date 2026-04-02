"""
src/image_processor.py
Utilities for reading, converting, and preparing images for Streamlit.
"""

import cv2
import numpy as np
from PIL import Image


def load_image_from_upload(uploaded_file) -> np.ndarray:
    """Read a Streamlit UploadedFile into an OpenCV BGR ndarray."""
    file_bytes = np.frombuffer(uploaded_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return img


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    """Convert OpenCV BGR image to RGB for Streamlit display."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def resize_for_display(img: np.ndarray, max_width: int = 900) -> np.ndarray:
    """Resize image proportionally so it doesn't exceed max_width pixels."""
    h, w = img.shape[:2]
    if w > max_width:
        scale  = max_width / w
        new_wh = (int(w * scale), int(h * scale))
        img    = cv2.resize(img, new_wh, interpolation=cv2.INTER_AREA)
    return img


def numpy_to_pil(img: np.ndarray) -> Image.Image:
    """Convert RGB numpy array to PIL Image."""
    return Image.fromarray(img)

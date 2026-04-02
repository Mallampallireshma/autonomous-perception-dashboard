"""
src/webcam.py
Webcam capture helper – reads a single frame from the default camera.
"""

import cv2
import numpy as np


# Classes that trigger the alert system
ALERT_CLASSES = {"person", "car", "truck", "bus", "bicycle", "motorcycle"}


def capture_frame(device_index: int = 0) -> np.ndarray | None:
    """
    Grab one frame from the webcam.

    Returns None if the camera cannot be opened or the frame is empty.
    """
    cap = cv2.VideoCapture(device_index)
    if not cap.isOpened():
        return None

    # Warm-up: skip first few frames (some cameras start dark)
    for _ in range(3):
        cap.grab()

    ret, frame = cap.read()
    cap.release()

    return frame if ret else None


def check_alerts(detections: list[dict]) -> list[str]:
    """
    Return a list of alert strings for any detected alert-class objects.

    Example: ['⚠ PERSON DETECTED', '⚠ CAR DETECTED']
    """
    found = set()
    for d in detections:
        cls = d["class"].lower()
        if cls in ALERT_CLASSES:
            found.add(cls.upper())

    return [f"⚠  {cls} DETECTED" for cls in sorted(found)]

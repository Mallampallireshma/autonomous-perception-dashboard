"""
src/detector.py
FINAL CLOUD-SAFE VERSION
"""

import streamlit as st

# ✅ SAFE YOLO IMPORT
try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


# ✅ LOAD MODEL
@st.cache_resource
def load_model(model_name="yolov8n.pt"):

    # 🔥 If ultralytics fails → return None
    if YOLO is None:
        return None

    try:
        return YOLO(model_name)
    except Exception:
        return None


# ✅ DETECTION FUNCTION
def detect_objects(frame, model, conf_threshold=0.25, enhance=False):

    # 🔥 If model not loaded → skip detection
    if model is None:
        return frame, []

    results = model(frame)

    annotated = frame.copy()
    detections = []

    if len(results) == 0:
        return annotated, []

    r = results[0]

    if r.boxes is None:
        return annotated, []

    for box in r.boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])

        if conf < conf_threshold:
            continue

        label = model.names[cls_id]

        detections.append({
            "class": label,
            "confidence": conf
        })

    return annotated, detections


# ✅ COUNT FUNCTION
def count_objects(detections):
    counts = {}
    for d in detections:
        counts[d["class"]] = counts.get(d["class"], 0) + 1
    return counts
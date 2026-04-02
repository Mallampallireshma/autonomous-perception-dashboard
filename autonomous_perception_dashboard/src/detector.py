"""
src/detector.py
FINAL WORKING VERSION (Detection + Boxes)
"""

import cv2
from ultralytics import YOLO
import streamlit as st


# ✅ LOAD MODEL (cached)
@st.cache_resource
def load_model(model_name="yolov8n.pt"):
    return YOLO(model_name)


# ✅ DETECTION FUNCTION
def detect_objects(frame, model, conf_threshold=0.40, enhance=False):

    if model is None:
        return frame, []

    results = model(frame, conf=conf_threshold)

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

        label = model.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # ✅ DRAW BOXES
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0,255,0), 2)
        cv2.putText(
            annotated,
            f"{label} {conf:.2f}",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,255,0),
            2
        )

        detections.append({
            "class": label,
            "confidence": conf
        })

    return annotated, detections


# ✅ COUNT
def count_objects(detections):
    counts = {}
    for d in detections:
        counts[d["class"]] = counts.get(d["class"], 0) + 1
    return counts
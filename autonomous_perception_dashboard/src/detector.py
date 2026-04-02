import cv2
from ultralytics import YOLO
import streamlit as st

# ✅ LOAD MODEL (FORCE CORRECT PATH)
@st.cache_resource
def load_model(model_name="yolov8n.pt"):
    model = YOLO(model_name)
    return model


def detect_objects(frame, model, conf_threshold=0.25, enhance=False):

    # Run YOLO
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

        # 🔥 FILTER BY CONFIDENCE
        if conf < conf_threshold:
            continue

        label = model.names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Draw box
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0,255,255), 3)
        cv2.rectangle(annotated, (x1, y1-25), (x2, y1), (0,255,255), -1)

        cv2.putText(
            annotated,
            f"{label} {conf:.2f}",
            (x1+5, y1-5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0,0,0),
            2
        )

        detections.append({
            "class": label,
            "confidence": conf
        })

    return annotated, detections


def count_objects(detections):
    counts = {}
    for d in detections:
        counts[d["class"]] = counts.get(d["class"], 0) + 1
    return counts
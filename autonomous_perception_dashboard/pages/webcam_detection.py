"""
pages/webcam_detection.py
(SPEED OPTIMIZED VERSION)
"""

import time
import streamlit as st
import cv2

from src.detector import load_model, detect_objects, count_objects
from src.image_processor import bgr_to_rgb
from src.webcam import capture_frame, check_alerts


def _page_header():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:16px; padding:8px 0 20px;
                border-bottom:1px solid rgba(56,189,248,0.15); margin-bottom:24px;'>
        <div style='font-size:32px;'>📷</div>
        <div>
            <div style='font-size:20px;
                        font-weight:700; color:#f0f9ff;'>
                WEBCAM DETECTION
            </div>
            <div style='font-size:14px; color:#64748b;'>
                Live camera · Fast YOLOv8 · Optimized
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show():
    _page_header()

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        conf_thresh  = st.slider("Confidence Threshold", 0.10, 0.95, 0.40, 0.05)
        enhance      = st.toggle("🌟 Brightness Enhancement", value=False)
        model_name   = st.selectbox("Model", ["yolov8n.pt", "yolov8s.pt"])
        cam_index    = st.number_input("Camera Index", 0, 5, 0, 1)

        frame_delay  = st.slider("Frame Delay (ms)", 50, 500, 120, 10)

        # 🔥 NEW SPEED CONTROL
        frame_skip   = st.slider("Speed Mode (Skip Frames)", 1, 5, 2)

        max_frames   = st.slider("Auto-stop after N frames", 30, 500, 100, 10)

    # ── Controls ──────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        start = st.button("▶ START", use_container_width=True)
    with col2:
        stop  = st.button("⏹ STOP", use_container_width=True)

    if "webcam_running" not in st.session_state:
        st.session_state.webcam_running = False

    if start:
        st.session_state.webcam_running = True
    if stop:
        st.session_state.webcam_running = False

    frame_placeholder = st.empty()
    alert_placeholder = st.empty()

    if not st.session_state.webcam_running:
        st.info("Press START to begin webcam detection")
        return

    # ── Load model ────────────────────────────────────────────────────────────
    with st.spinner("⚙️ Loading model..."):
        model = load_model(model_name)

    frame_count = 0

    while st.session_state.webcam_running and frame_count < max_frames:

        frame = capture_frame(int(cam_index))

        if frame is None:
            st.error("Cannot access webcam")
            break

        # 🔥 SPEED: Resize frame
        frame = cv2.resize(frame, (640, 480))

        # 🔥 SPEED: Skip frames
        if frame_count % frame_skip != 0:
            frame_count += 1
            continue

        # Detection
        annotated, detections = detect_objects(frame, model, conf_thresh, enhance)
        counts = count_objects(detections)
        alerts = check_alerts(detections)

        # Display
        frame_placeholder.image(
            bgr_to_rgb(annotated),
            caption=f"Frame {frame_count} | {len(detections)} objects",
            use_container_width=True
        )

        # Alerts
        if alerts:
            alert_placeholder.warning("⚠ ALERT: " + ", ".join(alerts))
        else:
            alert_placeholder.success("✔ Safe")

        frame_count += 1
        time.sleep(frame_delay / 1000)

    st.session_state.webcam_running = False
    st.success("Detection stopped")
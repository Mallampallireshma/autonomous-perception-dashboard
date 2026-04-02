"""
pages/video_detection.py  — FIXED VERSION
"""

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.detector        import load_model
from src.video_processor import process_video, save_csv_report, save_upload_to_temp


def show():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:16px; padding:8px 0 20px;
                border-bottom:1px solid rgba(56,189,248,0.15); margin-bottom:24px;'>
        <div style='font-size:32px;'>🎬</div>
        <div>
            <div style='font-size:22px; font-weight:800; color:#f0f9ff;'>
                VIDEO DETECTION
            </div>
            <div style='font-size:14px; color:#64748b; margin-top:2px;'>
                Upload video · YOLOv8 · Faster processing
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ─────────────────────────────────
    with st.sidebar:
        conf_thresh = st.slider("Confidence Threshold", 0.10, 0.95, 0.40, 0.05)
        enhance     = st.toggle("🌟 Brightness Enhancement", value=False)
        model_name  = st.selectbox("Model", ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"])
        frame_skip  = st.slider("Speed Mode (Skip Frames)", 1, 5, 2)

    # ── Upload ─────────────────────────────────
    st.markdown("### 📤 Upload Video")

    uploaded = st.file_uploader(
        "Upload MP4 / AVI / MOV",
        type=["mp4", "avi", "mov", "mkv"]
    )

    if uploaded is None:
        st.info("Upload a video to start detection")
        return

    # 👉 show original video (centered)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.video(uploaded)

    run = st.button("🚀 Run Detection")

    if not run:
        return

    uploaded.seek(0)
    input_path  = save_upload_to_temp(uploaded)
    base        = os.path.splitext(input_path)[0]
    output_path = base + "_annotated.mp4"
    csv_path    = base + "_report.csv"

    with st.spinner("⚙️ Loading YOLOv8..."):
        model = load_model(model_name)

    progress_bar = st.progress(0)
    status_text  = st.empty()

    def update_progress(frac):
        progress_bar.progress(min(frac, 1.0))
        status_text.write(f"Processing... {int(frac*100)}%")

    st.warning("⏳ Processing video... please wait")

    frame_records = process_video(
        input_path,
        output_path,
        model,
        conf_thresh,
        enhance,
        update_progress,
        frame_skip
    )

    progress_bar.progress(1.0)
    st.success("✅ Processing Complete")

    save_csv_report(frame_records, csv_path)

    # ── Summary ────────────────────────────────
    total_dets = sum(r.get("detections", 0) for r in frame_records)

    st.markdown("### 📊 Summary")
    st.write("Total Frames:", len(frame_records))
    st.write("Total Detections:", total_dets)

    # ── OUTPUT VIDEO (FIXED CENTER) ────────────
    if os.path.exists(output_path):
        with open(output_path, "rb") as f:
            video_bytes = f.read()

        st.markdown("### 🎬 Processed Video")

        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.video(video_bytes)

            st.download_button(
                "⬇ Download Video",
                data=video_bytes,
                file_name="output.mp4"
            )

    # ── CSV DOWNLOAD ───────────────────────────
    if os.path.exists(csv_path):
        with open(csv_path, "rb") as f:
            st.download_button(
                "⬇ Download CSV",
                data=f.read(),
                file_name="report.csv"
            )

    try:
        os.remove(input_path)
    except:
        pass
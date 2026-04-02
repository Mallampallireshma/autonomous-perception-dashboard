"""
pages/image_detection.py
Upload an image → run YOLOv8 → show original vs annotated side by side,
object count table, and bar chart.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.detector        import load_model, detect_objects, count_objects
from src.image_processor import load_image_from_upload, bgr_to_rgb, resize_for_display

# ─── Shared plotly theme ──────────────────────────────────────────────────────
_PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font         =dict(family="Inter, sans-serif", color="#94a3b8"),
    margin       =dict(l=20, r=20, t=40, b=20),
)


def _page_header():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:16px; padding:8px 0 20px;
                border-bottom:1px solid rgba(56,189,248,0.15); margin-bottom:24px;'>
        <div style='font-size:32px;'>🖼️</div>
        <div>
            <div style='font-size:20px;
                        font-weight:700; color:#f0f9ff;'>
                IMAGE DETECTION
            </div>
            <div style='font-size:14px; color:#64748b;'>
                Upload an image · YOLOv8 detects objects · View annotated results
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show():
    _page_header()

    # ── Sidebar controls ──────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("### ⚙ Detection Settings")

        conf_thresh = st.slider("Confidence Threshold", 0.10, 0.95, 0.40, 0.05)
        enhance     = st.toggle("🌟 Brightness Enhancement", value=False)
        model_name  = st.selectbox("Model", ["yolov8n.pt", "yolov8s.pt", "yolov8m.pt"])

    # ── File upload ───────────────────────────────────────────────────────────
    st.markdown("### 📤 Upload Image")

    uploaded = st.file_uploader(
        "Supported formats: JPG, JPEG, PNG, BMP, WEBP",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
    )

    if uploaded is None:
        st.info("Upload an image to start detection")
        return

    # ── Load model ────────────────────────────────────────────────────────────
    with st.spinner("⚙️ Loading YOLOv8 model..."):
        model = load_model(model_name)

    # ── Run inference ─────────────────────────────────────────────────────────
    img_bgr = load_image_from_upload(uploaded)

    with st.spinner("🔍 Detecting objects..."):
        annotated_bgr, detections = detect_objects(
            img_bgr, model, conf_thresh, enhance
        )

    st.success("✅ Detection Complete")

    counts = count_objects(detections)
    total  = len(detections)

    # ── Top metrics ───────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Objects Found", total)
    m2.metric("Unique Classes", len(counts))
    m3.metric("Confidence", f"{conf_thresh:.0%}")
    m4.metric("Image Size", f"{img_bgr.shape[1]}×{img_bgr.shape[0]}")

    st.markdown("---")

    # ── Images ────────────────────────────────────────────────────────────────
    left, right = st.columns(2)

    with left:
        st.subheader("Original Image")
        st.image(bgr_to_rgb(resize_for_display(img_bgr)), use_container_width=True)

    with right:
        st.subheader("Detected Image")
        st.image(bgr_to_rgb(resize_for_display(annotated_bgr)), use_container_width=True)

    if total == 0:
        st.warning("No objects detected. Try lowering confidence.")
        return

    st.markdown("---")

    # ── Table + Chart ─────────────────────────────────────────────────────────
    tab_table, tab_chart, tab_raw = st.tabs(
        ["📋 Table", "📊 Chart", "🔬 Raw"]
    )

    df_counts = pd.DataFrame(
        list(counts.items()), columns=["Class", "Count"]
    ).sort_values("Count", ascending=False)

    # ✅ FIXED TABLE (NO WHITE ISSUE)
    with tab_table:
        st.subheader("Detected Objects Summary")
        st.dataframe(df_counts, use_container_width=True)

    # Chart
    with tab_chart:
        fig = go.Figure(go.Bar(
            x=df_counts["Class"],
            y=df_counts["Count"],
            text=df_counts["Count"],
            textposition="outside",
        ))
        fig.update_layout(**_PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    # Raw detections
    with tab_raw:
        df_raw = pd.DataFrame(detections)
        st.dataframe(df_raw, use_container_width=True)
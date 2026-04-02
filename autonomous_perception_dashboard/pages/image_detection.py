import streamlit as st
import cv2
import numpy as np

from src.detector import load_model, detect_objects, count_objects


def show():
    st.title("🖼️ Image Detection")

    uploaded = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded is None:
        return

    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    conf_thresh = st.slider("Confidence", 0.1, 0.9, 0.4)

    model = load_model("yolov8n.pt")

    with st.spinner("Detecting objects..."):
        annotated, detections = detect_objects(image, model, conf_thresh)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Original Image", use_column_width=True)

    with col2:
        st.image(annotated, caption="Detected Image", use_column_width=True)

    counts = count_objects(detections)
    st.write("### Detected Objects")
    st.write(counts)
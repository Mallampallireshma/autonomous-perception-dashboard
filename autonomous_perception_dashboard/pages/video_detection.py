import streamlit as st
import tempfile
import cv2

from src.detector import load_model, detect_objects


def show():
    st.title("🎬 Video Detection")

    uploaded = st.file_uploader("Upload Video", type=["mp4","avi","mov"])

    if uploaded is None:
        return

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded.read())

    cap = cv2.VideoCapture(tfile.name)

    model = load_model("yolov8n.pt")

    stframe = st.empty()

    with st.spinner("Processing video..."):

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            annotated, _ = detect_objects(frame, model, 0.4)

            stframe.image(annotated, channels="BGR")

    cap.release()
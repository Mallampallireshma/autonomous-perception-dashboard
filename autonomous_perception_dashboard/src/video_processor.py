import cv2
import pandas as pd
import tempfile
import os

from src.detector import detect_objects


# ✅ SAVE UPLOADED VIDEO
def save_upload_to_temp(uploaded_file):
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())
    return tfile.name


# ✅ PROCESS VIDEO (WITH SPEED)
def process_video(input_path, output_path, model, conf, enhance, progress_callback=None, frame_skip=2):

    cap = cv2.VideoCapture(input_path)

    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (width, height)
    )

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0

    records = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # 🔥 SPEED BOOST (skip frames)
        if frame_count % frame_skip != 0:
            continue

        # 🔥 Resize for speed
        small_frame = cv2.resize(frame, (640, 480))

        annotated_small, detections = detect_objects(small_frame, model, conf, enhance)

# 🔥 Resize back
        annotated = cv2.resize(annotated_small, (frame.shape[1], frame.shape[0]))

        out.write(annotated)

        from collections import Counter

        class_counts = Counter([d["class"] for d in detections])

        row = {"frame": frame_count}

# add each class count
        for cls, count in class_counts.items():
          row[cls] = count

        records.append(row)

        if progress_callback:
            progress_callback(frame_count / total_frames)

    cap.release()
    out.release()

    return records


# ✅ SAVE CSV REPORT
def save_csv_report(records, csv_path):
    df = pd.DataFrame(records)
    df.to_csv(csv_path, index=False)
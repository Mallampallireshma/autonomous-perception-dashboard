import streamlit as st

st.set_page_config(
    page_title="Autonomous Perception Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 🔥 FONT + SPACING FIX (MAIN)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

/* GLOBAL FIX */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0px !important;
}

/* TOP SPACING FIX */
.block-container {
    padding-top: 3rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* REMOVE MONOSPACE */
code, pre {
    font-family: 'Inter', sans-serif !important;
}

/* TEXT */
p, span, label, div {
    color: #e2e8f0 !important;
}

/* HEADINGS */
h1, h2, h3 {
    font-weight: 700 !important;
    margin-top: 20px !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #020617 !important;
}

/* BUTTON */
.stButton > button {
    font-weight: 600 !important;
    border-radius: 8px !important;
}

/* CARD SPACING */
.apd-card {
    margin-top: 20px !important;
}

/* COLUMN GAP */
[data-testid="column"] {
    padding: 10px !important;
}

</style>
""", unsafe_allow_html=True)

# ── EXISTING CSS ──
st.markdown("""
<style>
:root {
    --bg-deep:#030712;
    --bg-card:rgba(15,23,42,0.85);
    --border:rgba(56,189,248,0.25);
    --accent-cyan:#38bdf8;
    --accent-green:#4ade80;
    --accent-amber:#fbbf24;
    --accent-purple:#a78bfa;
    --text-primary:#f0f9ff;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-primary) !important;
}
            /* FIX TABLE TEXT VISIBILITY */
[data-testid="stDataFrame"] * {
    color: white !important;
}

/* FIX TABLE BACKGROUND */
[data-testid="stDataFrame"] {
    background-color: #0f172a !important;
}

/* FIX SELECTED CELL (white issue remove) */
[data-testid="stDataFrame"] div[role="gridcell"] {
    background-color: transparent !important;
}
            /* FIX FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(15,23,42,0.6) !important;
    border: 1px dashed #38bdf8 !important;
    border-radius: 10px !important;
    padding: 15px !important;
}


/* CARD */
.apd-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px;'>
        <div style='font-size:20px; font-weight:800; color:#f0f9ff;'>
            Autonomous Perception
        </div>
        <div style='font-size:12px; color:#4ade80; margin-top:4px;'>
            Dashboard v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠 Home", "🖼️ Image Detection", "🎬 Video Detection",
         "📷 Webcam Detection", "📊 Analytics"],
        label_visibility="collapsed"
    )

# ── HOME PAGE (FULL FILLED UI) ──
if "Home" in page:

    st.markdown("""
    <div style='text-align:center; padding:60px 0 30px;'>
        <h1 style='font-size:48px; font-weight:900; color:#f0f9ff;'>
            Autonomous Perception
        </h1>
        <div style='font-size:20px; color:#38bdf8; margin:10px 0;'>
            AI Dashboard
        </div>
        <p style='font-size:16px; color:#94a3b8; max-width:700px; margin:auto;'>
            Real-time object detection powered by YOLOv8 and OpenCV
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 🔥 FEATURE CARDS
    st.markdown("### 🚀 Modules")

    col1, col2, col3, col4 = st.columns(4)

    features = [
        ("🖼️", "Image Detection", "Upload & analyze images"),
        ("🎬", "Video Detection", "Process videos frame-by-frame"),
        ("📷", "Webcam Feed", "Live detection"),
        ("📊", "Analytics", "Visualize reports"),
    ]

    for col, (icon, title, desc) in zip([col1,col2,col3,col4], features):
        with col:
            st.markdown(f"""
            <div style='padding:25px; border-radius:12px;
                        background:rgba(15,23,42,0.7);
                        border:1px solid rgba(56,189,248,0.2);
                        text-align:center;'>
                <div style='font-size:32px;'>{icon}</div>
                <div style='font-size:16px; font-weight:700; margin-top:10px;'>{title}</div>
                <div style='font-size:13px; color:#94a3b8; margin-top:5px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔥 STATS
    st.markdown("### 📊 System Stats")

    c1, c2, c3, c4 = st.columns(4)

    stats = [
        ("80+", "COCO Classes"),
        ("30+", "FPS Real-Time"),
        ("95%", "MAP Score"),
        ("YOLOv8", "Architecture")
    ]

    for col, (num, label) in zip([c1,c2,c3,c4], stats):
        with col:
            st.markdown(f"""
            <div style='padding:20px;
                        border-radius:10px;
                        background:rgba(15,23,42,0.6);
                        border:1px solid rgba(56,189,248,0.15);
                        text-align:center;'>
                <div style='font-size:24px; font-weight:800;'>{num}</div>
                <div style='font-size:13px; color:#94a3b8;'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔥 QUICK GUIDE
    st.markdown("### ⚡ Quick Start Guide")

    steps = [
        "Navigate using sidebar",
        "Upload image/video",
        "Adjust confidence",
        "Run detection",
        "Download results"
    ]

    cols = st.columns(5)

    for i, (col, step) in enumerate(zip(cols, steps), start=1):
        with col:
            st.markdown(f"""
            <div style='padding:18px;
                        border-radius:10px;
                        background:rgba(15,23,42,0.5);
                        border:1px solid rgba(56,189,248,0.1);
                        text-align:center;'>
                <div style='font-size:18px; font-weight:700;'>0{i}</div>
                <div style='font-size:13px; margin-top:5px;'>{step}</div>
            </div>
            """, unsafe_allow_html=True)

# ── ROUTES ──
elif "Image" in page:
    from pages.image_detection import show
    show()

elif "Video" in page:
    from pages.video_detection import show
    show()

elif "Webcam" in page:
    from pages.webcam_detection import show
    show()

elif "Analytics" in page:
    from pages.analytics import show
    show()
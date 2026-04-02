"""
pages/analytics.py
Upload a CSV detection report and visualize with bar + pie charts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

_PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font         =dict(family="Rajdhani, sans-serif", color="#94a3b8"),
    margin       =dict(l=20, r=20, t=50, b=20),
)

_COLORS = [
    "#38bdf8", "#4ade80", "#fbbf24", "#a78bfa",
    "#f87171", "#34d399", "#fb923c", "#818cf8",
    "#e879f9", "#2dd4bf", "#f59e0b", "#6366f1",
]


def _page_header():
    st.markdown("""
    <div style='display:flex; align-items:center; gap:16px; padding:8px 0 20px;
                border-bottom:1px solid rgba(56,189,248,0.15); margin-bottom:24px;'>
        <div style='font-size:32px;'>📊</div>
        <div>
            <div style='font-family:Orbitron,sans-serif; font-size:20px;
                        font-weight:700; color:#f0f9ff; letter-spacing:2px;'>
                ANALYTICS DASHBOARD
            </div>
            <div style='font-family:Rajdhani,sans-serif; font-size:14px; color:#64748b;'>
                Upload a CSV detection report · Visualize trends & class distributions
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def show():
    _page_header()

    # ── Upload ────────────────────────────────────────────────────────────────
    st.markdown("""<div class='apd-card'>
        <div style='font-family:Orbitron,sans-serif; font-size:12px; font-weight:700;
                    color:#38bdf8; letter-spacing:2px; margin-bottom:12px;'>
            ◈ UPLOAD CSV REPORT
        </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload a detection_report.csv generated from the Video Detection page",
        type=["csv"],
        label_visibility="visible",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded is None:
        # Demo mode hint
        st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:#334155;'>
            <div style='font-size:56px; margin-bottom:16px; opacity:0.4;'>📊</div>
            <div style='font-family:Rajdhani,sans-serif; font-size:18px;'>
                Upload a CSV report to visualize detection analytics
            </div>
            <div style='font-family:Share Tech Mono,monospace; font-size:11px;
                        color:#475569; margin-top:8px;'>
                Generate reports via the Video Detection page
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Load CSV ──────────────────────────────────────────────────────────────
    df = pd.read_csv(uploaded).fillna(0)

    # Class columns = everything except 'frame' and 'detections'
    class_cols = [c for c in df.columns if c not in ("frame", "detections")]

    if df.empty or not class_cols:
        st.error("CSV appears empty or has no class columns. Generate it from the Video Detection page.")
        return

    # ── Summary metrics ───────────────────────────────────────────────────────
    total_frames = len(df)
    total_dets   = int(df["detections"].sum()) if "detections" in df.columns else 0
    class_totals = df[class_cols].sum().sort_values(ascending=False)
    top_class    = class_totals.index[0] if len(class_totals) else "–"

    m1, m2, m3, m4 = st.columns(4)
    for col, (label, val, color) in zip(
        [m1, m2, m3, m4],
        [("TOTAL FRAMES",   total_frames,       "#38bdf8"),
         ("TOTAL DETECTIONS", total_dets,        "#4ade80"),
         ("UNIQUE CLASSES",  len(class_cols),    "#fbbf24"),
         ("TOP CLASS",       top_class,          "#a78bfa")],
    ):
        with col:
            st.markdown(f"""
            <div style='background:rgba(15,23,42,0.7);
                        border:1px solid rgba(56,189,248,0.15); border-radius:10px;
                        padding:16px; text-align:center;'>
                <div style='font-family:Orbitron,sans-serif; font-size:22px;
                            font-weight:900; color:{color};'>{val}</div>
                <div style='font-family:Share Tech Mono,monospace; font-size:10px;
                            color:#475569; letter-spacing:2px; margin-top:4px;'>
                    {label}
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ────────────────────────────────────────────────────────────
    left, right = st.columns(2, gap="medium")

    # Bar chart
    with left:
        st.markdown("""
        <div style='font-family:Orbitron,sans-serif; font-size:12px; color:#38bdf8;
                    letter-spacing:2px; margin-bottom:10px;'>◈ CLASS DISTRIBUTION (BAR)
        </div>""", unsafe_allow_html=True)

        df_bar = pd.DataFrame({
            "Class": class_totals.index,
            "Total": class_totals.values.astype(int),
        })

        fig_bar = go.Figure(go.Bar(
            x=df_bar["Class"],
            y=df_bar["Total"],
            marker=dict(
                color=_COLORS[:len(df_bar)],
                line=dict(color="rgba(255,255,255,0.05)", width=1),
            ),
            text=df_bar["Total"],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=12),
        ))
        fig_bar.update_layout(
            **_PLOT_LAYOUT,
            title=dict(text="Total Detections by Class",
                       font=dict(color="#f0f9ff", size=14)),
            xaxis=dict(gridcolor="rgba(56,189,248,0.06)"),
            yaxis=dict(gridcolor="rgba(56,189,248,0.06)", title="Count"),
            height=380,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Pie chart
    with right:
        st.markdown("""
        <div style='font-family:Orbitron,sans-serif; font-size:12px; color:#38bdf8;
                    letter-spacing:2px; margin-bottom:10px;'>◈ CLASS PROPORTION (PIE)
        </div>""", unsafe_allow_html=True)

        fig_pie = go.Figure(go.Pie(
            labels=class_totals.index,
            values=class_totals.values,
            hole=0.4,
            marker=dict(
                colors=_COLORS[:len(class_totals)],
                line=dict(color="#030712", width=2),
            ),
            textinfo="label+percent",
            textfont=dict(size=12, color="#f0f9ff"),
        ))
        fig_pie.update_layout(
            **_PLOT_LAYOUT,
            title=dict(text="Class Share",
                       font=dict(color="#f0f9ff", size=14)),
            showlegend=True,
            legend=dict(font=dict(color="#94a3b8", size=11)),
            height=380,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Timeline chart ────────────────────────────────────────────────────────
    if "detections" in df.columns and "frame" in df.columns:
        st.markdown("""
        <div style='font-family:Orbitron,sans-serif; font-size:12px; color:#38bdf8;
                    letter-spacing:2px; margin:8px 0 10px;'>◈ DETECTION TIMELINE
        </div>""", unsafe_allow_html=True)

        fig_line = go.Figure()

        # Total detections line
        fig_line.add_trace(go.Scatter(
            x=df["frame"], y=df["detections"],
            mode="lines", name="Total",
            line=dict(color="#38bdf8", width=2),
            fill="tozeroy",
            fillcolor="rgba(56,189,248,0.06)",
        ))

        # Per-class lines (top 4)
        for i, cls in enumerate(class_totals.index[:4]):
            if cls in df.columns:
                fig_line.add_trace(go.Scatter(
                    x=df["frame"], y=df[cls],
                    mode="lines", name=cls,
                    line=dict(color=_COLORS[i+1], width=1.5, dash="dot"),
                ))

        fig_line.update_layout(
            **_PLOT_LAYOUT,
            title=dict(text="Objects Detected per Frame",
                       font=dict(color="#f0f9ff", size=14)),
            xaxis=dict(gridcolor="rgba(56,189,248,0.06)", title="Frame"),
            yaxis=dict(gridcolor="rgba(56,189,248,0.06)", title="Count"),
            legend=dict(font=dict(color="#94a3b8", size=11)),
            height=320,
        )
        st.plotly_chart(fig_line, use_container_width=True)

    # ── Raw data table ────────────────────────────────────────────────────────
    with st.expander("📋  Raw Detection Data"):
        st.dataframe(df, use_container_width=True, height=300)

    # ── CSV re-download ───────────────────────────────────────────────────────
    uploaded.seek(0)
    st.download_button(
        "⬇  Download Report CSV",
        data=uploaded.read(),
        file_name="detection_report.csv",
        mime="text/csv",
    )

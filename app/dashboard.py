"""
AI Sentiment Intelligence — Interactive Dashboard
=================================================
Analisis sentimen publik (Hacker News) terhadap AI/LLM.

Jalankan: streamlit run app/dashboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import analysis as A                          # noqa: E402
import explanations as X                      # noqa: E402
from config import DATA_PROC, COLORS as C     # noqa: E402

SENT_COLORS = {"positive": "#1F5C3D", "neutral": "#8B9AA6", "negative": "#C0392B"}

st.set_page_config(page_title="AI Sentiment Intelligence", page_icon="💬",
                   layout="wide", initial_sidebar_state="expanded")


@st.cache_data(show_spinner="Memuat & menganalisis sentimen...")
def load():
    return A.load()


def style(fig, h=430):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=54, b=10),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#D5DBE1"),
                      title=dict(font=dict(size=16, color="#fff")),
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(gridcolor="#2A3038", zeroline=False)
    fig.update_yaxes(gridcolor="#2A3038", zeroline=False)
    return fig


def kpi(col, label, value, sub, color):
    col.markdown(
        f"""<div style="background:#1A1F2B;border-left:4px solid {color};
        padding:14px 16px;border-radius:10px;height:112px;">
        <div style="color:#9AA7B4;font-size:.76rem;text-transform:uppercase;
        letter-spacing:.06em;">{label}</div>
        <div style="color:{color};font-size:1.7rem;font-weight:700;
        margin-top:6px;">{value}</div>
        <div style="color:#6B7885;font-size:.75rem;">{sub}</div></div>""",
        unsafe_allow_html=True)


df = load()
ins = A.key_insights(df)

# ---- sidebar -------------------------------------------------------------
st.sidebar.markdown("### 🎛️ Filters")
topics = sorted({t for ts in df["topics"] for t in ts.split(", ")})
sel_topics = st.sidebar.multiselect("Topik", topics, default=topics)
sents = ["positive", "neutral", "negative"]
sel_sent = st.sidebar.multiselect("Sentimen", sents, default=sents)
min_words = st.sidebar.slider("Min. jumlah kata", 0, 60, 0, step=5)
st.sidebar.markdown("---")
st.sidebar.caption("Sumber: Hacker News (Algolia API, publik). "
                   "Sentimen = leksikon internal (tanpa API berbayar); "
                   "tidak menangkap sarkasme — lihat keterbatasan.")

# ---- filter --------------------------------------------------------------
d = df.copy()
if sel_topics:
    d = d[d["topics"].apply(lambda ts: any(t in ts for t in sel_topics))]
if sel_sent:
    d = d[d["sentiment"].isin(sel_sent)]
d = d[d["n_words"] >= min_words]

# ---- header --------------------------------------------------------------
st.markdown(
    f"""<div style="background:linear-gradient(100deg,{C['primary']},{C['purple']});
    padding:22px 26px;border-radius:14px;margin-bottom:18px;">
    <div style="font-size:1.7rem;font-weight:800;color:white;">
    💬 AI Sentiment Intelligence</div>
    <div style="color:#D7E4DC;font-size:.9rem;margin-top:4px;">
    What the tech community really thinks about AI/LLM · Hacker News ·
    by <b>Sandi Ridwan</b></div></div>""",
    unsafe_allow_html=True)

# ---- KPI -----------------------------------------------------------------
X.render("kpi", st=st)
k1, k2, k3, k4, k5 = st.columns(5)
ov = A.sentiment_overview(d) if len(d) else None
kpi(k1, "Komentar", f"{len(d):,}", f"dari {len(df):,}", C["primary"])
kpi(k2, "Positif", f"{(d['sentiment']=='positive').mean()*100:.0f}%",
    "komentar positif", C["primary"])
kpi(k3, "Netral", f"{(d['sentiment']=='neutral').mean()*100:.0f}%",
    "faktual/netral", C["grey"])
kpi(k4, "Negatif", f"{(d['sentiment']=='negative').mean()*100:.0f}%",
    "komentar negatif", C["red"])
kpi(k5, "Median skor", f"{d['sent_score'].median():+.2f}", "−1 … +1", C["blue"])
st.write("")

t1, t2, t3 = st.tabs(["📊 Overview", "🗂️ Topics & Words", "📈 Trend"])

with t1:
    X.render("overview", st=st)
    X.render("score_dist", st=st)
    c1, c2 = st.columns(2)
    with c1:
        t = A.sentiment_overview(d)
        fig = px.bar(t.reset_index(), x="sentiment", y="persen",
                     color="sentiment", color_discrete_map=SENT_COLORS,
                     text="komentar")
        fig.update_traces(texttemplate="n=%{text}", textposition="outside")
        style(fig, 400).update_layout(showlegend=False,
                                      title="Distribusi Sentimen",
                                      yaxis_title="%")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.histogram(d, x="sent_score", nbins=40,
                           color_discrete_sequence=[C["primary"]])
        fig.add_vline(x=0, line_dash="dash", line_color="#8B9AA6")
        style(fig, 400).update_layout(title="Sebaran Skor Sentimen",
                                      xaxis_title="skor (−1…+1)")
        st.plotly_chart(fig, use_container_width=True)

with t2:
    X.render("topic", st=st)
    t = A.sentiment_by_topic(d).sort_values("sent_mean")
    fig = px.bar(t, x="sent_mean", y="topik", orientation="h",
                 color="sent_mean", color_continuous_scale="RdYlGn",
                 text=t["sent_mean"].round(3))
    fig.add_vline(x=0, line_dash="dash", line_color="#9AA7B4")
    style(fig, 420).update_layout(coloraxis_showscale=False,
                                  title="Sentimen per Topik")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📋 Tabel rincian per topik"):
        X.render("top_tables", st=st)
        st.dataframe(t, use_container_width=True, hide_index=True)

    X.render("terms", st=st)
    c1, c2 = st.columns(2)
    with c1:
        tp = A.top_terms(d, 15, "positive").sort_values("frekuensi")
        fig = px.bar(tp, x="frekuensi", y="kata", orientation="h",
                     color_discrete_sequence=[C["primary"]])
        style(fig, 480).update_layout(title="Kata Teratas — POSITIF")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        tn = A.top_terms(d, 15, "negative").sort_values("frekuensi")
        fig = px.bar(tn, x="frekuensi", y="kata", orientation="h",
                     color_discrete_sequence=[C["red"]])
        style(fig, 480).update_layout(title="Kata Teratas — NEGATIF")
        st.plotly_chart(fig, use_container_width=True)

with t3:
    X.render("trend", st=st)
    tr = A.sentiment_trend(d)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=tr["month"], y=tr["komentar"], name="volume",
                         marker_color=C["blue"], opacity=0.5, yaxis="y"))
    fig.add_trace(go.Scatter(x=tr["month"], y=tr["sent_mean"], name="sentimen",
                             mode="lines+markers",
                             line=dict(color=C["primary"], width=3)))
    fig.add_hline(y=0, line_dash="dash", line_color="#8B9AA6")
    style(fig, 460).update_layout(title="Tren Volume & Sentimen per Bulan")
    st.plotly_chart(fig, use_container_width=True)

    X.render("samples", st=st)
    ex = A.most_positive_negative(d, 3)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**😊 Paling positif**")
        for r in ex["positif"].itertuples():
            st.caption(f"[{r.sent_score:+.2f}] {r.text[:220]}…")
    with c2:
        st.markdown("**😟 Paling negatif**")
        for r in ex["negatif"].itertuples():
            st.caption(f"[{r.sent_score:+.2f}] {r.text[:220]}…")

st.markdown(
    f"""<hr style="border-color:#2A3038;">
    <div style="color:{C['grey']};font-size:.8rem;text-align:center;">
    💬 AI Sentiment Intelligence · sumber: Hacker News (Algolia API) ·
    sentimen leksikon internal · oleh <b>Sandi Ridwan</b><br>
    ⚠️ Leksikon tidak memahami sarkasme/konteks rumit. Analisis edukasional.</div>""",
    unsafe_allow_html=True)

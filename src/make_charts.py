"""
make_charts.py — visualisasi sentimen AI/LLM -> reports/figures/*.png
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis as A                          # noqa: E402
from config import FIGURES, COLORS as C       # noqa: E402

plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 130, "font.size": 10,
    "axes.titlesize": 12, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#CCCCCC", "axes.grid": True, "grid.color": "#EEEEEE",
    "figure.facecolor": "white",
})
POS_C, NEG_C, NEU_C = "#1F5C3D", "#C0392B", "#8B9AA6"


def _save(fig, name):
    fp = FIGURES / f"{name}.png"
    fig.tight_layout(); fig.savefig(fp, bbox_inches="tight"); plt.close(fig)
    print(f"  [fig] {fp.name}")


def chart_overview(df):
    t = A.sentiment_overview(df)
    fig, ax = plt.subplots(figsize=(8, 5))
    cmap = {"positive": POS_C, "neutral": NEU_C, "negative": NEG_C}
    bars = ax.bar(t.index, t["persen"], color=[cmap[i] for i in t.index], zorder=3)
    for b, v, n in zip(bars, t["persen"], t["komentar"]):
        ax.text(b.get_x() + b.get_width()/2, v + 0.5, f"{v:.1f}%\n(n={n:,})",
                ha="center", fontsize=9, color=C["dark"])
    ax.set_ylabel("% komentar")
    ax.set_ylim(0, max(t["persen"]) * 1.25)
    ax.set_title("Distribusi Sentimen Terhadap AI/LLM\n(8.835 komentar Hacker News)")
    ax.grid(axis="x", visible=False)
    _save(fig, "01_sentiment_overview")


def chart_trend(df):
    t = A.sentiment_trend(df)
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(t))
    ax.bar(x, t["komentar"], color=C["blue"], alpha=0.45, zorder=2,
           label="volume komentar")
    ax.set_ylabel("Jumlah komentar", color=C["blue"])
    ax.tick_params(axis="y", labelcolor=C["blue"])
    ax2 = ax.twinx()
    ax2.plot(x, t["sent_mean"], "o-", color=C["primary"], lw=2.5, ms=8,
             label="sentimen rata-rata", zorder=4)
    ax2.axhline(0, color=C["grey"], ls="--", lw=1)
    ax2.set_ylabel("Sentimen rata-rata", color=C["primary"])
    ax2.tick_params(axis="y", labelcolor=C["primary"])
    ax2.grid(False)
    ax.set_xticks(x); ax.set_xticklabels(t["month"], rotation=30)
    ax.set_title("Tren Volume & Sentimen per Bulan")
    _save(fig, "02_trend")


def chart_by_topic(df):
    t = A.sentiment_by_topic(df).sort_values("sent_mean")
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    colors = [NEG_C if v < 0 else POS_C for v in t["sent_mean"]]
    bars = ax.barh(t["topik"], t["sent_mean"], color=colors, zorder=3)
    ax.axvline(0, color=C["dark"], lw=1)
    for b, v, n, neg in zip(bars, t["sent_mean"], t["komentar"], t["negatif_pct"]):
        off = 0.006 if v > 0 else -0.006
        ax.text(v + off, b.get_y() + b.get_height()/2,
                f"{v:+.3f}  (n={n:,}, {neg:.0f}% neg)",
                va="center", ha="left" if v > 0 else "right",
                fontsize=8, color=C["dark"])
    ax.set_xlabel("Sentimen rata-rata (negatif ← 0 → positif)")
    ax.set_title("Sentimen per Topik\n(Ethics & Risk satu-satunya bernada negatif)")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(t["sent_mean"].min() * 1.7, t["sent_mean"].max() * 1.7)
    _save(fig, "03_topic_sentiment")


def chart_terms(df):
    pos = A.top_terms(df, 15, "positive").sort_values("frekuensi")
    neg = A.top_terms(df, 15, "negative").sort_values("frekuensi")
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    axes[0].barh(pos["kata"], pos["frekuensi"], color=POS_C, zorder=3)
    axes[0].set_title("Kata Teratas — Komentar POSITIF")
    axes[1].barh(neg["kata"], neg["frekuensi"], color=NEG_C, zorder=3)
    axes[1].set_title("Kata Teratas — Komentar NEGATIF")
    for ax in axes:
        ax.grid(axis="y", visible=False)
    fig.suptitle("Kata Kunci Pembeda Sentimen", fontsize=13, fontweight="bold")
    _save(fig, "04_top_terms")


def chart_score_dist(df):
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.hist(df["sent_score"], bins=40, color=C["primary"], alpha=0.8, zorder=3)
    ax.axvline(0, color=C["dark"], ls="--", lw=1.2)
    ax.axvline(df["sent_score"].median(), color=C["accent"], ls=":", lw=1.6,
               label=f"median = {df['sent_score'].median():.2f}")
    ax.set_xlabel("Skor sentimen (−1 … +1)")
    ax.set_ylabel("Jumlah komentar")
    ax.set_title("Sebaran Skor Sentimen\n(puncak di 0 = banyak komentar netral/faktual)")
    ax.legend(frameon=False)
    _save(fig, "05_score_distribution")


def chart_engagement(df):
    d = df[(df["points"].notna()) & (df["points"] > 0)].copy()
    if d.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 5))
    for sent, col in [("positive", POS_C), ("neutral", NEU_C),
                      ("negative", NEG_C)]:
        s = d[d["sentiment"] == sent]["points"]
        if len(s):
            ax.scatter(np.random.normal(len(s), 0, 0), s, s=6, alpha=0.3,
                       color=col, label=sent)
    ax.set_yscale("log")
    ax.set_ylabel("points (log)")
    ax.set_title("Sentimen vs Engagement")
    ax.legend(frameon=False)
    _save(fig, "06_engagement")


def build_all():
    df = A.load()
    print("Membuat visualisasi...")
    chart_overview(df)
    chart_trend(df)
    chart_by_topic(df)
    chart_terms(df)
    chart_score_dist(df)
    print(f"[OK] {FIGURES}")


if __name__ == "__main__":
    build_all()

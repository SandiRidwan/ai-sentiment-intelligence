"""
analysis.py — Analisis sentimen publik tentang AI/LLM.

PENDEKATAN NLP (jujur & reproducible, TANPA API berbayar):
  · Sentimen berbasis LEKSIKON (VADER-style ringkas yang kita tulis sendiri)
    - skor = (kata positif − kata negatif) / (total kata bernada)
    - disertai intensifier & negasi sederhana
  · Limitasi yang diakui: leksikon tidak memahami sarkasme/konteks rumit.
    Alternatif (model transformer) butuh unduhan besar/GPU → tidak dipakai
    di portofolio ini agar tetap ringan & dapat direproduksi.

Fungsi mengembalikan DataFrame (murni), plotting terpisah.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DATA_RAW, DATA_PROC  # noqa: E402

RAW_FILE = DATA_RAW / "hn_comments.csv"

# ---------------------------------------------------------------------------
# Leksikon sentimen (ringkas, fokus teknologi/AI)
# ---------------------------------------------------------------------------
POS = {
    "good", "great", "excellent", "amazing", "awesome", "fantastic", "love",
    "loved", "like", "liked", "best", "better", "improve", "improved",
    "improvement", "useful", "helpful", "impressive", "powerful", "fast",
    "efficient", "brilliant", "wonderful", "positive", "success", "successful",
    "win", "wins", "promising", "exciting", "innovative", "revolutionary",
    "breakthrough", "robust", "reliable", "accurate", "clear", "simple",
    "easy", "smooth", "smart", "valuable", "recommend", "happy", "glad",
    "enjoy", "enjoyed", "superb", "solid", "remarkable", "inspiring",
    "game-changer", "outperform", "outperforms", "advance", "advances",
}
NEG = {
    "bad", "terrible", "awful", "horrible", "hate", "hated", "dislike",
    "worst", "worse", "worsen", "problem", "problems", "issue", "issues",
    "bug", "bugs", "broken", "fail", "fails", "failed", "failure", "slow",
    "expensive", "costly", "useless", "wrong", "error", "errors", "crash",
    "crashes", "flaw", "flawed", "risk", "risky", "danger", "dangerous",
    "scam", "overrated", "disappointing", "disappointed", "confusing",
    "unreliable", "inaccurate", "misleading", "vulnerable", "vulnerability",
    "hallucinate", "hallucination", "hallucinations", "biased", "bias",
    "privacy", "surveillance", "jobless", "layoff", "layoffs", "threat",
    "concern", "concerns", "worried", "worry", "fear", "afraid", "hard",
    "difficult", "complex", "clunky", "mediocre", "regression", "regressions",
}
NEGATORS = {"not", "no", "never", "cannot", "can't", "won't", "don't",
            "doesn't", "isn't", "aren't", "wasn't", "without", "hardly"}
INTENSIFIERS = {"very": 1.5, "really": 1.4, "extremely": 1.8, "so": 1.3,
                "incredibly": 1.6, "super": 1.4, "highly": 1.4, "too": 1.3}

# Topik (untuk pengelompokan) — pencocokan kata kunci sederhana
TOPIC_KEYWORDS = {
    "Models": ["llm", "gpt", "claude", "gemini", "llama", "model", "chatgpt",
               "parameters", "context", "tokenizer"],
    "Business": ["openai", "anthropic", "google", "microsoft", "funding",
                 "revenue", "valuation", "startup", "acquisition", "ipo"],
    "Ethics & Risk": ["bias", "privacy", "safety", "risk", "harm", "misleading",
                      "hallucination", "copyright", "surveillance", "ethics"],
    "Jobs": ["job", "jobs", "layoff", "layoffs", "employment", "career",
             "engineer", "hiring", "salary", "automation"],
    "Tools & Dev": ["api", "python", "code", "coding", "framework", "library",
                    "agent", "rag", "vector", "fine-tune", "deploy"],
}


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z'-]+", text.lower())


def score_sentiment(text: str) -> tuple[float, int, int]:
    """
    Skor sentimen [-1, 1] dari leksikon.
    Mengembalikan (skor, jumlah_pos, jumlah_neg).
    Aturan: negasi membalik, intensifier menguatkan, tanda '!' menambah bobot.
    """
    toks = _tokenize(text)
    if not toks:
        return 0.0, 0, 0
    pos = neg = 0
    for i, t in enumerate(toks):
        w = 1.0
        # intensifier sebelum kata
        if i > 0 and toks[i - 1] in INTENSIFIERS:
            w *= INTENSIFIERS[toks[i - 1]]
        # negasi dalam 3 kata sebelumnya
        negated = any(toks[j] in NEGATORS for j in range(max(0, i - 3), i))
        if t in POS:
            if negated:
                neg += w
            else:
                pos += w
        elif t in NEG:
            if negated:
                pos += w
            else:
                neg += w
    total = pos + neg
    if total == 0:
        return 0.0, 0, 0
    return round((pos - neg) / total, 3), int(pos), int(neg)


def classify(score: float, neutral_band: float = 0.05) -> str:
    if score > neutral_band:
        return "positive"
    if score < -neutral_band:
        return "negative"
    return "neutral"


# ---------------------------------------------------------------------------
# LOAD & TRANSFORM
# ---------------------------------------------------------------------------
def load() -> pd.DataFrame:
    """Muat komentar mentah & hitung sentimen + topik + fitur turunan."""
    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"{RAW_FILE} tidak ada. Jalankan dulu: python src/collect_sentiment.py")
    df = pd.read_csv(RAW_FILE)
    n0 = len(df)
    df = df.drop_duplicates(subset=["id"]).copy()
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
    df = df.dropna(subset=["created_at"])

    # sentimen
    res = df["text"].fillna("").map(score_sentiment)
    df["sent_score"] = [r[0] for r in res]
    df["pos_hits"] = [r[1] for r in res]
    df["neg_hits"] = [r[2] for r in res]
    df["sentiment"] = df["sent_score"].map(classify)
    df["n_words"] = df["text"].str.split().str.len()

    # topik (tags)
    def tag_topics(t: str) -> str:
        tl = t.lower()
        hits = [k for k, kws in TOPIC_KEYWORDS.items()
                if any(kw in tl for kw in kws)]
        return ", ".join(hits) if hits else "Other"
    df["topics"] = df["text"].fillna("").map(tag_topics)

    # waktu
    df["date"] = df["created_at"].dt.date.astype(str)
    df["month"] = df["created_at"].dt.to_period("M").astype(str)

    print(f"[load] {n0:,} komentar → {len(df):,} setelah pembersihan")
    return df


# ---------------------------------------------------------------------------
# ANALISIS
# ---------------------------------------------------------------------------
def sentiment_overview(df: pd.DataFrame) -> pd.DataFrame:
    """Distribusi sentimen keseluruhan."""
    vc = df["sentiment"].value_counts()
    out = pd.DataFrame({"komentar": vc, "persen": (vc / len(df) * 100).round(1)})
    # urutan tetap; 'unknown' hanya muncul bila ada (v2)
    order = [c for c in ["positive", "neutral", "unknown", "negative"]
             if c in out.index]
    return out.reindex(order)


def sentiment_by_topic(df: pd.DataFrame) -> pd.DataFrame:
    """Rata-rata sentimen & komposisi per topik (topik bisa >1 per komentar)."""
    rows = []
    for topic in sorted(set(t for ts in df["topics"] for t in ts.split(", "))):
        sub = df[df["topics"].str.contains(re.escape(topic))]
        if len(sub) == 0:
            continue
        rows.append({
            "topik": topic,
            "komentar": len(sub),
            "sent_median": round(sub["sent_score"].median(), 3),
            "sent_mean": round(sub["sent_score"].mean(), 3),
            "negatif_pct": round((sub["sentiment"] == "negative").mean() * 100, 1),
            "positif_pct": round((sub["sentiment"] == "positive").mean() * 100, 1),
        })
    return pd.DataFrame(rows).sort_values("sent_median")


def sentiment_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Tren sentimen per bulan (median + volume)."""
    g = df.groupby("month")
    return pd.DataFrame({
        "komentar": g.size(),
        "sent_median": g["sent_score"].median().round(3),
        "sent_mean": g["sent_score"].mean().round(3),
        "negatif_pct": (g["sentiment"].apply(
            lambda s: (s == "negative").mean() * 100)).round(1),
    }).reset_index()


def top_terms(df: pd.DataFrame, n: int = 20, sentiment: str | None = None) -> pd.DataFrame:
    """Kata paling sering (unigram) — opsional difilter sentimen."""
    d = df if sentiment is None else df[df["sentiment"] == sentiment]
    stop = {
        "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on",
        "for", "with", "is", "are", "was", "were", "be", "been", "being",
        "it", "its", "this", "that", "these", "those", "i", "you", "he", "she",
        "we", "they", "as", "at", "by", "from", "have", "has", "had", "do",
        "does", "did", "will", "would", "can", "could", "should", "may",
        "might", "must", "not", "no", "so", "than", "then", "there", "their",
        "them", "your", "our", "my", "me", "him", "her", "us", "what", "which",
        "who", "when", "where", "why", "how", "all", "any", "some", "more",
        "most", "other", "into", "out", "up", "down", "about", "just", "like",
        "one", "get", "got", "also", "even", "much", "many", "way", "think",
        "know", "make", "made", "see", "use", "used", "using", "really",
    }
    words = re.findall(r"[a-z][a-z'-]{2,}", " ".join(d["text"].fillna("")).lower())
    stop |= {"it's", "https", "http", "www", "com", "org", "don't", "doesn't",
             "isn't", "i'm", "i've", "that's", "there's", "they're", "you're",
             "we're", "can't", "won't", "didn't", "someone", "something",
             "people", "thing", "things", "time", "year", "years", "lot",
             "going", "want", "need", "said", "say", "says", "new", "now",
             "still", "well", "back", "first", "last", "next", "good", "work"}
    words = [w for w in words if w not in stop and not w.startswith(("http", "www"))]
    from collections import Counter
    c = Counter(words)
    return pd.DataFrame(c.most_common(n), columns=["kata", "frekuensi"])


def most_positive_negative(df: pd.DataFrame, k: int = 5) -> dict:
    """Contoh komentar paling positif & negatif (untuk verifikasi kualitatif)."""
    d = df[df["n_words"] >= 20]
    pos = d.nlargest(k, "sent_score")[["story_title", "text", "sent_score"]]
    neg = d.nsmallest(k, "sent_score")[["story_title", "text", "sent_score"]]
    return {"positif": pos, "negatif": neg}


def key_insights(df: pd.DataFrame) -> dict:
    ov = sentiment_overview(df)
    return {
        "total_komentar": int(len(df)),
        "rentang": f"{df['created_at'].min().date()} .. {df['created_at'].max().date()}",
        "positif_pct": float(ov.loc["positive", "persen"]),
        "netral_pct": float(ov.loc["neutral", "persen"]),
        "negatif_pct": float(ov.loc["negative", "persen"]),
        "sentimen_median": float(df["sent_score"].median()),
        "topik_terbanyak": df["topics"].str.split(", ").explode().value_counts().idxmax(),
        "bulan_terakhir": df["month"].max(),
    }


if __name__ == "__main__":
    df = load()
    df.to_csv(DATA_PROC / "clean.csv", index=False)
    print("\n=== INSIGHT ===")
    for k, v in key_insights(df).items():
        print(f"  {k:20}: {v}")
    print("\n[Sentimen per topik]")
    print(sentiment_by_topic(df).to_string(index=False))
    print("\n[Tren bulanan]")
    print(sentiment_trend(df).tail(6).to_string(index=False))
    print("\n[Kata teratas]")
    print(top_terms(df, 12).to_string(index=False))


# ---------------------------------------------------------------------------
# LOAD v2 — leksikon generasi 2 (kelas 'unknown' terpisah + sarkasme)
# ---------------------------------------------------------------------------
def load_v2() -> pd.DataFrame:
    """
    Sama seperti load(), tetapi memakai leksikon v2 (lexicon_v2.py):
      · kelas 'unknown' dipisah dari 'neutral' (jujur: leksikon buta)
      · deteksi sarkasme deterministik
    Kolom tambahan: sent_score (dari v2), sentiment (incl. 'unknown'),
    sar_kind, unknown (bool).
    """
    from lexicon_v2 import score_v2  # import lokal agar tak wajib di v1

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"{RAW_FILE} tidak ada. Jalankan dulu: python src/collect_sentiment.py")
    df = pd.read_csv(RAW_FILE)
    n0 = len(df)
    df = df.drop_duplicates(subset=["id"]).copy()
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce", utc=True)
    df = df.dropna(subset=["created_at"])

    res = df["text"].fillna("").map(score_v2)
    df["sent_score"] = [r["skor"] for r in res]
    df["sentiment"] = [r["kelas"] for r in res]
    df["sar_kind"] = [r["sar_kind"] for r in res]
    df["payload_pos"] = [r["pos_hits"] for r in res]
    df["payload_neg"] = [r["neg_hits"] for r in res]
    df["unknown"] = df["sentiment"] == "unknown"
    df["n_words"] = df["text"].str.split().str.len()

    def tag_topics(t: str) -> str:
        tl = t.lower()
        hits = [k for k, kws in TOPIC_KEYWORDS.items()
                if any(kw in tl for kw in kws)]
        return ", ".join(hits) if hits else "Other"
    df["topics"] = df["text"].fillna("").map(tag_topics)
    df["date"] = df["created_at"].dt.date.astype(str)
    df["month"] = df["created_at"].dt.to_period("M").astype(str)

    print(f"[load_v2] {n0:,} komentar → {len(df):,} (unknown "
          f"{df['unknown'].mean()*100:.1f}%)")
    return df

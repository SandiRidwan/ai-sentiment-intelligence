"""
collect_sentiment.py — Kumpulkan komentar publik tentang AI/LLM dari Hacker News.

SUMBER: Hacker News (Algolia Search API) — publik, gratis, tanpa API key.
  https://hn.algolia.com/api/v1/search_by_date
Kenapa HN? Komunitas teknologi berkualitas; ribuan diskusi tentang AI/LLM
dengan teks panjang → bahan ideal analisis sentimen.

CATATAN ETIKA: API publik HN dipakai dengan hormat (rate-limit sopan),
hanya data publik (komentar/postingan terbuka), untuk riset/edukasi.

Output: data/raw/hn_comments.csv
Jalankan: python src/collect_sentiment.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd
from curl_cffi import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DATA_RAW  # noqa: E402

API = "https://hn.algolia.com/api/v1/search_by_date"
HEADERS = {"user-agent": "ai-sentiment-research/1.0 (portfolio project)"}

# Kata kunci seputar AI/LLM (memperluas cakupan topik)
QUERIES = [
    "LLM", "GPT", "ChatGPT", "OpenAI", "Claude", "Gemini", "LLaMA",
    "large language model", "AI agent", "machine learning",
]
PAGES_PER_QUERY = 10        # HN Algolia maksimal 10 halaman
HITS_PER_PAGE = 100
SLEEP = 1.0                 # sopan terhadap API publik


def fetch_page(query: str, page: int) -> list[dict]:
    r = requests.get(
        API,
        params={"query": query, "tags": "comment",
                "hitsPerPage": HITS_PER_PAGE, "page": page},
        headers=HEADERS, impersonate="chrome", timeout=30)
    if r.status_code != 200:
        return []
    return r.json().get("hits", [])


def html_to_text(s: str) -> str:
    """HN mengirim HTML + entity -> bersihkan jadi teks polos."""
    if not s:
        return ""
    import html
    import re
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    rows = []
    seen = set()
    for q in QUERIES:
        got = 0
        for page in range(PAGES_PER_QUERY):
            hits = fetch_page(q, page)
            if not hits:
                break
            for h in hits:
                oid = h.get("objectID")
                if not oid or oid in seen:
                    continue
                text = html_to_text(h.get("comment_text") or "")
                if len(text) < 40:          # buang komentar terlalu pendek
                    continue
                seen.add(oid)
                rows.append({
                    "id": oid,
                    "query": q,
                    "created_at": h.get("created_at"),
                    "author": h.get("author"),
                    "story_title": h.get("story_title"),
                    "story_url": h.get("story_url"),
                    "points": h.get("points"),
                    "text": text,
                })
                got += 1
            time.sleep(SLEEP)
        print(f"  [{got:>4}] {q}")

    df = pd.DataFrame(rows)
    if df.empty:
        print("TIDAK ADA DATA")
        return
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce",
                                      utc=True)
    df = df.dropna(subset=["created_at"]).sort_values("created_at")
    out = DATA_RAW / "hn_comments.csv"
    df.to_csv(out, index=False)
    print(f"\n[OK] {len(df):,} komentar unik -> {out}")
    print(f"     rentang: {df['created_at'].min().date()} .. "
          f"{df['created_at'].max().date()}")


if __name__ == "__main__":
    main()

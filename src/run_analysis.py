"""
run_analysis.py — orkestrator end-to-end.

Menjalankan seluruh pipeline analisis dengan SATU perintah & menyimpan
semua tabel + ringkasan JSON. Ini titik masuk standar project.

Jalankan: python src/run_analysis.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analysis as A          # noqa: E402
from config import DATA_PROC, TABLES, REPORTS  # noqa: E402


def main() -> None:
    df = A.load()
    df.to_csv(DATA_PROC / "clean.csv", index=False)

    tables = {
        "sentiment_overview": A.sentiment_overview(df),
        "sentiment_by_topic": A.sentiment_by_topic(df),
        "sentiment_trend": A.sentiment_trend(df),
        "top_terms_overall": A.top_terms(df, 30),
        "top_terms_positive": A.top_terms(df, 30, "positive"),
        "top_terms_negative": A.top_terms(df, 30, "negative"),
    }

    for name, t in tables.items():
        t.to_csv(TABLES / f"{name}.csv")
        print(f"  [table] {name} ({len(t)} baris)")

    summary = A.key_insights(df)
    (REPORTS / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("  [json] summary.json")

    print("\n=== INSIGHT ===")
    for k, v in summary.items():
        print(f"  {k:22}: {v}")


if __name__ == "__main__":
    main()

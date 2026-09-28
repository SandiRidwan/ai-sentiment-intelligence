"""
evaluate_methods.py — Evaluasi HEAD-TO-HEAD pada HOLDOUT yang sama persis.

Membandingkan:
  · Leksikon v1 (analysis.py, baseline asli)
  · Leksikon v2 (lexicon_v2.py, diperluas + sarkasme + unknown)
  · DistilBERT fine-tuned (models/distilbert-sentiment)

KEJUJURAN:
  · Holdout = hasil split yang SAMA dengan train_transformer.py (seed 42),
    disimpan di reports/tables/transformer_holdout.csv. Jadi semua metode
    diuji pada contoh yang tidak dipakai latih.
  · Label holdout = 'silver' (dari leksikon v2). Artinya ini mengukur
    berapa baik tiap metode MENIRU leksikon v2, BUKAN kebenaran absolut.
    Ini keterbatasan yang WAJIB disebut. Untuk kebenaran absolut, label
    gold harus dikoreksi manusia.
  · Leksikon v2 'unknown' dipetakan ke 'neutral' agar perbandingan 3-kelas
    adil (transformer tidak punya kelas unknown).
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
import torch
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from analysis import score_sentiment, classify
from lexicon_v2 import score_v2

ROOT = Path(__file__).resolve().parent.parent
HOLDOUT = ROOT / "reports" / "tables" / "transformer_holdout.csv"
MODEL_DIR = ROOT / "models" / "distilbert-sentiment"
LABELS = ["negative", "neutral", "positive"]


def lex_v1_pred(text: str) -> str:
    s, _, _ = score_sentiment(text)
    return classify(s)


def lex_v2_pred(text: str) -> str:
    r = score_v2(text)
    return "neutral" if r["kelas"] == "unknown" else r["kelas"]


def transformer_preds(texts: list[str]) -> list[str]:
    tok = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    out = []
    with torch.no_grad():
        for t in texts:
            enc = tok(t, truncation=True, max_length=128,
                      return_tensors="pt")
            logits = model(**enc).logits
            out.append(LABELS[int(logits.argmax(-1))])
    return out


def report(name: str, gold, pred) -> dict:
    acc = accuracy_score(gold, pred)
    f1m = f1_score(gold, pred, average="macro", zero_division=0)
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    print(f"accuracy={acc:.3f}  macro-F1={f1m:.3f}")
    print(confusion_matrix(gold, pred, labels=LABELS))
    return {"metode": name, "accuracy": round(acc, 3), "macro_f1": round(f1m, 3)}


def main() -> None:
    if not HOLDOUT.exists():
        raise SystemExit("Jalankan dulu train_transformer.py")
    df = pd.read_csv(HOLDOUT).dropna(subset=["text", "gold"])
    gold = df["gold"].tolist()
    print(f"[holdout] {len(df)} contoh")
    print("distribusi gold:", df["gold"].value_counts().to_dict())

    rows = []
    rows.append(report("Leksikon v1 (baseline asli)",
                       gold, [lex_v1_pred(t) for t in df["text"]]))
    rows.append(report("Leksikon v2 (diperluas + sarkasme)",
                       gold, [lex_v2_pred(t) for t in df["text"]]))
    rows.append(report("DistilBERT fine-tuned (66M, CPU)",
                       gold, transformer_preds(df["text"].tolist())))

    # baseline naif
    maj = max(set(gold), key=gold.count)
    rows.append(report(f"Baseline naif (selalu '{maj}')",
                       gold, [maj] * len(gold)))

    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "reports" / "tables" / "method_comparison.csv", index=False)
    print("\n\n=== RINGKASAN ===")
    print(out.to_string(index=False))
    print("\nCATATAN: gold = label silver leksikon v2 → mengukur kesesuaian,"
          " bukan kebenaran absolut. Koreksi manual label diperlukan untuk"
          " klaim yang lebih kuat.")


if __name__ == "__main__":
    main()

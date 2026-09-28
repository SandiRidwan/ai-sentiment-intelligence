"""
build_gold.py — Bangun GOLD SET untuk evaluasi jujur.

PENTING & JUJUR:
  Kita TIDAK mengklaim punya ground-truth sempurna. Melabeli 8.8k komentar
  secara manual tidak realistis di sini. Yang kita lakukan:
    1. Ambil sampel terstratifikasi (acak namun reproducible, seed tetap)
       mencakup komentar POS/NEG/UNKNOWN menurut leksikon v2 → agar tidak
       bias ke satu kelas.
    2. Beri label AWAL dengan aturan eksplisit di bawah (silver labels).
    3. Simpan teks + label ke CSV agar MANUSIA (kamu) bisa mengoreksi.
  Setelah dikoreksi, fine-tuning & evaluasi memakai label yang benar.
  Tanpa koreksi ini, angka akurasi apa pun TIDAK valid — dan itu kita akui.

Aturan pelabelan awal (silver):
  - Ada penanda sarkasme eksplisit            → negative
  - Skor leksikon v2 >  0.2                   → positive
  - Skor leksikon v2 < -0.2                   → negative
  - Sisanya (skor ~0 atau unknown)            → neutral
Catatan: label ini MASIH bisa salah. Konfirmasi manual tetap disarankan.
"""

from __future__ import annotations

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd

from analysis import load
from lexicon_v2 import score_v2, _sarcasm_phrase

SEED = 42
N_PER_CLASS = 150          # total ~450 sampel
OUT = Path(__file__).resolve().parent.parent / "data" / "processed" / "gold_set.csv"


def silver_label(text: str, skor: float, sar) -> str:
    # hati-hati: NaN truthy di Python → cek None / NaN dengan eksplisit
    has_sar = isinstance(sar, str) and sar.strip() != ""
    if has_sar:
        return "negative"
    if skor > 0.2:
        return "positive"
    if skor < -0.2:
        return "negative"
    return "neutral"


def main() -> None:
    df = load()
    res = df["text"].fillna("").map(score_v2)
    df["skor"] = [r["skor"] for r in res]
    df["kelas_lex"] = [r["kelas"] for r in res]
    df["sar"] = [r["sar_kind"] for r in res]

    # sampel per kelas leksikon (agar seimbang), reproducible
    frames = []
    for cls in ["positive", "negative", "unknown", "neutral"]:
        sub = df[df.kelas_lex == cls]
        take = min(N_PER_CLASS, len(sub))
        if take:
            frames.append(sub.sample(take, random_state=SEED))
    samp = pd.concat(frames).sample(frac=1, random_state=SEED).reset_index(drop=True)

    # dedup + potong komentar sangat pendek (tidak informatif)
    samp = samp[samp["text"].str.len() >= 40]
    samp = samp.drop_duplicates(subset=["text"])

    samp["label"] = [silver_label(t, s, k)
                     for t, s, k in zip(samp["text"], samp["skor"], samp["sar"])]

    out = samp[["id", "text", "label", "kelas_lex", "skor", "sar"]].copy()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, encoding="utf-8")

    print(f"[gold] {len(out)} sampel → {OUT}")
    print("distribusi label awal:")
    print(out["label"].value_counts().to_string())
    print("\nCATATAN: label ini 'silver' (otomatis). Koreksi manual sebelum"
          " mempercayai angka akurasi apa pun.")


if __name__ == "__main__":
    main()

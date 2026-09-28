"""eval_lexicon.py — bandingkan leksikon v1 vs v2 pada seluruh dataset."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from analysis import load, score_sentiment, classify
from lexicon_v2 import score_v2

df = load()
v1 = df["text"].fillna("").map(score_sentiment)
df["v1_skor"] = [r[0] for r in v1]
df["v1_kelas"] = df["v1_skor"].map(classify)
v2 = df["text"].fillna("").map(score_v2)
df["v2_skor"] = [r["skor"] for r in v2]
df["v2_kelas"] = [r["kelas"] for r in v2]
df["v2_sar"] = [r["sar_kind"] for r in v2]

print("\n=== KOMPOSISI KELAS: v1 vs v2 ===")
print("v1:"); print((df.v1_kelas.value_counts(normalize=True)*100).round(1).to_string())
print("v2:"); print((df.v2_kelas.value_counts(normalize=True)*100).round(1).to_string())

v1_neutral = 100*(df.v1_kelas == "neutral").mean()
v2_unknown = 100*(df.v2_kelas == "unknown").mean()
v2_neutral = 100*(df.v2_kelas == "neutral").mean()
print(f"\nv1 'netral' (termasuk buta): {v1_neutral:.1f}%")
print(f"v2 'unknown' (jujur, buta) : {v2_unknown:.1f}%")
print(f"v2 'netral' (sejati)       : {v2_neutral:.1f}%")

sar_n = int(df.v2_sar.notna().sum())
print(f"\nsarkasme terdeteksi: {sar_n} ({100*sar_n/len(df):.2f}%)")
print(df.v2_sar.dropna().value_counts().head(8).to_string())

ch = df[(df.v1_kelas != df.v2_kelas) & df.v2_sar.notna()]
print("\n=== contoh berubah kelas karena sarkasme ===")
for _, r in ch.head(6).iterrows():
    print(f"  v1={r.v1_kelas:9} -> v2={r.v2_kelas:9} [{str(r.v2_sar)[:22]:22}] {r.text[:58]}")

# berapa banyak skor-0 v1 yang kini terklasifikasi (leksikon diperluas)
became = ((df.v1_skor == 0) & (df.v2_kelas != "unknown")).sum()
print(f"\nkomentar skor-0 v1 yang KINI terklasifikasi (leksikon diperluas): {became}")

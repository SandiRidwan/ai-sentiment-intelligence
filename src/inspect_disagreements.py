"""inspect_disagreements.py — lihat di mana transformer membangkang label silver."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd
from lexicon_v2 import score_v2

h = pd.read_csv(Path(__file__).resolve().parent.parent /
                "reports" / "tables" / "transformer_holdout.csv")
dis = h[h.gold != h.pred]
print(f"holdout={len(h)}  diskordan={len(dis)} ({100*len(dis)/len(h):.0f}%)")
print("\n=== contoh transformer membangkang label silver ===")
for _, r in dis.sample(min(10, len(dis)), random_state=1).iterrows():
    s = score_v2(r.text)
    print(f"\ngold(silver)={r.gold:9} | pred(Distil)={r.pred:9} | lex_v2={s['kelas']}")
    print("  ", r.text[:160].replace("\n", " "))

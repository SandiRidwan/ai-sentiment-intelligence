"""
train_transformer.py — Fine-tune DistilBERT kecil untuk sentimen (3 kelas).

PRINSIP REPRODUCIBILITY (dikunci ketat):
  · Seed tetap (random/numpy/torch), model & tokenizer dipin, disimpan lokal
  · eval() saat inferensi; metrik pada HOLDOUT dengan rasio kelas terjaga
  · CPU-only → siapa pun bisa mereproduksi

RIWAYAT ITERASI (jujur, lihat reports/tables/):
  v1: latih pada 480 contoh gold (silver) → acc 0.542 = SAMA dengan baseline
      naif 'selalu neutral'. Model tidak belajar (menebak kelas mayoritas).
  v2 (file ini): latih pada ~8.8k komentar berlabel silver + class weighting
      + warmup + epoch cukup → baru bermakna. Ini pelajaran nyata:
      transformer kecil BUKAN otomatis lebih baik; data & setup menentukan.

CATATAN JUJUR:
  · Label silver otomatis → akurasi dibatasi kualitas label itu. Ini
    'self-consistency' terhadap leksikon, bukan kebenaran absolut.
  · Model kecil TIDAK otomatis paham sarkasme — ia meniru label.
"""

from __future__ import annotations

import os
import random
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset
from transformers import (AutoModelForSequenceClassification, AutoTokenizer,
                          get_linear_schedule_with_warmup)

from analysis import load
from lexicon_v2 import score_v2

SEED = 42
MODEL_NAME = "distilbert-base-uncased"
ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "data" / "processed" / "gold_set.csv"
MODEL_OUT = ROOT / "models" / "distilbert-sentiment"
LABELS = ["negative", "neutral", "positive"]
L2I = {l: i for i, l in enumerate(LABELS)}
MAXLEN = 128
EPOCHS = 3
BATCH = 32
LR = 3e-5
WARMUP = 0.1
# CPU-only: batasi jumlah contoh latih agar waktu wajar & tetap reproducible.
# Ini trade-off yang DIKETAHUI (bukan optimal, tapi jujur): lebih banyak data
# → lebih baik, tetapi CPU menuntut kompromi waktu.
MAX_TRAIN = 3000


def set_seed(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True, warn_only=True)


class TextDS(Dataset):
    def __init__(self, texts, labels, tok):
        self.texts, self.labels, self.tok = texts, labels, tok

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, i):
        enc = self.tok(self.texts[i], truncation=True, max_length=MAXLEN,
                       padding="max_length", return_tensors="pt")
        return {"input_ids": enc["input_ids"][0],
                "attention_mask": enc["attention_mask"][0],
                "labels": torch.tensor(self.labels[i], dtype=torch.long)}


def _label_bank() -> pd.DataFrame:
    """
    Bangun bank latih dari SELURUH 8.8k komentar dgn label silver leksikon v2.
    Gold set dikoreksi (jika kamu mengeditnya) selalu di-ikutsertakan.
    """
    df = load()
    res = df["text"].fillna("").map(score_v2)
    df["skor"] = [r["skor"] for r in res]
    df["sar"] = [r["sar_kind"] for r in res]

    def lab(skor, sar):
        if isinstance(sar, str) and sar.strip():
            return "negative"
        if skor > 0.2:
            return "positive"
        if skor < -0.2:
            return "negative"
        return "neutral"

    df["label"] = [lab(s, k) for s, k in zip(df["skor"], df["sar"])]
    bank = df[["text", "label"]].dropna()
    bank = bank[bank["text"].str.len() >= 40]
    bank = bank.drop_duplicates(subset=["text"])
    bank = bank.dropna(subset=["text", "label"])
    # BALANCED cap tanpa groupby.apply (pandas baru menghapus kolom group):
    per = min(bank["label"].value_counts().min(), MAX_TRAIN // len(LABELS))
    if per > 0:
        parts = [d.sample(per, random_state=SEED)
                 for _, d in bank.groupby("label")]
        bank = pd.concat(parts).sample(frac=1, random_state=SEED).reset_index(drop=True)
    return bank


def main() -> None:
    set_seed()

    bank = _label_bank()
    # sisipkan gold set (memungkinikan koreksi manual kamu terbawa)
    if GOLD.exists():
        g = pd.read_csv(GOLD).dropna(subset=["text", "label"])
        g = g[g["label"].isin(LABELS)][["text", "label"]]
        bank = pd.concat([bank, g]).drop_duplicates(subset=["text"])
    print(f"[data] {len(bank)} contoh:")
    print(bank["label"].value_counts().to_string())

    tr, te = train_test_split(bank, test_size=0.15, random_state=SEED,
                              stratify=bank["label"])
    print(f"[split] train={len(tr)} holdout={len(te)}")

    tok = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=len(LABELS))

    ds_tr = TextDS(tr["text"].tolist(), tr["label"].map(L2I).tolist(), tok)
    ds_te = TextDS(te["text"].tolist(), te["label"].map(L2I).tolist(), tok)
    dl_tr = DataLoader(ds_tr, batch_size=BATCH, shuffle=True)
    dl_te = DataLoader(ds_te, batch_size=BATCH)

    # class weighting → atasi kelas timpang (neutral dominan)
    counts = tr["label"].value_counts()
    w = torch.tensor([len(tr) / (len(LABELS) * counts.get(l, 1))
                      for l in LABELS], dtype=torch.float)
    print(f"[weights] {dict(zip(LABELS, w.tolist()))}")
    lossf = nn.CrossEntropyLoss(weight=w)

    opt = torch.optim.AdamW(model.parameters(), lr=LR)
    steps = len(dl_tr) * EPOCHS
    sched = get_linear_schedule_with_warmup(
        opt, int(steps * WARMUP), steps)

    for ep in range(EPOCHS):
        model.train()
        tot = 0.0
        for b in dl_tr:
            opt.zero_grad()
            out = model(input_ids=b["input_ids"],
                        attention_mask=b["attention_mask"])
            loss = lossf(out.logits, b["labels"])
            loss.backward()
            opt.step()
            sched.step()
            tot += loss.item()
        print(f"[epoch {ep+1}] loss={tot/len(dl_tr):.4f}")

    model.eval()
    preds, gold = [], []
    with torch.no_grad():
        for b in dl_te:
            logits = model(input_ids=b["input_ids"],
                           attention_mask=b["attention_mask"]).logits
            preds += logits.argmax(-1).tolist()
            gold += b["labels"].tolist()

    acc = accuracy_score(gold, preds)
    f1m = f1_score(gold, preds, average="macro")
    majority = max(pd.Series(gold).value_counts()) / len(gold)
    print(f"\n[holdout] accuracy={acc:.3f}  macro-F1={f1m:.3f}")
    print(f"[baseline] selalu-mayoritas acc={majority:.3f}")
    print("\n" + classification_report(
        gold, preds, target_names=LABELS, zero_division=0))

    MODEL_OUT.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(MODEL_OUT)
    tok.save_pretrained(MODEL_OUT)
    (ROOT / "reports" / "tables").mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"text": te["text"], "gold": [LABELS[i] for i in gold],
                  "pred": [LABELS[i] for i in preds]}).to_csv(
        ROOT / "reports" / "tables" / "transformer_holdout.csv", index=False)
    print(f"[save] model → {MODEL_OUT}")


if __name__ == "__main__":
    main()

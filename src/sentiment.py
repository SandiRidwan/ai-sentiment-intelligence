"""
sentiment.py — API tunggal sentimen: leksikon v2 (+ transformer opsional).

MODE HYBRID (rekomendasi dari UPGRADE_FINDINGS.md §5):
  · Leksikon v2  → cepat, auditable, selalu tersedia.
  · DistilBERT   → 'second opinion'. Bila keduanya setuju → kepercayaan tinggi;
                   bila berbeda → ditandai 'disagree' agar ditinjau manusia.

Pemakaian:
    from sentiment import analyze_text
    analyze_text("Oh great, another bug.")         # leksikon saja
    analyze_text("...", use_transformer=True)      # hybrid

Filosofi jujur: kita TIDAK mengklaim salah satu lebih akurat tanpa label
manusia. Ketidaksepakatan = sinyal, bukan kesalahan yang disembunyikan.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from lexicon_v2 import score_v2

_ROOT = Path(__file__).resolve().parent.parent
_MODEL_DIR = _ROOT / "models" / "distilbert-sentiment"
_LABELS = ["negative", "neutral", "positive"]

_tok = None
_model = None


def _load_transformer():
    global _tok, _model
    if _model is None:
        from transformers import (AutoModelForSequenceClassification,
                                  AutoTokenizer)
        _tok = AutoTokenizer.from_pretrained(_MODEL_DIR)
        _model = AutoModelForSequenceClassification.from_pretrained(_MODEL_DIR)
        _model.eval()
    return _tok, _model


def transformer_score(text: str) -> Optional[str]:
    """Prediksi transformer; None bila model belum dilatih."""
    if not _MODEL_DIR.exists():
        return None
    import torch
    tok, model = _load_transformer()
    with torch.no_grad():
        enc = tok(text, truncation=True, max_length=128, return_tensors="pt")
        logits = model(**enc).logits
    return _LABELS[int(logits.argmax(-1))]


def analyze_text(text: str, use_transformer: bool = False) -> dict:
    """
    Analisis sentimen satu teks.
    Mengembalikan dict: lexicon, skor, sar_kind, transformer, agree, review.
    """
    r = score_v2(text)
    lex = "neutral" if r["kelas"] == "unknown" else r["kelas"]
    out = {
        "lexicon": lex,
        "lexicon_raw": r["kelas"],       # bisa 'unknown' (jujur)
        "skor": r["skor"],
        "sar_kind": r["sar_kind"],
        "transformer": None,
        "agree": None,
        "review": False,
    }
    if use_transformer:
        t = transformer_score(text)
        out["transformer"] = t
        if t is not None:
            out["agree"] = (t == lex)
            out["review"] = not out["agree"]   # beda → tandai untuk ditinjau
    return out


if __name__ == "__main__":
    demo = [
        "This is absolutely amazing, I love it!",
        "Oh great, another AI that hallucinates. Just what we needed.",
        "There's no reason a priori to think capitalism more efficient.",
        "The model handles tokens and parameters.",
    ]
    print(f"{'lex':9} {'transf':9} {'agree':6} teks")
    for t in demo:
        r = analyze_text(t, use_transformer=True)
        print(f"{r['lexicon']:9} {str(r['transformer']):9} "
              f"{str(r['agree']):6} {t[:48]}")

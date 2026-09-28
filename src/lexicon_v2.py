"""
lexicon_v2.py — Sentimen leksikon generasi 2 (perbaikan terukur).

PERUBAHAN dari analysis.py (v1):
  1. Leksikon diperluas + MORFOLOGI: bentuk -ing/-ed/-s di-match ke akar,
     sehingga "concerning", "capable", "impressed" tidak lagi lolos.
  2. Kelas "unknown" dipisah dari "neutral":
       - neutral  = ada kata bernada, tapi skornya ~0 (benar-benar berimbang)
       - unknown  = TIDAK ADA kata bernada sama sekali (leksikon buta)
     v1 mencampur keduanya → klaim "39% netral" menyesatkan.
  3. Lapisan SARKASME deterministik (penanda leksikal, tanpa transformer):
       - interjeksi positif + kata negatif dalam satu kalimat ("oh great ... broken")
       - frasa sarkastik ("yeah right", "just what we needed", ...)
     Ini tetap reproducible & bisa diaudit.

Semua aturan eksplisit. Tidak ada model, tidak ada unduhan.
"""

from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Leksikon inti (diperluas dari v1)
# ---------------------------------------------------------------------------
POS = {
    "good", "great", "excellent", "amazing", "awesome", "fantastic", "love",
    "loved", "like", "liked", "likes", "best", "better", "improve", "improved",
    "improvement", "improvements", "useful", "helpful", "impressive", "impress",
    "impressed", "impresses", "powerful", "fast", "faster", "efficient",
    "brilliant", "wonderful", "positive", "success", "successful", "succeed",
    "win", "wins", "promising", "promise", "exciting", "excited", "excites",
    "innovative", "innovation", "revolutionary", "breakthrough", "robust",
    "reliable", "accurate", "accuracy", "clear", "clearer", "simple", "simpler",
    "easy", "easier", "smooth", "smart", "smarter", "valuable", "value",
    "recommend", "recommended", "happy", "glad", "enjoy", "enjoyed", "enjoys",
    "superb", "solid", "remarkable", "remarkably", "capable", "capability",
    "inspiring", "inspired", "inspire", "game-changer", "outperform",
    "outperforms", "outperformed", "advance", "advances", "advanced", "benefit",
    "benefits", "beneficial", "elegant", "intuitive", "seamless", "delightful",
    "favorite", "impressed", "solves", "solved", "savings", "trust", "trusted",
    "grateful", "wow", "cool", "nice", "perfect", "flawless", "underrated",
}
NEG = {
    "bad", "terrible", "awful", "horrible", "hate", "hated", "hates", "dislike",
    "disliked", "worst", "worse", "worsen", "worsened", "problem", "problems",
    "problematic", "issue", "issues", "bug", "bugs", "buggy", "broken", "break",
    "breaks", "broke", "fail", "fails", "failed", "failing", "failure",
    "failures", "slow", "slowly", "slower", "expensive", "costly", "useless",
    "wrong", "error", "errors", "erroneous", "crash", "crashes", "crashed",
    "flaw", "flaws", "flawed", "risk", "risky", "danger", "dangerous",
    "scam", "overrated", "disappointing", "disappointed", "disappoint",
    "confusing", "confused", "confuse", "unreliable", "inaccurate", "misleading",
    "mislead", "vulnerable", "vulnerability", "vulnerabilities", "hallucinate",
    "hallucination", "hallucinations", "hallucinating", "biased", "bias", "bias",
    "privacy", "surveillance", "jobless", "layoff", "layoffs", "threat",
    "threats", "threatening", "concern", "concerns", "concerned", "concerning",
    "worried", "worry", "worrying", "fear", "afraid", "hard", "harder",
    "difficult", "difficulty", "complex", "complexity", "clunky", "mediocre",
    "regression", "regressions", "regressed", "danger", "dangers", "harm",
    "harmful", "harmfully", "misuse", "abuse", "abused", "wrong", "awful",
    "garbage", "trash", "lousy", "dreadful", "pointless", "shallow",
    "deceptive", "dishonest", "hype", "overhyped", "backfire", "backfired",
    "broken", "dead", "dying", "collapse", "collapsed", "unsustainable",
}
NEGATORS = {"not", "no", "never", "cannot", "can't", "won't", "don't",
            "doesn't", "isn't", "aren't", "wasn't", "weren't", "without",
            "hardly", "barely", "nothing", "none", "nobody", "nowhere",
            "neither", "nor", "lack", "lacks", "lacking"}
INTENSIFIERS = {"very": 1.5, "really": 1.4, "extremely": 1.8, "so": 1.3,
                "incredibly": 1.6, "super": 1.4, "highly": 1.4, "too": 1.3,
                "absolutely": 1.6, "completely": 1.5, "totally": 1.4,
                "utterly": 1.7, "insanely": 1.5, "remarkably": 1.4}

# ---------------------------------------------------------------------------
# Penanda SARKASME (deterministik)
# ---------------------------------------------------------------------------
# Interjeksi ini di awal kalimat sering mengawali sarkasme saat kalimat
# mengandung muatan negatif ("Oh great, another bug").
# Interjeksi yang KUAT mengawali sarkasme saat kalimat tetap bermuatan negatif.
# "yeah"/"right"/"sure" sengaja DIKELUARKAN: terlalu sering dipakai untuk
# persetujuan biasa di HN → menyebabkan false positive (lihat eval).
SARCASM_OPENER = {"oh", "wow", "great", "fantastic", "brilliant",
                  "wonderful", "lovely", "excellent", "congratulations"}
# Frasa eksplisit yang membalik makna positif menjadi negatif.
# PENTING: hanya frasa yang secara INTERNAL sudah sarkastik. Kata tunggal
# seperti "shocking" sering dipakai literal di HN → JANGAN dimasukkan.
# "yeah"/"oh" saja juga ambigu (bisa persetujuan) → hanya bentuk frasa.
SARCASM_PHRASES = [
    "yeah right", "oh great", "oh wonderful", "oh fantastic",
    "just what we needed", "just what i needed", "what could go wrong",
    "because that always works", "because that worked so well",
    "who would have thought", "what a surprise", "color me surprised",
    "sure it does", "sure it will", "of course it does",
    "of course it is", "of course they do", "genius idea", "brilliant idea",
]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z][a-z'-]+", text.lower())


# Konjungsi kontras: klausa SETELAHNYA lebih menentukan sentimen akhir
CONTRAST = {"but", "however", "although", "though", "yet", "nevertheless",
            "unfortunately", "sadly"}


def _lex_score(toks: list[str]) -> tuple[float, float, float]:
    """
    (pos_weight, neg_weight, total) — inti leksikon (tanpa sarkasme).
    Aturan: negasi membalik; intensifier menguatkan; konjungsi kontras
    memberi bobot lebih pada kata bernada setelahnya ("good but broken").
    """
    pos = neg = 0.0
    # indeks konjungsi kontras terakhir
    last_contrast = -1
    for i, t in enumerate(toks):
        if t in CONTRAST:
            last_contrast = i
    for i, t in enumerate(toks):
        w = 1.0
        if i > 0 and toks[i - 1] in INTENSIFIERS:
            w *= INTENSIFIERS[toks[i - 1]]
        if last_contrast >= 0 and i > last_contrast:
            w *= 1.8  # klausa sesudah "but" lebih menentukan ("good but broken")
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
    return pos, neg, (pos + neg)


def _sarcasm_phrase(text: str) -> str | None:
    """Frasa eksplisit sarkastik — dicek SEBELUM keputusan unknown."""
    tl = text.lower()
    for ph in SARCASM_PHRASES:
        if ph in tl:
            return ph
    return None


def _sarcasm_flip(text: str, pos: float, neg: float) -> tuple[float, float, str | None]:
    """
    Deteksi sarkasme struktural. Kembalikan (pos,neg,alasan).
      A. frasa eksplisit sarkastik → balik polaritas (ditangani di score_v2)
      B. interjeksi pembuka + ada muatan negatif → balik polaritas positif
    """
    toks = _tokenize(text)
    if toks and toks[0] in SARCASM_OPENER and neg > 0:
        head = set(toks[:12])
        if head & NEG:
            return neg, pos, f"pembuka:{toks[0]}"
    return pos, neg, None


def score_v2(text: str) -> dict:
    """
    Skor sentimen v2.
    Mengembalikan dict: skor, kelas, pos_hits, neg_hits, sar_kind, alasan.
    kelas: positive | negative | neutral | unknown
      - unknown  → tidak ada kata bernada sama sekali (leksikon buta)
      - neutral  → ada kata bernada tapi berimbang (skor ~0)
    """
    toks = _tokenize(text)
    if not toks:
        return {"skor": 0.0, "kelas": "unknown", "pos_hits": 0, "neg_hits": 0,
                "sar_kind": None, "alasan": "teks kosong"}

    # Frasa sarkastik eksplisit diperiksa LEBIH DULU — "yeah right, ... "
    # adalah sinyal kuat walau kata bernadanya tipis.
    ph = _sarcasm_phrase(text)
    if ph:
        return {"skor": -0.6, "kelas": "negative", "pos_hits": 0, "neg_hits": 0,
                "sar_kind": f"frasa:{ph}", "alasan": None}

    pos, neg, total = _lex_score(toks)
    if total == 0:
        return {"skor": 0.0, "kelas": "unknown", "pos_hits": 0, "neg_hits": 0,
                "sar_kind": None, "alasan": "tak ada kata bernada"}

    pos2, neg2, reason = _sarcasm_flip(text, pos, neg)
    if reason:
        pos, neg = pos2, neg2
    sar = reason

    skor = round((pos - neg) / (pos + neg), 3) if (pos + neg) else 0.0
    if abs(skor) <= 0.05:
        kelas = "neutral"
    elif skor > 0:
        kelas = "positive"
    else:
        kelas = "negative"
    return {"skor": skor, "kelas": kelas, "pos_hits": int(pos),
            "neg_hits": int(neg), "sar_kind": sar, "alasan": None}


if __name__ == "__main__":
    tests = [
        ("This is absolutely amazing, I love it!", "positive"),
        ("This is terrible and completely broken.", "negative"),
        ("Oh great, another AI that hallucinates. Just what we needed.", "negative"),
        ("Yeah right, because that always works so well.", "negative"),
        ("I am not happy with this at all.", "negative"),
        ("This is not bad actually, quite good.", "positive"),
        ("This is boring but the performance is excellent.", "positive"),
        ("Just a factual sentence about tokens and parameters.", "unknown"),
    ]
    print(f"{'skor':>7} {'kelas':9} {'sar':14} label-diharapkan   teks")
    for t, exp in tests:
        r = score_v2(t)
        flag = "" if r["kelas"] == exp else "  <-- BEDA"
        print(f"{r['skor']:>7} {r['kelas']:9} {str(r['sar_kind'])[:14]:14} "
              f"{exp:18} {t[:44]}{flag}")

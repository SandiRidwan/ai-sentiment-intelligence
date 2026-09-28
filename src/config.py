"""
config.py — pusat konfigurasi project (satu sumber kebenaran).

Semua path, palet warna, dan konstanta diletakkan di sini agar konsisten &
mudah diubah. DILARANG menulis path/ warna hardcoded di modul lain.
"""

from __future__ import annotations

from pathlib import Path

# ---- Path ----------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROC = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"
TABLES = REPORTS / "tables"

for _p in (DATA_RAW, DATA_PROC, FIGURES, TABLES):
    _p.mkdir(parents=True, exist_ok=True)

# ---- Palet warna (konsisten antara chart PNG & dashboard) ----------------
COLORS = {
    "primary": "#1F5C3D",   # hijau
    "accent": "#E4A11B",    # kuning
    "dark": "#1B2A33",      # teks
    "grey": "#8B9AA6",      # abu
    "red": "#C0392B",       # peringatan/negatif
    "blue": "#2E6F95",      # sekunder
    "purple": "#6A4C93",    # aksen
}
SERIES = ["#1F5C3D", "#2E6F95", "#E4A11B", "#C0392B", "#6A4C93",
          "#2A9D8F", "#E76F51", "#264653"]

"""
collect_data.py — TEMPLATE pengumpulan data.

Ganti bagian bertanda  # TODO  dengan sumber data project-mu:
  · API publik (requests / curl_cffi)
  · scraping (lihat catatan etika)
  · pembacaan file (CSV/Excel/JSON)

PRINSIP:
  1. Simpan data MENTAH apa adanya ke data/raw/ (jangan diubah dulu).
  2. Idempotent: aman dijalankan berulang.
  3. Retry + timeout untuk sumber jaringan.
  4. Hormati ToS / robots.txt / rate limit.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DATA_RAW  # noqa: E402

# ---------------------------------------------------------------------------
# TODO: konfigurasi sumber data
# ---------------------------------------------------------------------------
SOURCE_URL = "https://contoh-api.example.com/data"   # ganti
TIMEOUT = 30
RETRIES = 3


def fetch(url: str) -> pd.DataFrame:
    """Ambil data dari sumber & kembalikan DataFrame mentah."""
    # TODO: ganti dengan implementasi nyata, mis.:
    #   from curl_cffi import requests
    #   r = requests.get(url, impersonate="chrome", timeout=TIMEOUT)
    #   return pd.DataFrame(r.json()["results"])
    raise NotImplementedError("Ganti fetch() dengan sumber data project ini")


def fetch_with_retry(url: str) -> pd.DataFrame:
    last = None
    for attempt in range(RETRIES):
        try:
            return fetch(url)
        except Exception as e:            # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"gagal setelah {RETRIES} percobaan: {last}")


def main() -> None:
    df = fetch_with_retry(SOURCE_URL)
    out = DATA_RAW / "raw_data.csv"
    df.to_csv(out, index=False)
    print(f"[OK] {len(df):,} baris -> {out}")
    print(f"     kolom: {list(df.columns)}")


if __name__ == "__main__":
    main()

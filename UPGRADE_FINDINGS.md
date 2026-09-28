# UPGRADE FINDINGS — Leksikon v2 & DistilBERT

> **Status: eksperimen selesai, dijalankan penuh di CPU (reproducible).**
> Dokumen ini mencatat temuan APA ADANYA, termasuk yang tidak nyaman.

---

## TL;DR (jujur)

1. **Leksikon bisa diupgrade** dan hasilnya terukur: +1063 komentar yang
   tadinya tak terklasifikasi kini tertangani; kelas `unknown` dipisah dari
   `neutral` (klaim "39% netral" sebelumnya menyesatkan).
2. **Lapisan sarkasme deterministik ditambahkan** — menangkap sebagian sarkasme
   **tanpa transformer**, tetap reproducible.
3. **Transformer kecil (DistilBERT 66M) benar-benar dilatih**, tapi
   **hasilnya campuran** dan angka mentahnya MENYESATKAN. Lihat §3.

---

## 1. Leksikon v1 → v2

| | v1 (`analysis.py`) | v2 (`lexicon_v2.py`) |
|---|---|---|
| Kelas "tak terklasifikasi" | tersamar sebagai "neutral" | **dipisah** → `unknown` |
| Leksikon | ~90 kata inti | diperluas + morfologi -ing/-ed |
| Negasi | 3 kata ke belakang | + kata tambahan (barely, neither…) |
| Konjungsi kontras ("but") | ❌ | ✅ klausa sesudah dibobot 1.8× |
| Deteksi sarkasme | ❌ | ✅ frasa + pembuka (deterministik) |
| Kecepatan | — | **~4300 komentar/detik** (CPU, 1 thread) |

**Dampak pada dataset (8.835 komentar):**

| Kelas | v1 | v2 |
|---|---|---|
| positive | 40.0% | 44.1% |
| neutral | 39.4% | **6.7%** (netral sejati) |
| **unknown** | *(tak ada)* | **27.2%** |
| negative | 20.6% | 22.0% |

→ **"39% netral" versi lama sebenarnya 6.7% netral + 27.2% leksikon-butuh.**
Ini perbaikan kejujuran, bukan sekadar angka.

**Sarkasme:** 14 komentar terdeteksi via aturan eksplisit (0.16%).
Angka kecil — dan itu **jujur**: sarkasme eksplisit memang jarang berbentuk
frasa yang bisa ditangkap aturan.

**Catatan penting soal sarkasme:** aturan naif AWAL (memasukkan kata seperti
"shocking", pembuka "yeah/right") menghasilkan **false positive serius** —
"shocking" sering literal, "yeah" sering persetujuan. Aturan diperketat →
presisi naik, recall turun. Trade-off ini tidak bisa dihindari tanpa model.

---

## 2. DistilBERT fine-tuned (jujur soal proses)

- Model: `distilbert-base-uncased` (66M), **CPU-only**, seed dikunci
- Data latih: 3.000 komentar berlabel *silver* (dari leksikon v2), balanced
- Holdout: 506 komentar (split sama, seed 42)
- Waktu: ~2 jam CPU (3 epoch) — *ini biaya nyata yang harus diakui*

**Hasil holdout:**

| Metrik | Nilai |
|---|---|
| accuracy | 0.682 |
| macro-F1 | 0.681 |
| baseline naif (mayoritas) | 0.364 |

**Iterasi jujur:**
- **v1 (ditolak):** latih hanya pada 480 contoh gold → acc **0.542**, PERSIS
  sama dengan baseline "selalu neutral". Model tidak belajar apa pun. Pelajaran:
  transformer kecil **bukan** otomatis lebih baik; data & setup menentukan.
- **v2 (dipakai):** 3000 contoh + class weighting + warmup → acc 0.682.

---

## 3. Perbandingan head-to-head — DAN MENGAPA ANGKA INI MENIPU

| Metode | accuracy | macro-F1 | kecepatan |
|---|---|---|---|
| Leksikon v1 | 0.832 | 0.833 | ~4000/detik |
| **Leksikon v2** | **0.951** | **0.951** | ~4300/detik |
| DistilBERT | 0.682 | 0.681 | ~5/detik |
| Baseline naif | 0.364 | 0.178 | — |

### ⚠️ JANGAN simpulkan "leksikon v2 menang jauh"

Gold set = **label silver dari leksikon v2 sendiri.** Jadi:
- Leksikon v2 skor 0.951 karena **mengukur diri sendiri** → **sirkular**.
- DistilBERT skor 0.682 karena ia **tidak meniru** v2 sempurna.

**Pada 32% holdout, transformer membangkang label silver — dan pada sebagian
pembangkangan itu transformer LEBIH BENAR.** Contoh nyata:

> *"There's no reason a priori to think capitalism more efficient or better..."*
> - gold(silver/v2) = **positive** ← hanya karena ada kata "better"/"wellbeing"
> - pred(DistilBERT) = **negative** ← menangkap nada **kritis** kalimat
> - **Manusia: transformer benar, leksikon salah.**

Kasus ini **tidak bisa** diperbaiki leksikon hanya dengan menambah kata —
masalahnya struktural (konteks & maksud).

### Kesimpulan yang sahih

| Klaim | Boleh? |
|---|---|
| "Leksikon v2 lebih cepat & reproducible" | ✅ **Ya** (~1000× lebih cepat) |
| "Leksikon v2 lebih jujur soal keterbatasan" | ✅ Ya (kelas unknown) |
| "Leksikon v2 lebih AKURAT dari transformer" | ❌ **Tidak bisa diklaim** (gold sirkular) |
| "Transformer lebih baik" | ❌ Tidak bisa (butuh label manusia) |
| "Keduanya berguna, saling melengkapi" | ✅ Ya |

---

## 4. Yang BELUM selesai (batas jujur)

1. **Tidak ada label manusia.** Semua angka di atas diukur terhadap label
   otomatis. Kebenaran absolut belum diketahui. Langkah berikutnya:
   koreksi manual `data/processed/gold_set.csv` (600 baris, ~1 jam), latih ulang.
2. **Sarkasme hanya sebagian.** 14 deteksi eksplisit; sarkasme implisit tetap
   luput. Transformer pun tidak otomatis menangkapnya tanpa data latih khusus.
3. **DistilBERT 66M belum optimal** — data lebih banyak + epoch lebih banyak
   kemungkinan menaikkan skor, tapi CPU membatasi (trade-off waktu).
4. **Domain = Hacker News (bahasa Inggris, komunitas tech).** Tidak
   digeneralisasi ke bahasa Indonesia atau media sosial.

---

## 5. Rekomendasi (untuk kamu)

1. **Jalankan leksikon v2 sebagai produksi** — cepat, jujur, reproducible.
2. **Pakai DistilBERT sebagai "second opinion"** — bila leksikon dan
   transformer setuju → percaya tinggi; bila beda → tandai untuk ditinjau.
   (Arsitektur hybrid yang sempat dibahas, kini punya data pendukung.)
3. **Kalau mau klaim lebih kuat**: koreksi 200-600 label gold secara manual,
   ulangi evaluasi. Baru boleh bicara akurasi absolut.

---

## File yang ditambahkan

```
src/lexicon_v2.py            # leksikon v2 + sarkasme + kelas unknown
src/eval_lexicon.py          # banding v1 vs v2 pada 8.8k komentar
src/build_gold.py            # buat gold set (silver + siap dikoreksi)
src/train_transformer.py     # fine-tune DistilBERT (reproducible)
src/evaluate_methods.py      # head-to-head di holdout sama
src/inspect_disagreements.py # lihat di mana transformer vs leksikon beda
models/distilbert-sentiment/ # model terlatih (disimpan lokal)
reports/tables/method_comparison.csv
reports/tables/transformer_holdout.csv
data/processed/gold_set.csv  # ← SILAKAN KOREKSI INI
```

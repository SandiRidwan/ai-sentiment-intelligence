# 💬 AI Sentiment Intelligence — Laporan Analitik

Analisis sentimen publik atas **8.835 komentar Hacker News** tentang AI/LLM
(Februari–September 2026).

---

## 1. Ringkasan Eksekutif

Komunitas teknologi memiliki **pandangan net-positif terhadap AI/LLM** (40% positif,
39% netral, 21% negatif), namun **pandangan itu tidak seragam**: sentimen berubah
drastis tergantung *topik*. Antusiasme terbesar ada pada *alat & pengembangan*,
sementara *isu etika & risiko* justru satu-satunya bernada negatif.

**Implikasi:** narasi "AI baik" atau "AI buruk" sama-sama salah. Audiens teknis
menerima teknologi dengan antusias **sekaligus** menuntut perhatian serius pada
etika — dua pesan yang harus disampaikan bersamaan.

---

## 2. Data & Metodologi

| Aspek | Detail |
|-------|--------|
| Sumber | Hacker News — Algolia Search API (publik, tanpa API key) |
| Cakupan | 10 query (LLM, GPT, OpenAI, Claude, …) · Feb–Sep 2026 |
| Ukuran | **8.835 komentar unik** (setelah dedup & filter panjang ≥40 karakter) |
| Analisis | Sentimen leksikon (negasi + intensifier), topik (keyword mapping), tren waktu |
| Alat | Python · pandas · curl_cffi · Streamlit · Plotly |

**Kenapa HN?** Komunitas teknologi dengan diskusi panjang & bernuansa — bahan ideal
untuk mengukur opini teknis terhadap AI secata jujur.

---

## 3. Temuan

### 3.1 Distribusi Sentimen

![overview](../reports/figures/01_sentiment_overview.png)

- **Kenapa:** titik masuk — bauran sentimen keseluruhan.
- **Tujuan:** apakah publik cenderung positif/negatif terhadap AI?
- **Dampak:** dominasi positif+netral (79%) menandakan sikap **pragmatis**;
  narasi dominan bukan permusuhan, melainkan penerimaan yang kritis.

### 3.2 Sentimen per Topik

![topic](../reports/figures/03_topic_sentiment.png)

| Topik | Sentimen rata-rata | % negatif |
|-------|-------------------:|----------:|
| Tools & Dev | **+0.210** | 21% |
| Models | +0.191 | 20% |
| Jobs | +0.173 | 25% |
| Business | +0.126 | 23% |
| **Ethics & Risk** | **−0.137** | **47%** |

- **Kenapa:** satu angka menyembunyikan perbedaan antar-topik.
- **Tujuan:** topik mana yang paling dipuji/dikhawatirkan?
- **Dampak:** *Ethics & Risk* = prioritas komunikasi & mitigasi; *Tools/Models* =
  pesan yang bisa diperkuat. Strategi narasi harus **dibedakan per topik**.

### 3.3 Kata Kunci Pembeda

![terms](../reports/figures/04_top_terms.png)

- **Tujuan:** menemukan istilah khas tiap sentimen.
- **Dampak:** kata negatif ("problem", "because", "only") menandakan keluhan
  spesifik yang bisa ditindaklanjuti.

### 3.4 Tren Bulanan

![trend](../reports/figures/02_trend.png)

- Volume melonjak di September (6.763 komentar) — kemungkinan terkait peristiwa
  besar di dunia AI.
- Sentimen tetap stabil-positif sepanjang periode (tidak ada penurunan tajam).

---

## 4. Rekomendasi

| # | Rekomendasi | Dasar | Ekspektasi dampak |
|---|-------------|-------|-------------------|
| R1 | Komunikasikan AI dengan **dua pesan**: manfaat teknis + tanggung jawab etika | Ethics −0.137 vs Tools +0.210 | Menjangkau audiens teknis tanpa terkesan mengabaikan risiko |
| R2 | Prioritaskan **transparansi & keamanan** pada produk AI | topik Ethics paling negatif (47%) | Membangun kepercayaan komunitas kritis |
| R3 | Manfaatkan momentum (*Tools & Dev* positif) untuk adopsi developer | sentimen +0.210 | Mempercepat penerimaan & kontribusi |
| R4 | Pantau sentimen berkala (time-series) sebagai *early warning* isu | volume & sentimen berubah tajam | Deteksi krisis reputasi lebih dini |

---

## 5. Keterbatasan (Jujur)

1. **Leksikon tidak memahami sarkasme** & konteks rumit — skor bisa keliru untuk
   komentar ironis.
2. **Domain jargon:** kata seperti "bias" bisa berarti teknis (statistik) atau
   sosial — disambiguasi terbatas.
3. **Sampel HN** = komunitas teknologi, bukan populasi umum.
4. **Snapshot 8 bulan** — tren jangka panjang belum tercakup.
5. **Data mentah tidak di-commit** (13 MB); dapat diregenerasi via
   `collect_sentiment.py`.

> Validasi kualitatif (contoh komentar paling positif/negatif) disediakan di
> dashboard agar skor dapat diperiksa, bukan dipercaya buta.

---

## 6. Reproduksibilitas

```bash
python src/collect_sentiment.py     # ambil komentar HN
python src/run_analysis.py          # tabel + summary.json
python src/make_charts.py           # 6 chart
streamlit run app/dashboard.py      # dashboard
```

---

*Dibuat oleh Sandi Ridwan · sumber: Hacker News (Algolia API publik) · edukasional*

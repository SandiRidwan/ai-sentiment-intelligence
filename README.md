<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=900&size=40&duration=3000&pause=1000&color=6A4C93&center=true&vCenter=true&width=900&height=70&lines=AI+SENTIMENT+INTELLIGENCE" alt="AI Sentiment Intelligence" />

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=16&duration=2500&pause=800&color=6A4C93&center=true&vCenter=true&multiline=true&width=940&height=50&lines=8%2C835+Comments+%E2%86%92+Sentiment+%E2%86%92+Topics+%E2%86%92+Trend" alt="Tagline" />

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-6A4C93?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-2.0-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NLP](https://img.shields.io/badge/NLP-Lexicon_v2_%2B_DistilBERT-1F5C3D?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Data](https://img.shields.io/badge/Source-Hacker_News-FF6600?style=for-the-badge&logo=ycombinator&logoColor=white)

</div>

---

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   █████╗ ██╗    ███████╗███████╗███╗   ██╗████████╗██╗███╗   ███╗███████╗ ║
║  ██╔══██╗██║    ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗ ████║██╔════╝ ║
║  ███████║██║    ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔████╔██║█████╗   ║
║  ██╔══██║██║    ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╔╝██║██╔══╝   ║
║  ██║  ██║██║    ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚═╝ ██║███████╗ ║
║  ╚═╝  ╚═╝╚═╝    ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝     ╚═╝╚══════╝ ║
║                                                                          ║
║   WHAT THE TECH COMMUNITY REALLY THINKS ABOUT AI & LLM                   ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## 🎬 Demo

<div align="center">
  <img src="reports/figures/dashboard_top.png" width="880" alt="AI Sentiment Dashboard" />
  <br/>
  <sub><i>Interactive dashboard — sentiment distribution, topics, keywords, trend</i></sub>
</div>

<br/>

```bash
streamlit run app/dashboard.py     # → http://localhost:8506
```

---

## 🧠 Overview

**AI Sentiment Intelligence** mengubah **8.835 komentar publik** dari Hacker News
menjadi gambaran terukur: bagaimana komunitas teknologi **benar-benar** menilai
AI/LLM — sentimen keseluruhan, per topik, dan trennya.

<div align="center">

| Metric | Value |
|-------:|:------|
| 📊 Sumber | Hacker News (Algolia API publik) — tanpa API key |
| 💬 Komentar | **8.835** unik (Feb–Sep 2026) |
| 🎭 Positif / Netral / Negatif | **40% / 39% / 21%** |
| 🗂️ Topik | Models · Tools & Dev · Business · Jobs · Ethics & Risk |
| 🧠 NLP | Sentimen leksikon (tanpa API berbayar) + topik + tren waktu |
| 📁 Output | Streamlit app · 6 charts · 6 tabel insight |

</div>

---

## 🔑 Temuan Utama

| # | Temuan | Angka |
|---|--------|-------|
| 1 | Sentimen AI **net positif** | 40% positif vs 21% negatif |
| 2 | **Ethics & Risk satu-satunya topik negatif** | mean −0.137 · **47% negatif** |
| 3 | **Tools & Dev paling positif** | mean +0.210 · 47% positif |
| 4 | Keyword negatif = keluhan konkret | "problem", "because", "only" |
| 5 | Lonjakan volume September | 6.763 komentar (bulan terbesar) |

**Insight kunci:** publik **antusias pada teknologi & alat AI**, tetapi **khawatir pada etika/risiko** — pola klasik adopsi teknologi yang perlu komunikasi berbeda per audiens.

---

## 📊 Visualisasi

| Distribusi sentimen | Sentimen per topik |
|:---:|:---:|
| ![overview](reports/figures/01_sentiment_overview.png) | ![topic](reports/figures/03_topic_sentiment.png) |

| Kata kunci pembeda | Tren bulanan |
|:---:|:---:|
| ![terms](reports/figures/04_top_terms.png) | ![trend](reports/figures/02_trend.png) |

---

## ⚡ Metodologi NLP (Jujur & Reproducible)

**Sentimen leksikon internal v2** (`lexicon_v2.py`, bukan API berbayar):
- skor = (kata positif − negatif) / total kata bernada, dengan **negasi**,
  **intensifier**, dan **konjungsi kontras** ("but" → klausa sesudah dibobot 1.8×)
- **Kelas `unknown` dipisah dari `neutral`** — komentar tanpa kata bernada
  tidak lagi disamarkan sebagai "netral"
- **Lapisan sarkasme deterministik** (frasa + pembuka) — menangkap sebagian
  sarkasme **tanpa transformer**
- Kecepatan: ~4.300 komentar/detik (CPU, 1 thread)

**Kenapa leksikon jadi basis (bukan karena transformer "mustahil ringan"):**
DistilBERT kecil (66M, ~270MB) **bisa** jalan di CPU tanpa GPU dan tetap
reproducible bila di-pin. Alasan memilih leksikon di sini adalah **keputusan
lingkup**: leksikon ~1000× lebih cepat, tanpa unduhan, dan setiap skor bisa
diaudit kata-per-kata. Ini pilihan, bukan keterbatasan teknis.

**Keterbatasan yang diakui terbuka:**
1. Leksikon **tidak memahami sarkasme** & konteks rumit secara penuh
   (aturan hanya menangkap penanda eksplisit)
2. Domain teknologi punya jargon (mis. "bias" bisa teknis atau sosial)
3. Hacker News = komunitas tech (bukan sampel populasi umum)

> Sampel komentar paling positif/negatif disediakan di dashboard agar pembaca
> dapat **memverifikasi kualitas** skor — bukan hanya menerima angka.

### Eksperimen upgrade: leksikon vs transformer (terukur)

Project ini **tidak berhenti pada klaim** "transformer berat". Sebuah
eksperimen penuh dijalankan (CPU, reproducible) membandingkan tiga metode pada
holdout yang sama — **termasuk hasil yang tidak nyaman**. Lihat
[`UPGRADE_FINDINGS.md`](UPGRADE_FINDINGS.md).

| Metode | accuracy* | macro-F1* | kecepatan |
|---|---:|---:|---:|
| Leksikon v1 | 0.832 | 0.833 | ~4000/detik |
| **Leksikon v2** | **0.951** | **0.951** | ~4300/detik |
| DistilBERT (66M, fine-tuned) | 0.682 | 0.681 | ~5/detik |
| Baseline naif | 0.364 | 0.178 | — |

<small>*gold = label silver leksikon v2 → **sirkular**; mengukur kesesuaian,
bukan kebenaran absolut. Pada 32% holdout transformer membangkang label
silver, dan pada sebagian kasus transformer **lebih benar** (mis. kalimat
kritis yang ditandai "positif" oleh leksikon karena satu kata "better").
Lihat §3 di findings.</small>

> **Kesimpulan jujur:** leksikon v2 lebih cepat & auditable; transformer
> menangkap konteks yang leksikon lewatkan. Keduanya **komplementer**, dan
> tanpa label manusia kita **tidak boleh** mengklaim salah satu lebih akurat.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  collect_sentiment.py  (Hacker News Algolia API — publik)            │
│  10 query × 10 halaman × 100  → deduplikasi → 8.835 komentar         │
└──────────────────────────────┬───────────────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│  analysis.py — NLP LAYER                                             │
│  · lexicon sentiment (negasi + intensifier)                          │
│  · topik (keyword mapping)                                           │
│  · agregasi: per topik, per bulan, top terms, contoh komentar        │
└───────────────┬───────────────────────────────┬──────────────────────┘
                ▼                               ▼
      reports/figures (6 chart)        app/dashboard.py (Streamlit)
                                       + explanations.py (Kenapa-Tujuan-Dampak)
```

---

## 📁 File Structure

```
ai-sentiment-intelligence/
├── app/dashboard.py             # ⭐ dashboard interaktif (+ penjelasan tiap chart)
├── src/
│   ├── config.py                # path + warna (terpusat)
│   ├── collect_sentiment.py     # ambil komentar HN
│   ├── analysis.py              # NLP: sentimen, topik, tren (murni)
│   ├── explanations.py          # narasi Kenapa · Tujuan · Dampak
│   ├── run_analysis.py          # orkestrator
│   └── make_charts.py           # 6 visualisasi
├── data/{raw,processed}/
├── reports/{figures,tables}/
├── docs/DEPLOY_CHECKLIST.md
├── REPORT.md
└── requirements.txt
```

---

## 🚀 Quick Start

```bash
pip install -r requirements.txt

python src/collect_sentiment.py   # ambil 8.8k komentar HN
python src/run_analysis.py        # tabel + summary
python src/make_charts.py         # 6 chart
python src/explanations.py        # audit: semua penjelasan lengkap?
streamlit run app/dashboard.py
```

---

## 📖 Cara Membaca Dashboard (Kenapa · Tujuan · Dampak)

Setiap chart & tabel punya kotak penjelasan yang menjawab:

| Pertanyaan | Arti |
|-----------|------|
| **🔎 Kenapa** | Mengapa metrik ini dipilih (masalah & konteks) |
| **🎯 Tujuan** | Pertanyaan bisnis yang dijawab |
| **📈 Dampak** | Implikasi / keputusan yang timbul |
| **👁️ Cara baca** | Panduan bila grafik tak intuitif |

Narasi tersimpan di `src/explanations.py` (dapat diaudit).

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Teknologi |
|-------|-----------|
| **Data** | Hacker News Algolia API · curl_cffi |
| **NLP** | leksikon sentimen internal + negasi/intensifier |
| **Analisis** | pandas · numpy |
| **Visualisasi** | matplotlib · Plotly |
| **Dashboard** | Streamlit |

</div>

---

## 📝 Lessons Learned

1. **Data publik terbaik ada di API yang tepat.** HN Algolia memberi 8.8k komentar
   berkualitas tanpa API key — Reddit (403) & GDELT (rate-limit) lebih rumit.
2. **Sentimen leksikon cukup bermakna** bila ditangani dengan negasi + intensifier,
   dan **jujur soal batasnya** (sarkasme) lebih baik daripada klaim berlebihan.
3. **Satu angka menyesatkan.** Memecah per topik langsung mengungkap temuan
   terpenting (Ethics negatif, Tools positif).
4. **Sediakan contoh kualitatif** agar skor dapat diverifikasi, bukan dipercaya buta.
5. **Boilerplate mempercepat.** Project ini dibuat dari template #5 — standar
   (penjelasan, pisah analisis) langsung terpasang.

---

## ⚠️ Disclaimer

Analisis edukasional. Sentimen dihitung dengan leksikon v2 (negasi, intensifier,
kontras, aturan sarkasme eksplisit) sebagai basis, dengan eksperimen pembanding
DistilBERT kecil terdokumentasi di `UPGRADE_FINDINGS.md`. Hanya mewakili
komunitas Hacker News. Bukan saran bisnis/investasi.

---

<!-- INSIGHTS:START -->
## 💡 Insight & Rekomendasi (per analisis)

_Setiap analisis disertai kesimpulan, rekomendasi tindakan, dan risiko bila diabaikan — bukan sekadar angka._

### 🟠 Topic
**Kesimpulan.** Sentimen BERVARIASI tajam antar-topik: Tools & Dev paling positif (+0.21), Ethics & Risk satu-satunya negatif (-0.137). Publik antusias pada alat/teknologi AI, tetapi khawatir pada etika & risiko — dua hal yang tidak bertentangan.

**Rekomendasi tindakan:**
- Pisahkan komunikasi per audiens: untuk 'Tools', tonjolkan manfaat; untuk 'Ethics', akui kekhawatiran dengan komitmen konkret (bukan defensif).
- Prioritaskan mitigasi isu etika (bias, privasi, safety) — ini satu-satunya area negatif dan berpotensi menyebar ke topik lain.
- Gunakan Tools & Dev yang positif sebagai 'pesan pengimbang' saat mengelola isu etika.

**⚠️ Risiko bila diabaikan.** Mengambil angka sentimen nasional yang tampak positif akan mengabaikan kekhawatiran etika yang tajam & terfokus. Isu etika yang dibiarkan bisa menjadi krisis reputasi meski rata-rata nasional 'baik'.

### 🟠 Sarcasm
**Kesimpulan.** Hanya 14 komentar (0.16%) terdeteksi sarkasme eksplisit. Angka kecil ini JUJUR: sarkasme implisit tetap luput dan menjadi batas metode. Aturan menangkap penanda eksplisit saja.

**Rekomendasi tindakan:**
- Jangan percaya buta pada kelas 'negatif' untuk sarkasme — validasi sampel manual bila keputusan bergantung pada nada.
- Untuk kasus kritis, pertimbangkan model transformer khusus sarkasme (lihat tab metodologi).
- Dokumentasikan batas ini secara terbuka agar pengguna data tidak overclaim.

**⚠️ Risiko bila diabaikan.** Sarkasme yang salah diklasifikasi sebagai positif bisa memberi gambaran kabar baik palsu. Keputusan berbasis sentimen tanpa memahami batas ini berisiko salah membaca opini publik secara serius.

### 🔵 KPI / Ringkasan
**Kesimpulan.** Dari 8.835 komentar Hacker News, sentimen publik condong POSITIF (44%) vs negatif (22%) — komunitas teknologi umumnya antusias pada AI. Namun 27% masuk kelas 'unknown' (leksikon tidak menemukan kata bernada): angka ini JUJUR menunjukkan batas metode, bukan 'netral' sebenarnya.

**Rekomendasi tindakan:**
- Manfaatkan momentum positif: publik teknologi terbuka pada narasi manfaat AI — komunikasikan capaian, bukan hanya risiko.
- Untuk 27% 'unknown', jangan anggap netral — lakukan sampling manual atau model yang lebih kuat bila keputusan bergantung pada kelompok ini.
- Pantau pergeseran dari positif→negatif sebagai sinyal dini perubahan persepsi.

**⚠️ Risiko bila diabaikan.** Menganggap 27% 'unknown' sebagai netral akan melebih-lebihkan kepastian analisis. Keputusan komunikasi berbasis data yang 27% isinya tidak terbaca berisiko salah sasaran.

### 🔵 Overview
**Kesimpulan.** Distribusi sentimen: positif 44%, negatif 22%, netral sejati hanya 6.7%, unknown 27%. Mayoritas opini MITSBERSIFAT NET-POSITIF — AI diterima komunitas teknologi, bukan ditolak.

**Rekomendasi tindakan:**
- Fokuskan pesan pada penguatan persepsi positif yang sudah dominan (konsolidasi), bukan defensif melawan kritik yang lebih kecil.
- Selidiki 22% negatif untuk memahami keberatan spesifik (etika? pekerjaan?) sebelum menentukan respons.
- Jadikan komposisi ini baseline: bandingkan periode mendatang untuk mendeteksi pergeseran.

**⚠️ Risiko bila diabaikan.** Tanpa baseline, perubahan persepsi (mis. setelah peluncuran kontroversial) tidak akan terdeteksi. Persepsi publik bisa berbalik cepat dan tanpa pemantauan, respons datang terlambat.

### 🔵 Terms
**Kesimpulan.** Kata kunci pembeda: komentar negatif didominasi 'problem', 'because', 'only' — keluhan SPESIFIK (bukan sekadar emosi). Komentar positif memuat 'machine', 'learning', 'llm' — antusiasme pada teknologi itu sendiri.

**Rekomendasi tindakan:**
- Keluhan spesifik ('problem') berarti BISA DITINDAKLANJUTI: identifikasi masalah konkret yang dimaksud (bug, keterbatasan, biaya) dan perbaiki.
- Antusiasme pada teknologi dasar ('learning','llm') → komunikasikan kemajuan teknis sebagai bahan bakarnya.
- Pantau kemunculan kata negatif baru sebagai peringatan isu yang muncul.

**⚠️ Risiko bila diabaikan.** Mengabaikan kata kunci negatif spesifik berarti melewatkan umpan balik produk yang dapat ditindaklanjuti. 'Problem' yang tidak diselidiki bisa menjadi keluhan struktural yang menggerus adopsi.

### 🔵 Trend
**Kesimpulan.** Volume diskusi melonjak tajam di September 2026 (6.763 komentar), sementara sentimen rata-rata tetap stabil. Artinya lonjakan volume disebabkan PERISTIWA (peluncuran/berita), bukan perubahan sikap.

**Rekomendasi tindakan:**
- Selidiki pemicu lonjakan September — kesempatan memanfaatkan momen perhatian tinggi untuk pesan strategis.
- Karena sentimen stabil, tidak ada alarm reputasi; fokus pada amplifikasi.
- Bangun pemantauan real-time agar lonjakan berikutnya terdeteksi cepat.

**⚠️ Risiko bila diabaikan.** Lonjakan volume tanpa pemantauan = peluang komunikasi yang terbuang. Atau sebaliknya: lonjakan negatif yang tidak terdeteksi bisa berkembang menjadi krisis sebelum ada respons.

<!-- INSIGHTS:END -->

## 👤 Author

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Orbitron&weight=700&size=20&duration=3000&pause=1000&color=6A4C93&center=true&vCenter=true&width=400&lines=Sandi+Ridwan" />

**Data Analyst · Data Automation Engineer · Python**

📍 Palu, Central Sulawesi, Indonesia

[![Upwork](https://img.shields.io/badge/Upwork-Hire_Me-6A4C93?style=for-the-badge&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~011f6d0fbb4a372974)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/sandi-ridwan)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SandiRidwan)

</div>

---

## 📄 License

MIT License — Educational and portfolio purposes only. Data from Hacker News (public).

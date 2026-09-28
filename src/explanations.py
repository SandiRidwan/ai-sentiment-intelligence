"""
explanations.py — narasi Kenapa · Tujuan · Dampak untuk setiap chart/tabel.

STANDAR WAJIB (portofolio): setiap visual harus menjelaskan:
  mengapa dipilih (kenapa), pertanyaan bisnis apa yang dijawab (tujuan),
  dan implikasinya (dampak) + cara membaca bila tidak intuitif.
"""

from __future__ import annotations

EXPLAIN: dict[str, dict] = {
    "kpi": {
        "judul": "Metrik Ringkas (KPI Band)",
        "kenapa": "Sebelum masuk detail, pembaca butuh gambaran angka tunggal: "
                  "berapa banyak suara, dan kecenderungan umumnya apa.",
        "tujuan": "Menampilkan ukuran sampel, komposisi sentimen, dan median "
                  "sentimen sebagai konteks analisis lanjutan.",
        "dampak": "Memberi kesan pertama yang bisa dipercaya; bila komposisi "
                  "berubah (mis. setelah filter topik), itu sinyal diskusi "
                  "terarah yang perlu ditelusuri.",
        "baca": "Persentase dihitung dari seluruh komentar pada data terfilter.",
    },
    "overview": {
        "judul": "Distribusi Sentimen",
        "kenapa": "Langkah pertama analisis sentimen adalah mengetahui bauran "
                  "umum — apakah publik cenderung positif, netral, atau negatif.",
        "tujuan": "Menjawab: bagaimana sikap keseluruhan komunitas terhadap AI/LLM?",
        "dampak": "Bila mayoritas netral (faktual), berarti diskusi teknologis "
                  "cenderung pragmatis, bukan emosional — memengaruhi cara "
                  "membaca temuan lain. Bila negatif dominan, ada isu yang "
                  "harus diselidiki.",
        "baca": "Batang = % komentar per kelas sentimen; label memuat jumlah (n).",
    },
    "trend": {
        "judul": "Tren Volume & Sentimen per Bulan",
        "kenapa": "Sentimen bisa berubah mengikuti peristiwa (rilis produk, "
                  "skandal, terobosan). Snapshot tunggal menyembunyikan itu.",
        "tujuan": "Menjawab: apakah sikap publik membaik/memburuk seiring waktu, "
                  "dan kapan diskusi melonjak?",
        "dampak": "Lonjakan volume + penurunan sentimen menandakan insiden/kontroversi; "
                  "sebaliknya, sentimen naik saat volume naik berarti adopsi positif. "
                  "Berguna untuk timing narasi/PR.",
        "baca": "Batang biru = volume komentar (sumbu kiri); garis hijau = sentimen "
                "rata-rata (sumbu kanan). Garis putus-putus = nol (netral).",
    },
    "topic": {
        "judul": "Sentimen per Topik",
        "kenapa": "Satu angka sentimen menyembunyikan perbedaan penting: orang bisa "
                  "antusias pada teknologi tapi khawatir soal etika.",
        "tujuan": "Menemukan topik mana yang paling direspons positif/negatif "
                  "(mis. Tools vs Ethics & Risk).",
        "dampak": "Topik negatif (mis. Ethics & Risk) = prioritas komunikasi & "
                  "mitigasi; topik positif = pesan yang bisa diperkuat. Memandu "
                  "strategi narasi & produk.",
        "baca": "Batang hijau = sentimen positif, merah = negatif. Label memuat "
                "nilai rata-rata, jumlah komentar, dan % negatif.",
    },
    "terms": {
        "judul": "Kata Kunci Pembeda Sentimen",
        "kenapa": "Skor angka tidak menunjukkan APA yang dibicarakan. Kata kunci "
                  "mengungkap isi argumen di balik tiap sentimen.",
        "tujuan": "Menemukan istilah khas komentar positif vs negatif.",
        "dampak": "Memberi bukti kualitatif: kata negatif seperti 'problem'/'because' "
                  "menandakan keluhan spesifik yang bisa ditindaklanjuti; kata positif "
                  "menunjukkan apa yang dihargai pengguna.",
        "baca": "Kiri = kata teratas di komentar positif; kanan = di komentar negatif. "
                "Kata umum (netral) sudah difilter.",
    },
    "score_dist": {
        "judul": "Sebaran Skor Sentimen",
        "kenapa": "Rata-rata bisa menyesatkan bila sebarannya condong atau bergerombol.",
        "tujuan": "Melihat bentuk distribusi: apakah komentar cenderung ekstrem, "
                  "netral, atau tersebar merata.",
        "dampak": "Puncak di 0 berarti banyak komentar faktual/netral (khas forum "
                  "teknis); ekor tebal di ujung berarti polarisasi kuat — dua "
                  "kondisi yang menuntut strategi berbeda.",
        "baca": "Histogram skor (−1 … +1); garis oranye = median.",
    },
    "samples": {
        "judul": "Contoh Komentar (verifikasi kualitatif)",
        "kenapa": "Model berbasis leksikon bisa salah (sarkasme, konteks). Melihat "
                  "contoh nyata adalah cara jujur memvalidasi & mengakui batas.",
        "tujuan": "Memeriksa apakah skor sentimen sesuai dengan isi komentar.",
        "dampak": "Bila contoh tampak keliru, kesimpulan angka perlu diperlakukan "
                  "hati-hati — transparansi ini menjaga kredibilitas analisis.",
        "baca": "Diambil dari komentar dengan skor paling positif & paling negatif.",
    },
    "top_tables": {
        "judul": "Tabel Sentimen per Topik & Bulan",
        "kenapa": "Angka ringkas memudahkan pembaca memeriksa/mengutip temuan "
                  "tanpa membaca seluruh dataset.",
        "tujuan": "Menyediakan rincian terukur (median, %, jumlah) yang mendasari "
                  "kesimpulan laporan.",
        "dampak": "Menjadi bukti pendukung (evidence) yang dapat diverifikasi & "
                  "dipakai untuk keputusan berbasis angka.",
        "baca": "Median lebih tahan pencilan; % negatif menunjukkan proporsi keluhan.",
    },
}


def text(key: str) -> str:
    e = EXPLAIN.get(key)
    if not e:
        return ""
    parts = [f"**{e['judul']}**",
             f"- **Kenapa:** {e['kenapa']}",
             f"- **Tujuan:** {e['tujuan']}",
             f"- **Dampak:** {e['dampak']}"]
    if e.get("baca"):
        parts.append(f"- **Cara baca:** {e['baca']}")
    return "\n".join(parts)


def render(key: str, expanded: bool = False, st=None):
    if st is None:
        import streamlit as st  # noqa
    e = EXPLAIN.get(key)
    if not e:
        return
    with st.expander(f"💡 {e['judul']} — Kenapa · Tujuan · Dampak", expanded=expanded):
        st.markdown(
            f"**🔎 Kenapa** — {e['kenapa']}\n\n"
            f"**🎯 Tujuan** — {e['tujuan']}\n\n"
            f"**📈 Dampak** — {e['dampak']}")
        if e.get("baca"):
            st.caption(f"👁️ Cara baca: {e['baca']}")


def audit(verbose: bool = True) -> bool:
    ok = True
    for k, v in EXPLAIN.items():
        miss = [f for f in ("kenapa", "tujuan", "dampak") if not v.get(f)]
        if miss:
            ok = False
            if verbose:
                print(f"  MISSING {k}: {miss}")
    if verbose:
        print(f"Penjelasan: {len(EXPLAIN)} | "
              f"{'SEMUA LENGKAP' if ok else 'ADA YANG KURANG'}")
    return ok


if __name__ == "__main__":
    raise SystemExit(0 if audit() else 1)

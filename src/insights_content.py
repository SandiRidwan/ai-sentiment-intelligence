
# ---------------------------------------------------------------------------
# KONTEN INSIGHT — AI Sentiment Intelligence
# Sudut pandang: tim produk/komunikasi/risiko yang memantau persepsi publik
# terhadap AI/LLM & merancang respons.
# ---------------------------------------------------------------------------
from insight import register

register(
    "kpi",
    kesimpulan=(
        "Dari 8.835 komentar Hacker News, sentimen publik condong POSITIF "
        "(44%) vs negatif (22%) — komunitas teknologi umumnya antusias pada AI. "
        "Namun 27% masuk kelas 'unknown' (leksikon tidak menemukan kata bernada): "
        "angka ini JUJUR menunjukkan batas metode, bukan 'netral' sebenarnya."),
    rekomendasi=[
        "Manfaatkan momentum positif: publik teknologi terbuka pada narasi "
        "manfaat AI — komunikasikan capaian, bukan hanya risiko.",
        "Untuk 27% 'unknown', jangan anggap netral — lakukan sampling manual atau "
        "model yang lebih kuat bila keputusan bergantung pada kelompok ini.",
        "Pantau pergeseran dari positif→negatif sebagai sinyal dini perubahan persepsi.",
    ],
    risiko=(
        "Menganggap 27% 'unknown' sebagai netral akan melebih-lebihkan kepastian "
        "analisis. Keputusan komunikasi berbasis data yang 27% isinya tidak "
        "terbaca berisiko salah sasaran."),
    tingkat="sedang",
)

register(
    "overview",
    kesimpulan=(
        "Distribusi sentimen: positif 44%, negatif 22%, netral sejati hanya 6.7%, "
        "unknown 27%. Mayoritas opini MITSBERSIFAT NET-POSITIF — AI diterima "
        "komunitas teknologi, bukan ditolak."),
    rekomendasi=[
        "Fokuskan pesan pada penguatan persepsi positif yang sudah dominan "
        "(konsolidasi), bukan defensif melawan kritik yang lebih kecil.",
        "Selidiki 22% negatif untuk memahami keberatan spesifik (etika? pekerjaan?) "
        "sebelum menentukan respons.",
        "Jadikan komposisi ini baseline: bandingkan periode mendatang untuk "
        "mendeteksi pergeseran.",
    ],
    risiko=(
        "Tanpa baseline, perubahan persepsi (mis. setelah peluncuran kontroversial) "
        "tidak akan terdeteksi. Persepsi publik bisa berbalik cepat dan tanpa "
        "pemantauan, respons datang terlambat."),
    tingkat="sedang",
)

register(
    "topic",
    kesimpulan=(
        "Sentimen BERVARIASI tajam antar-topik: Tools & Dev paling positif "
        "(+0.21), Ethics & Risk satu-satunya negatif (-0.137). Publik antusias "
        "pada alat/teknologi AI, tetapi khawatir pada etika & risiko — dua hal "
        "yang tidak bertentangan."),
    rekomendasi=[
        "Pisahkan komunikasi per audiens: untuk 'Tools', tonjolkan manfaat; "
        "untuk 'Ethics', akui kekhawatiran dengan komitmen konkret (bukan defensif).",
        "Prioritaskan mitigasi isu etika (bias, privasi, safety) — ini satu-satunya "
        "area negatif dan berpotensi menyebar ke topik lain.",
        "Gunakan Tools & Dev yang positif sebagai 'pesan pengimbang' saat mengelola "
        "isu etika.",
    ],
    risiko=(
        "Mengambil angka sentimen nasional yang tampak positif akan mengabaikan "
        "kekhawatiran etika yang tajam & terfokus. Isu etika yang dibiarkan bisa "
        "menjadi krisis reputasi meski rata-rata nasional 'baik'."),
    tingkat="tinggi",
)

register(
    "terms",
    kesimpulan=(
        "Kata kunci pembeda: komentar negatif didominasi 'problem', 'because', "
        "'only' — keluhan SPESIFIK (bukan sekadar emosi). Komentar positif memuat "
        "'machine', 'learning', 'llm' — antusiasme pada teknologi itu sendiri."),
    rekomendasi=[
        "Keluhan spesifik ('problem') berarti BISA DITINDAKLANJUTI: identifikasi "
        "masalah konkret yang dimaksud (bug, keterbatasan, biaya) dan perbaiki.",
        "Antusiasme pada teknologi dasar ('learning','llm') → komunikasikan "
        "kemajuan teknis sebagai bahan bakarnya.",
        "Pantau kemunculan kata negatif baru sebagai peringatan isu yang muncul.",
    ],
    risiko=(
        "Mengabaikan kata kunci negatif spesifik berarti melewatkan umpan balik "
        "produk yang dapat ditindaklanjuti. 'Problem' yang tidak diselidiki bisa "
        "menjadi keluhan struktural yang menggerus adopsi."),
    tingkat="sedang",
)

register(
    "trend",
    kesimpulan=(
        "Volume diskusi melonjak tajam di September 2026 (6.763 komentar), "
        "sementara sentimen rata-rata tetap stabil. Artinya lonjakan volume "
        "disebabkan PERISTIWA (peluncuran/berita), bukan perubahan sikap."),
    rekomendasi=[
        "Selidiki pemicu lonjakan September — kesempatan memanfaatkan momen "
        "perhatian tinggi untuk pesan strategis.",
        "Karena sentimen stabil, tidak ada alarm reputasi; fokus pada amplifikasi.",
        "Bangun pemantauan real-time agar lonjakan berikutnya terdeteksi cepat.",
    ],
    risiko=(
        "Lonjakan volume tanpa pemantauan = peluang komunikasi yang terbuang. "
        "Atau sebaliknya: lonjakan negatif yang tidak terdeteksi bisa berkembang "
        "menjadi krisis sebelum ada respons."),
    tingkat="sedang",
)

register(
    "sarcasm",
    kesimpulan=(
        "Hanya 14 komentar (0.16%) terdeteksi sarkasme eksplisit. Angka kecil "
        "ini JUJUR: sarkasme implisit tetap luput dan menjadi batas metode. "
        "Aturan menangkap penanda eksplisit saja."),
    rekomendasi=[
        "Jangan percaya buta pada kelas 'negatif' untuk sarkasme — validasi "
        "sampel manual bila keputusan bergantung pada nada.",
        "Untuk kasus kritis, pertimbangkan model transformer khusus sarkasme "
        "(lihat tab metodologi).",
        "Dokumentasikan batas ini secara terbuka agar pengguna data tidak overclaim.",
    ],
    risiko=(
        "Sarkasme yang salah diklasifikasi sebagai positif bisa memberi gambaran "
        "kabar baik palsu. Keputusan berbasis sentimen tanpa memahami batas ini "
        "berisiko salah membaca opini publik secara serius."),
    tingkat="tinggi",
)

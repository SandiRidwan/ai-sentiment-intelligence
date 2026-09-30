
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
        {"aksi": "Manfaatkan momentum positif dengan narasi manfaat AI yang terukur",
         "langkah": [
             "Kurasi 50 komentar ber-skor positif tertinggi dari 8.835 komentar "
             "sebagai bukti sosial (kutipan & tautan).",
             "Susun 3 materi kampanye yang menonjolkan penggunaan nyata AI/LLM "
             "(bukan klaim risiko umum).",
             "Terbitkan materi ke kanal komunitas teknologi dan lacak resonansinya "
             "selama 4 minggu.",
         ],
         "metrik": "Rasio sentimen positif pada periode pasca-kampanye naik dari 44% "
                   "menjadi ≥48% pada 8.835 komentar segar.",
         "pemilik": "Lead Komunikasi Produk"},
        {"aksi": "Tindak lanjuti kelas 'unknown' secara terukur, jangan anggap netral",
         "langkah": [
             "Ambil sampel acak 300 dari 27% komentar 'unknown' (≈2.385 komentar) "
             "untuk pelabelan manual.",
             "Ukur berapa banyak yang sebenarnya bermuatan (target: ≥30% terklasifikasi).",
             "Jalankan model transformer sebagai lapis kedua khusus segmen 'unknown' ini.",
         ],
         "metrik": "Proporsi kelas 'unknown' turun dari 27% ke ≤15% setelah pelabelan "
                   "manual + model transformer.",
         "pemilik": "Data Scientist (NLP)"},
        {"aksi": "Bangun sistem peringatan dini pergeseran positif→negatif",
         "langkah": [
             "Tetapkan baseline komposisi: positif 44%, negatif 22%, netral 6.7%, "
             "unknown 27% dari 8.835 komentar.",
             "Pasang ambang alarm bila negatif naik >5 poin dari baseline dalam "
             "satu siklus pemantauan.",
             "Jadwalkan tinjauan mingguan atas anomali yang terdeteksi.",
         ],
         "metrik": "Pergeseran negatif ≥5 poin terdeteksi dalam ≤7 hari sejak terjadi.",
         "pemilik": "Manajer Risiko Reputasi"},
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
        {"aksi": "Konsolidasikan dominasi persepsi positif alih-alih bersikap defensif",
         "langkah": [
             "Fokuskan anggaran pesan pada penguatan 44% sentimen positif yang sudah "
             "dominan dari 8.835 komentar.",
             "Hindari alokasi berlebih untuk melawan 22% kritik yang proporsinya "
             "lebih kecil.",
             "Terbitkan 1 ringkasan bulanan yang mengulang bukti manfaat AI.",
         ],
         "metrik": "Porsi sentimen positif bertahan ≥44% selama 3 bulan berturut-turut.",
         "pemilik": "Lead Komunikasi Produk"},
        {"aksi": "Selidiki akar 22% sentimen negatif sebelum menyusun respons",
         "langkah": [
             "Segmentasi 22% negatif menurut topik (Business, Ethics & Risk, Jobs, "
             "Models, Other, Tools & Dev).",
             "Identifikasi keberatan spesifik dominan memakai kata kunci pembeda "
             "('problem', 'because', 'only').",
             "Susun 1 respons berfokus per topik negatif terbesar.",
         ],
         "metrik": "Setiap topik negatif teratas memiliki respons tertulis & prioritas "
                   "penanganan dalam ≤2 minggu.",
         "pemilik": "Manajer Riset Pasar"},
        {"aksi": "Jadikan komposisi 44/22/6.7/27 sebagai baseline pemantauan tetap",
         "langkah": [
             "Simpan komposisi 8.835 komentar sebagai garis dasar resmi (positif 44%, "
             "negatif 22%, netral 6.7%, unknown 27%).",
             "Bandingkan setiap periode baru terhadap baseline ini secara otomatis.",
             "Laporkan deviasi >5 poin ke pemangku kepentingan.",
         ],
         "metrik": "Laporan deviasi tersedia otomatis setiap periode dengan akurasi "
                   "≥1 titik poin.",
         "pemilik": "Analis Data Sentimen"},
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
        {"aksi": "Pisahkan komunikasi per audiens sesuai polaritas tiap topik",
         "langkah": [
             "Untuk Tools & Dev (skor +0.21): tonjolkan manfaat & kemudahan alat.",
             "Untuk Ethics & Risk (skor −0.137): akui kekhawatiran dengan komitmen "
             "konkret, bukan pembelaan defensif.",
             "Susun pesan berbeda untuk Business, Jobs, Models, dan Other sesuai "
             "skor topik masing-masing.",
         ],
         "metrik": "Skor sentimen Ethics & Risk naik dari −0.137 menjadi ≥ −0.05 dalam "
                   "2 kuartal.",
         "pemilik": "Lead Komunikasi Produk"},
        {"aksi": "Prioritaskan mitigasi isu etika sebelum menyebar ke topik lain",
         "langkah": [
             "Susun daftar isu etika teratas (bias, privasi, safety) dari komentar "
             "negatif pada topik Ethics & Risk.",
             "Alokasikan rencana aksi per isu dengan tenggat dan penanggung jawab.",
             "Pantau apakah sentimen negatif 'menular' ke topik Models dan Jobs.",
         ],
         "metrik": "Tidak ada topik lain yang turun ke skor negatif (< 0) dalam 2 kuartal.",
         "pemilik": "Manajer Risiko Reputasi"},
        {"aksi": "Gunakan sentimen positif Tools & Dev sebagai pesan pengimbang",
         "langkah": [
             "Sorot skor +0.21 Tools & Dev saat menanggapi kekhawatiran etika.",
             "Sandingkan capaian alat dengan komitmen perbaikan isu etika.",
             "Distribusikan ke kanal komunitas yang membahas kedua topik tersebut.",
         ],
         "metrik": "Sentimen agregat lintas-topik tetap net-positif (rata-rata ≥ 0) "
                   "selama penanganan isu etika.",
         "pemilik": "Lead Komunikasi Produk"},
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
        {"aksi": "Tindaklanjuti keluhan spesifik yang dimulai dari kata 'problem'",
         "langkah": [
             "Ekstrak semua komentar negatif yang memuat 'problem' dari 8.835 komentar.",
             "Klasifikasikan ke kategori konkret: bug, keterbatasan, atau biaya.",
             "Teruskan tiap kategori ke tim teknis terkait dengan bukti kutipan.",
         ],
         "metrik": "≥80% keluhan ber-'problem' memiliki tiket tindak lanjut resmi "
                   "dalam 30 hari.",
         "pemilik": "Product Manager"},
        {"aksi": "Perkuat narasi teknis dengan kata antusiasme dasar",
         "langkah": [
             "Kumpulkan komentar positif yang memuat 'machine', 'learning', 'llm'.",
             "Kemas kemajuan teknis nyata sebagai materi komunikasi berbasis kata kunci ini.",
             "Uji penerbitan 1 konten teknis per bulan ke komunitas.",
         ],
         "metrik": "Frekuensi kata positif kunci ('learning', 'llm') naik ≥10% pada "
                   "periode berikutnya.",
         "pemilik": "Lead Komunikasi Produk"},
        {"aksi": "Pasang pemantauan kemunculan kosakata negatif baru",
         "langkah": [
             "Bangun daftar kata negatif baseline dari komentar saat ini ('problem', "
             "'because', 'only').",
             "Deteksi kosakata negatif baru yang muncul di luar daftar baseline.",
             "Keluarkan peringatan isu untuk setiap kata negatif yang melonjak.",
         ],
         "metrik": "Kata negatif baru terdeteksi & dilaporkan dalam ≤7 hari sejak "
                   "kemunculan pertamanya.",
         "pemilik": "Analis Data Sentimen"},
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
        {"aksi": "Manfaatkan lonjakan perhatian September sebagai momentum pesan",
         "langkah": [
             "Telusuri pemicu lonjakan ke 6.763 komentar pada September 2026 "
             "(peluncuran/berita mana).",
             "Siapkan pesan strategis yang menumpang momen perhatian tinggi tersebut.",
             "Terbitkan pesan dalam jendela 2 minggu saat volume masih tinggi.",
         ],
         "metrik": "Jangkauan pesan pada periode lonjakan naik ≥1,5× dibanding "
                   "periode volume normal.",
         "pemilik": "Lead Komunikasi Produk"},
        {"aksi": "Amplifikasi saat sentimen stabil, bukan mitigasi krisis",
         "langkah": [
             "Konfirmasi bahwa sentimen rata-rata tetap stabil selama lonjakan volume.",
             "Alihkan fokus dari respons krisis ke amplifikasi capaian positif.",
             "Alokasikan sumber daya komunikasi ke kanal ber-lonjakan.",
         ],
         "metrik": "Tidak ada kenaikan porsi sentimen negatif >5 poin selama periode "
                   "lonjakan.",
         "pemilik": "Manajer Risiko Reputasi"},
        {"aksi": "Bangun pemantauan volume real-time untuk deteksi cepat",
         "langkah": [
             "Pasang ambang alarm volume bila harian melampaui level September 2026.",
             "Otomatiskan notifikasi ke tim saat ambang terlewati.",
             "Tinjau lonjakan berikutnya dalam ≤24 jam sejak alarm berbunyi.",
         ],
         "metrik": "Lonjakan volume berikutnya terdeteksi dalam ≤24 jam sejak mulai.",
         "pemilik": "Analis Data Sentimen"},
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
        {"aksi": "Validasi manual kelas 'negatif' sebelum dipakai untuk keputusan nada",
         "langkah": [
             "Ambil sampel acak dari kelas 'negatif' untuk pemeriksaan manual "
             "sarkasme implisit.",
             "Ukur tingkat salah klasifikasi yang ditemukan pada sampel tersebut.",
             "Gunakan hasil validasi sebagai faktor koreksi saat menafsirkan nada.",
         ],
         "metrik": "Tingkat salah klasifikasi sarkasme pada sampel terukur dan "
                   "terdokumentasi (target <10%).",
         "pemilik": "Data Scientist (NLP)"},
        {"aksi": "Terapkan model transformer khusus sarkasme untuk kasus kritis",
         "langkah": [
             "Jalankan model transformer pada keputusan bernada tinggi yang "
             "bergantung pada deteksi sarkasme.",
             "Bandingkan hasilnya dengan aturan leksikon v2 yang mendeteksi 14 "
             "komentar (0.16%).",
             "Validasi silang temuan pada subsampel manual.",
         ],
         "metrik": "Recall deteksi sarkasme naik dari 0.16% (14 komentar) ke ≥2% pada "
                   "subsampel validasi.",
         "pemilik": "Data Scientist (NLP)"},
        {"aksi": "Dokumentasikan batas deteksi sarkasme secara terbuka",
         "langkah": [
             "Cantumkan batas 'hanya sarkasme eksplisit' pada tab metodologi.",
             "Sertakan peringatan overclaim pada setiap keluaran ber-basis nada.",
             "Latih pengguna data agar tidak menafsirkan nada secara berlebihan.",
         ],
         "metrik": "100% keluaran ber-basis nada memuat disclaimer batas sarkasme.",
         "pemilik": "Analis Data Sentimen"},
    ],
    risiko=(
        "Sarkasme yang salah diklasifikasi sebagai positif bisa memberi gambaran "
        "kabar baik palsu. Keputusan berbasis sentimen tanpa memahami batas ini "
        "berisiko salah membaca opini publik secara serius."),
    tingkat="tinggi",
)


# --------------------------------------------------------------------------
# Chart ECharts (v2) — insight & rekomendasi.
# --------------------------------------------------------------------------

register(
    "echarts_theme_river",
    kesimpulan=(
        "Theme River menunjukkan KOMPOSISI perhatian antar-topik sepanjang waktu, "
        "bukan sekadar volume total. Pita yang melebar = topik yang menguat; "
        "menyempit = meredup. Ini mengungkap pergeseran agenda komunitas — "
        "mis. dari 'Models' ke 'Ethics & Risk' — yang tak terlihat pada garis "
        "tren agregat."),
    rekomendasi=[
        {"aksi": "Pantau topik dengan pita melebar cepat sebagai sinyal isu naik",
         "langkah": [
             "Identifikasi topik (Business, Ethics & Risk, Jobs, Models, Other, "
             "Tools & Dev) dengan laju pelebaran pita tercepat.",
             "Siapkan narasi komunikasi untuk topik tersebut sebelum memuncak.",
             "Laporkan topik yang melebar ke tim terkait setiap siklus.",
         ],
         "metrik": "Narasi siap untuk topik tercepat-melebar dalam ≤2 minggu sebelum "
                   "puncaknya.",
         "pemilik": "Manajer Riset Pasar"},
        {"aksi": "Kaitkan lebar pita dengan sentimen untuk deteksi potensi krisis",
         "langkah": [
             "Silangkan laju pelebaran pita tiap topik dengan skor sentimennya.",
             "Tandai kombinasi volume naik + sentimen negatif (mis. seperti Ethics & "
             "Risk di −0.137) sebagai sinyal krisis.",
             "Naikkan frekuensi pemantauan pada topik bertanda tersebut.",
         ],
         "metrik": "Topik ber-volume naik + sentimen negatif tertangani dalam ≤1 "
                   "minggu sejak tanda muncul.",
         "pemilik": "Manajer Risiko Reputasi"},
        {"aksi": "Gunakan pergeseran komposisi untuk memutuskan prioritas konten",
         "langkah": [
             "Petakan tema yang tumbuh (mis. Models → Ethics & Risk) versus yang "
             "meredup.",
             "Realokasi prioritas konten/edukasi ke tema yang menguat.",
             "Tinjau ulang alokasi perhatian pada topik yang menyempit.",
         ],
         "metrik": "≥80% konten baru selaras dengan topik yang pita-nya melebar tiap "
                   "kuartal.",
         "pemilik": "Lead Komunikasi Produk"},
    ],
    risiko=(
        "Membaca hanya total volume menyembunyikan pergeseran tema. Organisasi "
        "bisa bereaksi terlambat pada isu yang tumbuh, atau salah mengalokasikan "
        "perhatian ke topik yang justru meredup."),
    tingkat="tinggi",
)

register(
    "echarts_boxplot",
    kesimpulan=(
        "Boxplot skor sentimen per topik memperlihatkan MEDIAN, SEBARAN, dan "
        "PENCILAN opini tiap topik. Topik dengan kotak lebar = publik terbelah "
        "(pro & kontra kuat); kotak sempit = konsensus. Median jauh dari skor 0 "
        "menandakan topik itu umumnya positif/negatif, bukan cuma berisik."),
    rekomendasi=[
        {"aksi": "Prioritaskan topik ber-median negatif sekaligus sebaran lebar",
         "langkah": [
             "Urutkan topik (Business, Ethics & Risk, Jobs, Models, Other, Tools & "
             "Dev) berdasarkan median dan lebar kotak.",
             "Fokuskan sumber daya pada topik ber-median negatif (mis. Ethics & Risk "
             "−0.137) dengan sebaran lebar.",
             "Tetapkan rencana perbaikan per topik prioritas tersebut.",
         ],
         "metrik": "Topik prioritas (median negatif + sebaran lebar) menunjukkan "
                   "perbaikan median ≥0,05 dalam 1 kuartal.",
         "pemilik": "Manajer Risiko Reputasi"},
        {"aksi": "Sapa audiens topik 'terbelah' secara terpisah, jangan pukul rata",
         "langkah": [
             "Identifikasi topik berkotak lebar (publik terbelah pro & kontra).",
             "Pisahkan segmen pendukung dan penentang pada topik tersebut.",
             "Susun pesan khusus untuk masing-masing segmen.",
         ],
         "metrik": "Setiap topik 'terbelah' memiliki 2 segmen audiens terdefinisi "
                   "dengan pesan masing-masing.",
         "pemilik": "Manajer Riset Pasar"},
        {"aksi": "Periksa pencilan komentar ekstrem secara manual",
         "langkah": [
             "Ekstrak pencilan (komentar ekstrem) dari boxplot tiap topik.",
             "Periksa manual: mana meme/sarkasme yang lolos aturan leksikon v2.",
             "Catat temuan untuk memperbaiki aturan sarkasme deterministik.",
         ],
         "metrik": "≥90% pencilan tiap topik tersaring menjadi temuan meme/sarkasme "
                   "atau komentar substantif.",
         "pemilik": "Data Scientist (NLP)"},
    ],
    risiko=(
        "Mengandalkan rata-rata tunggal membuat topik terbelah tampak 'netral' "
        "sehingga luput dari perhatian, padahal justru di situ gesekan opini "
        "paling tajam. Analisis edukasional — bukan pengganti riset audiens."),
    tingkat="sedang",
)

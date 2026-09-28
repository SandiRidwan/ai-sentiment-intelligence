# ⚠️ Checklist Deploy ke Streamlit Cloud

> Pelajaran nyata dari 4 project. Bug yang **lolos di lokal** tapi **gagal di cloud**
> hampir selalu berasal dari daftar di bawah. Baca sebelum deploy.

---

## 1. Data — kesalahan #1 saat deploy

**Gejala:** app tampil `FileNotFoundError` (atau tabel kosong) walau jalan lokal.

**Penyebab umum:** `.gitignore` memblokir file data yang **dibutuhkan app**, jadi
file tidak ikut ter-commit ke GitHub.

**Cara cek (WAJIB sebelum deploy):**

```bash
# 1) File apa saja yang benar-benar ada di remote?
git ls-files | grep data/

# 2) Apakah file yang dibaca app ada di daftar itu?
#    (cari pd.read_csv / read_json di app & src)
grep -rn "read_csv\|read_json\|read_parquet" app/ src/

# 3) Kalau TIDAK ada -> paksa commit (bila ukurannya wajar, < ~10MB):
git add -f data/processed/clean.csv
git commit -m "fix: commit data required by app"
```

**Aturan ukuran:**
| Ukuran file | Tindakan |
|-------------|----------|
| < 10 MB | ✅ commit langsung (app butuh) |
| 10–45 MB | ⚠️ pertimbangkan; atau app generate sendiri dari data kecil |
| > 50 MB | ❌ jangan commit; buat langkah generate/unduh di app, atau simpan ringkasan agregat saja |

> **Prinsip:** app yang di-deploy harus bisa **jalan tanpa langkah manual**.
> Kalau butuh data, data itu harus ada di repo (kecil) atau dihasilkan app.

---

## 2. Dependensi — hanya yang ada di `requirements.txt`

**Gejala:** `ModuleNotFoundError: No module named 'X'`.

**Penyebab:** library terpasang di lokal tapi lupa masuk `requirements.txt`.
Kasus nyata: `pandas.corr(method="spearman")` butuh **scipy** — tidak ada di cloud.

**Cara cek:**
```bash
# daftar impor di kode
grep -rhoE "^(import|from) [a-zA-Z0-9_]+" app/ src/ | sort -u
# bandingkan dengan requirements.txt
cat requirements.txt
```

**Solusi:** tambahkan ke `requirements.txt` **ATAU** hindari library tersebut.
Contoh menghindari scipy untuk Spearman (cukup pandas):
```python
# Spearman = korelasi Pearson dari RANK -> tidak butuh scipy
rho = df["a"].rank().corr(df["b"].rank())
```

---

## 3. Skema data berubah → jangan andalkan satu dataset

**Gejala:** `KeyError: 'kolom_x'` hanya di deploy (karena data/kolom beda).

**Solusi:** buat kode **tahan-skema**:
```python
if "composite_score" in df.columns:
    fig = ...          # versi lengkap
else:
    st.info("Kolom skor tidak tersedia pada dataset ini.")
```
Jangan akses kolom yang mungkin tidak ada tanpa pengecekan.

---

## 4. Konfigurasi tema

- File config tema harus ada di **root** `/.streamlit/config.toml` (cloud membaca dari situ).
- Menyalin ke `app/.streamlit/config.toml` tidak cukup.
- **Jangan** menetapkan `server.port` (cloud memakai port sendiri).

---

## 5. Verifikasi SETELAH deploy (jangan hanya tab pertama!)

1. Buka URL → tunggu app selesai "baking".
2. Klik **setiap tab** dan **setiap filter**.
3. Cari kata kunci error di halaman: `Traceback`, `Error`, `FileNotFoundError`,
   `ModuleNotFoundError`, `KeyError`.
4. Bila muncul error, cek log: tombol **"Manage app"** (kanan bawah) → *Logs*.
5. Perbaiki → `git push` → tunggu auto-redeploy (~1–2 menit) → ulangi cek.

> **Aturan:** deploy belum "selesai" sampai **semua tab** diverifikasi tanpa error.

---

## 6. Keamanan

- Jangan pernah commit `.env`, `credentials.json`, service-account `*.json` .
- Cek: `git ls-files | grep -iE "env|credential|key|secret|service_account"`.
- Bila ragu, tambahkan pola ke `.gitignore` **sebelum** `git add .`.
- Bila kredensial sudah terlanjur bocor: **rotasi key**, bukan hanya hapus file.

---

## 7. Checklist ringkas (salin ke tiap project)

```
[ ] requirements.txt memuat SEMUA impor
[ ] data yang dibaca app ada di git ls-files
[ ] kode tahan-skema (kolom dicek sebelum diakses)
[ ] .streamlit/config.toml ada di root, tanpa server.port
[ ] tidak ada kredensial di repo
[ ] SETIAP tab dites di live tanpa error
```

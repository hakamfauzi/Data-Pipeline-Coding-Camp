# ETL Pipeline - Fashion Studio

Proyek ini membangun sebuah pipeline **ETL (Extract, Transform, Load)** untuk mengekstrak data produk fashion dari website kompetitor, melakukan transformasi serta pembersihan data, lalu menyimpannya ke dalam file CSV, PostgreSQL, dan (opsional) Google Sheets.

---

## Tujuan

- Mengotomatisasi proses pengambilan dan pembersihan data dari website kompetitor Fashion Studio.
- Menyimpan data hasil scraping yang telah dibersihkan untuk digunakan pada proses analisis atau integrasi sistem lainnya.

---

## Fitur

- Scraping data produk dari website.
- Pembersihan data: konversi rating, harga, warna, dan validasi nilai string.
- Konversi harga ke Rupiah (kurs: **1 USD = Rp16.000**).
- Simpan ke **CSV**, **PostgreSQL**, dan (opsional) **Google Sheets**.
- Dilengkapi dengan **unit test** dan **test coverage**.

---

## Struktur Proyek

```
.
├── main.py                     # Entry point ETL pipeline
├── utils/
│   ├── extract.py             # Proses scraping dari website
│   ├── transform.py           # Pembersihan dan transformasi data
│   ├── load.py                # Penyimpanan data (CSV, DB, Sheets)
├── tests/
│   ├── test_extract.py        # Unit test extract
│   ├── test_transform.py      # Unit test transform
│   ├── test_load.py           # Unit test load
├── requirements.txt           # Daftar dependency
├── submission.txt             # Instruksi eksekusi
└── README.md                  # Dokumentasi proyek
```

---

## Menjalankan Proyek

1. **Menjalankan pipeline ETL:**
```bash
python3 main.py
```

2. **Menjalankan unit test:**
```bash
python3 -m pytest tests
```

3. **Menjalankan test coverage:**
```bash
coverage run -m pytest tests
```

---

## Spesifikasi Kolom Output

| Kolom   | Tipe   | Deskripsi                                         |
|---------|--------|---------------------------------------------------|
| `title` | str    | Nama produk                                       |
| `price` | float  | Harga produk dalam **Rupiah** (setelah dikonversi)|
| `colors`| int    | Jumlah pilihan warna                              |
| `rating`| float  | Rating produk                                     |
| `size`  | str    | Ukuran produk                                     |
| `gender`| str    | Target gender produk                              |

---

## Validasi Data

- **Kolom `price`** sudah dikalikan Rp16.000 dan bertipe float.
- **Kolom `rating`** diformat sebagai float (contoh: `4.2`) – nilai seperti `4.8 / 5` atau `Invalid` dihapus.
- **Kolom `colors`** bertipe integer – string seperti `3 Colors` dikonversi ke `3`.
- **Kolom `size` dan `gender`** dipastikan sebagai string dan tidak kosong.
- **Nilai tidak valid** seperti `Unknown Product`, `Invalid Rating`, `Price Unavailable` akan dibersihkan dari data.

---

## Dependencies

Tersedia di file [requirements.txt](requirements.txt), dan mencakup:
- `requests`
- `beautifulsoup4`
- `pandas`
- `sqlalchemy`
- `pytest`
- `coverage`

---
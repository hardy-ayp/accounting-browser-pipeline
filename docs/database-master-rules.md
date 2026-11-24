# Referensi: Aturan Rekayasa Spreadsheet Database Master Enterprise

Dokumen ini memuat standar teknis pengelolaan berkas spreadsheet database skala enterprise (berukuran besar, memuat puluhan sheet, formula kompleks, dan data transaksi masif).

---

## 1. Arsitektur Berkas Master Induk & Salinan Operasional

Dalam sistem akuntansi enterprise yang mengandalkan spreadsheet sebagai repositori master:
1. **Berkas Master Induk (Historical Archive Master):**
   - Merupakan repositori pusat data historis perusahaan yang mencakup puluhan lembar kerja (multi-sheet).
   - Memuat jejaring formula lintas sheet yang padat (`VLOOKUP`, `INDEX/MATCH`, `XLOOKUP`, dan pivot tables).
   - **Kaidah:** Berkas master induk tidak boleh dimodifikasi secara langsung dalam siklus kerja harian.
2. **Berkas Salinan Kerja Aktif (Working Copy):**
   - Berkas duplikat resmi yang dijadikan tempat eksekusi pembaruan data berjalan (harian/mingguan).
   - Melindungi berkas master dari risiko korupsi data atau kesalahan komputasi yang tidak dapat di-rollback.
3. **Berkas Pelaporan Eksekutif (Executive Summary Workbook):**
   - Berkas ringkas yang mengambil data teragregasi dari salinan kerja aktif untuk disajikan kepada jajaran pimpinan/manajemen.

---

## 2. Aturan Perlindungan Formula (Anti `#REF!` Enforcement)

Saat memperbarui lembar kerja yang memiliki referensi formula inter-sheet:

```text
┌────────────────────────────────────────────────────────┐
│ BARIS 1 s/d 5: HEADER & KAMUS FORMULA (DILINDUNGI)    │
│ - Label Nama Kolom Utama                               │
│ - Tabel Referensi Lookup di area kanan lembar kerja    │
├────────────────────────────────────────────────────────┤
│ BARIS 6 s/d N: DATA TRANSAKSI BERJALAN                 │
│ - Kolom Formula Kiri      : Formula Lookup (FILL DOWN) │
│ - Kolom Data Mentah (Raw) : Data Transaksi (TIMPA BARU)│
│ - Kolom Klasifikasi Kanan : Formula Kategori (FILL DOWN)│
└────────────────────────────────────────────────────────┘
```

### A. Larangan Keras:
1. **Dilarang Menghapus Sheet (`wb.remove(sheet)`):**
   Menghapus sheet lama dan membuat sheet baru dengan nama yang sama akan memutus pointer XML internal Excel. Seluruh formula di sheet lain yang merujuk pada sheet tersebut akan rusak permanen menjadi `#REF!`.
2. **Dilarang Menimpa Baris Header (Baris 1–5):**
   Baris 1 hingga 5 sering kali memuat label header, formula dinamis, atau tabel kamus referensi. Pembersihan data lama hanya boleh dilakukan mulai baris ke-6 ke bawah.

### B. Prosedur Pembaruan Data Aman:
1. **Identifikasi Kolom Data Mentah (Raw Columns):**
   Hanya kolom yang menampung data input transaksi mentah yang dikosongkan dan ditimpa dengan data penarikan terbaru.
2. **Penyalinan Formula Dinamis (*Dynamic Fill Down*):**
   Setelah baris data mentah baru terpasang, formula pada kolom kalkulasi (misal: formula VLOOKUP kode master, klasifikasi kategori, atau perhitungan margin) disalin ke bawah (*fill down*) secara dinamis mengikuti jumlah baris data baru.

---

## 3. Sinkronisasi Kamus Master & Validasi Referensi

1. **Pemanfaatan Sheet Kamus Resmi:**
   Gunakan sheet referensi kamus yang telah ada di dalam berkas (tabel kode akun, daftar cabang resmi, kamus kategori produk) sebagai acuan tunggal (*single source of truth*).
2. **Penanganan Data Baru Tidak Terdaftar:**
   Apabila ditemukan kode cabang atau kode transaksi yang belum terdaftar di sheet kamus master:
   - Dilarang mengarang padanan kode atau menebak deskripsinya.
   - Tandai baris tersebut sebagai `UNREGISTERED CODE / PERLU VERIFIKASI` agar dapat diaudit secara manual oleh verifikator.

---

## 4. Standar Penyajian Visual & Format Finansial

1. **Pemformatan Angka:**
   - Nilai Moneter: Diformat akuntansi `Rp #,##0` atau `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)`.
   - Kuantitas / Satuan: Diformat `#,##0.00` atau `#,##0.000` sesuai tingkat presisi komoditas.
2. **Hierarki Visual:**
   - Baris Header menggunakan latar warna gelap elegan (Slate/Navy) dengan teks tebal warna putih.
   - Baris Total dan Subtotal menggunakan garis batas ganda bawah (*double bottom border*).
   - Baris selisih audit atau anomali diberi warna sorotan lembut (Soft Red / Soft Amber).
3. **Pengaturan Tampilan Kerja:**
   - Aktifkan *Freeze Panes* pada baris header agar navigasi data ribuan baris tetap nyaman dibaca.
   - Lakukan penyesuaian lebar kolom otomatis (*auto-fit column width*) dengan margin toleransi 3–4 karakter agar angka tidak terpotong menjadi `###`.

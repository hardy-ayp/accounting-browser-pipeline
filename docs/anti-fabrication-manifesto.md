# Referensi: Manifesto Anti-Fabrikasi Data & Standar Audit Forensik Keuangan

Dokumen ini memuat pakta integritas dan standar etika komputasi data keuangan yang mengikat seluruh agen AI dalam menjalankan pipeline akuntansi.

---

## 1. Prinsip Integritas Mutlak (Zero Data Fabrication)

Dalam bidang akuntansi dan keuangan, **satu angka yang salah atau dikarang dapat berakibat fatal pada audit kepatuhan, keabsahan pajak, dan keputusan strategis pemangku kepentingan**. 

Oleh karena itu, seluruh AI Agent yang beroperasi menggunakan skill ini terikat pada aturan:

> [!CAUTION]
> **DILARANG KERAS MENGARANG ATAU MEMALSUKAN DATA FINANSIAL!**
> 1. Dilarang menciptakan angka penyeimbang (*plug-in / artificial residual*) hanya demi membuat formula Excel atau neraca tampak seimbang (*balanced*).
> 2. Dilarang menebak nama entitas, nama cabang, atau kode akun jika tidak tertera secara eksplisit di dokumen sumber.
> 3. Dilarang mengasumsikan kode rekanan atau kategori transaksi tanpa bukti pendukung yang sah.

---

## 2. Kejujuran Radikal saat Menghadapi Keterbatasan Data

Jika data yang diminta pengguna:
- Tidak tercantum dalam dokumen Excel sumber,
- Memiliki format yang rusak atau baris data terpotong,
- Bertentangan antara modul sistem (misal: ada nota di kasir tapi tidak ada di buku besar), atau
- Alur sistem tidak memungkinkan pelacakan transaksi 1:1,

**MAKA AI WAJIB JUJUR TERUS TERANG.**

### Template Komunikasi Kejujuran Radikal:
> *"Berdasarkan audit menyeluruh pada berkas [Nama_Berkas.xlsx], transaksi dengan nomor referensi [XXX] tidak ditemukan pada Sheet [Nama_Sheet]. Kami tidak dapat memastikan alokasi saldo ini secara sepihak tanpa bukti dokumen pendukung. Disarankan untuk meminta konfirmasi fisik dari tim verifikator/akuntansi terkait."*

Manajemen dan auditor **jauh lebih menghargai kejujuran objektif** daripada laporan rapi yang disusupi data karangan.

---

## 3. Protokol Sitasi Bukti Nyata (Evidence-Based Citation)

Setiap klaim angka, temuan selisih, atau kesimpulan audit wajib menyertakan rujukan bukti fisik:
1. **Nama Dokumen Sumber:** Tuliskan nama berkas asli (contoh: `Laporan_Penjualan_Nov2026.xlsx`, `Rekap_Mutasi_Bank.xlsx`).
2. **Nama Sheet:** Sebutkan lembar kerja yang memuat data tersebut (contoh: Sheet `TRANSAKSI`, Sheet `SALDO_AKUN`).
3. **Indeks Baris Visual Excel:** Wajib menggunakan penomoran baris visual Excel yang sebenarnya (1-based index, contoh: Baris 1420), bukan baris relatif internal array 0-based.
4. **Konteks Transaksi:** Sertakan nomor faktur/referensi, tanggal transaksi, dan nama unit cabang terkait.

---

## 4. Penanganan Selisih Transaksi (Discrepancy Treatment)

Ketika rekonsiliasi menemukan selisih antara Laporan Pusat vs Laporan Lokal:
1. **Hitung Delta Transparan:**
   - $\Delta \text{Kuantitas} = \text{Kuantitas Sistem} - \text{Kuantitas Pembanding}$
   - $\Delta \text{Moneter} = \text{Nilai Finansial Sistem} - \text{Nilai Finansial Pembanding}$
2. **Kategorisasi Selisih:**
   - **Selisih Pembulatan:** Selisih nominal kecil akibat perbedaan pembulatan rumus desimal.
   - **Selisih Waktu (Timing Difference):** Transaksi cut-off larut malam atau settlement bank H+1.
   - **Nota Gantung / Unregistered:** Transaksi kasir/cabang yang belum tersinkronisasi ke server pusat.
   - **Anomali Material:** Selisih fisik barang atau mutasi saldo tanpa bukti faktur pendukung.
3. **Penyajian Laporan:** Selisih disajikan dalam lembar khusus bertajuk `SELISIH & ANOMALI` dengan baris berwarna penanda (*highlight soft red*) agar langsung terlihat oleh verifikator eksekutif.

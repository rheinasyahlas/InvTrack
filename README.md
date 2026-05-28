# Sheraton Bandung - Integrated Invoice Monitor 🏨

Aplikasi web interaktif berbasis Streamlit yang dirancang untuk memantau status invoice, manajemen risiko aging (usia dokumen), dan pengiriman notifikasi otomatis untuk operasional finansial di Sheraton Bandung Hotel & Towers.

## 🚀 Fitur Utama
- **Real-time Dashboard**: Pantau total outstanding dan invoice kritis secara instan.
- **Risk Categorization**: Klasifikasi otomatis (Safe, Warning, Critical) berdasarkan jumlah hari aging.
- **Ingress System**: Formulir entri data invoice baru langsung ke dalam sistem.
- **Auto-Dispatcher**: Menghasilkan draf pesan profesional untuk follow-up ke Department Head (HOD).
- **Search & Filter**: Pencarian cepat berdasarkan supplier atau departemen.

## 🛠️ Teknologi yang Digunakan
- [Streamlit](https://streamlit.io/) - Framework aplikasi web.
- [Pandas](https://pandas.pydata.org/) - Manipulasi dan analisis data.
- [NumPy](https://numpy.org/) - Komputasi numerik.

## 📂 Struktur File
- `streamlit_app.py`: Kode utama aplikasi.
- `requirements.txt`: Daftar pustaka (dependencies) yang dibutuhkan.
- `README.md`: Dokumentasi proyek ini.

## 💻 Cara Menjalankan Secara Lokal
1. Clone repositori ini.
2. Instal kebutuhan: `pip install -r requirements.txt`
3. Jalankan aplikasi: `streamlit run streamlit_app.py`

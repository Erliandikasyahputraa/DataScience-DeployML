# 💬 Analisis Sentimen Bahasa Indonesia - Web App (6 Emosi)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask Version](https://img.shields.io/badge/Flask-2.3.3-green)](https://flask.palletsprojects.com/)
[![Vite Version](https://img.shields.io/badge/Vite-5.2.0-purple)](https://vitejs.dev/)

Aplikasi web sederhana untuk analisis sentimen teks berbahasa Indonesia, mampu mengklasifikasikan 6 kategori emosi (`happy`, `anger`, `fear`, `sadness`, `love`, `disgust`). Proyek ini mendemonstrasikan proses *end-to-end* dari pelatihan model Machine Learning hingga *deployment* di lingkungan web menggunakan Flask (back-end) dan Vite (front-end).

## ✨ Fitur Utama

* **Analisis Sentimen Multi-Kelas:** Mampu mendeteksi 6 kategori emosi berbeda dari teks Bahasa Indonesia.
* **API Back-End:** Dibangun dengan Flask untuk menangani permintaan prediksi, pra-pemrosesan teks, dan inferensi model.
* **Antarmuka Web Interaktif:** Front-end yang dibuat dengan Vite (Vanilla JavaScript) untuk interaksi pengguna yang *responsive*.
* **Pra-pemrosesan Teks Komprehensif:** Termasuk pembersihan teks, tokenisasi, penghapusan *stopwords* bahasa Indonesia, dan *stemming* menggunakan pustaka `Sastrawi`.
* **Model Machine Learning:** Menggunakan `PassiveAggressiveClassifier` yang dilatih dengan fitur TF-IDF, dikenal efektif untuk klasifikasi teks.
* **Skema Deployment Lokal:** Menjelaskan cara menjalankan aplikasi secara lokal untuk pengembangan dan pengujian.

## 🚀 Teknologi yang Digunakan

**Back-End (Python):**
* [Flask](https://flask.palletsprojects.com/) - Web microframework
* [Scikit-learn](https://scikit-learn.org/stable/) - Machine Learning library (untuk `PassiveAggressiveClassifier` dan `TfidfVectorizer`)
* [Joblib](https://joblib.readthedocs.io/en/latest/) - Untuk menyimpan dan memuat model Python
* [NLTK (Natural Language Toolkit)](https://www.nltk.org/) - Untuk tokenisasi dan *stopwords*
* [Sastrawi](https://github.com/harisawang/Sastrawi) - Library *stemming* Bahasa Indonesia
* [NumPy](https://numpy.org/) - Untuk operasi numerik
* [Pandas](https://pandas.pydata.org/) - Untuk manipulasi data
* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/) - Untuk mengelola CORS di API

**Front-End (JavaScript):**
* [Vite](https://vitejs.dev/) - Next-generation front-end tooling (development server dan bundler)
* [Vanilla JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) - Untuk logika interaksi UI
* HTML & CSS

## 📁 Struktur Proyek



## 📁 Struktur Proyek

nama-proyek-ml-web/
├── backend/
│   ├── app.py                      # Flask API untuk inferensi model
│   ├── model_sentimen_indo_6emosi.pkl # Model ML yang sudah dilatih (PassiveAggressiveClassifier)
│   ├── tfidf_vectorizer_indo_6emosi.pkl # TF-IDF Vectorizer yang sudah dilatih
│   └── requirements.txt            # Daftar dependensi Python
├── frontend/
│   ├── index.html                  # Struktur utama halaman web (UI)
│   ├── main.js                     # Logika JavaScript untuk interaksi dan komunikasi API
│   ├── vite.config.js              # Konfigurasi Vite (default)
│   └── package.json                # Dependensi JavaScript untuk Vite
└── README.md                       # File ini


## ⚙️ Instalasi dan Menjalankan Proyek (Lokal)

Ikuti langkah-langkah di bawah ini untuk mengatur dan menjalankan aplikasi di komputer lokal Anda.

### Prasyarat

* **Python 3.9+**: Pastikan Python terinstal di sistem Anda.
* **Node.js dan npm/yarn**: Diperlukan untuk menjalankan proyek Front-end.
* **Microsoft C++ Build Tools (khusus Windows)**: Diperlukan untuk menginstal beberapa *package* Python seperti `scikit-learn`. Jika Anda mengalami *error* kompilasi saat `pip install`, unduh dan instal dari [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) dan pastikan komponen "Desktop development with C++" terpilih. **Setelah instalasi, restart komputer Anda.**

### Langkah-langkah Instalasi

1.  **Clone Repository ini:**
    ```bash
    git clone [https://github.com/namapenggunaanda/Sentiment-Analysis-ID-Deployment.git](https://github.com/namapenggunaanda/Sentiment-Analysis-ID-Deployment.git) # Ganti dengan URL repo Anda
    cd Sentiment-Analysis-ID-Deployment
    ```

2.  **Siapkan Back-End (Python Flask):**
    * **Pindahkan Model dan Vectorizer:** Pastikan file `model_sentimen_indo_6emosi.pkl` dan `tfidf_vectorizer_indo_6emosi.pkl` yang sudah Anda unduh dari Google Colab berada di dalam folder `backend/`.
    * **Buat Lingkungan Virtual:**
        ```bash
        python -m venv venv_deploy_ml
        ```
    * **Aktifkan Lingkungan Virtual:**
        * Windows (PowerShell): `.\venv_deploy_ml\Scripts\Activate.ps1`
        * Windows (Command Prompt): `venv_deploy_ml\Scripts\activate.bat`
        * macOS/Linux: `source venv_deploy_ml/bin/activate`
    * **Navigasi ke Direktori Backend:**
        ```bash
        cd backend
        ```
    * **Instal Dependensi Python:**
        ```bash
        pip install -r requirements.txt
        ```

3.  **Siapkan Front-End (Vite JavaScript):**
    * **Buka Terminal Baru** di VS Code (biarkan terminal back-end tetap berjalan).
    * **Navigasi ke Direktori Frontend:**
        ```bash
        cd frontend
        ```
    * **Instal Dependensi JavaScript:**
        ```bash
        npm install
        ```

### Menjalankan Aplikasi

1.  **Jalankan Back-End API:**
    * Di terminal yang aktif di direktori `backend/` (`(venv_deploy_ml) PS C:\nama-proyek-ml-web\backend>`), jalankan:
        ```bash
        python app.py
        ```
    * API akan berjalan di `http://localhost:5000/`. Biarkan terminal ini tetap terbuka.

2.  **Jalankan Front-End Web Server:**
    * Di terminal yang aktif di direktori `frontend/` (`PS C:\nama-proyek-ml-web\frontend>`), jalankan:
        ```bash
        npm run dev
        ```
    * Vite akan memulai server development. Buka URL yang diberikan (misalnya `http://localhost:5173/`) di browser Anda.

3.  **Gunakan Aplikasi:**
    * Di browser, masukkan teks berbahasa Indonesia ke dalam kotak input.
    * Klik "Analisis Sentimen" untuk melihat prediksi emosi.


    ## 🤝 Kontribusi

Kontribusi dalam bentuk *issue*, *bug report*, atau *pull request* sangat diterima.

## 📄 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

---
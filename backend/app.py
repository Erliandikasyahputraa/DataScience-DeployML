import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)
# Mengizinkan Cross-Origin Resource Sharing (CORS) untuk semua origin.
# PENTING: Untuk produksi, batasi ini ke domain frontend Anda saja.
CORS(app)

# Mendefinisikan path ke file model dan vectorizer.
# os.path.dirname(__file__) akan mendapatkan direktori tempat app.py berada.
# Path ke model dan vectorizer Anda
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_svm.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'tfidf_vectorizer.pkl')

# Variabel global untuk menyimpan model dan vectorizer yang dimuat.
model_svm = None
vectorizer = None

# --- MUAT MODEL DAN VECTORIZER SAAT APLIKASI DIMULAI ---
# Blok try-except untuk menangani kesalahan saat memuat file.
try:
    # Memeriksa apakah kedua file model ada di direktori yang ditentukan.
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        # Memuat model SVM dan TF-IDF Vectorizer menggunakan joblib.
        model_svm = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("Model SVM dan TF-IDF Vectorizer berhasil dimuat!")
    else:
        # Pesan error jika file tidak ditemukan.
        print(f"ERROR: File model atau vectorizer tidak ditemukan. Pastikan ada di {os.path.dirname(__file__)}")
except Exception as e:
    # Menangkap dan mencetak error jika gagal memuat model/vectorizer.
    print(f"ERROR: Gagal memuat model atau vectorizer. Detail: {e}")

# --- HALAMAN UTAMA (ROOT ENDPOINT) ---
# Endpoint ini akan diakses ketika pengguna mengunjungi URL dasar server.
@app.route('/')
def home():
    return "API Analisis Sentimen Anda sudah berjalan. Kunjungi '/sentimen' dengan metode POST."

# --- ENDPOINT UNTUK ANALISIS SENTIMEN TEKS ---
# Endpoint ini akan menerima permintaan POST untuk menganalisis sentimen teks.
@app.route('/sentimen', methods=['POST'])
def sentimen():
    if model_svm is None or vectorizer is None:
        return jsonify({"error": "Model atau Vectorizer tidak tersedia. Server bermasalah."}), 500

    try:
        data = request.get_json(force=True)

        if 'teks' not in data:
            return jsonify({"error": "Data input harus memiliki kunci 'teks'."}), 400

        input_teks = data['teks']

        if not isinstance(input_teks, str):
            if isinstance(input_teks, list) and all(isinstance(i, str) for i in input_teks):
                pass
            else:
                return jsonify({"error": "Input 'teks' harus berupa string tunggal atau list of strings."}), 400
        else:
            input_teks = [input_teks]

        print(f"DEBUG: Teks input diterima: {input_teks}")

        teks_tfidf = vectorizer.transform(input_teks)
        print(f"DEBUG: Bentuk TF-IDF setelah transform: {teks_tfidf.shape}")

        # Lakukan prediksi
        prediction = model_svm.predict(teks_tfidf)

        print(f"DEBUG: Prediksi mentah dari model: {prediction}")
        print(f"DEBUG: Tipe data prediksi mentah: {type(prediction)}")

        # --- PERUBAHAN DI SINI ---
        # Karena model memprediksi langsung string, kita ambil saja langsung nilai stringnya.
        # prediction.tolist() akan mengonversi array numpy ke list Python.
        # prediction.tolist()[0] akan mengambil elemen pertama dari list (yaitu string emosi).
        prediksi_label_string = prediction.tolist()[0]
        
        # Sekarang, hasil sentimen adalah string yang langsung dari model
        hasil_sentimen = prediksi_label_string
        
        # --- Opsional: Jika Anda ingin memetakan 'sadness' ke 'Sedih' (Bahasa Indonesia) ---
        # Ini hanya jika model Anda memprediksi label dalam bahasa Inggris (joy, sadness, etc.)
        # dan Anda ingin menampilkannya dalam Bahasa Indonesia.
        sentimen_terjemahan = {
            'joy': 'Bahagia',
            'sadness': 'Sedih',
            'anger': 'Marah',
            'fear': 'Takut',
            'surprise': 'Terkejut',
            'neutral': 'Netral', # Mungkin ada netral atau kategori lain
            # Tambahkan label lain jika model Anda memprediksinya
        }
        hasil_sentimen_terjemahan = sentimen_terjemahan.get(prediksi_label_string.lower(), prediksi_label_string) # .lower() jika prediksi_label_string bisa kapital

        return jsonify(
            teks_input=input_teks[0],
            prediksi_sentimen_mentah=prediksi_label_string, # Berikan juga prediksi mentahnya
            prediksi_sentimen_teks=hasil_sentimen_terjemahan # Tampilkan yang sudah diterjemahkan
        )

    except Exception as e:
        print(f"DEBUG: Error di endpoint /sentimen: {e}")
        return jsonify({"error": str(e), "pesan": "Terjadi kesalahan. Pastikan input JSON benar, contoh: {'teks': 'ini teksnya'}"}), 500
# --- JALANKAN APLIKASI FLASK ---
# Bagian ini hanya akan dieksekusi jika script dijalankan secara langsung (bukan diimpor).
if __name__ == '__main__':
    # app.run() akan menjalankan server pengembangan Flask.
    # host='0.0.0.0' membuat server dapat diakses dari IP lain di jaringan lokal.
    # port=5000 adalah port default.
    # debug=True mengaktifkan mode debug, yang berguna untuk pengembangan (reload otomatis, debugger).
    app.run(host='0.0.0.0', port=5000, debug=True)

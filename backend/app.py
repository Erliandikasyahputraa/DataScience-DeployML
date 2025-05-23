import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk

app = Flask(__name__)
CORS(app) # Mengizinkan Cross-Origin Resource Sharing (CORS)

# --- Konfigurasi NLTK Data Path ---
# Ini akan menambahkan direktori tempat app.py berada ke path pencarian NLTK.
# Penting agar NLTK dapat menemukan data seperti stopwords dan punkt jika diunduh di sana.
nltk.data.path.append(os.path.dirname(__file__))

# --- NLTK Downloads (Penting untuk lingkungan deployment) ---
# Kode ini akan memastikan data NLTK tersedia saat aplikasi dijalankan.
# Menggunakan 'except Exception' untuk menangani berbagai jenis error download NLTK.
try:
    nltk.data.find('corpora/stopwords')
except Exception: # Menggunakan Exception yang lebih umum
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')
    print("NLTK stopwords downloaded.")

try:
    nltk.data.find('tokenizers/punkt')
except Exception: # Menggunakan Exception yang lebih umum
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')
    print("NLTK punkt tokenizer downloaded.")

# Inisialisasi komponen pra-pemrosesan teks
factory = StemmerFactory()
stemmer_id = factory.create_stemmer()
list_stopwords = set(stopwords.words('indonesian'))

# --- Fungsi Pra-pemrosesan Teks (Harus sama persis dengan yang di Colab) ---
def clean_text_for_model(text):
    """
    Membersihkan dan memproses teks input agar sesuai dengan format yang diharapkan model.
    Langkah-langkah: lowercase, hapus mention/URL/karakter khusus, tokenisasi,
    hapus stopwords, dan stemming.
    """
    text = str(text).lower()
    text = re.sub(r'\[USERNAME\]', ' ', text) # Remove [USERNAME] mentions
    text = re.sub(r'\[URL\]', ' ', text) # Remove [URL] mentions
    text = re.sub(r'\[.*?\]', ' ', text) # Remove other text in square brackets
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text) # Remove URLs
    text = re.sub(r'<.*?>+', ' ', text) # Remove HTML tags
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text) # Replace punctuation with space
    text = re.sub(r'\n', ' ', text) # Remove newlines
    text = re.sub(r'\w*\d\w*', ' ', text) # Remove words containing numbers
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) # Remove non-ASCII characters (emojis, etc.)
    text = re.sub(r'\s+', ' ', text).strip() # Replace multiple spaces with single space and strip whitespace

    tokens = word_tokenize(text)
    cleaned_tokens = []
    for token in tokens:
        if token not in list_stopwords: # Filter stopwords
            stemmed_token = stemmer_id.stem(token) # Perform stemming
            cleaned_tokens.append(stemmed_token)
    cleaned_text = " ".join(cleaned_tokens)
    return cleaned_text

# Path ke file model dan vectorizer yang sudah Anda unduh dari Colab
# Menggunakan nama file yang Anda inginkan: model_svm.pkl dan tfidf_vectorizer.pkl
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_svm.pkl')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'tfidf_vectorizer.pkl')

# Variabel global untuk model dan vectorizer
model_sentimen = None
vectorizer = None

# --- MUAT MODEL DAN VECTORIZER SAAT APLIKASI DIMULAI ---
# Blok try-except untuk menangani kesalahan saat memuat file model.
try:
    if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
        model_sentimen = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("Model sentimen (dari model_svm.pkl) dan TF-IDF Vectorizer berhasil dimuat!")
    else:
        print(f"ERROR: File model atau vectorizer tidak ditemukan. Pastikan ada di {os.path.dirname(__file__)}")
except Exception as e:
    print(f"ERROR: Gagal memuat model atau vectorizer. Detail: {e}")

# --- HALAMAN UTAMA API (Root Endpoint) ---
# Endpoint ini akan diakses ketika pengguna mengunjungi URL dasar server.
@app.route('/')
def home():
    """
    Endpoint root untuk API. Mengembalikan pesan sederhana untuk mengindikasikan bahwa API berjalan.
    """
    return "API Analisis Sentimen Bahasa Indonesia Anda (6 Emosi) sudah berjalan. Kunjungi '/sentimen' dengan metode POST."

# --- ENDPOINT UNTUK ANALISIS SENTIMEN TEKS ---
# Endpoint ini akan menerima permintaan POST untuk menganalisis sentimen teks.
@app.route('/sentimen', methods=['POST'])
def sentimen():
    """
    Endpoint untuk memprediksi sentimen dari teks input.
    Menerima JSON dengan kunci 'teks'.
    Mengembalikan prediksi sentimen (misal: 'happy', 'anger', 'sadness', dll.).
    """
    # Periksa apakah model dan vectorizer berhasil dimuat
    if model_sentimen is None or vectorizer is None:
        return jsonify({"error": "Model atau Vectorizer tidak tersedia. Server bermasalah."}), 500

    try:
        # Ambil data JSON dari request
        data = request.get_json(force=True)

        # Validasi bahwa kunci 'teks' ada dalam data
        if 'teks' not in data:
            return jsonify({"error": "Data input harus memiliki kunci 'teks'."}), 400

        input_teks_mentah = data['teks']

        # Pastikan input 'teks' adalah string tunggal
        if not isinstance(input_teks_mentah, str):
            if isinstance(input_teks_mentah, list) and all(isinstance(i, str) for i in input_teks_mentah):
                input_teks_mentah = input_teks_mentah[0] # Ambil elemen pertama jika dikirim sebagai list
            else:
                return jsonify({"error": "Input 'teks' harus berupa string tunggal."}), 400
        
        # Pra-pemrosesan teks input menggunakan fungsi yang sama seperti saat pelatihan
        cleaned_text = clean_text_for_model(input_teks_mentah)

        # Ubah teks bersih menjadi representasi TF-IDF menggunakan vectorizer yang sudah dimuat
        # vectorizer.transform() mengharapkan input berupa list of strings
        teks_tfidf = vectorizer.transform([cleaned_text])

        # Lakukan prediksi menggunakan model yang sudah dimuat
        prediction = model_sentimen.predict(teks_tfidf)
        
        # Hasil prediksi adalah label string langsung (misal: 'happy', 'anger', dll.)
        hasil_sentimen_teks = prediction.tolist()[0] # Ambil elemen pertama dari array prediksi

        # Mengembalikan respons JSON dengan teks input, teks bersih, dan prediksi sentimen
        return jsonify(
            teks_input=input_teks_mentah,
            teks_bersih=cleaned_text,
            prediksi_sentimen=hasil_sentimen_teks # Kunci ini akan dicocokkan oleh main.js
        )

    except Exception as e:
        # Tangani kesalahan yang mungkin terjadi selama proses prediksi
        print(f"DEBUG: Error di endpoint /sentimen: {e}")
        return jsonify({"error": str(e), "pesan": "Terjadi kesalahan. Pastikan input JSON Anda benar, contoh: {'teks': 'ini teksnya'}"}), 500

# --- JALANKAN APLIKASI FLASK ---
# Bagian ini hanya akan dieksekusi jika script dijalankan secara langsung (bukan diimpor).
if __name__ == '__main__':
    # app.run() akan menjalankan server pengembangan Flask.
    # host='0.0.0.0' membuat server dapat diakses dari IP lain di jaringan lokal.
    # port=5000 adalah port default.
    # debug=True mengaktifkan mode debug, yang berguna untuk pengembangan (reload otomatis, debugger).
    # Untuk produksi, ubah debug=False.
    app.run(host='0.0.0.0', port=5000, debug=True)
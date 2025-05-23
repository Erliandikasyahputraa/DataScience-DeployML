import joblib
import pandas as pd
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import re # Untuk membersihkan teks

# --- 1. Simulasi Dataset (Ganti dengan dataset Anda jika ada) ---
# Ini adalah contoh dataset yang mirip dengan struktur data sentimen Twitter
# Dalam proyek nyata, Anda akan memuat data dari file CSV/JSON
data = {
    'text': [
      "Aku suka produk ini, sungguh luar biasa!",
"Film ini benar-benar jelek dan membosankan.",
"Layanan pelanggannya sangat bagus, sangat membantu.",
"Aku tidak punya perasaan kuat tentang ini, ya lumayanlah.",
"Pengalaman terburuk yang pernah ada, benar-benar kecewa.",
"Sangat merekomendasikan, berfungsi sempurna bagiku.",
"Lumayanlah, tidak ada yang istimewa tapi berfungsi.",
"Sangat senang dengan pembelianku!",
"Tidak akan pernah membeli ini lagi, buang-buang uang.",
"Cukup bagus, tapi bisa lebih baik."
    ],
    'sentiment': [
        'positive',
        'negative',
        'positive',
        'neutral',
        'negative',
        'positive',
        'neutral',
        'positive',
        'negative',
        'positive'
    ]
}
df = pd.DataFrame(data)

print("Dataset awal:")
print(df.head())
print("-" * 30)

# --- 2. Pra-pemrosesan Teks ---
# Fungsi sederhana untuk membersihkan teks
def clean_text(text):
    text = text.lower() # Ubah jadi huruf kecil
    text = re.sub(r'[^a-z\s]', '', text) # Hapus karakter non-alfabet
    text = re.sub(r'\s+', ' ', text).strip() # Hapus spasi berlebih
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

print("\nDataset setelah dibersihkan:")
print(df[['text', 'cleaned_text']].head())
print("-" * 30)

# --- 3. Peta Label Sentimen ke Angka ---
# SVM biasanya bekerja dengan label numerik (0, 1, 2, dst.)
sentiment_mapping = {'negative': -1, 'neutral': 0, 'positive': 1}
df['sentiment_numeric'] = df['sentiment'].map(sentiment_mapping)

# --- 4. Pisahkan Data Latih dan Data Uji ---
X = df['cleaned_text']
y = df['sentiment_numeric']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nJumlah data training: {len(X_train)}")
print(f"Jumlah data testing: {len(X_test)}")
print("-" * 30)

# --- 5. Inisialisasi dan Latih TfidfVectorizer ---
# Vectorizer akan belajar kosa kata dan bobot TF-IDF dari data pelatihan
vectorizer = TfidfVectorizer(max_features=5000) # Batasi jumlah fitur untuk efisiensi
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test) # Transform data uji, jangan fit_transform

print(f"\nUkuran fitur TF-IDF (training): {X_train_tfidf.shape}")
print("-" * 30)

# --- 6. Latih Model SVM ---
# Untuk analisis sentimen teks, 'linear' kernel seringkali performanya baik
model_svm = svm.SVC(kernel='linear', probability=True, random_state=42)
model_svm.fit(X_train_tfidf, y_train)

print("\nModel SVM berhasil dilatih!")

# --- 7. Evaluasi Model ---
y_pred = model_svm.predict(X_test_tfidf)
print(f"\nAkurasi model pada data uji: {accuracy_score(y_test, y_pred):.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['negative', 'neutral', 'positive']))
print("-" * 30)

# --- 8. Simpan Model SVM dan TF-IDF Vectorizer ---
# Penting: keduanya harus disimpan agar saat deploy bisa mengubah teks baru
joblib.dump(model_svm, 'backend/model_svm.pkl')
joblib.dump(vectorizer, 'backend/tfidf_vectorizer.pkl')

print("\nModel SVM dan TF-IDF Vectorizer berhasil disimpan di folder 'backend/'!")
print("Sekarang Anda bisa melanjutkan ke langkah deployment.")
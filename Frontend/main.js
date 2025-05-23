document.addEventListener('DOMContentLoaded', () => {
  const analisisBtn = document.getElementById('analisis-btn');
  const teksInput = document.getElementById('teks-input');
  const hasilPrediksiDiv = document.getElementById('hasil-prediksi');
  const errorMsgDiv = document.getElementById('error-msg');

  analisisBtn.addEventListener('click', async () => {
    // Kosongkan pesan error dan hasil sebelumnya
    hasilPrediksiDiv.textContent = '';
    hasilPrediksiDiv.className = ''; // Hapus kelas warna
    errorMsgDiv.textContent = '';

    const teks = teksInput.value.trim(); // Ambil teks dan hapus spasi di awal/akhir

    if (!teks) {
      errorMsgDiv.textContent = 'Mohon masukkan teks untuk dianalisis.';
      return;
    }

    // Buat objek data yang akan dikirim ke API Flask
    const dataUntukAPI = {
      teks: teks // Kunci 'teks' harus sama dengan yang diharapkan di app.py Anda
    };

    try {
      // URL API Flask Anda
      const apiEndpoint = 'http://localhost:5000/sentimen'; // Ganti /prediksi jadi /sentimen

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataUntukAPI),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Terjadi kesalahan pada server.');
      }

      const result = await response.json();
      
      // Tampilkan hasil prediksi
      hasilPrediksiDiv.textContent = `Sentimen: ${result.prediksi_sentimen_teks}`;
      
      // Tambahkan kelas CSS untuk warna sentimen
      if (result.prediksi_sentimen_teks === 'Positif') {
        hasilPrediksiDiv.classList.add('positif');
      } else if (result.prediksi_sentimen_teks === 'Netral') {
        hasilPrediksiDiv.classList.add('netral');
      } else if (result.prediksi_sentimen_teks === 'Negatif') {
        hasilPrediksiDiv.classList.add('negatif');
      }

    } catch (error) {
      console.error('Error saat melakukan analisis sentimen:', error);
      errorMsgDiv.textContent = `Gagal menganalisis sentimen: ${error.message}`;
    }
  });
});
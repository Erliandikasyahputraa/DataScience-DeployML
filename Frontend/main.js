document.addEventListener('DOMContentLoaded', () => {
  const analisisBtn = document.getElementById('analisis-btn');
  const teksInput = document.getElementById('teks-input');
  const hasilPrediksiDiv = document.getElementById('hasil-prediksi');
  const errorMsgDiv = document.getElementById('error-msg');

  // Set teks awal saat DOM siap
  hasilPrediksiDiv.textContent = 'PROSES: MENUNGGU DATA';

  analisisBtn.addEventListener('click', async () => {
    // Kosongkan pesan error dan hasil sebelumnya
    hasilPrediksiDiv.textContent = ''; // Kosongkan teks hasil
    hasilPrediksiDiv.className = ''; // Hapus semua kelas warna sebelumnya
    errorMsgDiv.textContent = '';

    const teks = teksInput.value.trim(); // Ambil teks dan hapus spasi di awal/akhir

    if (!teks) {
      errorMsgDiv.textContent = 'ERROR: MASUKKAN TEKS UNTUK ANALISIS.';
      hasilPrediksiDiv.textContent = 'PROSES: ERROR INPUT';
      hasilPrediksiDiv.classList.add('unknown'); // Kelas default error
      return;
    }

    // Tampilkan pesan loading/proses
    hasilPrediksiDiv.textContent = 'PROSES: MENGANALISIS...';
    hasilPrediksiDiv.classList.add('unknown'); // Warna default saat loading

    // Buat objek data yang akan dikirim ke API Flask
    const dataUntukAPI = {
      teks: teks
    };

    try {
      // URL API Flask Anda. Saat development lokal, ini adalah 'http://localhost:5000/sentimen'
      // Saat Anda deploy back-end ke server publik, GANTI URL INI!
      // Contoh: 'https://nama-aplikasi-anda.herokuapp.com/sentimen' atau 'https://url-cloud-run-anda/sentimen'
      const apiEndpoint = 'http://localhost:5000/sentimen'; 

      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataUntukAPI),
      });

      // Cek apakah response berhasil (status code 2xx)
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'SERVER ERROR: RESPON TIDAK VALID.');
      }

      const result = await response.json();
      
      // Ambil label sentimen langsung dari respons back-end
      const predictedSentiment = result.prediksi_sentimen; 

      // Tampilkan hasil prediksi
      hasilPrediksiDiv.textContent = `SENTIMEN: ${predictedSentiment.toUpperCase()}`;
      
      // Hapus kelas yang ada dan tambahkan kelas baru sesuai sentimen
      hasilPrediksiDiv.className = ''; // Reset semua kelas
      hasilPrediksiDiv.classList.add(predictedSentiment.toLowerCase()); // Tambahkan kelas sesuai nama emosi
      
    } catch (error) {
      console.error('SERVER ERROR:', error);
      hasilPrediksiDiv.textContent = 'PROSES: GAGAL ANALISIS'; // Pesan error di hasil
      hasilPrediksiDiv.className = 'unknown'; // Kelas default untuk error
      errorMsgDiv.textContent = `ERROR: ${error.message}`; // Pesan error detail
    }
  });
});
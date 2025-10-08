# project-b02
Tugas Project per Kelompok
Jonathan Hans Emanuelle 2406414025
Alexius Christhoper Wijaya 2406496164
Jovian Felix Rustan 2406360016
Aufa Daffa' Satriatama 2406426321
Mirza Radithya Ramadhana 2406405563 
Jovanus Irwan Susanto 2406434140



Deskripsi

Ballistic adalah sebuah website e-commerce peralatan olahraga yang dirancang untuk mempermudah pengguna dalam membeli, menjual, dan berinteraksi seputar perlengkapan olahraga secara praktis dan personal. Platform ini ditujukan bagi pecinta olahraga maupun penjual perlengkapan olahraga yang ingin memiliki satu tempat untuk bertransaksi, berbagi pengalaman, serta mengelola akun dan produk dengan efisien. Produk yang dijual meliputi baju olahraga, celana, bola, botol minum, dan kaus kaki, lengkap dengan informasi harga, stok, ukuran, dan ulasan pengguna lainnya.

Salah satu keunggulan Ballistic adalah adanya modul rekomendasi ukuran berbasis berat dan tinggi badan, di mana pengguna cukup memasukkan data tubuh mereka untuk mendapatkan rekomendasi ukuran yang sesuai (S, M, L, atau XL). Fitur ini membantu pengguna memilih produk dengan lebih akurat dan mengurangi risiko kesalahan ukuran saat berbelanja online. Selain itu, terdapat modul review produk yang memungkinkan pengguna memberikan komentar dan rating terhadap barang yang telah dibeli. Review dengan rating tertinggi akan muncul di bagian atas, sehingga calon pembeli dapat menilai kualitas produk dengan cepat dan objektif.

Proses transaksi di Ballistic didukung oleh modul pembelian produk yang mengatur seluruh tahapan pembelian mulai dari pemilihan produk, konfirmasi pembayaran melalui saldo internal, hingga proses verifikasi oleh admin. Transaksi akan masuk ke status pending sebelum disetujui oleh admin untuk memastikan keaslian dan keamanan pembelian. Setelah disetujui, saldo pembeli otomatis terpotong dan saldo penjual bertambah.

Di sisi manajemen, terdapat dua modul yang hanya dapat diakses oleh admin: modul News dan modul Voucher. Modul News digunakan untuk membuat dan mengelola berita seputar promosi, event olahraga, maupun pengumuman penting dari toko. Sedangkan modul Voucher digunakan untuk membuat, memperbarui, atau menghapus kode promo dan potongan harga yang berlaku. Kedua modul ini membantu admin menjaga informasi dan promosi toko agar selalu menarik dan relevan bagi pengguna.

Selain berfokus pada transaksi, Ballistic juga membangun sisi komunitas melalui modul Forum Diskusi, tempat pengguna dapat membuat postingan, berdiskusi, dan berbagi tips seputar olahraga atau pengalaman menggunakan produk. Forum ini menjadikan Ballistic bukan hanya platform jual beli, tetapi juga ruang interaktif bagi komunitas olahraga.

Dengan integrasi keenam modul tersebut — Admin News, Admin Voucher, Pembelian Produk, Review Produk, Berat Badan, dan Forum Diskusi — Ballistic menghadirkan pengalaman belanja yang lebih cerdas, efisien, dan interaktif. Platform ini tidak hanya membantu pengguna mendapatkan produk yang sesuai, tetapi juga membangun ekosistem olahraga digital yang aman, aktif, dan saling terhubung.

Modul Produk

1. Modul Review Produk (Aufa Daffa)

Modul ini menampilkan ulasan pengguna terhadap produk peralatan olahraga yang dijual di website. Setiap pengguna dapat memberikan komentar dan penilaian berupa bintang (1–5). Sistem akan otomatis mengurutkan ulasan berdasarkan nilai bintang tertinggi, sehingga review dengan rating 5 bintang akan tampil paling atas. Hal ini bertujuan agar pengguna lain dapat langsung melihat penilaian terbaik dari pelanggan sebelumnya dan meningkatkan kepercayaan terhadap produk. Admin atau penjual juga dapat melihat rata-rata rating untuk memantau kualitas produknya.
 
2. Modul Forum (Mirza)

Modul Forum berfungsi sebagai wadah interaksi antar pengguna untuk berdiskusi mengenai olahraga, produk, maupun tips penggunaan perlengkapan. Pengguna dapat membuat postingan baru, membaca diskusi dari pengguna lain, mengedit posting mereka, serta menghapus komentar atau topik yang tidak relevan. Forum ini juga dapat dimoderasi oleh admin untuk menjaga kenyamanan dan etika diskusi. Melalui fitur ini, Ballistic tidak hanya menjadi platform jual beli, tetapi juga komunitas bagi para pecinta olahraga.

 3. Modul Rekomendasi Ukuran (Baju dan Celana) (Jovian)

Modul ini digunakan untuk menyimpan data tinggi dan berat pengguna yang menjadi dasar bagi sistem rekomendasi ukuran. Setiap pengguna dapat menambahkan data berat badan mereka, memperbaruinya seiring waktu, atau menghapus data lama yang tidak relevan. Modul ini memiliki relasi one-to-many dengan pembelian atau produk, karena satu pengguna bisa memiliki beberapa data pengukuran yang digunakan untuk menyesuaikan rekomendasi ukuran pakaian (S, M, L, XL). Fitur ini membuat pengalaman belanja menjadi lebih personal dan akurat.

4. Modul Create News (Jovanus)

Modul News hanya dapat diakses oleh admin dan berfungsi untuk mengelola berita resmi yang berkaitan dengan promosi, event olahraga, maupun pengumuman penting dari Ballistic. Admin dapat membuat, membaca, memperbarui, dan menghapus (CRUD) berita sesuai kebutuhan. Setiap berita akan muncul di halaman utama atau menu informasi pengguna, membantu menjaga komunikasi antara pihak toko dan pelanggan. Dengan adanya modul ini, platform selalu menampilkan informasi terbaru, relevan, dan profesional..


5. Modul Tampilan Produk dan Pembelian ( Jonathan Hans Emanuelle)

Modul ini menangani seluruh proses pembelian produk oleh pengguna. Ketika pengguna membeli barang dan saldo mencukupi, sistem akan mencatat transaksi baru dengan status “Pending” untuk diverifikasi oleh admin. Setelah disetujui, saldo pembeli otomatis terpotong dan saldo penjual bertambah. Modul ini juga menampilkan daftar riwayat pembelian, status transaksi, serta detail produk yang dibeli. Admin dan pengguna dapat memantau pembelian melalui dashboard yang aman dan transparan.

6. Modul Voucher (Alexius Christhoper)

Modul Voucher juga bersifat eksklusif untuk admin dan digunakan untuk mengatur sistem diskon atau promo pembelian. Admin dapat membuat kode voucher baru, seperti potongan harga, cashback, atau promo kategori tertentu, serta menentukan masa berlaku dan syarat penggunaannya. Admin juga dapat melihat daftar voucher aktif, memperbarui informasi voucher, dan menghapus voucher yang sudah tidak berlaku. Modul ini mendukung strategi pemasaran toko agar lebih menarik dan meningkatkan penjualan produk olahraga di platform..


DATASET : https://www.kaggle.com/datasets/larysa21/retail-data-american-football-gear-sales

PWS : https://pbp.cs.ui.ac.id/jovian.felix/ballistic

Penjelasan User

1. Admin

Role Admin memiliki tingkat akses tertinggi dalam sistem Ballistic. User dengan role ini bertanggung jawab untuk mengawasi, mengatur, dan memverifikasi seluruh aktivitas penting di platform, khususnya yang berkaitan dengan transaksi dan konten publik. Admin memiliki akses penuh terhadap dua modul khusus, yaitu modul News dan modul Voucher.
Melalui modul News, admin dapat membuat, mengedit, dan menghapus berita atau pengumuman terkait promosi, event olahraga, maupun informasi penting lainnya. Sementara modul Voucher digunakan untuk mengatur kode promo, potongan harga, serta masa berlaku voucher yang dapat digunakan oleh pembeli. Selain itu, admin juga memiliki kemampuan untuk melihat data analitik sistem, seperti jumlah akun, total transaksi, transaksi gagal (karena saldo tidak cukup atau ditolak), dan produk paling populer.
Admin juga berperan penting dalam verifikasi transaksi pembelian, di mana setiap pembelian dengan status pending harus disetujui (approve) agar transaksi dinyatakan berhasil.
Batasan: User dengan role Admin tidak dapat memiliki role lain seperti Penjual atau Pembeli.
Tujuan utama: menjaga transparansi, keamanan, dan kelancaran seluruh proses dalam sistem Ballistic.

2. Penjual

Role Penjual memungkinkan user untuk menawarkan dan mengelola produk di platform melalui modul Pembelian (Produk). Penjual dapat membuat entri produk baru, melengkapi informasi seperti nama barang, deskripsi, kategori, stok, harga, dan gambar. Modul ini juga memungkinkan mereka untuk menghapus atau memperbarui data produk sesuai kebutuhan.
Penjual dapat memantau status transaksi produk mereka, apakah sedang dalam proses, berhasil, atau dibatalkan oleh admin. Selain itu, penjual juga bisa menerima review produk dari pembeli sebagai bentuk umpan balik yang membantu meningkatkan kualitas produk.
Hak akses utama: mengelola data produk dan memantau transaksi yang berkaitan dengan barang yang mereka jual.
Tujuan utama: memberikan kesempatan bagi user untuk membuka toko olahraga secara digital dan memperluas jangkauan penjualan mereka.

3. Pembeli

Role Pembeli berfungsi untuk memungkinkan user melakukan pencarian, pemilihan, dan pembelian produk olahraga yang dijual oleh para penjual di Ballistic. Melalui modul Pembelian Produk, pembeli dapat melakukan transaksi dengan saldo internal yang dimiliki, yang akan otomatis terpotong setelah admin menyetujui pembelian. Jika saldo tidak mencukupi, maka transaksi otomatis gagal.
Pembeli juga dapat memberikan review dan rating produk melalui modul Review, membantu pengguna lain dalam menilai kualitas barang. Selain itu, terdapat modul Berat Badan, di mana pembeli dapat memasukkan tinggi dan berat badan mereka untuk memperoleh rekomendasi ukuran produk (S, M, L, XL) yang sesuai.
Pembeli juga dapat berpartisipasi dalam modul Forum Diskusi, tempat berbagi pengalaman, bertanya seputar olahraga, dan berinteraksi dengan komunitas.
Hak akses utama: melihat katalog produk, melakukan pembelian, memberikan ulasan, dan ikut serta dalam forum.
Tujuan utama: memberikan pengalaman belanja yang mudah, akurat, dan interaktif bagi pengguna.
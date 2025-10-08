# project-b02
Tugas Project per Kelompok
Jonathan Hans Emanuelle 2406414025
Alexius Christhoper Wijaya 2406496164
Jovian Felix Rustan 2406360016
Aufa Daffa' Satriatama 2406426321
Mirza Radithya Ramadhana 2406405563 
Jovanus Irwan Susanto 2406434140



Deskripsi

Ballistic adalah sebuah website e-commerce peralatan olahraga yang dirancang untuk mempermudah pengguna dalam membeli dan menjual perlengkapan olahraga dengan cara yang praktis, personal, dan interaktif. Website ini ditujukan untuk para pecinta olahraga maupun penjual perlengkapan olahraga yang ingin memiliki satu tempat untuk melakukan digital transaksi, rekomendasi produk, serta pengelolaan akun yang efisien. Kategori utama produk yang dijual meliputi baju olahraga, celana, botol minum, bola, dan kaus kaki. Setiap produk dapat ditampilkan lengkap dengan ukuran, harga, stok, serta ulasan pengguna lainnya.

Salah satu fitur unggulan dari Ballistic adalah terdapat fitur rekomendasi ukuran cerdas, di mana pengguna cukup memasukkan tinggi dan berat badan mereka, lalu sistem akan secara otomatis merekomendasikan ukuran yang sesuai (S, M, L, atau XL).
Fitur ini bekerja seperti sistem prediksi sederhana berdasarkan data tinggi dan berat badan serta menggunakan acuan perhitungan BMI (Body Mass Index). Hasil rekomendasi tersebut kemudian digunakan sebagai filter di fitur pencarian, sehingga ketika pengguna menekan tombol Search, produk yang ditampilkan akan disesuaikan dengan ukuran yang direkomendasikan.

Dengan demikian, pengguna tidak perlu bingung menentukan ukuran yang pas saat berbelanja online. Selain itu, aplikasi ini dilengkapi dengan fitur review produk yang mengurutkan ulasan dari bintang tertinggi, sehingga produk dengan penilaian terbaik selalu tampil di posisi atas. Hal ini membantu calon pembeli melihat kualitas produk secara objektif dan meningkatkan kepercayaan terhadap toko

Ballistic juga menghadirkan fitur saldo dan pembayaran internal, di mana pengguna bisa mengisi saldo pada halaman profil dan menggunakannya untuk bertransaksi. Saldo ini terpotong secara otomatis setiap kali pembelian dilakukan, sehingga proses pembayaran menjadi lebih cepat dan aman. Selain itu saldo penjual akan masuk jika transaksi telah berhasil. 

Pada bagian profil akun, pengguna dapat melihat saldo yang dimiliki, deskripsi akun, daftar barang yang telah dibeli, serta daftar produk yang dijual (jika pengguna juga memiliki akun penjual). Jika pengguna hanya berperan sebagai pembeli dan belum memiliki akun penjual, maka akan muncul pesan “Maaf, Anda belum membuat akun penjualan.”. ”Sebaliknya, jika pengguna adalah penjual tetapi belum pernah membeli barang, maka akan muncul pesan “Maaf, Anda belum melakukan pembelian barang.”. Selain itu, tombol Beli akan otomatis dinonaktifkan apabila penjual mencoba membeli produknya sendiri, untuk mencegah transaksi tidak valid.

Dengan seluruh fitur tersebut, Ballistic tidak hanya berfungsi sebagai toko peralatan olahraga biasa, tetapi juga memberikan pengalaman berbelanja yang cerdas, efisien, dan aman. Aplikasi ini membantu pengguna mendapatkan produk yang sesuai kebutuhan mereka, mempermudah penjual mengelola barang dagangan, dan menciptakan ekosistem jual beli alat olahraga yang terpercaya dan mudah digunakan.



Modul Produk

1. Modul Review Produk (Aufa Daffa)

Modul ini menampilkan ulasan (review) pengguna terhadap produk peralatan olahraga yang dijual di website. Setiap pengguna dapat memberikan komentar dan penilaian berupa bintang (1–5). Sistem akan otomatis mengurutkan ulasan berdasarkan nilai bintang tertinggi, sehingga review dengan rating 5 bintang akan tampil paling atas. Hal ini bertujuan agar pengguna lain bisa langsung melihat penilaian terbaik dari pelanggan sebelumnya dan meningkatkan kepercayaan terhadap produk. Admin atau penjual juga dapat melihat rata-rata rating untuk memantau kualitas produknya.
 
2. Modul Pembayaran dan Saldo (Jovan)

Modul ini mengatur sistem pembayaran dan penyimpanan saldo pengguna. Pengguna dapat melakukan top up saldo melalui halaman profil, dan saldo tersebut digunakan untuk membeli produk di website. Saat pembelian dilakukan, saldo akan otomatis terpotong sesuai harga barang. Jika saldo tidak cukup maka akan menampilkan notifikasi saldo tidak cukup dan harus top up. Jika berhasil maka akan muncul invoice pembayaran serta saldo penjual akan bertambah. Dengan sistem saldo ini, proses pembayaran menjadi lebih cepat dan efisien tanpa harus keluar dari aplikasi.

 3. Modul Rekomendasi Ukuran (Baju dan Celana) (Jovian)

Modul ini berfungsi untuk membantu pengguna memilih ukuran produk yang sesuai berdasarkan data tinggi dan berat badan. Saat pengguna memasukkan tinggi dan berat badan, sistem akan menghitung estimasi ukuran yang cocok (misalnya: S, M, L, XL) menggunakan logika sederhana seperti perhitungan mirip BMI (Body Mass Index). Setelah ukuran direkomendasikan, hasil tersebut akan digunakan untuk memfilter hasil pencarian di tombol “Search”. Misalnya, jika pengguna direkomendasikan ukuran “L”, maka hasil pencarian otomatis akan menampilkan produk dengan ukuran “L” terlebih dahulu. Fitur ini meningkatkan pengalaman pengguna dengan memberikan rekomendasi yang personal dan efisien.

4. Modul Profil Akun (Mirza)

Modul ini menampilkan informasi lengkap tentang akun pengguna, termasuk saldo yang dimiliki, deskripsi akun, daftar barang yang telah dibeli, serta daftar produk yang dijual (jika pengguna memiliki akun penjual). Jika pengguna hanya pembeli dan belum membuat akun penjual, maka pada bagian “Produk yang Dijual” akan muncul pesan: “Maaf, Anda belum membuat akun penjualan.”

Sebaliknya, jika pengguna hanya penjual dan belum membeli barang, maka pada bagian “Barang yang Dibeli” akan muncul pesan: “Maaf, Anda belum melakukan pembelian barang.”. Fitur ini juga memungkinkan pengguna untuk mengatur saldo dan mengedit deskripsi profil mereka agar lebih personal.


5. Modul Tampilan Produk dan Pembelian ( Jonathan Hans Emanuelle)

Modul ini menampilkan daftar produk peralatan olahraga yang dijual di platform. Terdapat tombol “Beli” di setiap produk, namun sistem akan mematikan tombol tersebut (disable) apabila penjual mencoba membeli produknya sendiri. Hal ini mencegah aktivitas pembelian tidak valid. Modul ini juga akan menampilkan produk yang ukurannya sudah dianjurkan pada baju dan celana. Selain itu nanti juga akan menampilkan barang-barang lain yaitu  botol minum (dalam milliliter), kaos kaki, dan bola sehingga pengguna dapat lebih mudah mencari barang sesuai kebutuhan. 

6. Admin Dashboard (Alexius Christhoper)

Salah satu fitur utama dalam modul *Admin & Analitik* Ballistic adalah *verifikasi pembelian, yang memastikan setiap transaksi berlangsung aman dan valid. Ketika pengguna melakukan pembelian dan saldo mencukupi, transaksi akan masuk ke **antrian dengan status “Pending”* hingga admin melakukan verifikasi. Melalui dashboard, admin dapat melihat daftar transaksi menunggu persetujuan beserta detail seperti nama pembeli, produk, harga, dan waktu pembelian. Admin dapat menekan tombol *Approve (✔)* untuk menyetujui transaksi — saldo pembeli akan otomatis terpotong dan saldo penjual bertambah — atau *Reject (❌)* untuk menolak transaksi tanpa mengubah saldo. Semua aktivitas tersebut tercatat dalam log sistem untuk keperluan audit dan pelacakan.

Selain itu, modul ini dilengkapi dengan *dashboard analitik* yang menampilkan data penting seperti *jumlah akun pengguna, **total transaksi, serta statistik **transaksi berhasil, **gagal karena saldo tidak cukup, dan **gagal karena ditolak admin. Admin juga dapat melihat **kategori produk yang paling banyak dibeli*, membantu dalam memahami tren penjualan dan mengoptimalkan strategi toko. Data ini disajikan melalui grafik dan diagram interaktif, memberikan admin kontrol penuh untuk memantau performa platform, menjaga keamanan transaksi, serta mengambil keputusan berdasarkan data secara efisien dan transparan.


DATASET : https://www.kaggle.com/datasets/larysa21/retail-data-american-football-gear-sales

PWS : https://pbp.cs.ui.ac.id/jovian.felix/ballistic

Penjelasan User

1. Admin
Role Admin adalah peran dengan tingkat akses tertinggi. User dengan role ini bertanggung jawab untuk mengawasi dan mengontrol aktivitas platform, khususnya yang berkaitan dengan transaksi.
Hak akses utama:
- Melihat daftar transaksi yang sedang menunggu persetujuan. Ini berarti admin dapat melakukan verifikasi terhadap transaksi sebelum transaksi tersebut benar-benar dianggap sah.
- Memberikan keputusan terhadap transaksi, apakah disetujui atau ditolak, tergantung pada hasil pemeriksaan validitas transaksi.
- Mengakses data statistik platform, misalnya: Jumlah akun yang terdaftar, total transaksi yang terjadi dalam sistem (baik sukses maupun gagal), serta Daftar produk paling populer atau paling banyak dibeli, yang bisa digunakan untuk analisis tren pembelian.
Batasan:
- User yang sudah memiliki role Admin tidak bisa memiliki role lain seperti Penjual atau Pembeli.
Tujuan utama: menjaga transparansi, keamanan, dan kelancaran jalannya sistem transaksi.

2. Penjual
Role Penjual adalah peran yang memungkinkan user untuk menawarkan produk atau jasa di dalam platform. User dengan role ini bertindak sebagai penyedia barang/jasa yang dapat diakses oleh pembeli. User dengan role Penjual masih dapat memiliki role lain, yaitu Pembeli, sehingga mereka tidak hanya bisa menjual, tapi juga bisa membeli produk dari penjual lain.
Hak akses utama: Membuat dan mengelola daftar produk yang dijual, termasuk menambahkan deskripsi, harga, stok, dan gambar produk.
Tujuan utama: memberi kesempatan kepada user untuk membuka usaha atau berjualan melalui platform.

3. Pembeli
Role Pembeli adalah peran yang memungkinkan user untuk melakukan aktivitas pembelian produk atau jasa yang ditawarkan oleh para penjual di dalam platform. User dengan role Pembeli dapat juga memiliki role Penjual, sehingga memungkinkan mereka untuk menjadi pembeli sekaligus penjual di platform.
Hak akses utama:
- Melihat katalog produk yang tersedia.
- Melakukan transaksi pembelian dengan memilih produk dan melakukan pembayaran.
Tujuan utama: memberikan kemudahan kepada user dalam berbelanja berbagai produk sesuai kebutuhan mereka.
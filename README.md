IF2150-2024-K02-G13-AMBATUFIT

# Project AMBATUFIT

## Deskripsi Singkat Aplikasi
Aplikasi ini merupakan aplikasi untuk membantu user untuk kebugarannya. Aplikasi ini memiliki fitur profil, latihan, aktivitas, nutrisi, saran kebugaran, dan notifikasi

## Cara Menjalankan Aplikasi
### Persyaratan Sistem
- Python 3.x terinstal di komputer.
- Library PyQt5 dan dependensi lainnya.

### Langkah-Langkah
1. **Clone Repository**  
   Clone repository ini ke komputer Anda:
   ```bash
   git clone https://github.com/username/nama-proyek.git
   cd nama-proyek
   
2. **Instal Dependensi**
   Jalankan perintah berikut untuk menginstal semua dependensi:
   ```bash
   pip install -r requirements.txt

3. **Menjalankan Aplikasi**
   Jalankan file utama aplikasi dengan perintah:
   ```bash
   python main.py

## Daftar Modul yang Diimplementasi

### Modul 1: Home

- #### Deskripsi Singkat Modul: Home adalah halaman awal dari aplikasi AMBATUFIT

- #### Pembagian Tugas: Aryo Bama Wiratama

- #### Tangkapan Layar:


### Modul 2: Profile

- #### Deskripsi Singkat Modul: Profile adalah halaman yang dapat menerima data dari pengguna dan pengguna dapat mengubah atau melihat data tersebut

- #### Pembagian Tugas: Aryo Bama Wiratama

- #### Tangkapan Layar:

### Modul 3: Exercise

- #### Deskripsi Singkat Modul: Excercise adalah halaman yang berisi latihan-latihan yang kemudian dapat ditambah, diubah, atau dihapus oleh pengguna dan pengguna dapat melihatnya.

- #### Pembagian Tugas: Bob Kunanda

- #### Tangkapan Layar:

### Modul 4: Activity

- #### Deskripsi Singkat Modul: Activity adalah halaman yang berisi langkah dan kalori dari pengguna yang kemudian dapat ditambah, diubah, atau dihapus oleh pengguna dan pengguna dapat melihatnya.

- #### Pembagian Tugas: Dzubyan Ilman Ramadhan 

- #### Tangkapan Layar:

### Modul 5: Nutritional Intake

- #### Deskripsi Singkat Modul: Nutritional Intake adalah halaman yang berisi nutrisi yang dikonsumsi dari pengguna yang kemudian dapat ditambah, diubah, atau dihapus oleh pengguna dan pengguna dapat melihatnya.

- #### Pembagian Tugas: Zulfaqqar Nayaka Athadiansyah

- #### Tangkapan Layar:


### Modul 6: Fitness Advice

- #### Deskripsi Singkat Modul: Fitness Advice adalah halaman yang berisi saran kebugaran untuk user berdasarkan data yang diberikan user kepada aplikasi.

- #### Pembagian Tugas: Zulfaqqar Nayaka Athadiansyah

- #### Tangkapan Layar:

### Modul 7: Notifikasi

- #### Deskripsi Singkat Modul: Notifikasi adalah halaman yang berisi tempat untuk input notifikasi, notifikasi dapat ditambah, diubah, dan dihapus.

- #### Pembagian Tugas: Aryo Bama Wiratama

- #### Tangkapan Layar:

## Basis Data

### Tabel `personal_data`
| Kolom   | Tipe     | Deskripsi                                |
|---------|----------|------------------------------------------|
| `id`    | INTEGER  | ID unik untuk setiap data pribadi (Auto Increment) |
| `nama`  | TEXT     | Nama lengkap dari individu              |
| `usia`  | INTEGER  | Usia individu dalam tahun                |
| `tinggi`| REAL     | Tinggi badan individu dalam sentimeter  |
| `berat` | REAL     | Berat badan individu dalam kilogram     |
| `tujuan`| TEXT     | Tujuan yang ingin dicapai oleh individu (misalnya: menurunkan berat badan, meningkatkan massa otot) |

### Tabel `latihan`
| Kolom   | Tipe     | Deskripsi                                |
|---------|----------|------------------------------------------|
| `id`    | INTEGER  | ID unik untuk setiap latihan (Auto Increment) |
| `nama`  | TEXT     | Nama latihan (misalnya: push-up, squat)  |

### Tabel `skema_latihan`
| Kolom       | Tipe     | Deskripsi                                  |
|-------------|----------|--------------------------------------------|
| `id`        | INTEGER  | ID unik untuk setiap skema latihan (Auto Increment) |
| `nama`      | TEXT     | Nama skema latihan (misalnya: latihan kardio, latihan kekuatan) |
| `deskripsi` | TEXT     | Deskripsi tentang skema latihan tersebut  |
| `tipe`      | TEXT     | Tipe latihan (misalnya: aerobic, strength, flexibility) |
| `durasi`    | INTEGER  | Durasi latihan dalam menit                 |

### Tabel `detail_skema_latihan`
| Kolom        | Tipe     | Deskripsi                                         |
|--------------|----------|---------------------------------------------------|
| `id_skema`   | INTEGER  | ID skema latihan yang merujuk pada tabel `skema_latihan` |
| `id_urut`    | INTEGER  | Urutan dalam detail skema latihan (digabung dengan `id_skema` sebagai primary key) |
| `id_latihan` | INTEGER  | ID latihan yang merujuk pada tabel `latihan`      |
| `reps`       | INTEGER  | Jumlah repetisi dalam latihan                    |
| `sets`       | INTEGER  | Jumlah set dalam latihan                         |

### Tabel `aktivitas_fisik`
| Kolom        | Tipe     | Deskripsi                                             |
|--------------|----------|-------------------------------------------------------|
| `id_aktivitas` | INTEGER  | ID aktivitas fisik, sebagai primary key yang auto increment |
| `id_latihan`  | INTEGER  | ID latihan yang merujuk pada tabel `latihan`          |
| `nama`        | TEXT     | Nama aktivitas fisik                                  |
| `kalori`      | REAL     | Jumlah kalori yang dibakar dalam aktivitas            |
| `tanggal`     | TEXT     | Tanggal aktivitas fisik dilakukan                     |


### Tabel `nutrisi`
| Kolom     | Tipe     | Deskripsi                                      |
|-----------|----------|------------------------------------------------|
| `id`      | INTEGER  | ID nutrisi, sebagai primary key yang auto increment |
| `name`    | TEXT     | Nama dari nutrisi, tidak boleh kosong (NOT NULL) |

### Tabel `asupan_nutrisi`
| Kolom     | Tipe     | Deskripsi                                      |
|-----------|----------|------------------------------------------------|
| `id`      | INTEGER  | ID asupan nutrisi, sebagai primary key yang auto increment |
| `name`    | TEXT     | Nama dari asupan nutrisi, tidak boleh kosong (NOT NULL) |
| `datetime`| TEXT     | Waktu dan tanggal pencatatan asupan nutrisi |


### Tabel `detail_asupan_nutrisi`
| Kolom      | Tipe     | Deskripsi                                           |
|------------|----------|-----------------------------------------------------|
| `id_urut`  | INTEGER  | Urutan detail asupan nutrisi, digunakan bersama `id_asupan` sebagai primary key |
| `id_asupan`| INTEGER  | ID asupan nutrisi, merujuk pada ID yang ada di tabel `asupan_nutrisi` |
| `id_nutrisi`| INTEGER | ID nutrisi yang terkait, merujuk pada ID yang ada di tabel `nutrisi` |
| `kandungan`| REAL     | Jumlah kandungan nutrisi dalam asupan (misalnya dalam gram atau miligram) |

### Tabel `saran_kebugaran`
| Kolom           | Tipe     | Deskripsi                                                   |
|-----------------|----------|-------------------------------------------------------------|
| `id`            | INTEGER  | ID saran kebugaran, primary key, auto-increment              |
| `saran_latihan` | TEXT     | Saran latihan fisik yang disarankan                          |
| `saran_nutrisi` | TEXT     | Saran nutrisi yang disarankan untuk mendukung kebugaran      |

### Tabel `notifikasi`
| Kolom     | Tipe     | Deskripsi                                               |
|-----------|----------|---------------------------------------------------------|
| `id`      | INTEGER  | ID notifikasi, primary key, auto-increment              |
| `nama`    | TEXT     | Nama notifikasi                                         |
| `waktu`   | INTEGER  | Waktu notifikasi dalam detik sejak epoch (1 Januari 1970) |

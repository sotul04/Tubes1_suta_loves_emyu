[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Tugas Besar Strategi Algoritma

## Kelompok 14 : suta_loves_emyu

<br>
<p align="center">
<img src="loves_madrid.png" alt="Kelompok suta_loves_emyu" width="400"/>
</p>
<br>

|   NIM    |              Nama                   |
| :------: |    :---------------------------:    |
| 13522054 |         Benjamin Sihombing          |
| 13522098 |     Suthasoma Mahardhika Munthe     |
| 13522110 |      Marvin Scifo Y. Hutahaean      |

## 💎 Etimo Diamonds 2

Diamonds adalah sebuah *programming challenge*. Permainan ini meminta programmer untuk membuat bot yang dapat memperoleh skor tertinggi. 

### Algoritma Greedy 

Bot yang diimplementasikan memakai strategi greedy dengan formula yang menghitung nilai sebuah tujuan pilihan terhadap beberapa aspek, yaitu jarak dari bot ke diamond ($d$), jarak total diamond ke diamond lain ($o$), jarak diamond ke base ($b$), dan poin diamond ($p$). Nilai setiap diamond ($value$) akan dihitung berdasarkan formula di bawah ini.

$$ value_i = {d_i^2o_ib_i \over {p_i+3}} $$

dengan:

$i =$ diamond ke- $i$ pada list obyek

$d_i =$ jarak bot ke diamond

$b_i =$ jarak diamond ke- $i$ ke base

$o_i=\sum_{k=1}^n distance(o_i,o_k)$ , dengan $n =$ jumlah diamond pada board

$p_i =$ poin diamond ke- $i$

Kemudian akan dilakukan pemilihan diamond dengan nilai terkecil. Diamond dengan nilai terkecil memiliki beberapa sifat, yaitu paling dekat dengan bot, relatif dekat dengan diamond-diamond lain di board, relatif dekat dengan base, dan memiliki poin yang lebih besar. Solusi greedy yang kami pilih tidak memperhitungkan keberadaan bot lainnya. Hal ini terjadi karena setelah diuji coba dengan memperhitungkan keberadaan bot lain, jumlah skor rata-rata yang diperoleh bot relatif rendah dibandingkan bot yang mengabaikan keberadaan bot lainnya.

### Requirements

Bot dan Game Engine dimuat terpisah. Bagian ini adalah *bot starter* yang akan digunakan untuk memberikan instruksi pergerakan bot saat permainan. 
Silahkan ikuti instruksi di bawah ini untuk menyiapkan *dependencies* yang diperlukan.
-   [Get Started with Diamonds](https://docs.google.com/document/d/1L92Axb89yIkom0b24D350Z1QAr8rujvHof7-kXRAp7c/edit)

### How to Run 💻

Sebelum menjalankan bot, pastikan bahwa *game engine* yang diperlukan pada bagian [Get Started with Diamonds](#requirements) telah disiapkan dan dijalankan.

Selanjutnya pindah direktori ke folder ```src``` dengan command ```cd src```. Lanjutkan dengan mengikuti instruksi di bawah ini.

1. Command yang dipakai untuk menjalankan bot

    ```
    python main.py --logic Random --email=your_email@example.com --name=your_name --password=your_password --team etimo
    ```

2. Jalankan command di bawah ini untuk menjalankan beberapa bot sekaligus

    Windows

    ```
    ./run-bots.bat
    ```

    Linux / (possibly) macOS

    ```
    ./run-bots.sh
    ```

    <b>Sebelum menjalankan script, ingat untuk mengubah izin script shell agar dapat menjalankan script (linux/macOS)</b>

    ```
    chmod +x run-bots.sh
    ```

#### Note:

-   Jika beberapa bot dijalankan bersamaan, pastikan email dan nama unik
-   Email dapat berupa apapun asalkan masih sesuai dengan sintaks email yang benar
-   Nama dan password bot dibebaskan dan tanpa spasi

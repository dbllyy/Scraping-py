from google_play_scraper import reviews, Sort
import pandas as pd
import threading
import time

# App ID untuk aplikasi yang ingin di-scrape
app_id = 'com.basys.kalteng'

# Inisialisasi list untuk menampung semua ulasan dan set untuk memeriksa duplikasi
all_reviews = []
unique_reviews = set()  # Set untuk menyimpan kombinasi unik dari ulasan
lock = threading.Lock()  # Lock untuk menghindari konflik saat menulis ke list

def fetch_reviews(token=None):
    global all_reviews, unique_reviews
    try:
        result, continuation_token = reviews(
            app_id,
            sort=Sort.NEWEST,  # Mengambil ulasan terbaru
            count=200,  # Ambil 200 ulasan per permintaan (maksimum)
            continuation_token=token  # Token untuk melanjutkan dari ulasan sebelumnya
        )
        
        # Menambahkan ulasan yang diambil ke list dengan lock dan cek duplikat
        with lock:
            for review in result:
                # Identifikasi unik untuk setiap ulasan menggunakan kombinasi userName, content, dan tanggal
                review_key = (review['userName'], review['content'], review['at'])
                
                if review_key not in unique_reviews:  # Hanya tambahkan jika belum ada di set
                    unique_reviews.add(review_key)
                    all_reviews.append(review)

        return continuation_token  # Kembalikan token untuk pagination berikutnya
    except Exception as e:
        print(f"Error during fetching reviews: {e}")
        return None

# Inisialisasi token untuk pagination
next_token = None

# List untuk menyimpan thread
threads = []

# Loop untuk mengambil semua ulasan
while True:  # Loop hingga semua ulasan diambil
    if next_token is None:  # Jika ini adalah permintaan pertama
        next_token = fetch_reviews()
    else:
        # Mulai thread baru untuk mengambil ulasan
        thread = threading.Thread(target=lambda: fetch_reviews(next_token))
        threads.append(thread)
        thread.start()
        time.sleep(1)  # Delay sejenak untuk menghindari pembatasan

        # Perbarui token kelanjutan setelah thread berjalan
        next_token = fetch_reviews(next_token)
    
    # Jika tidak ada token kelanjutan, hentikan loop
    if next_token is None:
        print("Semua ulasan sudah diambil.")
        break

# Tunggu semua thread selesai
for thread in threads:
    thread.join()

# Mengambil hanya kolom yang diperlukan
filtered_reviews = []
for review in all_reviews:
    filtered_reviews.append({
        'userName': review['userName'],  # Mengambil username
        'content': review['content'],      # Mengambil komentar
        'score': review['score'],          # Mengambil rating
        'at': review['at']            # Mengambil tanggal/waktu
        # Waktu balasan developer
    })

# Mengubah data ulasan ke dalam DataFrame pandas
df = pd.DataFrame(filtered_reviews)

# Menyimpan ulasan ke file CSV
df.to_csv('bank_kalteng_reviews_all_languages_countries.csv', index=False)

# Menyimpan ulasan ke file Excel
df.to_excel('bank_kalteng_reviews_all_languages_countries.xlsx', index=False)

print(f'Successfully scraped {len(filtered_reviews)} unique reviews.')

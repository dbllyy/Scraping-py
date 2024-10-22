from google_play_scraper import reviews_all
import pandas as pd

# App ID untuk Betang Mobile
app_id = 'com.basys.kalteng'

# Mengambil semua ulasan
reviews = reviews_all(
    app_id,
    lang='id',  # Bahasa Indonesia
    country='id'  # Negara Indonesia
)

# Mengambil hanya kolom yang diperlukan
filtered_reviews = []
for review in reviews:
    filtered_reviews.append({
        'userName': review['userName'],
        'content': review['content'],
        'score': review['score'],
        'at': review['at']
    })

# Mengubah data ulasan ke dalam DataFrame pandas
df = pd.DataFrame(filtered_reviews)

# Menyimpan ulasan ke file CSV
df.to_csv('betang_mobile_reviews_filtered.csv', index=False)

# Menyimpan ulasan ke file Excel
df.to_excel('betang_mobile_reviews_filtered.xlsx', index=False)

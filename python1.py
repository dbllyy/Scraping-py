from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd

# Path ke ChromeDriver
driver_path = r'D:\DEBI\MAGANG KP\chromedriver-win64\chromedriver.exe'  # Sesuaikan dengan path ke ChromeDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# Buka halaman ulasan aplikasi Betang Mobile di Google Play
url = 'https://play.google.com/store/apps/details?id=com.basys.kalteng&hl=id&showAllReviews=true'
driver.get(url)

# Simulasikan scroll untuk memuat lebih banyak ulasan
SCROLL_PAUSE_TIME = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Mengambil data ulasan
reviews = driver.find_elements(By.CLASS_NAME, 'd15Mdf')
review_list = []

for review in reviews:
    user = review.find_element(By.CLASS_NAME, 'X43Kjb').text
    content = review.find_element(By.CLASS_NAME, 'UD7Dzf').text
    rating = review.find_element(By.CLASS_NAME, 'nt2C1d').get_attribute("aria-label")
    date = review.find_element(By.CLASS_NAME, 'p2TkOb').text
    review_list.append({
        'userName': user,
        'content': content,
        'score': rating,
        'at': date
    })

# Simpan ulasan ke CSV
df = pd.DataFrame(review_list)
df.to_csv('betang_mobile_reviews.csv', index=False)

driver.quit()

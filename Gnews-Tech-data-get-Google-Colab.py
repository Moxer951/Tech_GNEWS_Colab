# نصب کتابخانه‌های لازم
!pip install pandas openpyxl --quiet
!apt-get install p7zip-full -qq

# اتصال به گوگل درایو
from google.colab import drive
drive.mount('/content/drive')

# وارد کردن کتابخانه‌ها
import os
import requests
import pandas as pd
from datetime import datetime
import shutil

# پارامترهای قابل تنظیم
API_KEY = "copy_you_api"
LANG = "en"
TOPIC = "technology"
RESULT_LIMIT = 10

BASE_PATH = "/content/tech_news_gnews"
EXCEL_PATH = os.path.join(BASE_PATH, "excel")
IMAGES_PATH = os.path.join(BASE_PATH, "images")
NEWS_ITEMS_PATH = os.path.join(BASE_PATH, "news_items_eng")
os.makedirs(EXCEL_PATH, exist_ok=True)
os.makedirs(IMAGES_PATH, exist_ok=True)
os.makedirs(NEWS_ITEMS_PATH, exist_ok=True)

# فراخوانی API
url = f"https://gnews.io/api/v4/top-headlines?topic={TOPIC}&lang={LANG}&max={RESULT_LIMIT}&token={API_KEY}"
response = requests.get(url)
articles = response.json().get("articles", [])

# پردازش خبرها
data_list = []
for idx, article in enumerate(articles, 1):
    title = article.get("title", "No Title").strip().replace(":", "").replace("/", "-")[:40]
    description = article.get("description", "No Description")
    content = article.get("content", "No Content")
    source = article.get("source", {}).get("name", "Unknown Source")
    published = article.get("publishedAt", "Unknown Date")
    url_article = article.get("url", "")
    image_url = article.get("image")
    
    # ذخیره تصویر
    image_file_name = "Not Available"
    if image_url:
        try:
            image_data = requests.get(image_url).content
            image_file_name = f"{idx}_{title[:30]}.jpg"
            image_path = os.path.join(IMAGES_PATH, image_file_name)
            with open(image_path, "wb") as f:
                f.write(image_data)
        except:
            image_file_name = "Download Error"

    # ساخت پوشه خبر
    news_folder = os.path.join(NEWS_ITEMS_PATH, f"news_{idx}")
    os.makedirs(news_folder, exist_ok=True)

    # ذخیره فایل تکست
    text_content = f"""Title: {title}
Date: {published}
Source: {source}
Description: {description}
URL: {url_article}
"""
    with open(os.path.join(news_folder, "info.txt"), "w", encoding="utf-8") as f:
        f.write(text_content)

    # کپی تصویر داخل پوشه خبر
    if image_file_name != "Not Available" and image_file_name != "Download Error":
        shutil.copy(os.path.join(IMAGES_PATH, image_file_name), os.path.join(news_folder, image_file_name))

    # افزودن به دیتافریم
    data_list.append({
        "Index": idx,
        "Title": title,
        "Description": description,
        "Published": published,
        "Source": source,
        "URL": url_article,
        "Image": image_file_name,
        "Content": content,
    })

# ذخیره در Excel
df = pd.DataFrame(data_list)
excel_file = os.path.join(EXCEL_PATH, f"gnews_tech_news.xlsx")
df.to_excel(excel_file, index=False)

# فشرده‌سازی کل پوشه

#-----زمان و تاریخ جهانی ساعت 0 -----------
# فشرده‌سازی کل پوشه با تاریخ و ساعت در نام فایل
#now = datetime.now()
#formatted_date = now.strftime("%Y.%m.%d")
#formatted_time = now.strftime("%H:%M:%S")
#zip_filename = f"gnews_tech_news_date_{formatted_date}_time_{formatted_time}.7z"
#ZIP_FILE = f"/content/drive/MyDrive/{zip_filename}"



#-----زمان و تاریخ تهران ساعت +3:30 -----------

from datetime import datetime
from zoneinfo import ZoneInfo  # نیازی به نصب نیست

# زمان به وقت تهران
now_tehran = datetime.now(ZoneInfo("Asia/Tehran"))
formatted_date = now_tehran.strftime("%Y.%m.%d")
formatted_time = now_tehran.strftime("%H:%M:%S")
zip_filename = f"gnews_tech_news_date_{formatted_date}_time_{formatted_time}.7z"
ZIP_FILE = f"/content/drive/MyDrive/{zip_filename}"

!7z a -mx=9 "{ZIP_FILE}" "{BASE_PATH}"

print(f"✅ Done! Zipped archive saved to: {ZIP_FILE}")


!7z a -mx=9 "{ZIP_FILE}" "{BASE_PATH}"

print(f"✅ Done! Zipped archive saved to: {ZIP_FILE}")
#Done

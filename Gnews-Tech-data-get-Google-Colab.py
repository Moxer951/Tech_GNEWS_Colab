# نصب کتابخانه‌های لازم
!pip install pandas openpyxl --quiet
import os
import requests
import pandas as pd
from datetime import datetime

# پارامترهای قابل تنظیم
API_KEY = "YOUR_GNEWS_API_KEY"  # 🔑 کلید API
LANG = "en"                     # 🌐 زبان خبر
TOPIC = "technology"           # 🔍 موضوع
RESULT_LIMIT = 10              # 🔢 حداکثر خبر در هر درخواست (پلن رایگان فقط 10)
SAVE_PATH = "/content/tech_news_gnews"  # مسیر ذخیره‌سازی

# مسیرها
EXCEL_PATH = os.path.join(SAVE_PATH, "excel")
IMAGES_PATH = os.path.join(SAVE_PATH, "images")
os.makedirs(EXCEL_PATH, exist_ok=True)
os.makedirs(IMAGES_PATH, exist_ok=True)

# فراخوانی API
url = f"https://gnews.io/api/v4/top-headlines?topic={TOPIC}&lang={LANG}&max={RESULT_LIMIT}&token={API_KEY}"
response = requests.get(url)
articles = response.json().get("articles", [])

# پردازش نتایج
data_list = []
for idx, article in enumerate(articles, 1):
    title = article.get("title", "بدون عنوان").strip().replace(":", "").replace("/", "-")[:40]
    description = article.get("description", "بدون توضیح")
    content = article.get("content", "ندارد")
    source = article.get("source", {}).get("name", "نامشخص")
    published = article.get("publishedAt", "تاریخ نامشخص")
    url_article = article.get("url", "")
    image_url = article.get("image")

    image_file_name = "ندارد"
    if image_url:
        try:
            image_data = requests.get(image_url).content
            image_file_name = f"{idx}_{title[:30]}.jpg"
            with open(os.path.join(IMAGES_PATH, image_file_name), "wb") as f:
                f.write(image_data)
        except:
            image_file_name = "خطا در دانلود"

    data_list.append({
        "ردیف": idx,
        "عنوان": title,
        "توضیح": description,
        "تاریخ انتشار": published,
        "منبع": source,
        "آدرس خبر": url_article,
        "تصویر": image_file_name,
        "متن": content,
    })

# ذخیره در Excel
df = pd.DataFrame(data_list)
excel_file = os.path.join(EXCEL_PATH, f"gnews_tech_news.xlsx")
df.to_excel(excel_file, index=False)

# چاپ خلاصه
print(f"✅ دریافت {len(data_list)} خبر تکنولوژی با موفقیت انجام شد.")
print(f"📁 فایل Excel ذخیره شد: {excel_file}")
print(f"🖼 تصاویر در مسیر: {IMAGES_PATH}")

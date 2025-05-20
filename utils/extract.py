import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime  # Tambahkan di atas file kamu jika belum ada

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetching_content(url):
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None



def extract_product_data(card):
    try:
        title = card.find("h3", class_="product-title").text.strip() if card.find("h3", class_="product-title") else None
        price = card.find("span", class_="price").text.strip() if card.find("span", class_="price") else None

        # Ekstrak rating (misalnya: "Rating: ⭐ 4.2 / 5")
        rating_tag = card.find("p", string=lambda t: t and "Rating" in t)
        if rating_tag:
            rating_text = rating_tag.text.strip()
            match = re.search(r"(\d+(\.\d+)?)", rating_text)
            rating = float(match.group(1)) if match else None
        else:
            rating = None

        color_tag = card.find("p", string=lambda t: t and "Colors" in t)
        colors = color_tag.text.strip().replace("Colors", "").strip() if color_tag else None

        size_tag = card.find("p", string=lambda t: t and "Size" in t)
        size = size_tag.text.strip().replace("Size:", "").strip() if size_tag else None

        gender_tag = card.find("p", string=lambda t: t and "Gender" in t)
        gender = gender_tag.text.strip().replace("Gender:", "").strip() if gender_tag else None

        # Tambahkan timestamp saat ekstraksi
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "title": title,
            "price": price,
            "colors": colors,
            "size": size,
            "gender": gender,
            "rating": rating,
            "timestamp": timestamp
        }

    except Exception as e:
        print(f"[ERROR] Gagal mengekstrak data dari card: {e}")
        return None


def scrape_products(base_url, start_page=1, delay=2):
    """Melakukan scraping semua halaman dan mengembalikan data produk sebagai list of dict."""
    data = []
    page = start_page
    
    while True:
        if page ==1:  # Batasi hingga 10 halaman
            url = "https://fashion-studio.dicoding.dev/"
            print(f"[INFO] Scraping halaman: {url}")
        else:
            url = base_url.format(page)
            print(f"[INFO] Scraping halaman: {url}")
        
        content = fetching_content(url)
        if not content:
            break
        
        soup = BeautifulSoup(content, "html.parser")
        product_cards = soup.find_all("div", class_="collection-card")

        if not product_cards:
            print("[INFO] Tidak ada produk ditemukan di halaman ini.")
            break

        for card in product_cards:
            product = extract_product_data(card)
            if product:
                data.append(product)

        # Asumsi: lanjut ke halaman berikutnya jika masih ada produk
        page += 1
        time.sleep(delay)

    return data

def extract_to_dataframe():
    """Menjalankan proses scraping dan mengubah hasil ke dalam DataFrame."""
    BASE_URL ="https://fashion-studio.dicoding.dev/page{}"  # ganti sesuai URL asli
    data = scrape_products(BASE_URL)
    return pd.DataFrame(data)

import pandas as pd

# Fungsi untuk mengubah raw_data menjadi DataFrame
def transform_to_DataFrame(raw_data):
    """Mengubah list of dict menjadi DataFrame pandas."""
    try:
        df = pd.DataFrame(raw_data)
        return df
    except Exception as e:
        print(f"[ERROR] Gagal mengubah data mentah ke DataFrame: {e}")
        return pd.DataFrame()  # DF kosong agar tidak error

# Fungsi transformasi data utama
def transform_data(df, price_threshold=20000):
    """Melakukan pembersihan dan transformasi data sesuai ketentuan."""
    try:
        df = df.copy()

        # Step 1: Hapus data kotor
        dirty_patterns = {
            "title": ["Unknown Product"],
            "rating": ["Invalid Rating / 5", "Not Rated"],
            "price": ["Price Unavailable", None]
        }
        for column, patterns in dirty_patterns.items():
            df = df[~df[column].isin(patterns)]

        # Step 2: Bersihkan kolom price: hilangkan simbol dan konversi ke float lalu ke Rupiah
        def clean_price(price):
            try:
                clean = str(price).replace(",", "").replace("$", "")
                return float(clean) * 16000
            except:
                return None

        df["price"] = df["price"].apply(clean_price)

        # Step 3: Bersihkan kolom rating: ubah "4.5 / 5" menjadi 4.5
        def clean_rating(rating):
            try:
                return float(str(rating).split("/")[0].strip())
            except:
                return None

        df["rating"] = df["rating"].apply(clean_rating)

        # Step 4: Bersihkan kolom colors: ambil angka saja
        def clean_colors(color):
            try:
                return int(''.join(filter(str.isdigit, str(color))))
            except:
                return 0

        df["colors"] = df["colors"].apply(clean_colors)

        # Step 5: Pastikan kolom string
        df["title"] = df["title"].astype(str)
        df["size"] = df["size"].astype(str)
        df["gender"] = df["gender"].astype(str)

        # Drop baris yang masih ada nilai NaN
        df.dropna(inplace=True)

        # Optional: filter harga minimum
        df = df[df["price"] >= price_threshold]

        return df

    except Exception as e:
        print(f"[FATAL ERROR] Terjadi kesalahan saat transformasi data: {e}")
        return pd.DataFrame()

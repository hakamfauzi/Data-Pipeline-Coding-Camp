from utils.extract import scrape_products
from utils.transform import transform_to_DataFrame, transform_data
from utils.load import store_to_postgre, store_to_csv
import pandas as pd
from sqlalchemy import create_engine

def main():
    """Fungsi utama untuk keseluruhan proses scraping, transformasi data, dan penyimpanan."""
    BASE_URL = 'https://fashion-studio.dicoding.dev/page{}'  # Ganti dengan URL yang sesuai
    
    # Menjalankan scraping untuk mengambil data fashion
    all_product_data = scrape_products(BASE_URL)
    
    # Jika data berhasil diambil, lakukan transformasi dan simpan ke PostgreSQL + CSV
    if all_product_data:
        try:
            # Mengubah data menjadi DataFrame
            DataFrame = transform_to_DataFrame(all_product_data)

            # Mentransformasikan data (membersihkan harga, rating, size, dll)
            DataFrame_tf = transform_data(DataFrame)

            # Menyimpan data ke PostgreSQL
            db_url = 'postgresql+psycopg2://developer:password@localhost:5432/submissiondb'
            store_to_postgre(DataFrame_tf, db_url)

            # Menyimpan data ke file CSV juga
            store_to_csv(DataFrame_tf, 'output/fashion.csv')
            
            # Tampilkan DataFrame hasil akhir
            print("\nDataFrame awal:\n")
            print(DataFrame)
            print(DataFrame.dtypes)
            print("\nDataFrame Hasil Transformasi:\n")
            print(DataFrame_tf)
            print(DataFrame_tf.dtypes)

            # Melihat data yang disimpan di PostgreSQL
            print("\nData yang disimpan di PostgreSQL:\n")
            db_url = 'postgresql+psycopg2://developer:password@localhost:5432/submissiondb'
            engine = create_engine(db_url)

            dfpostgres = pd.read_sql('SELECT * FROM fashion', con=engine)
            print(dfpostgres.head())


        except Exception as e:
            print(f"Terjadi kesalahan dalam proses ETL: {e}")
    else:
        print("Tidak ada data yang ditemukan.")

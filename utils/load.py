import pandas as pd
from sqlalchemy import create_engine
import os
import logging

def store_to_postgre(data: pd.DataFrame, db_url: str):
    """Menyimpan data ke dalam PostgreSQL."""
    try:
        engine = create_engine(db_url)
        with engine.connect() as con:
            data.to_sql('fashion', con=con, if_exists='append', index=False)
            print("[INFO] Data berhasil disimpan ke PostgreSQL.")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke PostgreSQL: {e}")


def store_to_csv(data: pd.DataFrame, filename="output/fashion.csv"):
    """Menyimpan data ke dalam file CSV."""
    try:
        # Pastikan folder output ada
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Simpan ke file CSV
        data.to_csv(filename, index=False)
        print(f"[INFO] Data berhasil disimpan ke CSV: {filename}")
        logging.info(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan ke CSV: {e}")
        logging.error(f"Gagal menyimpan ke CSV: {e}")

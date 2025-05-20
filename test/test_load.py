import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import store_to_csv, store_to_postgre

class TestLoad(unittest.TestCase):
    def setUp(self):
        # Data dummy
        self.df = pd.DataFrame([{"title": "Item A", "price": 100.0}])

    # ---------- Test store_to_csv ----------
    def test_store_to_csv_success(self):
        with patch("utils.load.os.makedirs"), \
            patch("utils.load.pd.DataFrame.to_csv") as mock_to_csv, \
            patch("utils.load.logging.info") as mock_log_info, \
            patch("builtins.print") as mock_print:

            store_to_csv(self.df, "output/test.csv")
            mock_to_csv.assert_called_once()
            mock_print.assert_called_with("[INFO] Data berhasil disimpan ke CSV: output/test.csv")
            mock_log_info.assert_called()

    def test_store_to_csv_failure(self):
        with patch("utils.load.os.makedirs"), \
            patch("utils.load.pd.DataFrame.to_csv", side_effect=Exception("Write failed")), \
            patch("utils.load.logging.error") as mock_log_error, \
            patch("builtins.print") as mock_print:

            store_to_csv(self.df, "output/test.csv")
            mock_print.assert_called_with("[ERROR] Gagal menyimpan ke CSV: Write failed")
            mock_log_error.assert_called_with("Gagal menyimpan ke CSV: Write failed")

    # ---------- Test store_to_postgre ----------
    @patch("utils.load.create_engine")
    def test_store_to_postgre_success(self, mock_create_engine):
        mock_conn = MagicMock()
        mock_engine = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_create_engine.return_value = mock_engine

        with patch("builtins.print") as mock_print:
            store_to_postgre(self.df, "postgresql://user:pass@localhost/dbname")
            mock_conn.__enter__().execute.assert_not_called()  # karena to_sql, bukan execute langsung
            mock_print.assert_called_with("[INFO] Data berhasil disimpan ke PostgreSQL.")

    @patch("utils.load.create_engine", side_effect=Exception("DB connection failed"))
    def test_store_to_postgre_failure(self, mock_create_engine):
        with patch("builtins.print") as mock_print:
            store_to_postgre(self.df, "postgresql://user:pass@localhost/dbname")
            mock_print.assert_called_with("[ERROR] Gagal menyimpan ke PostgreSQL: DB connection failed")

if __name__ == "__main__":
    unittest.main()

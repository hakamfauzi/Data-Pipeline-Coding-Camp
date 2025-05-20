import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data

class TestTransform(unittest.TestCase):

    def test_transform_to_dataframe_valid(self):
        raw_data = [
            {"title": "Product A", "price": "$10.0", "colors": "2", "rating": 4.5, "size": "L", "gender": "Male"}
        ]
        df = transform_to_DataFrame(raw_data)
        self.assertFalse(df.empty)
        self.assertIn("price", df.columns)

    def test_transform_data_success(self):
        data = {
            "title": ["Product A"],
            "price": ["$100.0"],
            "colors": ["2"],
            "rating": ["4.2"],
            "size": ["L"],
            "gender": ["Male"]
        }
        df = pd.DataFrame(data)
        df_transformed = transform_data(df)
        self.assertEqual(df_transformed["price"].iloc[0], 100.0 * 16000)
        self.assertEqual(df_transformed["colors"].iloc[0], 2)
        self.assertAlmostEqual(df_transformed["rating"].iloc[0], 4.2)

    def test_transform_data_invalid_price(self):
        df = pd.DataFrame([{
            "title": "Test",
            "price": "invalid",
            "colors": "2",
            "rating": "4.5",
            "size": "S",
            "gender": "Unisex"
        }])
        df_result = transform_data(df)
        self.assertTrue(df_result.empty)

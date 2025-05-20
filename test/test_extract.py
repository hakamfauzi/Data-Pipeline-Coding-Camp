import unittest
from unittest.mock import patch, MagicMock
from utils.extract import fetching_content, extract_product_data, scrape_products

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.Session.get')
    def test_fetching_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b"<html>mocked content</html>"
        mock_get.return_value = mock_response

        url = "https://fashion-studio.dicoding.dev"
        result = fetching_content(url)
        self.assertEqual(result, b"<html>mocked content</html>")

    @patch('utils.extract.requests.Session.get', side_effect=Exception("Connection failed"))
    def test_fetching_content_failure(self, mock_get):
        result = fetching_content("http://invalid.url")
        self.assertIsNone(result)

    def test_extract_product_data_complete(self):
        from bs4 import BeautifulSoup
        html = '''
        <div class="collection-card">
            <h3 class="product-title">Test Product</h3>
            <span class="price">$29.99</span>
            <p>Rating: ⭐ 4.5 / 5</p>
            <p>Colors: 3</p>
            <p>Size: M</p>
            <p>Gender: Unisex</p>
        </div>
        '''
        soup = BeautifulSoup(html, 'html.parser')
        card = soup.find("div", class_="collection-card")
        data = extract_product_data(card)
        self.assertEqual(data["title"], "Test Product")
        self.assertEqual(data["price"], "$29.99")
        self.assertEqual(data["colors"].replace(":", "").strip(), "3")
        self.assertEqual(data["size"], "M")
        self.assertEqual(data["gender"], "Unisex")
        self.assertEqual(data["rating"], 4.5)


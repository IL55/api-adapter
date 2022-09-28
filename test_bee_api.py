import logging
import unittest
from unittest.mock import patch

from bee_api import get_products, search_product_id_by_sku



class TestBee_api(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)

    @patch("bee_api.post_request")
    def test_get_product_id_ok(self, mk_post):
        mk_post.return_value = {
            "Products": [{
                "Id": 58311429,
                "ShortText": "HOLZSATZ BUKO - SET 3in1 137 TEILE",
                "SKU": "M01-001",
                "Tags": None
            }],
            "Orders": [],
            "Customers": []
        }
        id = search_product_id_by_sku("test")
        self.assertEqual(id, 58311429)

    @patch("bee_api.post_request")
    def test_get_product_id_no(self, mk_post):
        mk_post.return_value = {
            "Products": [],
            "Orders": [],
            "Customers": []
        }
        id = search_product_id_by_sku("test")
        self.assertEqual(id, None)

    @patch("bee_api.get_request")
    def test_get_all_products(self, mk_get):
        mk_get.return_value = {
            'Paging': {'Page': 1, 'TotalPages': 46, 'TotalRows': 91, 'PageSize': 2},
            'ErrorMessage': None,
            'ErrorCode': 0,
            'ErrorDescription': 'NoError',
            'Data':
            [
                {'InvoiceText': [{'Text': None, 'LanguageCode': 'DE'}],
                    'Manufacturer': 'MK Design', 'Id': 423647, "SKU": "M01-040",
                 "EAN": "0706"},
                {'InvoiceText': [{'Text': None, 'LanguageCode': 'DE'}],
                    'Manufacturer': 'MK Design', 'Id': 66464,  "SKU": "M02-040",
                 "EAN": "07046"}
            ]
        }
        products = get_products()
        self.assertEqual(products, mk_get.return_value['Data'])



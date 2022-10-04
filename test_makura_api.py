import logging
from unittest.mock import patch
import unittest

from makura_api import parse_product_list, update_makura_products

xml = """<?xml version="1.0" encoding="utf-8"?>
<SHOP>
	<SHOPITEM>
		<ID>137V5</ID>
		<CATALOG_NUMBER>M01-080-1</CATALOG_NUMBER>
		<VARIANT>1</VARIANT>
		<DELIVERY_DATE></DELIVERY_DATE>
		<AVAILABILITY>available for order</AVAILABILITY>
	</SHOPITEM>
	<SHOPITEM>
        <ID>180</ID>
        <CATALOG_NUMBER>M01-121</CATALOG_NUMBER>
        <EAN>0708828931789</EAN>
        <DELIVERY_DATE/>
        <AVAILABILITY>out of stock</AVAILABILITY>
        <STOCK_QUANTITY>-5</STOCK_QUANTITY>
    </SHOPITEM>
    <SHOPITEM>
        <ID>183</ID>
        <CATALOG_NUMBER>M01-124</CATALOG_NUMBER>
        <EAN>0708828931765</EAN>
        <DELIVERY_DATE>0</DELIVERY_DATE>
        <AVAILABILITY>in stock</AVAILABILITY>
        <STOCK_QUANTITY>2</STOCK_QUANTITY>
    </SHOPITEM>
    <SHOPITEM>
        <ID>184</ID>
        <CATALOG_NUMBER>M01-125</CATALOG_NUMBER>
        <EAN>55454</EAN>
        <DELIVERY_DATE>0</DELIVERY_DATE>
        <AVAILABILITY>in stock</AVAILABILITY>
    </SHOPITEM>
</SHOP>"""

class Makura_api(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)

    def test_parse_xml(self):
        result = parse_product_list(xml)
        self.assertEqual(result["message"], "")
        self.assertDictEqual(result["products"][0], {
            'count': 0, 'sku': 'M01-080-1', 'state': 'available for order'
        })
        self.assertDictEqual(result["products"][1], {
            'count': 0, 'sku': 'M01-121', 'state': 'out of stock'
        })
        self.assertDictEqual(result["products"][2], {
            'count': 2, 'sku': 'M01-124', 'state': 'in stock'
        })
        self.assertDictEqual(result["products"][3], {
            'count': 100, 'sku': 'M01-125', 'state': 'in stock'
        })

    @patch("makura_api.get_makura_products")
    @patch("makura_api.get_products")
    @patch("makura_api.update_stocks")
    def test_update_makura_products(self, mk_update_stocks, mk_get_bee_products, mk_get_makura_products):
        mk_update_stocks.return_value = {"message": None}
        mk_get_bee_products.return_value = [
            {'Id': 42364, "SKU": "M01-080-1", "EAN": "0706", "StockCurrent": None},
            {'Id': 45345,  "SKU": "M01-123", "EAN": "56778", "StockCurrent": None},
            {'Id': 66464,  "SKU": "M01-124", "EAN": "07056", "StockCurrent": 4}
        ]
        mk_get_makura_products.return_value = {'products': [
            {
                'count': 0, 'sku': 'M01-080-1', 'state': 'available for order'
            },
            {
                'count': 20, 'sku': 'M01-121', 'state': 'out of stock'
            },
            {
                'count': 12, 'sku': 'M01-124', 'state': 'in stock'
            },
            {
                'count': 18, 'sku': 'M01-123', 'state': 'in stock'
            },
        ],
        "message": ""}
        result = update_makura_products()
        self.assertEqual(result["message"], "")
        self.assertEqual(result["updated_products"], {
            'M01-123': {'bee_product_id': 45345, 'count': 18, 'sku': 'M01-123', 'count_in_stock': None},
            'M01-124': {'bee_product_id': 66464, 'count': 12, 'sku': 'M01-124', 'count_in_stock': 4}
        })
        self.assertEqual(result["non_updated_products"], {})
        self.assertEqual(result["unknown_products"], {
                         'M01-121': {'bee_product_id': None, 'count': 20, 'sku': 'M01-121'}})

        mk_update_stocks.assert_called_once_with([
            {'Sku': 'M01-124', 'NewQuantity': 12},
            {'Sku': 'M01-123', 'NewQuantity': 18}
        ])




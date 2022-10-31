from unittest.mock import MagicMock, patch
import unittest

from process_bee_order import get_bee_products

OrderItems = [
    {
        'BillbeeId': 334738293,
        'TransactionId': None,
        'Product':
            {
                'OldId': None,
                'Id': None,
                'Title': 'rwerwerwerwe',
                'Weight': None,
                'SKU': '4234234',
                'SkuOrId': '4234234',
                'IsDigital': False,
                'Images': None,
                'EAN': '43344',
                'PlatformData': None,
                'TARICCode': None,
                'CountryOfOrigin': 'CZ',
                'BillbeeId': 434343
            },
        'Quantity': 1.0,
        'TotalPrice': 1.0,
        'TaxAmount': 0.15966386554621848,
            'TaxIndex': 1,
            'Discount': 0.0,
            'Attributes': [],
            'GetPriceFromArticleIfAny': False,
            'IsCoupon': False,
            'ShippingProfileId': None,
            'DontAdjustStock': False,
            'UnrebatedTotalPrice': 1.0,
            'SerialNumber': None,
            'InvoiceSKU': '434343'
    },
    {
        'BillbeeId': 334738294,
        'TransactionId': None,
        'Product':
            {
                'OldId': None,
                'Id': None,
                'Title': 'rttretertertert',
                'Weight': None,
                'SKU': 'M01-6565554',
                'SkuOrId': 'M01-6565554',
                'IsDigital': False,
                'Images': None,
                'EAN': '0708828930874',
                'PlatformData': None,
                'TARICCode': None,
                'CountryOfOrigin': 'CZ',
                'BillbeeId': 34343
            },
        'Quantity': 2.0,
        'TotalPrice': 2.0,
        'TaxAmount': 0.31932773109243695,
            'TaxIndex': 1,
            'Discount': 0.0,
            'Attributes': [],
            'GetPriceFromArticleIfAny': False,
            'IsCoupon': False,
            'ShippingProfileId': None,
            'DontAdjustStock': False,
            'UnrebatedTotalPrice': 2.0,
            'SerialNumber': None,
            'InvoiceSKU': 'M01-6565554'
    }
]

class TestProcessBeeOrder(unittest.TestCase):
    def test_get_bee_products_none(self):
        result = get_bee_products("170081072", {
            'OrderItems': []
        })
        self.assertEqual(result, [])

    @patch("process_bee_order.get_product", MagicMock(
        side_effect=[{
            'Data': {
                'StockCode': 'ST-1'
            }
        }, {
            'Data': {
                'StockCode': 'ST-2'
            }
        }]
    ))
    def test_get_bee_products_ok(self):
        result = get_bee_products("170081072", {
            'OrderItems': OrderItems
        })
        self.assertEqual(result, [
          {'fulfillmentProductCode': 'ST-1', 'quantity': 1},
          {'fulfillmentProductCode': 'ST-2', 'quantity': 2}
        ])

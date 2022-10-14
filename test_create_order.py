import logging
from unittest.mock import MagicMock, patch
import unittest

from create_order import OrderDestination, create_order

makura_order = {
    "external_id": "1632-170081072",
    "carrier_id": 43,
    "payment_id": 2,
    "note": "",
    "delivery_address": {
        "firstname": "test1",
        "lastname": "test2",
        "company": "test3",
        "street": "test4 25",
        "zip": "12345",
        "city": "test",
        "country": "DE",
        "email": "test_test@seznam.cz",
        "phone": "00420111111111"
    },
    "products": [
        {
            "catalog_number": "A01-002",
            "quantity": 1
        },
        {
            "catalog_number": "A01-004",
            "quantity": 3
        }
    ]
}


class CreateOrder(unittest.TestCase):
  @patch("create_order.get_order", MagicMock(return_value=None))
  def test_create_order_get_order_failed(self):
    result = create_order("100", OrderDestination.MAKURA)
    self.assertTrue(result['response-code'] < 0)

  @patch("create_order.get_order", MagicMock(return_value="some_data"))
  @patch("create_order.process_order_for_makura", MagicMock(return_value=makura_order))
  @patch("create_order.add_makura_order", MagicMock(return_value=None))
  def test_create_order_add_makura_order_failed(self):
    result = create_order("100", OrderDestination.MAKURA)
    self.assertTrue(result['response-code'] < 0)

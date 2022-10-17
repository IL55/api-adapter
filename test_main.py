from unittest.mock import MagicMock, patch
import unittest
from create_order import OrderDestination

from main import get_tracking


class GetMakuraTracking(unittest.TestCase):
  @patch("main.get_makura_tracking_info", MagicMock(return_value=None))
  def test_get_tracking_failed(self):
    result = get_tracking("100", OrderDestination.MAKURA)
    self.assertTrue(result['response-code'] < 0)

  @patch("main.get_makura_tracking_info", MagicMock(return_value={
      "id": 1281,
      "external_id": "1501665316608",
      "number": "12345674069168",
      "status_id": 2,
      "tracking_number": "p7k5m"
  }))
  @patch("main.set_order_state", MagicMock(return_value={"message": None}))
  @patch("main.set_order_tracking")
  def test_get_tracking_ok(self, mk_set_order_tracking):
    mk_set_order_tracking.return_value = {"message": None}
    result = get_tracking("100", OrderDestination.MAKURA)
    mk_set_order_tracking.assert_called_with(
        '100', {'message': None, 'ShippingId': 'p7k5m', 'TrackingUrl': '12345674069168'}
    )
    self.assertTrue(result['response-code'] == 0)

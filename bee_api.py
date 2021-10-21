import logging
from config import BeeConfig
from network import get_request, put_request, patch_request

def get_order(bee_order_id: str):
  """
  Get order data from bee API
  Returns json data
  """
  logging.info(f'Get order for Bee order id is {bee_order_id}')

  if (not bee_order_id):
    logging.error(f'Empty bee order id is {bee_order_id}')
    return None

  url = '{0}{1}'.format(BeeConfig.orders_url, bee_order_id)

  return get_request(url, BeeConfig.headers)


def get_product(bee_product_id: str):
  """
  Get stock code from bee API
  Returns string
  """
  logging.info(f'Bee product id is {bee_product_id}')

  if (not bee_product_id):
    logging.error(f'Empty bee product id is {bee_product_id}')
    return None

  url = '{0}{1}'.format(BeeConfig.products_url, bee_product_id)

  return get_request(url, BeeConfig.headers)


def set_order_state(bee_order_id: str, order_state: int):
  """
  Set order data from bee API
  Returns json data
  """
  logging.info(f'Set order state for Bee order id is {bee_order_id}')

  if (not bee_order_id):
    logging.error(f'Empty bee order id is {bee_order_id}')
    return None

  url = '{0}{1}{2}'.format(
      BeeConfig.orders_url, bee_order_id, BeeConfig.order_state_url)

  data = {
    "NewStateId": order_state
  }

  return put_request(url, BeeConfig.headers, data)

def set_order_tracking(ps_order_id: str, tracking_data: dict):
  """
  Set tracking data from bee API
  Returns json data
  """
  logging.info(f'Set order state for ps order id is {ps_order_id}')

  try:
    bee_order_id = ps_order_id.split('-')[1]
  except:
    bee_order_id = None

  if (not bee_order_id):
    logging.error(f'Empty bee order id is {bee_order_id}')
    return None

  url = '{0}{1}'.format(BeeConfig.orders_url, bee_order_id)

  data = {
    "ShippingIds": [
      {
        "BillbeeId": 0,
        "ShippingId": tracking_data["ShippingId"],
        "Shipper": tracking_data["Shipper"],
        "Created": "2021-10-19T20:42:49.307Z",
        "TrackingUrl": tracking_data["TrackingUrl"],
        "ShippingProviderId": 0,
        "ShippingProviderProductId": 0,
        "ShippingCarrier": 0,
        "ShipmentType": 0
      }
    ]
  }

  return patch_request(url, BeeConfig.headers, data)

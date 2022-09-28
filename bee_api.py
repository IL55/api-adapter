import logging
from config import BeeConfig
from network import get_request, put_request, post_request

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

  url = '{0}/{1}'.format(BeeConfig.products_url, bee_product_id)

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


def search_product_id_by_sku(bee_sku: str):
  """
  Find product by SKU
  """
  logging.info(f'Find product by sku {bee_sku}')

  data = {
      "Type": [
          "string"
      ],
      "Term": bee_sku,
      "SearchMode": 0
  }

  response = post_request(BeeConfig.search_url, BeeConfig.headers, data)
  if (not response):
    return None

  try:
    product_id = response["Products"][0]["Id"]
  except:
    return None

  return product_id


def get_products():
  """
  Get all products
  Returns list
  """
  logging.info(f'Get all bee products')

  # TODO if products list will be more than 250 we should add pagination
  page_size = 250
  url = '{0}?pageSize={1}'.format(BeeConfig.products_url, page_size)

  response = get_request(url, BeeConfig.headers)
  if not response:
    return None

  try:
    products = response["Data"]
  except:
    return None

  return products


def update_stocks(data: dict):
  """
  Update stock data via bee API
  Returns json data
  """
  logging.info('Update stocks data')

  response = post_request(BeeConfig.update_stock_url, BeeConfig.headers, data)
  if (not response):
    message = f'Cannot update stocks data'
    logging.error(message)
    return {
        "message": message
    }

  return {
      "message": None
  }


def set_order_tracking(bee_order_id: str, tracking_data: dict):
  """
  Set tracking data from bee API
  Returns json data
  """
  logging.info(f'Set order state for ps order id is {bee_order_id}')

  url = '{0}{1}{2}'.format(BeeConfig.orders_url, bee_order_id, BeeConfig.shipment)
  """
  data = {
      "InvoiceNumber": tracking_data["ShippingId"],
      "SellerComments": tracking_data["TrackingUrl"]
  }
  """
  data = {
    "ShippingId": tracking_data["ShippingId"],
    "Comment": tracking_data["TrackingUrl"],
    "ShippingProviderId": 8008,
    "ShippingProviderProductId": 67905,
    "ShippingCarrier": 4,
    "ShipmentType": 0
  }

  response = post_request(url, BeeConfig.headers, data)
  if (not response):
    message = f'Cannot add new shipping {bee_order_id}'
    logging.error(message)
    return {
        "message": message
    }

  return {
    "message": None
  }

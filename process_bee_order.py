import logging
from bee_api import get_product

def process_order(bee_order_id: str, json: dict):
  """
  Process json data for specific bee order
  see https://apidoc.postabezhranic.cz/en/fulfillmenton/endpoints#add-fulfillment-order
  """

  logging.info(f'process_order {bee_order_id} started')

  json_data = json.get('Data', {})

  # result for Posta bez Hranic
  order = {}
  address = {}

  # get order id "Data.Id" - "Data.OrderNumber"
  order['orderNumber'] = '{0}-{1}'.format(json_data.get('Id', ''),
                                    json_data.get('OrderNumber', ''))

  if (not order['orderNumber']):
    logging.error(
        f'OrderNumber and Id for order {bee_order_id} should be defined json={json_data}')
    return None

  shipping_address = json_data.get('ShippingAddress', {})
  address['name'] = '{0} {1}'.format(shipping_address.get('FirstName', ''),
                                shipping_address.get('LastName', ''))

  address['companyName'] = shipping_address.get('Company', '')

  if (not address['name'] and not address['companyName']):
    logging.error(
        f'FirstName, LastName or Company for order {bee_order_id} should be defined json={json_data}')
    return None

  street = '{0} {1}'.format(shipping_address.get('Street', ''),
                            shipping_address.get('HouseNumber', ''))
  if (street):
    address['street'] = street
  else:
    logging.error(
        f'Street, HouseNumber for order {bee_order_id} should be defined json={json_data}')
    return None

  zip = shipping_address.get('Zip', '')
  if (zip):
    address['zip'] = shipping_address.get('Zip', '')
  else:
    logging.error(
        f'no Zip for order {bee_order_id} json={json_data}')
    return None

  city = shipping_address.get('City', '')
  if (city):
    address['city'] = city
  else:
    logging.error(
        f'no City for order {bee_order_id} json={json_data}')
    return None

  country = shipping_address.get('CountryISO2', '')
  if (country):
    address['country'] = country
  else:
    logging.error(
        f'no CountryISO2 for order {bee_order_id} json={json_data}')
    return None

  email = shipping_address.get('Email', '')
  if (email):
    address['email'] = email

  phone = shipping_address.get('Phone', '')
  if (phone):
    address['phone'] = phone

  insurance = json_data.get('PaidAmount', '')
  if (insurance):
    order['insurance'] = insurance

  tags = json_data.get('Tags', [])
  if (tags and len(tags) > 0):
    order['courierNumber'] = tags[0]
  else:
    logging.error(f'no Tags(courierNumber) for order {bee_order_id} json={json_data}')
    return None

  order_items = json_data.get('OrderItems', [])
  products = []
  for item in order_items:
    product = item.get('Product', {})
    product_bee_id = product.get('BillbeeId', '')
    if (not product_bee_id):
      logging.error(
          f'BillbeeId is not defined for {item} for order {bee_order_id} json={json_data}')
      return None

    product_info = get_product(product_bee_id) or {}
    product_info_data = product_info.get('Data', {})
    quantity = int(item.get('Quantity', ''))
    if (not quantity):
      logging.error(
          f'Quantity is not defined for {item} for order {bee_order_id} json={json_data}')
      return None

    stock_code = product_info_data.get('StockCode', '')
    if (not stock_code):
      logging.error(
          f'StockCode is not defined for {product_info} for order {bee_order_id} json={json_data}')
      return None

    products.append(
      {
          'fulfillmentProductCode': stock_code,
          'quantity': quantity
      }
    )

  if (not products):
    logging.error(
        f'At least one product for order {bee_order_id} should be defined json={json_data}')
    return None

  order['address'] = address
  ps = {
    'order': order,
    'products': products
  }

  logging.info(f'process_order {bee_order_id} end, {ps}')

  return ps
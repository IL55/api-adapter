import logging
from config import BeeConfig
from process_bee_order import get_bee_products
import re

def has_numbers(inputString: str):
  return any(char.isdigit() for char in inputString)

def get_phone(phone: str):

  if not phone:
    phone = '+49111111111'

  is_plus_presented = phone[0] == "+"

  phone = re.sub("[^0-9]", "", phone)
  phone = "+" + phone if is_plus_presented else phone

  return phone

def process_order_for_makura(bee_order_id: str, json: dict):
  """
  It uses different API vs PS API
  """

  logging.info(f'process_order {bee_order_id} started')

  json_data = json.get('Data', {})

  order = {}
  address = {}

  # get order id "Data.Id" - "Data.OrderNumber"
  order['external_id'] = '{0}-{1}'.format(str(BeeConfig.ps_id), bee_order_id)

  if (not order['external_id']):
    logging.error(
        f'OrderNumber and Id for order {bee_order_id} should be defined json={json_data}')
    return None

  order['carrier_id'] = 43 # 73 for production
  order['payment_id'] = 2
  order['note'] = ""

  shipping_address = json_data.get('ShippingAddress', {})
  address['firstname'] = shipping_address.get('FirstName', '')
  address['lastname'] = shipping_address.get('LastName', '')
  address['company'] = shipping_address.get('Company', '')

  if not address['firstname'] and \
    not address['lastname'] and \
    not address['company']:
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

  if (not has_numbers(street)):
    message = f'Street, HouseNumber for order {bee_order_id} should contain (at least) one digit json={json_data}'
    logging.error(message)
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

  address['phone'] = get_phone(shipping_address.get('Phone', ''))

  products = get_bee_products(bee_order_id, json_data)
  products = [{
      "catalog_number": product.get('fulfillmentProductCode', ""),
      "quantity": product.get('quantity', 0),
  } for product in products]
  if (not products):
    logging.error(
        f'At least one product for order {bee_order_id} should be defined json={json_data}')
    return None

  order['delivery_address'] = address
  order['products'] = products

  logging.info(f'process_order {bee_order_id} end, {order}')

  return order

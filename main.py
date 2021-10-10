import logging
from config import BeeConfig, logging_level
from bee_api import get_order, set_order_state
from process_bee_order import process_order
from ps_api import add_order
from version import API_VERSION

logging.basicConfig(level=logging_level)

def create_ps_order(bee_order_id: str):
  logging.info(f'Get order {bee_order_id} data')

  order_data = get_order(bee_order_id)
  logging.info(f'Order {bee_order_id} data received {order_data}')
  if (not order_data):
    message = f'Get order {bee_order_id} failed'
    logging.info(message)
    return {
      'version': API_VERSION,
      'response-code': -1,
      'message': message
    }

  ps_order_data = process_order(bee_order_id, order_data)
  logging.info(f'Order {bee_order_id} processed, order data is {ps_order_data}')
  if (not ps_order_data):
    message = f'Process order {bee_order_id} failed'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': -2,
        'message': message
    }

  add_order_result = add_order(bee_order_id, ps_order_data)
  logging.info(
      f'New PS for order {bee_order_id} created, result {add_order_result}')

  if (not add_order_result):
    message = f'Create PS for order {bee_order_id} failed, api error'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': -3,
        'message': message
    }

  if (add_order_result['status'] == 'error'):
    message = f'Create PS for order {bee_order_id} logic error {add_order_result["statusInfo"]}'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': -4,
        'message': message
    }

  set_order_state_result = set_order_state(
      bee_order_id, BeeConfig.order_state_shipping)
  logging.info(
      f'New state for order {bee_order_id} defined, result {set_order_state_result}')
  if (not set_order_state_result):
    message = f'Cannot set status for order {bee_order_id} api error'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': -5,
        'message': message
    }

  message = f'End order {bee_order_id} SUCCESS'
  return {
      'version': API_VERSION,
      'response-code': 0,
      'message': message
  }

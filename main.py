import logging
from config import BeeConfig, logging_level
from bee_api import get_order, set_order_state, set_order_tracking
from process_bee_order import process_order
from ps_api import add_order, get_tracking_info
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
      bee_order_id, BeeConfig.order_state_preparing)
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


def get_tracking(bee_order_id: str):
  ps_order_id = '{0}-{1}'.format(str(BeeConfig.ps_id), bee_order_id)
  logging.info(f'Get tracking {ps_order_id} data')
  tracking_data = get_tracking_info(ps_order_id)
  if (not tracking_data):
    message = f'Get tracking info from ps with ps order id {ps_order_id} failed'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': -11,
        'message': message
    }

  if (not tracking_data["ShippingId"]):
    message = f'No shipping id for {ps_order_id}'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': 0,
        'message': message
    }

  if (tracking_data["message"]):
    return {
        'version': API_VERSION,
        'response-code': -12,
        'message': tracking_data["message"]
    }

  logging.info(f'Received track data from PS {tracking_data}')

  tracking_response = set_order_tracking(bee_order_id, tracking_data)
  if (tracking_response["message"]):
    return {
        'version': API_VERSION,
        'response-code': -14,
        'message': tracking_response["message"]
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
        'response-code': -15,
        'message': message
    }

  return {
      'version': API_VERSION,
      'response-code': 0,
      'message': "OK"
  }


def get_ppl_tracking(bee_order_id: str):
  ppl_order_id = '{0}-{1}'.format(str(BeeConfig.ps_id), bee_order_id)
  logging.info(f'Get ppl tracking {ppl_order_id} data')
  tracking_data = get_tracking_info(ppl_order_id)
  if (not tracking_data):
    message = f'Get tracking info from ppl with ppl order id {ppl_order_id} failed'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': -100,
        'message': message
    }

  if (not tracking_data["ShippingId"]):
    message = f'No shipping id for {ppl_order_id}'
    logging.info(message)
    return {
        'version': API_VERSION,
        'response-code': 0,
        'message': message
    }

  if (tracking_data["message"]):
    return {
        'version': API_VERSION,
        'response-code': -101,
        'message': tracking_data["message"]
    }

  logging.info(f'Received track data from PS {tracking_data}')

  tracking_response = set_order_tracking(bee_order_id, tracking_data)
  if (tracking_response["message"]):
    return {
        'version': API_VERSION,
        'response-code': -102,
        'message': tracking_response["message"]
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
        'response-code': -103,
        'message': message
    }

  return {
      'version': API_VERSION,
      'response-code': 0,
      'message': "OK"
  }

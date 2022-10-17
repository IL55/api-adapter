import logging
from config import BeeConfig, logging_level
from bee_api import set_order_state, set_order_tracking
from makura_api import get_makura_tracking_info
from create_order import OrderDestination
from ps_api import get_tracking_info
from version import API_VERSION

logging.basicConfig(level=logging_level)


def get_tracking(bee_order_id: str, destination: OrderDestination = OrderDestination.PS):
  ps_order_id = '{0}-{1}'.format(str(BeeConfig.ps_id), bee_order_id)
  logging.info(f'Get tracking {ps_order_id} data')
  if destination == OrderDestination.PS:
    tracking_data = get_tracking_info(ps_order_id)

    if (not tracking_data):
      message = f'Get tracking info from ps with ps order id {ps_order_id} failed'
      logging.info(message)
      return {
          'version': API_VERSION,
          'response-code': -11,
          'message': message
      }
  else:
    makura_tracking_data = get_makura_tracking_info(ps_order_id)
    if not makura_tracking_data:
      message = f'Get makura tracking info from order id {ps_order_id} failed'
      logging.info(message)
      return {
          'version': API_VERSION,
          'response-code': -121,
          'message': message
      }
    tracking_data = {"message": None}
    tracking_data["ShippingId"] = makura_tracking_data.get("tracking_number")
    tracking_data["TrackingUrl"] = makura_tracking_data.get("number")

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

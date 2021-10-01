import logging
from config import BeeConfig, logging_level
from bee_api import get_order, set_order_state
from process_bee_order import process_order
from ps_api import add_order

logging.basicConfig(level=logging_level)

logging.info('Start script')

#TODO get parameter for args
# test id is 166651740
# input parameter
test_bee_order_id = '166651740'

def create_ps_order(bee_order_id: str):
  logging.info(f'Get order {bee_order_id} data')

  order_data = get_order(bee_order_id)
  logging.info(f'Order {bee_order_id} data received {order_data}')
  if (not order_data):
    logging.info(f'Get order {bee_order_id} failed')
    return

  ps_order_data = process_order(bee_order_id, order_data)
  logging.info(f'Order {bee_order_id} processed, order data is {ps_order_data}')
  if (not ps_order_data):
    logging.info(f'Process order {bee_order_id} failed')
    return

  add_order_result = add_order(bee_order_id, ps_order_data)
  logging.info(
      f'New PS for order {bee_order_id} created, result {add_order_result}')

  if (not add_order_result):
    logging.info(f'Create PS for order {bee_order_id} failed, api error')
    return

  if (add_order_result['status'] == 'error'):
    logging.info(f'Create PS for order {bee_order_id} logic error {add_order_result["statusInfo"]}')
    return

  set_order_state_result = set_order_state(
      bee_order_id, BeeConfig.order_state_shipping)
  logging.info(
      f'New state for order {bee_order_id} defined, result {set_order_state_result}')
  if (not set_order_state_result):
    logging.info(f'Cannot set status for order {bee_order_id} api error')
    return

  logging.info(f'End order {bee_order_id} SUCCESS')

create_ps_order(test_bee_order_id)

logging.info('End script')

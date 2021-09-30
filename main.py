import logging
from config import logging_level
from bee_api import get_order
from process_bee_order import process_order
from ps_api import add_order

logging.basicConfig(level=logging_level)

logging.info('Start script')

#TODO get parameter for args
# input parameter
bee_order_id = '164658970'

json = get_order(bee_order_id)
ps_order_data = process_order(bee_order_id, json)
# ps_result = add_order(bee_order_id, ps_order_data)

logging.info('End script')

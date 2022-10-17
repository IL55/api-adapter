import logging
import sys
from create_order import OrderDestination, create_order
from main import get_tracking
from makura_api import update_makura_products
from ppl_api import get_ppl_tracking

logging.info('Start script from console')

# test id is 166651740
# input parameter
# test_bee_order_id = '166651740'

logging.info(
    f'Arguments from console len:{len(sys.argv)} args:{str(sys.argv)}')

if (len(sys.argv) < 3):
  logging.info('Wrong number of argument, example:')
  logging.info('python console_function.py create_ps_order 166651740')
  logging.info('python console_function.py get_tracking 166651740')
  logging.info('python console_function.py get_ppl_tracking 166651740')
  logging.info('python console_function.py update_makura_products makura_secret')
  exit()

try:
  action = sys.argv[1]
except:
  action = None

try:
  id = sys.argv[2]
except:
  id = None

if (action == "get_tracking"):
  try:
    response = get_tracking(id, OrderDestination.PS)
  except:
    response = None
elif action == "get_makura_tracking":
  try:
    response = get_tracking(id, OrderDestination.MAKURA)
  except:
    response = None
elif action == "get_ppl_tracking":
  try:
    response = get_ppl_tracking(id)
  except:
    response = None
elif action == "update_makura_products":
  try:
    response = update_makura_products()
  except:
    response = None
elif action == "create_makura_order":
  try:
    response = create_order(id, OrderDestination.MAKURA)
  except:
    response = None
else:
  try:
    response = create_order(id, OrderDestination.PS)
  except:
    response = None

logging.info(f'Response from console {response}')

logging.info('End script from console')

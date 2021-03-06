import logging
import sys
from main import create_ps_order, get_tracking

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
    response = get_tracking(id)
  except:
    response = None
else:
  try:
    response = create_ps_order(id)
  except:
    response = None

logging.info(f'Response from console {response}')

logging.info('End script from console')

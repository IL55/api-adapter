import logging
import sys
from main import create_ps_order

logging.info('Start script from console')

# test id is 166651740
# input parameter
# test_bee_order_id = '166651740'

logging.info(
    f'Arguments from console len:{len(sys.argv)} args:{str(sys.argv)}')

if (len(sys.argv) < 2):
  logging.info('Wrong number of argument, example:')
  logging.info('python console_function.py 166651740')
  exit()

try:
  id = sys.argv[1]
except:
  id = None

try:
  response = create_ps_order(id)
except:
  response = None

logging.info(f'Response from console {response}')

logging.info('End script from console')

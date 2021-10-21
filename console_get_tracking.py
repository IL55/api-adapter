import logging
import sys
from main import get_tracking

logging.info('Start get tracking script from console')


logging.info(
    f'Arguments from console len:{len(sys.argv)} args:{str(sys.argv)}')

if (len(sys.argv) < 2):
  logging.info('Wrong number of argument, example:')
  logging.info('python console_get_tracking.py psUserId-beeOrderId')
  exit()

try:
  id = sys.argv[1]
except:
  id = None

try:
  response = get_tracking(id)
except:
  response = None

logging.info(f'Response from console {response}')

logging.info('End get tracking script from console')

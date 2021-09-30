import sys
import logging
import requests
from config import default_timeout


def get_request(url: str, headers: dict):
  logging.info(f'Fetching {url} ')
  response = None
  try:
    response = requests.get(
        url, headers=headers, timeout=default_timeout)
  except:
    logging.error(f'Timeout for {url} exception is {sys.exc_info()}')
    return None

  logging.info(f'Response status code {response.status_code}')
  if (response.status_code != 200):
    logging.error(f'Cannot get {url} response is {response}')
    return None

  json = response.json()
  logging.debug(f'Json is {json}')
  return json


def post_request(url: str, headers: dict, json_data: dict):
  logging.info(f'Posting {url} ')
  response = None
  try:
    response = requests.post(
        url, json=json_data, headers=headers, timeout=default_timeout)
  except:
    logging.error(f'Timeout for {url} exception is {sys.exc_info()}')
    return None

  logging.info(f'Response status code {response.status_code}')
  if (response.status_code != 200):
    logging.error(f'Cannot get {url} response is {response}')
    return None

  json = response.json()
  logging.debug(f'Json is {json}')
  return json

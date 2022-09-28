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
  return json


def post_html_request(url: str, headers: dict):
  logging.info(f'Post html {url} ')
  response = None
  try:
    response = requests.post(
        url, headers=headers, json={}, timeout=default_timeout)
  except:
    logging.error(f'Timeout for {url} exception is {sys.exc_info()}')
    return None

  logging.info(f'Response status code {response.status_code}')
  if (response.status_code != 200 or
      not response.text):
    logging.error(f'Cannot get {url} response is {response}')
    return None

  # logging.info(response.text)

  return response.text

def post_xml_request(url: str, headers: dict, xml_text: str):
  logging.info(f'Post xml {url} ')
  response = None
  try:
    response = requests.post(
        url, headers=headers, data=xml_text, timeout=default_timeout)
  except:
    logging.error(f'Timeout for {url} exception is {sys.exc_info()}')
    return None

  logging.info(f'Response status code {response.status_code} {response.content}')
  if (response.status_code != 200 or
          not response.text):
    logging.error(f'Cannot get {url} response is {response}')
    return None

  logging.info(response.text)

  return response.text


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
    logging.error(f'Cannot post {url} response is {response}')
    return None

  try:
    json = response.json()
  except:
    logging.debug(f'No json in POST response')
    json = response.status_code

  logging.debug(f'Json is {json}')
  return json


def put_request(url: str, headers: dict, json_data: dict):
  logging.info(f'Posting {url} ')
  response = None
  try:
    response = requests.put(
        url, json=json_data, headers=headers, timeout=default_timeout)
  except:
    logging.error(f'Timeout for {url} exception is {sys.exc_info()}')
    return None

  logging.info(f'Response status code {response.status_code}')
  if (response.status_code != 200):
    logging.error(f'Cannot put {url} response is {response}')
    return None

  try:
    json = response.json()
  except:
    logging.debug(f'No json in PUT response')
    json = response.status_code

  logging.debug(f'Json is {json}')
  return json


def patch_request(url: str, headers: dict, json_data: dict):
  logging.info(f'Patching {url} ')
  response = None
  try:
    response = requests.patch(
        url, json=json_data, headers=headers, timeout=default_timeout)
  except:
    logging.error(f'Timeout for {url} exception is {sys.exc_info()}')
    return None

  logging.info(f'Response status code {response.status_code}')
  if (response.status_code != 200):
    logging.error(f'Cannot patch {url} response is {response}')
    return None

  try:
    json = response.json()
  except:
    logging.debug(f'No json in PATCH response')
    json = response.status_code

  logging.debug(f'Json is {json}')
  return json

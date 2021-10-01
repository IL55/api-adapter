import logging
import secrets

# log level for logger could be INFO/ERROR/DEBUG
logging_level = logging.INFO

# default timeout for http requests in seconds
default_timeout = 60

# bee config
# TODO .env variables
class BeeConfig:
    api_key = secrets.BEE_API_KEY
    base_url = "https://app.billbee.io/api/v1"
    orders_url = base_url + "/orders/"
    products_url = base_url + "/products/"
    ps_id = 1632
    order_state_url = "/orderstate"

    headers = {
        "Content-Type": "application/json",
        "X-Billbee-Api-Key": api_key,
        "Authorization": "Basic " + secrets.BEE_AUTH
    }

class PsConfig:
  api_key = secrets.PS_API_KEY
  user_id = secrets.PS_USER_ID
  base_url = "https://api.fulfillmenton.com"
  add_order_url = base_url + "/add-fulfillment-order"

  headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + api_key
  }

  data = {
      "userId": user_id,
      "data": {
          "isLive": True
      }
  }

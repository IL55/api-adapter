import logging
from config import PsConfig
from network import post_request

def add_order(bee_order_id: str, json_data: dict):
    """
    Add order to ps API
    Returns json data
    """
    logging.info(f'Add order for Bee order id is {bee_order_id}')

    url = PsConfig.add_order_url
    data = PsConfig.data.copy()
    data['data'] = json_data

    return post_request(url, PsConfig.headers, data)

import logging
from bee_api import get_products, update_stocks
from config import MakuraConfig
from network import get_request, post_html_request, post_request
import xml.etree.ElementTree as ET
from version import API_VERSION


def get_value(item, name: str, default_value: str):
    element = item.find(name)
    if element is not None:
        return element.text
    else:
        return default_value

def parse_product_list(xmlstring: str):
    result = {
        "message": "",
        "products": []
    }

    # parse xml
    try:
        tree = ET.ElementTree(ET.fromstring(xmlstring))
    except:
        result["message"] = "Parse xml exception"
        tree = None

    if (not tree):
        return result

    try:
        for item in tree.findall('SHOPITEM'):
            sku = get_value(item, "CATALOG_NUMBER", "")
            state = get_value(item, "AVAILABILITY", "")
            default_count = "100" if state == "in stock" else "0"
            count = int(get_value(item, "STOCK_QUANTITY", default_count))

            if state == "out of stock":
                count = 0

            result["products"].append({
                "sku": sku,
                "state": state,
                "count": count
            })

    except:
        result["message"] = "Cannot find some fields in xml"

    return result


def get_makura_products():
    """
    Get and parse makuta product
    Returns json data
    """
    logging.info(f'Get makura products')

    xml_string = post_html_request(
        MakuraConfig.get_products_url, MakuraConfig.headers)

    return parse_product_list(xml_string)


def update_makura_products():
    result = {
        "version": API_VERSION,
        "message": "",
        "updated_products": {},
        "non_updated_products": {},
        "unknown_products": {}
    }

    makura_products_data = get_makura_products()
    makura_products = makura_products_data['products']
    if makura_products_data["message"] != "" or not makura_products:
        return makura_products_data

    bee_products = get_products()
    products_ids = {product['SKU']: product['Id'] for product in bee_products}
    products_stock = {product['SKU']: int(product['StockCurrent'] if product['StockCurrent'] else 0)
                      for product in bee_products}

    for product in makura_products:
        count = product["count"]

        if not count or count <= 0:
            continue

        sku = product["sku"]
        product_id = products_ids.get(sku)
        if product_id:
            count_in_stock = products_stock.get(sku)
            if count_in_stock != count:
                result["updated_products"][sku] = {
                    "bee_product_id": product_id,
                    "sku": sku,
                    "count": count,
                    "count_in_stock": count_in_stock
                }
                logging.info(f'updated {result["updated_products"][sku]}')
            else:
                result["non_updated_products"][sku] = {
                    "bee_product_id": product_id,
                    "sku": sku,
                    "count": count,
                    "count_in_stock": count_in_stock
                }
                logging.info(f'non-updated {result["non_updated_products"][sku]}')
        else:
            logging.info(f'unknown product id={product_id} sku={sku} count={count}')
            result["unknown_products"][sku] = {
                "bee_product_id": product_id,
                "sku": sku,
                "count": count
            }

    if result["updated_products"]:
        update_data = [
            {
                "Sku": sku,
                "NewQuantity": result["updated_products"][sku]["count"]
            } for sku in result["updated_products"]
        ]
        update_response = update_stocks(update_data)
        for bee_result, sku in zip(update_response["result"], result["updated_products"]):
            result["updated_products"][sku]["ErrorCode"] = bee_result["ErrorCode"]

        if update_response["message"]:
            result['message'] = update_response["message"]

    return result


def add_makura_order(bee_order_id: str, json_data: dict):
    """
    Add order to Makura API
    Returns json data
    """
    logging.info(f'Add order for Makura, bee order id is {bee_order_id}')

    return post_request(MakuraConfig.create_order_url, MakuraConfig.create_order_headers, json_data)


def get_makura_tracking_info(bee_order_id: str):
    """
    Add order to Makura API
    Returns json data
    """
    logging.info(f'Get makura tracking info order id is {bee_order_id}')
    """
    {
        "id": 1281,
        "external_id": "1501665316608",
        "number": "12345674069168",
        "status_id": 2,
        "tracking_number": "p7k5m"
    }
    """

    url = f'{MakuraConfig.create_order_url}/{bee_order_id}'
    return get_request(url, MakuraConfig.create_order_headers)

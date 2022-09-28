import logging
from bee_api import get_products, update_stocks
from config import MakuraConfig
from network import post_html_request
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
            count = int(get_value(item, "STOCK_QUANTITY", "0"))

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
    products_stock = {product['SKU']: product['StockCurrent']
                      for product in bee_products}

    for product in makura_products:
        count = product["count"]

        if not count or count <= 0:
            continue

        sku = product["sku"]
        product_id = products_ids.get(sku)
        if product_id:
            count_in_stock = products_stock.get(sku)
            if not count_in_stock or count_in_stock < count:
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
        print(update_data)
        update_response = update_stocks(update_data)
        if update_response["message"]:
            result['message'] = update_response["message"]

    return result


import logging
from config import PsConfig
from network import post_request, post_html_request
import xml.etree.ElementTree as ET

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


def parse_tracking_info_xml(xmlstring: str):
    result = {
        "message": "",
        "ShippingId": "",
        "TrackingUrl": "",
        "Shipper": ""
    }

    # parse xml
    try:
        tree = ET.ElementTree(ET.fromstring(xmlstring))
    except:
        result["message"] = "Parse xml exception"
        tree = None

    if (not tree):
        return result

    result["ShippingId"] = tree.find("package_tracking_number").text
    result["TrackingUrl"] = tree.find("package_tracking_link").text
    result["Shipper"] = tree.find("package_shipping_company").text

    return result


def get_tracking_info(ps_order_id: str):
    """
    Add order to ps API
    Returns json data
    """
    logging.info(f'Get tracking info for PS order id is {ps_order_id}')

    url = '{0}{1}'.format(PsConfig.get_tracking_url, ps_order_id)

    xml_string = post_html_request(url, PsConfig.headersBasic)

    return parse_tracking_info_xml(xml_string)

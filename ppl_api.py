import logging
from config import PplConfig
from network import post_xml_request

def get_api_version():
    version_xml = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://myapi.ppl.cz/v1">
            <soapenv:Header />
            <soapenv:Body>
                <v1:Version />
            </soapenv:Body>
        </soapenv:Envelope>"""

    headers = {
        "Content-Type": "text/xml",
        "SOAPAction": PplConfig.version_url
    }

    xml_string = post_xml_request(
        PplConfig.base_url, headers, version_xml)
    logging.info(f'XML output {xml_string}')


def get_ppl_tracking(ppl_order_id: str):
    """
    Add order to ps API
    Returns json data
    """
    logging.info(f'Get tracking info for PPL order id is {ppl_order_id}')
    get_api_version()

    headers = {
        "Content-Type": "text/xml",
        "SOAPAction": PplConfig.get_packages_url
    }

    params = {
        'password': PplConfig.password,
        'username': PplConfig.username,
        'customer_id': PplConfig.customer_id,
    }

    xml_text = """
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v1="http://myapi.ppl.cz/v1" xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
        <soapenv:Header/>
            <soapenv:Body>
                <v1:GetPackages>
                    <v1:Auth>
                        <v1:CustId>{customer_id}</v1:CustId>
                        <v1:UserName>{username}</v1:UserName>
                        <v1:Password>{password}</v1:Password>
                    </v1:Auth>
                    <v1:Filter>
                        <v1:DateFrom>2022-09-01</v1:DateFrom>
                        <v1:DateTo>2022-09-23</v1:DateTo>
                    </v1:Filter>
                </v1:GetPackages>
            </soapenv:Body>
        </soapenv:Envelope>""".format(**params)
    print(xml_text)
    xml_string = post_xml_request(PplConfig.base_url, headers, xml_text)
    logging.info(f'XML output {xml_string}')

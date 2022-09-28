import logging
import json
from main import create_ps_order, get_ppl_tracking, get_tracking
from makura_api import update_makura_products

def lambda_handler(event, context):
    logging.info('Start script from lambda')
    try:
        id=event["queryStringParameters"]['id']
    except:
        id=None

    try:
        action = event["queryStringParameters"]['action']
    except:
        action = None

    if (action == "get_tracking"):
        try:
            response = get_tracking(id)
        except:
            response = None
    elif action == "get_ppl_tracking":
        try:
            response = get_ppl_tracking(id)
        except:
            response = None
    elif action == "update_makura_products":
        try:
            response = update_makura_products()
        except:
            response = None
    else:
        try:
            response = create_ps_order(id)
        except:
            response = None

    body = {
        'id': id,
        'action': action,
        'response': response
    }

    logging.info(f'End script from lambda {response}')

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }

import logging
import json
from main import create_ps_order

def lambda_handler(event, context):
    logging.info('Start script from lambda')
    try:
        id=event["queryStringParameters"]['id']
    except:
        id=None

    try:
      response = create_ps_order(id)
    except:
      response = None


    body = {
        'id': id,
        'response': response
    }

    logging.info(f'End script from lambda {response}')

    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }
